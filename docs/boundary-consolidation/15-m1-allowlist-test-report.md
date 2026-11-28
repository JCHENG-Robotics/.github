# M1 Allowlist Test Report

> Status: **v1.0 (2026-11-27)**. Evidence for Decision C: the `.github`
> Python prohibition now has a two-file governance allowlist. Report-only
> boundary checks remain non-blocking for product CI.

## 1. Change

| File | Purpose |
|---|---|
| `scripts/check_python_policy.sh` | Exact allowlist; rejects unlisted `.py`/`.py.*`, nested copies, hidden files and symlinks |
| `scripts/test_python_policy.sh` | 8-case self-test of the allowlist |
| `scripts/check_org_files.sh` | Calls the policy instead of the blanket `find -name '*.py'` |
| `scripts/check_boundaries.py` | Allowed governance tool (report-only) |
| `scripts/test_check_boundaries.py` | Allowed test file (17 tests) |

Allowlist: **only** the two boundary-checker files. Every other Python file is
rejected, including `scripts/other.py`, `scripts/sub/check_boundaries.py`,
`check_boundaries.py.bak`, hidden `.py` files, and symlinks.

## 2. Test evidence

`bash scripts/test_python_policy.sh`:

| Case | Expected | Result |
|---|---|---|
| Both allowed files | exit 0 | PASS |
| Unlisted `scripts/other.py` | exit 1 | PASS |
| Near-miss `check_boundaries.py.bak` | exit 1 | PASS |
| Nested `scripts/sub/check_boundaries.py` | exit 1 | PASS |
| Hidden `.hidden.py` | exit 1 | PASS |
| Symlink `scripts/evil.py` | exit 1 | PASS |
| Symlink at the allowed path | exit 1 | PASS |
| No Python files | exit 0 | PASS |

**8 passed, 0 failed.**

`bash scripts/check_org_files.sh` → **M1 .github gate OK**.
`python3 -m pytest -q scripts/test_check_boundaries.py` → **17 passed**.

## 3. Residual risk

- The policy is path-based; it does not inspect file content. A non-`.py` file
  containing Python is not rejected (e.g., a shell script with embedded
  Python). This is acceptable for the M1 gate's purpose.
- Hardlinks to files outside the repository are not distinguishable by path;
  the CI checkout has no such links.
- The policy does not replace code review; a change to the allowlist itself
  still requires Board approval.
- The boundary checker is static and report-only; it is not a runtime safety
  proof.

## 4. Delivery

- Branch: `feat/controlled-git-20261127`
- Policy commit: `ed1b175` (`feat(governance): add the M1 python allowlist and report-only boundary checker`)
- PR: https://github.com/JCHENG-Robotics/.github/pull/28 (stacked on #27)
- CI: `m1-gate` success on both commits
- No product repository code; no real-robot motion.

## Related

- [Controlled Git Operations](../controlled-git-operations.md)
- [Boundary check report](12-architecture-boundary-check-report.md)
- [Gate design](08-check-boundaries-design.md)
