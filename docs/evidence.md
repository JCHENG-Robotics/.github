# Evidence and status

> Status: **v1.0** as of 2026-11-28. English canonical.  
> This document defines how claims in the organization profile are read. It does
> not replace a repository-level `ACCEPTANCE.md`, a signed tag or an evidence
> bundle. Where this summary and an evidence bundle disagree, the bundle wins.

## 1. Why this exists

The ecosystem spans contracts, a privileged runtime, capability modules,
simulation, benchmarks and a frozen baseline. A reader must be able to tell
**what was measured, on which platform, at which evidence level, and what it does
not imply**. Three rules apply everywhere:

1. Synthetic, mock and replay results are never counted as hardware validation.
2. A partial hardware run is not an acceptance.
3. Results from one platform do not transfer to another platform.

## 2. Status vocabulary

The organization uses ten labels. A label is a claim with a threshold, not a
synonym for "done".

| Label | Meaning | Minimum evidence | Never implies |
|---|---|---|---|
| **Frozen** | Immutable baseline or frozen platform | Tag + commit + evidence index; no new feature PRs | Deployment readiness, active support |
| **Hardware verified** | A named scope passed on a named physical platform | L5 logs, bus/CAN read-back, supervised authorization | Whole-repository acceptance, platform-wide validation, safety certification |
| **Offline verified** | Contracts, mock, offline or replay path passed | L0–L4 tests, reports, hashes; no hardware claim | Hardware availability, deployability |
| **Experimental** | Admitted repository, only its declared gates pass | `capability.yaml` + repository acceptance | Stability, production use |
| **Planned** | Declared, not implemented | Roadmap/ADR/proposal | Scheduled, committed delivery |
| **Dormant** | Code retained, no current work | Roadmap says so | Deleted, abandoned |
| **Conditional** | Technical checks pass, approvals/merges remain | Acceptance report + open items | Complete, releasable |
| **Not ready** | Deployment blockers exist | Blocker list | "Almost there" |
| **Inconclusive** | Evidence is insufficient to pass or fail | No dataset/suite | Pass, fail |
| **Legacy** | Retained as a reference, no new installs | Freeze/retirement record | Supported |

**Delivery status** (`Complete` / `In progress` / `Planned` / `Not started`) and
**verification status** (`Verified` / `Partially verified` / `Unverified` /
`Inconclusive`) are separate fields. Do not collapse them.

## 3. Evidence classes

| Class | What it proves | What it does not prove |
|---|---|---|
| **L0** | Structure, contracts, schemas, repository gates | Any runtime behaviour |
| **L1** | Unit-level logic and contract tests | Integration |
| **L2** | Mock integration (process, service or gateway) | Real transport or hardware |
| **L3** | Mock end-to-end or simulation | Real hardware |
| **L4** | Replay of recorded decisions/data | Live execution |
| **L5** | Supervised hardware execution with measurement | Safety certification, population reliability |

A claim must name its class. "Verified" without a class is incomplete.

## 4. Frozen baseline — ArmPi Ultra v1.0.0

`jcheng-manipulation v1.0.0` at commit `b3411e4` is the frozen experimental
baseline. It is MIT-licensed and read-only. Its results are **baseline results**,
not results of the new ecosystem. The platform was frozen on 2026-11-28; these
results stay valid for ArmPi and do not transfer to PiPER X or AR5.

### 4.1 Hand–eye calibration

| Item | Result |
|---|---|
| 14-pose board-pose scatter | **2.94 mm / 0.39°** |
| Held-out poses | **3.29 mm / 0.43°** |
| Leave-one-out standard deviation | 3.41 mm / 0.44° |
| Table-down re-calibration, 15 poses | 2.7 mm / 0.42° scatter; held-out 2.2 mm / 0.29° |
| Validation | Independent checkerboard; not vendor defaults |

### 4.2 Paired hardware trials

| Trial | Baseline | Intervention | Test |
|---|---|---|---|
| Fixed-site, 24 pairs | 12/24 | **24/24** | McNemar p = 0.00049 |
| Random placement, 24 pairs | 9/24 | **24/24** | McNemar p = 6.1 × 10⁻⁵ |

The fixed-site trial used a pre-registered constant low-configuration
correction. The random-placement follow-up used free by-eye spots, wrist/front
camera locate and a base approach. These are paired trials on one platform, not a
population-level reliability claim.

### 4.3 Error budget

| Item | Result | Reading |
|---|---|---|
| Translation RSS | **13.325 mm** (worst 24.014 mm) | The pre-registered **6 mm bound is not met** |
| Rotation RSS | 1.858° (worst 3.322°) | Against a provisional 2° bound |
| Fixture-inclusive translation | 19.926 mm | A different aggregation |
| Empirical placement mean | **3.080 mm** | A different statistic; inside 6 mm but **not** a pass of the RSS bound |
| Dominant terms | Placement 74.7%; execution rotation 64.7% | Where the error comes from |

The failed bound is reported as failed. It is not reframed through a more
favourable statistic.

