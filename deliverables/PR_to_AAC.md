# PR proposal: Integrate `NATEBJONES` Policy Forge artifacts into ResonanceEnergy/AAC

Summary:
- Add `nate_policy.json` (policy templates), CI policy check workflow, and agent SOPs to the AAC governance directory.

Files to include (this repo):
- `policy/nate_policy.json` — machine readable Policy Forge example
- `agents/*.md` — SOPs and runnable prompts for 10 factory agents
- `.github/workflows/nate_policy_check.yml` — CI job to validate policy files
- `scripts/policy_checker.py` — simple validator used in CI
- `deliverables/250_insights.md` — prioritized insight backlog

PR description (copy‑paste for AAC PR):
- Purpose: provide a production‑ready Policy Forge example and 10 factory agent SOPs that can be used as templates across AAC projects.
- Changes: adds policy JSON, SOPs, CI validation for policy files, and a 250‑insight backlog for Nate B. Jones content.
- Tests: CI validates the `nate_policy.json` file format using `scripts/policy_checker.py`.

Suggested reviewers: `@policy-team`, `@gov‑lead`, `@content‑ops`.

Notes for integrator:
- The files are self‑contained; if merged into `docs/policies/` or `policy/examples/` in AAC they will align with existing structure.
- Adjust contact field in `nate_policy.json` to match AAC org emails.

Next steps I can do for you:
- Open the PR (if you give repository write access or tell me to open against a fork).
- Convert `nate_policy.json` to the AAC canonical schema if you point me at that file.
