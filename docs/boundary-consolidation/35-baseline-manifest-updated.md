# Ecosystem Integration Baseline 1 — Updated Manifest

> Status: **INCOMPLETE (2026-11-28)**. All governance/hardening PRs are merged
> and the main integration QA passed; the device/scenario source-of-truth
> implementation and the ArmPi Ultra × ore_sorting reference are not yet
> merged. This is **not** a release, tag or deployment approval.

| Field | Value |
|---|---|
| Baseline ID | `EIB-1-20261128-incomplete` |
| Main integration | PASS |
| Deployment | **NOT READY** |
| Release/tag | **none** |
| Real-robot authorized | **no** |

## 1. Fixed main SHAs

| Repository | `main` SHA | Version | Tests on main |
|---|---|---|---|
| `.github` | `94b4cd5` | governance | gate OK; allowlist 8; checker 20 |
| `jcheng-interfaces` | `1e6ecd0` | 0.3.0 unreleased | 16 + schema check |
| `jcheng-system` | `72b2ce2` | 0.3.0-dev0 | 191; gate OK |
| `jcheng-mobile` | `f96cfee` | 0.1.0 | 50 |
| `jcheng-studio` | `40c002b` | 0.8.0 | 13 root + 222 backend; gate OK |
| `jcheng-learning` | `6997825` | 0.2.0 | 68; gate OK |
| `jcheng-devices` | `86c721c` | 0.1.0 | 57; gate OK |
| `jcheng-scenarios` | `6dbedad` | 0.1.0 | 62; gate OK |
| `jcheng-manipulation` | `v1.0.0` | 1.0.0 | frozen `b3411e4` |

## 2. Contract / device / scenario

| Item | Value |
|---|---|
| Interfaces | v0.2.0, `afca22…`; 0.3.0 unreleased |
| Lock | 0.2.0, `afca22…` |
| Device reference | `hiwonder.armpi-ultra`, 0.1.0, hash `99d4631a…` |
| Scenario reference | `ore_sorting`, 0.1.0, hash `43d15c21…` |
| Device SoT implementation | convergence on PR #5 (`source_hash`/artifact hash, role attributes); not merged |
| Scenario SoT implementation | convergence on PR #3 (role/interface/threshold, owner-required algorithm requirements); not merged |
| Reference integration | cell reference on PR #19; real artifacts complete as `matched_with_unverified` ([40](40-td-contract-convergence-report.md)); main pending |

## 3. Decision 9 exit criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Necessary governance/hardening PRs merged | ✅ |
| 2 | Actual-main integration regression | ✅ PASS |
| 3 | Independent integration QA | ✅ Development/Main PASS |
| 4 | Devices/Scenarios first SoT consolidation | ✅ **on convergence branches** (#5/#3); main pending merge |
| 5 | ArmPi × ore_sorting offline vertical | ✅ **on convergence branches** (`matched_with_unverified`); main pending |
| 6 | Accurate security/debt status + evidence | ✅ 31/32/34/37 |
| 7 | Fixed SHAs/contract/device/scenario in manifest | ✅ this file |
| 8 | Repeatable build/test/offline entry | ✅ **on convergence branches**; main pending merge/QA |

## 4. Merged PR set

`.github` #27/#28/#29, devices #2, scenarios #1, learning #5, interfaces #19,
system #41, studio #10, mobile #7. Mobile #6 closed as superseded. No release or
tag was created.

## 5. Applicability

Offline/mock/static only. Does not authorize robot start, motion, legacy
restore, production deployment, a release, or a functional-safety claim.

## Related

- [Main boundary report](34-boundary-report-main.md)
- [Post-merge regression](26-post-merge-regression-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