### 4.4 Fast motion

| Item | Result |
|---|---|
| Grasp + put-back | **11.67 s → 8.94 s** (−23%) |
| G8 fast-path landing | **2.27 mm** planar |
| Profile | S-curve 4.0 rad/s / 20 rad/s², bus-verified |
| Scope | Validated in one direction; not a general high-speed validation |

### 4.5 Repeatability, backlash and gripper envelope

| Item | Result |
|---|---|
| Arm repeatability, 30 visits | **0.449 mm RMS / 1.017 mm max**; joints repeat to 0–1 pulse |
| Backlash, joint4 ±0.1 rad | **1.117 mm** hysteresis; joint4 settles 10 pulses apart |
| Gripper tolerance envelope, 46 grasps | Opening axis passes **[-6, +12] mm** (±9 mm about a +3 mm centre); x/z pass at ±9 mm; 0/2 at ±15 and −12 |
| Gripper stroke | 2.22 rad (open −2.22, closed 0.0); ~34 counts backlash |

### 4.6 Full G8 and runtime integration

| Item | Result | Class |
|---|---|---|
| Full G8 acceptance (2026-11-23) | 8 phases / 11 commands, all `Completed` with `verification: bus`; put-back at 0.236 m | L5 |
| M4 read-only telemetry | 30 min, **1799/1799** samples `measured`, `writes=0` | L5 |
| M5.2 supervised joint | `joint1` **505 vs 512** pulses (within 8-pulse tolerance) | L5 |
| M5.2 gripper | close 183→645, open 647→183; timer + bus evidence | L5 |
| M5.2 stop | **0.266 ms** software stop; in-flight command did not continue | L5 |
| M6 S13 replay | **21/21** decisions consistent; validation mean 0.0166 ms, p95 0.0352 ms | L4 |
| M6 S17 real MoveIt | MoveIt 2.5.10, `SUCCESS`, 8-point plan, 0 controller servers, no command topics | L5 |
| Runtime image | `armpi-ultra:flatten-20261125`, 7.1 GB arm64; 20 nodes / 60 topics preserved; reboot persistent | L5 |

**Platform claim level:** these are **partially verified** for the platform as a
whole. M4/M5.2/S13/S17 scopes passed; the platform was never validated end to
end. The freeze record records this explicitly.

## 5. What the baseline does not show

- The 6 mm error-budget bound is **not met** by the RSS aggregation.
- The fast path was validated in one direction only.
- There is no hardware e-stop, brake, independent encoder, torque sensing or
  self-collision model. A software stop is a hold/zero command.
- The base is open-loop with no odometry; any base motion invalidates the table
  calibration.
- Results come from one platform, one site and a small number of supervised
  sessions.
- M6 S14 and the ecosystem G8 re-run were **never started**; the platform freeze
  retires them, not defers them.
- S7 stale-state injection and S9 runtime publisher detection were **not run on
  hardware**.
- None of these results is a safety certification.

## 6. Ecosystem Baseline 1 — offline integration

Baseline 1 is the offline integration of the new repositories. It is **not** the
frozen baseline and **not** a hardware acceptance. As of 2026-11-28:

| Status | Result |
|---|---|
| **DEVELOPMENT READY** | **YES** |
| **OFFLINE INTEGRATION READY** | **YES** |
| **BASELINE 1 COMPLETE** | **NO — technical PASS; formal COMPLETE after #40** |
| **DEPLOYMENT READY** | **NO** |

### 6.1 What passed on the candidate tree

| Check | Result |
|---|---|
| Real CLI vertical integration | `matched_with_unverified`; 2-step plan; mock `SUCCEEDED`; benchmark inconclusive; simulation not checked |
| Device snapshots | ArmPi 5-DoF, PiPER X 6-DoF, AR5 7-DoF (vendor-public, partial); no invented reach/payload/aperture/resolution |
| Hash contract | `source_hash` and artifact `content_hash` distinct; stale hash rejected |
| Cell composition | Arm + gripper + camera; missing role fails closed; missing fact unverified |
| Unit enforcement | Wrong threshold unit rejected (`INCOMPATIBLE_UNIT`) |
| Mock ore-sorting task | 8/8 expected classifications; only `normal` `SUCCEEDED`; failures stop once |
| Benchmark discrimination | Observed `INCONCLUSIVE`; test-pass `PASS`; test-fail `FAIL` |
| Regression | 15 repositories at fixed main SHAs + frozen `v1.0.0`; tests and gates pass (48) |
| Offline artifact contract 1.0.0 | **Accepted** for offline artifacts only; vocabulary `contracted`; golden vectors pass |

### 6.2 Blocking items at the time of the record

The 2026-11-28 record listed these items:

1. `jcheng-devices` #8, `jcheng-applications` #20 and `jcheng-interfaces` #21
   needed reviewer approval and merge-queue completion.
2. The interfaces proposal needed its owner's acceptance before the vocabulary
   could be called `contracted`.
