# Post-Merge Regression Report — Baseline 1

> Status: **partial / incomplete (2026-11-27)**. Only three of the approved PRs
> are on `main`; six are blocked by approval, review dismissal or conflicts.
> This is an **actual-main** regression for the merged set plus branch evidence
> for the unmerged set — not a complete Baseline 1 acceptance.
> No hardware, no ROS runtime, no deployment change.

## 1. Actual main baseline

| Repository | main SHA | Regression on main | Result |
|---|---|---|---|
| `.github` | `b66966c` | `bash scripts/check_org_files.sh` | **OK** |
| `jcheng-interfaces` | `1e6ecd0` | `pytest` + schema check | **16 passed** |
| `jcheng-learning` | `6997825` | isolated gate (`uv --frozen --extra test`) | **68 passed**, gate OK |
| `jcheng-system` | `3fed859` | `pytest` (archive of main) | **94 passed** |
| `jcheng-mobile` | `0972e4b` | `pytest` (archive of main) | **10 passed** |
| `jcheng-studio` | `1c7b099` | root `pytest` (archive of main) | **13 passed** |
| `jcheng-devices` | `f87c448` | `pytest` (archive of main) | **54 passed** |
| `jcheng-scenarios` | `4390212` | `pytest` (archive of main) | **61 passed** |

Notes:

- `system`, `mobile`, `studio` main do **not** contain the hardening; their
  main counts are the pre-hardening baseline.
- `studio` backend tests were not run from the archive because the installed
  editable venv points at the working tree; branch backend is 222 passed.
- `devices`/`scenarios` main do not contain the admission commits; branch counts
  are 57/62.

## 2. Unmerged PR branch evidence

| PR | Head | Tests | QA | Blocker |
|---|---|---|---|---|
| `.github` #28 | `847f7c5` | checker 20, allowlist 8, gate OK | **not final-head** | review dismissed; merge commit after QA |
| devices #2 | `9026c16` | 57 passed | prior | no approval |
| scenarios #1 | `6ee7928` | 62 passed | prior | no approval |
| system #41 | `220b0ce` | 190 passed, gate OK | PASS | conflict with main |
| studio #10 | `ce7199b` | 13 root + 222 backend | PASS | conflict with main |
| mobile #7 (port) | `dc93f4b` | 50 passed, colcon OK | PASS | no approval |

## 3. Contract and cross-repository checks

- Interfaces pin remains **v0.2.0 / `afca22…`**; `main` has the proposal commit
  but **no IDL/schema/hash change** and no 0.3.0 tag.
- `jcheng-mobile` main pins interfaces v0.2.0 (`cbe6f51`); the port branch keeps
  that pin.
- System/mobile/studio joint authority tests are **not** covered by main:
  system hardening is not merged, so `ExecuteMotion`/base intake and the
  holder/deadman changes are branch-only. The branch QA covers them.
- The mobile envelope ↔ system parser match is verified on the branches, not on
  main.
- Frozen baseline `jcheng-manipulation@v1.0.0` (`b3411e4`) is unchanged.

## 4. Boundary check

Working-tree report after the fixes:

- **29 findings: 28 open + 1 waived Critical** (studio legacy).
- Open Critical = 0.
- Mobile B4 `/cmd_vel` eliminated (branch/port).
- Studio B4 remains only in default-disabled `legacy_motion.py`, waived
  `W-2026-11-27-01` until 2026-12-31.
- System B6 deployed-tree mismatch remains High; deployment not changed.
- Device copies B8/B10 and contract skew remain for Phase 2/MIG-04.

The checker itself is on the CGO branch (#28), not on main; main cannot run it
yet.

## 5. Findings classification

| Class | Items |
|---|---|
| **Eliminated** | mobile `/cmd_vel` direct publish; studio default legacy motion; missing-holder/deadman/DDS-service gaps on the branch |
| **Mitigated** | studio legacy isolated/default-disabled; DDS privileged surface default-deny; base fail-closed |
| **Waived** | studio B4 `legacy_motion.py` (expires 2026-12-31) |
| **Pending** | system deployed-tree mismatch; device-fact duplication; contract pin skew; base hardware bridge; cross-process lease sharing; Learning Humble/Gazebo evidence |

## 6. CI / merge status

- Merged: `.github` #27, interfaces #19, learning #5 — all green.
- Blocked: #28 (review dismissed), devices #2 / scenarios #1 (no approval),
  system #41 / studio #10 (conflicts), mobile #7 (no approval yet; CI green).
- No merge, tag, release or deployment by this round's agent.

## 7. Conclusion

**Baseline 1 is not achieved.** The merged set is green, and the branch set is
QA-passed except for the review/conflict blockers. A complete post-merge
regression requires all approved PRs merged into `main`; the baseline manifest
is therefore marked **incomplete**.

## Related

- [PR merge report](21-pr-merge-integration-report.md)
- [Remote delivery](19-remote-delivery-report.md)
- [Baseline manifest](25-ecosystem-integration-baseline-1-manifest.md)
- [Independent QA](18-independent-qa-report.md)
