# Ecosystem Integration Baseline 1 — Manifest

> Status: **INCOMPLETE / not released (2026-11-27)**. This manifest records the
> actual `main` SHAs, contract/device/scenario versions, tests and open risks at
> the time of the integration round. It is **not** a release, tag or deployment
> approval. Real-robot use remains **NOT READY**.

| Field | Value |
|---|---|
| Baseline ID | `EIB-1-partial-20261127` |
| Scope | Offline/mock/static integration only |
| Release/tag | **none** (Board decision required) |
| Real-robot authorized | **no** |
| Merge status | 3 merged, 6 blocked |

## 1. Repository baseline

| Repository | `main` SHA | Version | Contract pin | Tests on main | PR / status |
|---|---|---|---|---|---|
| `.github` | `b66966c` | governance (no VERSION) | — | gate OK | #27 merged; #28 open/blocked |
| `jcheng-interfaces` | `1e6ecd0` | 0.3.0 (unreleased) | v0.2.0 `afca22…` | 16 passed | #19 merged; proposal only |
| `jcheng-system` | `3fed859` | 0.3.0-dev0 | v0.2.0 `afca22…` | 94 passed | #41 open/conflict |
| `jcheng-mobile` | `0972e4b` | 0.1.0 | v0.2.0 `afca22…` | 10 passed | #6 superseded; #7 open/QA PASS |
| `jcheng-studio` | `1c7b099` | 0.8.0 | v0.2.0 `afca22…` | 13 root | #10 open/conflict |
| `jcheng-learning` | `6997825` | 0.2.0 | v0.2.0 `afca22…` | 68 passed | #5 merged |
| `jcheng-devices` | `f87c448` | 0.1.0 | v0.2.0 `afca22…` | 54 passed | #2 open/no approval |
| `jcheng-scenarios` | `4390212` | 0.1.0 | v0.2.0 `afca22…` | 61 passed | #1 open/no approval |
| `jcheng-manipulation` | frozen `v1.0.0` | 1.0.0 | — | not run | frozen baseline `b3411e4` |

`jcheng-system`/`mobile`/`studio` main do **not** contain the authority
hardening; the branch counts (190 / 50 / 13+222) are evidence, not main.

## 2. Contract baseline

| Item | Value |
|---|---|
| Interfaces release | **v0.2.0**, tag `v0.2.0`, commit `b03a054a…`, hash `sha256:afca22a4…` |
| Interfaces `main` | 0.3.0 unreleased, manifest hash `sha256:8120c502…` |
| Ecosystem lock | `jcheng-system/locks/ecosystem.lock.yaml`, 0.2.0, `afca22…` |
| Proposal | BaseIntent/lease-holder **merged as a proposal** (#19); no IDL/schema/hash change |
| Known skew | six repos still pin 0.1.0/`0b8d72…` (applications, learning, mobile, simulation, studio, teleop) |

## 3. Device baseline (reference)

| Field | Value |
|---|---|
| Repository | `jcheng-devices` v0.1.0 (PR #2 not merged) |
| `device_id` | `hiwonder.armpi-ultra` |
| `device_version` | 0.1.0 |
| Content hash | `sha256:99d4631a14dc6e53c730aa24a36ea05fb842faeb8e1248cb35cb5128d3f06723` |
| Capabilities | `arm.position_control`, `arm.joint_feedback` (+ gripper/chassis separate) |
| Authority | devices = declaration; system `robot-profile.v1` = deployment instance + safety overlay |
| Compatibility | not yet implemented; design in `24-phase2-source-of-truth-design.md` |

## 4. Scenario baseline (reference)

| Field | Value |
|---|---|
| Repository | `jcheng-scenarios` v0.1.0 (PR #1 not merged) |
| `scenario_id` | `ore_sorting` |
| `scenario_version` | 0.1.0 |
| Scenario hash | `sha256:43d15c2179d3977d971551700462d39ee24dd20a08466744859356ef2860c786` |
| Task/evaluation | `task.yaml`, `evaluation.yaml`; thresholds `not_set` |
| Authority | scenarios = task/success/evaluation spec; applications = orchestration; benchmark = execution/report; system = safety |
| Compatibility | not yet implemented; design in `24-phase2-source-of-truth-design.md` |

## 5. Test and evidence baseline

| Layer | Evidence |
|---|---|
| L0 gates | `.github` gate; system/mobile/studio/devices/scenarios/learning gates; checker 20; allowlist 8 |
| L1 unit | main: 16 + 68 + 94 + 10 + 13 + 54 + 61; branches: 190 + 50 + 222 |
| L2 mock | system base/gateway, studio legacy/stop, mobile intent |
| L3 mock e2e | system S1–S17 (existing) |
| L4 replay | not run |
| L5 hardware | **not run / not authorized** |
| QA | system/mobile/studio/mobile-port PASS; #28 final head not QA'd |

## 6. Open risks (not closed by this manifest)

| Risk | Class | Owner |
|---|---|---|
| system #41 and studio #10 conflict with main | merge blocker | Board |
| #28 review dismissed / final merge commit not QA'd | merge blocker | Board/QA |
| devices #2 / scenarios #1 lack approval | merge blocker | Board |
| mobile #7 lacks approval | merge blocker | Board |
| base hardware bridge unavailable | deployment blocker | system |
| cross-process lease sharing unimplemented | deployment blocker | system |
| deployed tree 0.1.0 vs dev 0.3.0-dev0 | deployment blocker | system |
| contract pin skew / `system_api` unverifiable | migration | interfaces/system |
| device-fact duplication and scenario duplication | migration | Phase 2 |
| 200/300 ms provisional; no brake-distance data | safety | system/QA |
| studio legacy B4 | waived until 2026-12-31 | studio |
| no Humble/Gazebo/hardware regression | evidence gap | all |

## 7. Applicability statement

This baseline may be used for offline/mock design, review and CI comparison
only. It does **not** authorize:

- starting the robot, sending motion, restoring legacy motion, or enabling
  real hardware output;
- modifying the production deployment;
- creating a release, tag or stable version;
- claiming functional safety, a measured stopping time or a braking distance.

## Related

- [Post-merge regression](26-post-merge-regression-report.md)
- [PR merge report](21-pr-merge-integration-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
- [Phase 2 design](24-phase2-source-of-truth-design.md)
