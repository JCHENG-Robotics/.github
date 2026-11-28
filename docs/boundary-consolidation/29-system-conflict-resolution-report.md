# System Conflict Resolution Report — #41

> Status: **resolved on `main`; no manual port was needed by this agent**.
> The Board/owner merged #41 as a squash and reconciled the branch with main.
> No rebase, cherry-pick, reset or force-push was used.

## 1. Original and final state

| Item | Value |
|---|---|
| Original PR | [#41](https://github.com/JCHENG-Robotics/jcheng-system/pull/41) |
| Audited head (QA) | `220b0ce` |
| Local hardening branch before merge | `feat/authority-hardening-20261127` |
| Local branch after main reconciliation | `d10006f Merge origin/main` |
| `main` squash commit | `72b2ce2 feat(authority): unify hardware authority, lease, stop and base intent (#41)` |
| `main` before #41 | `3fed859` |

## 2. Semantic equivalence

- `git diff origin/main..d10006f` is **empty** (the local branch tree equals
  main).
- The hardening commits (`9b00466`, `b808208`, `19629bf`, `fde2e14`, `b56cf57`,
  `220b0ce`) are represented on main through the squash `72b2ce2`.
- Main also contains `#35` (read-only `/v1` gateway), `#40` (R10 hardware
  gateway unit) and `#38` (contract pin from lockfile); these are preserved.
- The local reconciliation merge brought those main commits into the branch
  without reverting the hardening.

## 3. Verification on `main`

| Check | Result |
|---|---|
| `python3 -m pytest` | **191 passed** |
| `bash scripts/check_repo_gate.sh` | OK (14 packages) |
| Hardening suites | `test_base_authority`, `test_base_intake`, `test_lease_holder`, `test_dds_gate`, `test_hardware_authority`, `test_watchdog` all pass |
| Holder/deadman/DDS services | default-required, default-deny, tests pass |
| Base intake | default disabled, `lease_source=none` fail-closed |
| `deploy/` changes | none in the hardening; #40/#35 deployment units are separate and remain untouched by this report |

## 4. Residual limits

- Base hardware bridge remains unavailable/fail-closed.
- Cross-process lease sharing remains unimplemented.
- DDS `ExecuteMotion` lacks a holder field and fails closed even if the gate
  opens; HTTP `/v1/motion/*` is the usable path.
- 200 ms freshness / 300 ms deadman remain provisional.
- Deployed tree `0.1.0` vs development `0.3.0-dev0` remains a deployment
  blocker; no production deployment was changed.

## 5. Disposition

Original branch, commits and QA evidence are preserved. No history was
rewritten. No further system port work is required for Baseline 1.

## Related

- [Implementation report](17-authority-hardening-implementation-report.md)
- [Independent QA](18-independent-qa-report.md)
- [Post-merge regression](26-post-merge-regression-report.md)
