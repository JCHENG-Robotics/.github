# Ecosystem acceptance report

> Status: **inconclusive** as of 2026-11-24. This report records milestone-gate
> status; it is **not** a signed v1.0 acceptance. No ecosystem v1.0 acceptance
> run has been attempted.
> Operator: JerichoCheng. Reviewer: pending.
> Scope: the whole ecosystem (governance, contracts, system runtime, frozen
> baseline, capability and operations repositories).
> No motion commands were sent by this documentation change.

## 1. How to read this report

Acceptance is layered L0–L5 as defined in
[`docs/documentation-standard.md`](docs/documentation-standard.md#7-acceptancemd).
Each repository keeps its own detailed report; this file aggregates the result
and links to it. Synthetic, mock and replay results are never counted as
hardware validation. A milestone is `pass` only when its declared exit
criterion is met and the evidence exists.

Evidence paths that begin with `docs/ecosystem/` are in the
`jcheng-manipulation` design record (branch `design/ecosystem-v1`); the M1
verification JSON is in the local staging archive
`jcheng-ecosystem-bootstrap/`. They are not in this repository.

## 2. Gate results

| Gate | Repository | Level | Result | Evidence |
|---|---|---|---|---|
| M1 organization and repository initialization | `.github`, interfaces, system | L0 | pass (111/111 API checks) | `jcheng-ecosystem-bootstrap/M1-VERIFICATION.json` |
| M2 contract definition and audit | `jcheng-interfaces` | L0–L1 | pass (15 tests; Humble CI, local Jazzy build) | `docs/ecosystem/09-m2-execution.md`; tag `v0.1.0` |
| M3 mock stack and S1–S17 | `jcheng-system` | L2–L3 | pass (15 passed, 2 skipped, 0 required failures; 16 pytest) | `docs/ecosystem/10-m3-execution.md` |
| M4 read-only hardware integration | `jcheng-system` | L5 | pass (1799/1799 `measured`, `writes=0`, 30 min) | `docs/ecosystem/evidence/m4-readonly-20261123/` |
| M5.1 mock ROS transport | `jcheng-system` | L2–L3 | pass (5 ROS tests; CI `m5-mock`) | `jcheng-system/tests_ros/` |
| M5.2 supervised hardware motion | `jcheng-system` | L5 | inconclusive (core motions pass; S7/S9 not run) | `docs/ecosystem/evidence/m52-final-20261124/` |
| M6 S13 replay | `jcheng-system` | L4 | pass (21/21 decisions match) | `docs/ecosystem/evidence/m6-s13-20261124/` |
| M6 S17 plan-only | `jcheng-system` | L1 | pass (construction and rejection tests) | `jcheng-system/tests/test_moveit_plan_only.py` |
| M6 real MoveIt / S14 base / full G8 | `jcheng-system` | L5 | not started | — |
| Frozen baseline v1.0.0 | `jcheng-manipulation` | L5 | pass (G8, build, ops; see its ACCEPTANCE.md) | `evidence/g8_acceptance_20261123/` |
| Mobile capability v0.1.0 | `jcheng-mobile` | L0–L1 | pass (offline only) | `jcheng-mobile/ACCEPTANCE.md` |
| Perception capability v0.1.0 | `jcheng-perception` | L1–L5 | partial (synthetic + data path; no metric motion) | `jcheng-perception/ACCEPTANCE.md` |
| Operations v0.1.0 | `jcheng-ops` | L5 | partial (installed and verified; watchdog never fired) | `jcheng-ops/ACCEPTANCE.md` |

## 3. Verified claims

| Claim | Level | Evidence |
|---|---|---|
| The organization and repository rules exist and are enforced | L0 | 111/111 M1 API checks; branch protection |
| Contract v0.1.0 builds, parses and passes parity checks | L0–L1 | `jcheng-interfaces` 15 tests; contract hash |
| The mock system has no bypass publisher and rejects invalid motion | L3 | S1–S17: 15 scenarios pass, 2 skipped, 0 required failures |
| Read-only integration does not write to the robot | L5 | 30-minute run, `writes=0`, independent bus reads |
| Supervised single-joint and gripper motion completes with bus verification | L5 | 505 vs 512 pulses; gripper 183→645 / 647→183 |
| A stop request latches and rejects new commands | L5 | `ABORTED`/`STOP_LATCHED`; hold 0.266 ms |
| G8 decision replay matches the baseline | L4 | 21/21 decisions |
| The frozen baseline meets its recorded G8 and trial results | L5 | `jcheng-manipulation` `ACCEPTANCE.md` |
| The mobile capability starts no hardware path | L0 | `tests/test_no_hardware.py`; 2 test files pass |
| The perception edge produces timestamp-matched fused targets in synthetic runs | L3 | 58–77 tests; synthetic demo, 99%+ match |
| The operations guards are installed and observe the robot | L5 | 2026-11-24 verification; `status.json` green |

## 4. Not verified

| Item | Reason | Risk |
|---|---|---|
| M5.2 S7 stale-state injection | Not run on hardware | Stale state may not be rejected as designed |
| M5.2 S9 runtime unauthorized publisher | Not run on hardware | Publisher guard is not proven at runtime |
| M6 real MoveIt plan-only (S17) | Not executed; only construction/validation | Planner integration may differ from the plan contract |
| M6 S14 hardware base | Not executed | Base intent path unproven on hardware |
| M6 full G8 re-run and landing evidence | Not executed | End-to-end ecosystem path unproven |
| Mobile navigation on hardware | No M10, Nav2 or RTAB-Map on the robot; mount pose provisional | No `/scan`, `/odom`, `/map` claim |
| Perception multi-pose accuracy, aligned depth, motion TF | Single static pose only; external depth unaligned | Poses are not cleared for motion |
| Perception dual-view repeatability | Wrist depth DDS reader wedged at 7.5 s in run 10 | Full dual-view window not repeatable |
| Operations watchdog real trigger | No wedge reproduced; no synthetic kernel stall | Trigger path correct by design only |
| Operations reboot with drop-ins | Vendor boot sequence moves the arm; needs an operator | OOM settings take effect after restart only |
| Ecosystem v1.0 acceptance | Not run | No v1.0 release claim |
| License review | Pending; `jcheng-mobile` carries MIT from initialization (retained pending review), the other new repositories have no `LICENSE` | No uniform reuse position; the review must confirm or replace the mobile file |

## 5. Limitations

- One ArmPi Ultra, one site, a small number of supervised sessions; results are
  not a population-level reliability claim.
- No hardware e-stop, brake, independent encoder, torque sensing or
  self-collision model. A software stop is a hold/zero command.
- The base is open-loop with no odometry; any base motion invalidates the table
  calibration.
- Vendor restarts can move the arm; unattended operation must keep the
  workspace clear.
- The mobile mount/footprint values and the perception external depth are
  provisional; neither repository may be used for motion on the current
  evidence.
- The ecosystem is not safety-certified and claims no SIL/PL compliance.
- License status is not uniform: `jcheng-mobile` carries an MIT `LICENSE`,
  retained pending review, while the other new repositories have no `LICENSE`
  and grant no reuse until the review closes.

## 6. Sign-off

| Role | Name | Date |
|---|---|---|
| Operator | JerichoCheng | 2026-11-24 |
| Reviewer | pending | — |

A signed acceptance requires a second reviewer and, for any L5 claim, the
operator's per-session authorization. This status report does not substitute
for either.

## 7. Machine-readable report

[`acceptance/ecosystem-2026-11-24.json`](acceptance/ecosystem-2026-11-24.json)
follows `acceptance-report.v1` and validates against
[`acceptance-report.v1.schema.json`](https://github.com/JCHENG-Robotics/jcheng-interfaces/blob/main/schemas/acceptance-report.v1.schema.json).
Its `reviewer` is `pending` and its `result` is `inconclusive`; it is a status
record, not a signed acceptance. Per-repository reports, when produced, must use
the same schema.
