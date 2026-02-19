"""ARCHON + SENTRY demo

Run: python demos/archon_sentry_demo.py --n 3

What this demo shows:
- ARCHON: prioritizes top-N transcripts and builds a JSON workplan for FORGE/SCRIBE
- SENTRY: runs policy checks (no-credentials, PII detection, external-action approval, copyright)
- If SENTRY passes, ARCHON marks task as "ready-to-schedule"; otherwise it emits remediation steps

This is intentionally self-contained and uses local transcripts and `policy/nate_policy.json`.
"""
import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "analysis" / "50_videos_with_transcripts.csv"
POLICY_PATH = ROOT / "policy" / "nate_policy.json"

# -----------------------------
# Simple SENTRY implementation
# -----------------------------
class Sentry:
    def __init__(self, policy_path: Path):
        with open(policy_path, "r", encoding="utf-8") as f:
            self.policy = json.load(f)

    def _detect_credentials(self, text: str) -> List[str]:
        creds = []
        patterns = [r"api[_-]?key", r"secret", r"token", r"password", r"access[_-]?token", r"bearer\s+[A-Za-z0-9\-_.]+"]
        for p in patterns:
            if re.search(p, text, flags=re.I):
                creds.append(p)
        return creds

    def _pii_score(self, text: str) -> float:
        # very small heuristic PII detector (emails/phones/ssn)
        email_re = re.compile(r"\b[\w.-]+@[\w.-]+\.[A-Za-z]{2,6}\b")
        phone_re = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
        ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        matches = len(email_re.findall(text)) + len(phone_re.findall(text)) + len(ssn_re.findall(text))
        words = max(1, len(re.findall(r"\w+", text)))
        return matches / words

    def _detect_external_actions(self, plan: Dict[str, Any]) -> int:
        # plan can include an 'external_actions_count' -- otherwise naive text scan
        if "external_actions_count" in plan:
            return int(plan["external_actions_count"])
        txt = plan.get("notes", "")
        triggers = ["send email", "delete file", "call api", "write to s3", "deploy", "ssh ", "exec "]
        return sum(1 for t in triggers if t in txt.lower())

    def _copyright_risk(self, text: str) -> float:
        indicators = ["copyright", "©", "licensed", "lyrics", "song"]
        return 1.0 if any(ind in text.lower() for ind in indicators) else 0.0

    def evaluate(self, transcript: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        creds = self._detect_credentials(transcript + "\n" + plan.get("notes", ""))
        pii = self._pii_score(transcript)
        ext_actions = self._detect_external_actions(plan)
        copy_risk = self._copyright_risk(transcript)

        results = {
            "contains_secrets": len(creds) > 0,
            "creds_patterns": creds,
            "pii_score": round(pii, 6),
            "external_actions_count": ext_actions,
            "copyright_risk_score": copy_risk,
        }

        # map to policy enforcement decisions
        decisions = []
        for r in self.policy.get("rules", []):
            rid = r.get("id")
            chk = r.get("check", "")
            enforcement = r.get("enforcement", "")

            # Very small interpreter for the checks used in nate_policy.json
            passed = True
            if rid == "no-credentials-in-demos":
                passed = not results["contains_secrets"]
            elif rid == "pii-detection":
                passed = results["pii_score"] < 0.1
            elif rid == "external-action-approval":
                passed = (results["external_actions_count"] == 0) or plan.get("human_approved", False)
            elif rid == "copyright-check":
                passed = results["copyright_risk_score"] < 0.2

            decisions.append({"rule": rid, "enforcement": enforcement, "passed": passed})

        overall_pass = all(d["passed"] for d in decisions)
        remediation = []
        if results["contains_secrets"]:
            remediation.append("Remove any credential-like strings from the transcript/notes and rotate keys.")
        if results["pii_score"] >= 0.1:
            remediation.append("Sanitize or redact detected PII and re-run tests.")
        if results["external_actions_count"] > 0 and not plan.get("human_approved", False):
            remediation.append("Mark demo as requiring human approval for external actions.")
        if results["copyright_risk_score"] >= 0.2:
            remediation.append("Request legal review for potential copyright content.")

        return {
            "policy_evaluation": decisions,
            "overall_pass": overall_pass,
            "remediation": remediation,
            "raw": results,
        }

# -----------------------------
# ARCHON demo (orchestrator)
# -----------------------------
class Archon:
    def __init__(self, csv_path: Path, sentry: Sentry):
        self.csv_path = csv_path
        self.sentry = sentry

    def _load_top_n(self, n: int) -> List[Dict[str, str]]:
        rows = []
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, r in enumerate(reader):
                if i >= n:
                    break
                rows.append(r)
        return rows

    def _scribe_summarize(self, transcript: str) -> Dict[str, Any]:
        # ultra‑lightweight summarizer: first 3 sentences + chapter placeholders
        sentences = re.split(r"(?<=[.!?])\s+", transcript.strip())
        tldr = " ".join(sentences[:3])[:800]
        chapters = [
            {"start": "0:00", "title": "Intro"},
            {"start": "1:30", "title": "Core idea"},
            {"start": "6:00", "title": "Demo / Example"},
        ]
        return {"tldr": tldr, "chapters": chapters}

    def _forge_create_short(self, tldr: str) -> Dict[str, str]:
        # create a single 60s social script + simple thumbnail headline
        script = (
            f"Hook: {tldr.split('.')[0][:110]}...\n" +
            "Body: 3 quick points from the episode.\nCTA: Read the full thread / Subscribe."
        )
        thumbnail = tldr.split('.')[0][:40]
        return {"script": script, "thumbnail_headline": thumbnail}

    def plan_for_transcript(self, row: Dict[str, str]) -> Dict[str, Any]:
        transcript_path = row.get("transcript_path")
        transcript_text = ""
        if transcript_path:
            p = Path(transcript_path)
            if p.exists():
                transcript_text = p.read_text(encoding='utf-8')

        scribe = self._scribe_summarize(transcript_text or row.get('summary',''))
        plan = {
            "task": "create_short_and_post",
            "assignee": "FORGE",
            "acceptance": ["subtitle present", "thumbnail A/B test"],
            "notes": scribe["tldr"][:800],
            "external_actions_count": 0,
            "human_approved": False,
        }

        sentry_report = self.sentry.evaluate(transcript_text, plan)
        ready = sentry_report["overall_pass"]

        return {
            "video_id": row.get("video_id") or row.get("index"),
            "title": row.get("title"),
            "plan": plan,
            "scribe": scribe,
            "sentry": sentry_report,
            "ready_to_schedule": ready,
        }

    def run(self, n: int = 3) -> List[Dict[str, Any]]:
        rows = self._load_top_n(n)
        workplans = [self.plan_for_transcript(r) for r in rows]
        return workplans

# -----------------------------
# CLI
# -----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=3, help="Number of top transcripts to plan for")
    parser.add_argument("--output", type=str, default=None, help="Write JSON output to a file")
    args = parser.parse_args()

    sentry = Sentry(POLICY_PATH)
    archon = Archon(CSV_PATH, sentry)
    plans = archon.run(n=args.n)

    out = {"plans": plans}
    txt = json.dumps(out, indent=2, ensure_ascii=False)
    print(txt)

    if args.output:
        Path(args.output).write_text(txt, encoding='utf-8')
        print(f"Wrote plan to {args.output}")


if __name__ == "__main__":
    main()
