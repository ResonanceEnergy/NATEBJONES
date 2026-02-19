# Sprint: Top 10 Prioritized Tasks (2-week sprint)

Sprint goals: convert the highest-impact insights into shippable work that improves safety, discoverability, and monetization. Target cadence: 2 weeks (Sprint owner: @content-ops / @engineering).

Sprint window: 2026-02-20 → 2026-03-05

Priorities, estimates, owners, acceptance criteria, and tasks:

1) Implement pre‑publish SENTRY checklist (MVP)
- Priority: P0
- Estimate: 5 days
- Owner: @safety / @dev
- Acceptance criteria:
  - CI runs `scripts/policy_checker.py` and blocks PRs with malformed policies
  - `demos/archon_sentry_demo.py` demonstrates automated checks and rejects PII/credentials
- Tasks:
  - Finish rule set in `policy/nate_policy.json` (done)
  - Wire `scripts/policy_checker.py` into CI (workflow added)
  - Add SENTRY CLI checks for PII/credentials (demo script verifies)

2) Build a spec‑driven production pipeline (MVP for one video)
- Priority: P0
- Estimate: 6 days
- Owner: @engineering + @content-ops
- Acceptance criteria:
  - `ARCHON` can accept a spec and produce a JSON workplan for FORGE/SCRIBE
  - Workplan includes acceptance tests and routes to `SENTRY` before scheduling
- Tasks:
  - Create `demos/archon_sentry_demo.py` (ARCHON orchestration) — demoed
  - Create simple acceptance tests template for FORGE outputs
  - Validate end‑to‑end on one video

3) Automate chapter generation from transcripts (SCRIBE automation)
- Priority: P1
- Estimate: 2 days
- Owner: @content-ops / @nlp-eng
- Acceptance criteria:
  - Chapters generated automatically for long videos (>12 mins)
  - Human validation flag added to UI/PR template
- Tasks:
  - Implement chapter extraction using transcript timestamps
  - Add chapter output to `demos/archon_sentry_demo.py`

4) Batch‑produce Shorts + schedule via AUTOMAT
- Priority: P1
- Estimate: 3 days
- Owner: @social / @automation
- Acceptance criteria:
  - FORGE outputs 2–3 short scripts per long video
  - AUTOMAT scheduling job created (simulated) and validated in demo
- Tasks:
  - Add short generation templates to FORGE
  - Add scheduling stub to AUTOMAT

5) Publish transcripts & closed captions to YouTube + site
- Priority: P1
- Estimate: 2 days
- Owner: @content-ops
- Acceptance criteria:
  - Transcript files exist for top 20 videos (store path in CSV)
  - Captions file ready for upload and article pages include full transcript
- Tasks:
  - Audit `analysis/transcripts/` and add missing captions
  - Update upload checklist

6) Standardize title & thumbnail A/B test
- Priority: P1
- Estimate: 3 days
- Owner: @growth
- Acceptance criteria:
  - Title template applied to next 8 videos
  - Thumbnail A/B test framework instrumented (CTR comparison in PULSE)
- Tasks:
  - Implement title template in MAPPER
  - Create thumbnail variants and schedule A/B test

7) Productize first prompt pack: "Agent Starter"
- Priority: P2
- Estimate: 4 days
- Owner: @product
- Acceptance criteria:
  - Publish prompt pack as downloadable with 10 prompts + examples
  - Landing page + Substack CTA available
- Tasks:
  - Assemble prompts from KEEPER
  - Create landing page and gate for email capture

8) Release reproducible demo repo for "10‑minute build" video
- Priority: P2
- Estimate: 4 days
- Owner: @engineering
- Acceptance criteria:
  - Demo repo contains code + prompt inputs + instructions
  - CI validates that sample prompt produces expected output (smoke test)
- Tasks:
  - Extract demo artifacts into `examples/10-minute-build/`
  - Add README and smoke test

9) Seed KEEPER with 10 canonical prompts and artifact IDs
- Priority: P2
- Estimate: 2 days
- Owner: @ops
- Acceptance criteria:
  - 10 prompts stored in `agents/KEEPER.md` and referenced in `analysis/` where used
  - Retrieval URL / artifact ID format documented
- Tasks:
  - Curate the prompts, add version metadata
  - Add retrieval examples to ARCHON workflow

10) Launch weekly "AI News Brief" short (process + first episode)
- Priority: P2
- Estimate: 3 days
- Owner: @content-ops / @social
- Acceptance criteria:
  - Template for 60s brief created in FORGE
  - First episode published and measured (KPI: views, sub signups)
- Tasks:
  - Create template, assign Anchorage to `AUTOMAT` for weekly scheduling
  - Publish episode and collect PULSE analytics

---

How to use this sprint file:
- Convert each item into GitHub issues (title => task, copy acceptance criteria).
- Tag assignees and milestones; create PRs for code changes and link to issues.

Would you like me to open these as GitHub issues and create a milestone for the sprint?