# Baseline 1 Final Acceptance Report

> Date: 2026-11-28. Scope: offline ecosystem baseline for ArmPi Ultra ×
> ore_sorting, developer handover and contract governance.
>
> **Status: BASELINE 1 INCOMPLETE — conditional acceptance pending review.**
> The candidate tree passes the technical acceptance checks, but the required
> implementation PRs and the handover PR are not merged. No release or tag was
> created. Real deployment remains **NOT READY**.

## 1. Four separate statuses

| Status | Result | Basis |
|---|---|---|
| **DEVELOPMENT READY** | **YES** | environment check, builds, tests, mock gateway, simulation mock, device/scenario validation |
| **OFFLINE INTEGRATION READY** | **YES** | real CLI artifacts complete the ArmPi cell reference on main; eight-case mock task passes on the candidate branch |
| **BASELINE 1 COMPLETE** | **NO — conditional** | technical checks pass; PRs #7/#20 (apps)/#20 (interfaces) and handover docs are unmerged and unapproved |
| **DEPLOYMENT READY** | **NO** | deployed tree 0.1.0 vs dev 0.3.0, no base hardware bridge, no cross-process lease source, watchdog not deployed, DDS authority not certificate-based, no bench/hardware evidence |

These statuses are independent. A green mock suite is not deployment readiness;
a capability match is not motion authorization.

## 2. What passed on the candidate tree

| Check | Result |
|---|---|
| Real CLI vertical integration (main) | `matched_with_unverified`; 2-step plan; mock SUCCEEDED; benchmark inconclusive; simulation not_checked |
| Device snapshots | ArmPi 5-DOF, PiPER X 6-DOF, AR5 7-DOF (vendor-public, partial); no invented reach/payload/aperture/resolution |
| Hash contract | `source_hash` and artifact `content_hash` distinct; stale hash rejected |
| Cell composition | arm+gripper+camera; missing role fails closed; missing fact unverified; algorithm requirements deferred |
| Unit enforcement | wrong threshold unit rejected (`INCOMPATIBLE_UNIT`) |
| Mock ore-sorting task | 8/8 expected classifications; only `normal` SUCCEEDED; failures stop once |
| Benchmark discrimination | observed INCONCLUSIVE; test-pass PASS; test-fail FAIL |
| Regression | 15 repositories at fixed main SHAs + frozen `v1.0.0` tag; tests and gates pass (48) |
| Contract proposal | Proposed to interfaces; golden vectors pass; vocabulary still `local_draft` |
| Developer handover | guide, quick start and first task prepared; independent QA PASS WITH FINDINGS (P2 fixed, 49) |

## 3. Decision 10 exit criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Necessary governance/authority/source-of-truth PRs merged | **PARTIAL** — #36 merged; devices #7, applications #20, interfaces #20 unmerged |
| 2 | Public artifact contract has version, owner and approval | **NO** — proposal is Proposed; vocabulary `local_draft`; interface-owner approval pending |
| 3 | Real CLI artifacts interoperate on main | **YES** for the 2-step reference; 8-case mock task is candidate-only |
| 4 | Unverified/incompatible/illegal inputs classified and rejected | **YES** — stale hash, wrong unit, missing role, threshold mismatch, unauthorized run |
| 5 | Minimal positive mock ore-sorting task runs end to end | **YES on candidate** (PR #20) |
| 6 | Benchmark produces a traceable offline report | **YES** — suite/dataset hashes, scenario/evaluation IDs, data source; observed INCONCLUSIVE |
| 7 | Simulation assets validated in the declared scope | **YES (offline only)** — no ore_sorting world asset; Gazebo runtime not verified |
| 8 | Final main regression and independent QA | **YES on fixed main/candidate**; QA PASS WITH FINDINGS (49) |
| 9 | Developer Handover complete | **Content ready; merge pending** (#32 to be superseded by this delivery) |
| 10 | Manifest fixes SHAs, versions, hashes and limits | **YES** (42) |
| 11 | Repeatable build/test/offline entry | **YES** — `dev/baseline1-acceptance.sh` reruns the chain |

## 4. Blocking items

1. Devices #7, applications #20 and interfaces #20 need a real reviewer
   approval and merge-queue completion.
2. The interfaces proposal must be accepted by its owner before the vocabulary
   can be called `contracted`; criterion 2 cannot be met by the author alone.
3. This report PR needs approval and merge.
4. After merge, rerun the fixed-main regression and independent QA; only then
   can the status be changed to COMPLETE.

## 5. Non-blocking, explicitly recorded limits

- ArmPi reach, payload, gripper aperture and camera resolution are unverified.
- AR5 is vendor-public and locally unverified; no SDK/URDF/calibration/unit.
- PiPER X has no hardware and no runtime adapter.
- Real perception, IK, grasp success, AMR and LeRobot integration are out of
  scope and unimplemented.
- Gazebo runtime is unavailable; simulation is offline asset validation.
- Boundary checker reports 25 open findings and 1 waived (B4 studio); none is
  newly introduced by this sprint.
- Deployment blockers are unchanged.

## 6. Safety statement

No robot was started, no real motion was sent, no `ExecuteMotion` was called on
hardware, no DDS/ROS graph was joined, no production deployment was modified
and no real hardware output was enabled. All execution was loopback mock with
`evidence_class: L2` and `data_source: synthetic`.
