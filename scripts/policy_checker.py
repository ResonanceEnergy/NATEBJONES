"""
Simple policy validator used by CI. Checks required top‑level fields and rule format.
"""
import json
import sys

REQUIRED_TOP_LEVEL = ["policy_name", "version", "scopes", "rules"]


def validate_policy(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        p = json.load(f)

    missing = [k for k in REQUIRED_TOP_LEVEL if k not in p]
    if missing:
        print(f"ERROR: missing top-level fields: {missing}")
        return 2

    if not isinstance(p.get("rules"), list):
        print("ERROR: 'rules' must be an array")
        return 2

    for r in p.get("rules"):
        for field in ["id", "description", "enforcement", "check"]:
            if field not in r:
                print(f"ERROR: rule missing '{field}': {r}")
                return 2

    print("OK: policy looks well-formed")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: policy_checker.py <policy.json>")
        sys.exit(2)
    sys.exit(validate_policy(sys.argv[1]))