3. The final acceptance/freeze PR needed approval and merge.
4. After merge, rerun fixed-main regression and independent QA on the final SHAs;
   only then could the status change to `COMPLETE`.

**Final status (2026-11-28, #41):** #8, #5, #21 and applications #20 have
merged. The ecosystem pages record **technical acceptance PASS** and an
independent QA result of **PASS WITH FINDINGS, P2 fixed**. Formal completion
awaits record **#40** (Board approval/merge); until then the status remains
`BASELINE 1 COMPLETE: NO` and `DEPLOYMENT READY: NO`.

### 6.3 Explicitly recorded limits

- ArmPi reach, payload, gripper aperture and camera resolution are unverified.
- AR5 is vendor-public and locally unverified; no SDK, URDF, calibration or unit.
- PiPER X has no motion adapter; P2 is read-only.
- Real perception, IK, grasp success, AMR and LeRobot integration are out of scope
  and unimplemented.
- Gazebo runtime is unavailable; simulation is offline asset validation.
- Deployment blockers are unchanged.

The full record is in [`docs/baseline1/`](baseline1/README.md), including the
manifest, independent QA and ratification package. No release or tag was
created for Baseline 1.

**Contract note.** Baseline 1 was recorded against `jcheng-interfaces` v0.2.0
(`afca22…`). v0.3.0 was released later on 2026-11-28 with robot-profile v2,
`chain_id` and gripper units (`8bc92d18…`). v0.2.0 remains the signed pin for the
current runtime consumers; v0.3.0 migration is in progress. Baseline 1's
contract-related rows are therefore historical and are not a v0.3.0 acceptance.

## 7. Capability evidence levels

| Repository | Version | Strongest evidence | Status |
|---|---|---|---|
| `jcheng-manipulation` | 1.0.0 | L5 full G8; paired trials; frozen | Frozen baseline |
| `jcheng-system` | 0.3.0-dev0 | L5 M4/M5.2/S13/S17 on ArmPi; PiPER P2 read-only | Experimental; scoped hardware |
| `jcheng-interfaces` | 0.3.0 | v0.3.0 released; v0.2.0 signed pin still deployed by 7 consumers | Verified contract; migration |
| `jcheng-perception` | 0.1.0 | One dual-view run; S1 offline synthetic + public | Experimental; partial |
| `jcheng-mobile` | 0.1.0 | Static `/scan`, `/odom`, `/map` | Experimental; dormant |
| `jcheng-learning` | 0.2.0 | M1 dataset contract and LeRobot round-trip | Experimental; offline |
| `jcheng-teleop` | 0.3.0 | M1 ROS-free core; mock/simulation L3 | Experimental; offline |
| `jcheng-devices` | 0.1.0 | 10 profiles / 7 capabilities; validator | Experimental; offline |
| `jcheng-scenarios` | 0.1.0 | 8 schemas; `ore_sorting` reference | Experimental; offline |
| `jcheng-simulation` | 0.1.0 | Domain 43; mock verified, Gazebo partial | Experimental; offline |
| `jcheng-studio` | 0.8.0 | Read-only REST/WS, sessions, replay | Experimental; no hardware |
| `jcheng-applications` | 0.1.0 | M3 mock run; 181 tests | Experimental; no hardware |
| `jcheng-benchmark` | 0.1.0 | Synthetic self-test; one migrated host snapshot | Inconclusive |
| `jcheng-ops` | 0.1.0 | Guards installed; watchdog never fired | Deployed; legacy |
| `jcheng-research` | 0.1.0 | Draft reports; unreviewed experiments | Experimental; no product claim |

## 8. Evidence index

- Frozen baseline: `jcheng-manipulation/evidence/` (G8, phase 2/3, calibration,
  repeatability, backlash, envelope, error budget).
- Runtime: `jcheng-system/e2e/reports/` (M3–M6, replay, concurrency, guard race)
  and `jcheng-system/deploy/armpi-ultra/docs/ACCEPTANCE-20261125.md`.
- Baseline 1: [`docs/baseline1/`](baseline1/README.md).
- Perception: `jcheng-perception/evidence/` and `ACCEPTANCE.md`.
- Learning: `jcheng-learning/evidence/20261126_m1/` and `ACCEPTANCE.md`.
- Benchmark: `jcheng-benchmark/evidence/host_benchmark_20261117_session4/`.
- Operations: `jcheng-ops/docs/VERIFICATION.md` and the 2026-11-24 incident record.

## 9. Reading rules

1. **Name the platform.** A result without a platform is not a hardware claim.
2. **Name the class.** L0–L5; do not call a mock test "verified".
3. **Separate baseline from ecosystem.** The frozen `v1.0.0` is not the new
   system's acceptance.
4. **Separate Baseline 1 from deployment.** Offline integration can be ready
   while deployment is not.
5. **Keep failed bounds.** A failed pre-registered bound is part of the result.
6. **Do not transfer.** ArmPi evidence does not validate PiPER X or AR5.
7. **Check the date.** Status changes; evidence paths are stable.
