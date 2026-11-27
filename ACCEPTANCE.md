# Ecosystem acceptance report

> Status: **inconclusive** as of 2026-11-27. This report records milestone-gate
> status; it is **not** a signed v1.0 acceptance. No ecosystem v1.0 acceptance
> run has been attempted.
> Operator: JerichoCheng. Reviewer: pending.
> Scope: the whole ecosystem (governance, contracts, system runtime, frozen
> baseline, capability, L4, benchmark, research and operations repositories).
> No motion commands were sent by this documentation change.
> Since 2026-11-26 the contract moved to v0.2.0 and 7 of 8 runtime consumers
> adopted it; the organization merge queue is active. No L0 gate fails.
> Organization CI reuse is in progress: the interfaces pilot references `@v1`
> and awaits merge (section 4).

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
| M2 contract definition and audit | `jcheng-interfaces` | L0–L1 | pass (15 tests; Humble CI, local Jazzy build) | `docs/ecosystem/09-m2-execution.md`; tag `v0.1.0` (historical) |
| Contract v0.2.0 rollout | `jcheng-interfaces` + 7 consumers | L1 | pass — signed tag verified; 7/8 consumers pin `afca22…`; perception not migrated | `docs/ecosystem/15-v020-alignment.md` |
| Organization merge queue | all protected repositories | L0 | pass — 11 repositories merged `merge_group`; ruleset active; break-glass recorded | `break-glass/2026-11-27-merge-queue-bootstrap.md` (workspace root) |
| Lockfile module topology | `jcheng-system` | L0–L1 | pass — `release 2026.11.1` pins teleop 0.3.0, applications 0.1.0 and studio 0.7.0; `verify_lock --module-root` checks the pinned commits | `jcheng-system/locks/ecosystem.lock.yaml`; PR #37 |
| Public system API version | `jcheng-system` | L0 | pass — `configs/api.yaml` defines `api_version 0.1.0`; module `system_api` ranges are checked against it | `jcheng-system/configs/api.yaml`; PR #39 |
| Teleop probe and publisher pins | `jcheng-system`, `jcheng-teleop` | L0–L1 | pass — both probes read the lockfile; the test-only publisher default matches `capability.yaml` | PRs #38, #8 |
| Organization CI reuse | `.github` | L0 | inconclusive — 3/7 reusable workflows are implemented; the interfaces pilot (PR #15) references `@v1` but is not merged | `.github/workflows/reusable-{contract-check,security,release}.yml`; `jcheng-interfaces` PR #15 |
| Workspace path consistency | workspace root | L0 | pass — the `~/jcheng` compatibility symlink points at `/home/jerichocheng/01_Projects/jcheng-robotics`; documented paths and `git_preflight.sh` work again | `/home/jerichocheng/jcheng` symlink |
| M3 mock stack and S1–S17 | `jcheng-system` | L2–L3 | pass (15 passed, 2 skipped, 0 required failures; 16 pytest) | `docs/ecosystem/10-m3-execution.md` |
| M4 read-only hardware integration | `jcheng-system` | L5 | pass (1799/1799 `measured`, `writes=0`, 30 min) | `docs/ecosystem/evidence/m4-readonly-20261123/` |
| M5.1 mock ROS transport | `jcheng-system` | L2–L3 | pass (5 ROS tests; CI `m5-mock`) | `jcheng-system/tests_ros/` |
| M5.2 supervised hardware motion | `jcheng-system` | L5 | inconclusive (core motions pass; S7/S9 not run) | `docs/ecosystem/evidence/m52-final-20261124/` |
| M6 S13 replay | `jcheng-system` | L4 | pass (21/21 decisions match; validate mean 0.0166 ms) | `docs/ecosystem/evidence/m6-s13-20261124/` |
| M6 S17 plan-only | `jcheng-system` | L1 | pass (construction and rejection tests) | `jcheng-system/tests/test_moveit_plan_only.py` |
| M6 S17 real MoveIt | `jcheng-system` | L5 | pass — MoveIt 2.5.10, `SUCCESS`, 8-point plan, 0 controller servers, no command topics | `jcheng-manipulation/docs/ecosystem/evidence/m6-s17-20261125/` |
| ArmPi Ultra image rebuild | `jcheng-system` | L5 | pass — 7.1 GB image, 20 nodes / 60 topics preserved, reboot persistent | `jcheng-system/deploy/armpi-ultra/docs/ACCEPTANCE-20261125.md` |
| M6 S14 base / full G8 | `jcheng-system` | L5 | not started | — |
| Teleop intake + simulation bridge | `jcheng-system`, `jcheng-teleop` | L2–L3 | pass (mock/simulation only) — intake 7+3 tests, ArmPi/Gate-2 domain-43 bridge; no hardware | `jcheng-system/e2e/reports/20261126_teleop_sim/`; `jcheng-teleop/ACCEPTANCE.md` |
| Frozen baseline v1.0.0 | `jcheng-manipulation` | L5 | pass (G8, build, ops; see its ACCEPTANCE.md) | `evidence/g8_acceptance_20261123/` |
| Mobile capability v0.1.0 | `jcheng-mobile` | L0–L5 | partial pass — offline + static `/scan`, `/odom`, `/map`; motion, mount pose and navigation unverified | `jcheng-mobile/ACCEPTANCE.md` |
| Perception capability v0.1.0 | `jcheng-perception` | L1–L5 | partial — synthetic + data path + aligned depth + split edge + one dual-view run + offline ore-scene S0/S1; repeatability, real-ore accuracy, multi-pose and motion unverified | `jcheng-perception/ACCEPTANCE.md` |
| Operations v0.1.0 | `jcheng-ops` | L5 | partial (installed and verified; watchdog never fired) | `jcheng-ops/ACCEPTANCE.md` |
| Operator console v0.7.0 | `jcheng-studio` | L0–L5 | pass — ported console, read-only REST/WS, sessions, intent path and M3 replay; no hardware acceptance | `jcheng-studio/ACCEPTANCE.md` |
| Application orchestration v0.1.0 | `jcheng-applications` | L0–L3 | pass — 181 tests with tree extra (161+3 skip without), M2 transport, M3 mock run and S3 branches/tree/WAITING/derived; no hardware | `jcheng-applications/ACCEPTANCE.md` |
| Learning capability v0.2.0 | `jcheng-learning` | L0–L1 | pass — M1 offline dataset infrastructure; no runtime node, policy or hardware | `jcheng-learning/ACCEPTANCE.md` |
| Teleoperation v0.3.0 | `jcheng-teleop` | L0–L3 | pass — M0 design/M1 ROS-free core + system mock intake/simulation bridge; no hardware | `jcheng-teleop/ACCEPTANCE.md` |
| Simulation plant v0.1.0 | `jcheng-simulation` | L0–L5 | pass (offline only) — mock verified, Gazebo partial; no hardware | `jcheng-simulation/ACCEPTANCE.md` |
| Benchmark harness v0.1.0 | `jcheng-benchmark` | L0–L2 | inconclusive — synthetic self-test only; no suite result | `jcheng-benchmark/ACCEPTANCE.md` |
| Research workspace v0.1.0 | `jcheng-research` | L0 | pass — structure/gate only; draft reports and SAM3/AGX Orin experiments recorded but unreviewed | `jcheng-research/ACCEPTANCE.md` |

## 3. Verified claims

| Claim | Level | Evidence |
|---|---|---|
| The organization and repository rules exist and are enforced | L0 | 111/111 M1 API checks; branch protection |
| Contract v0.2.0 builds, parses and passes parity checks | L0–L1 | `jcheng-interfaces` tag `v0.2.0`; hash `afca22…`; signed tag verified |
| Seven runtime consumers pin the v0.2.0 contract | L0 | `jcheng-system`, mobile, learning, simulation, teleop, studio and applications declare `>=0.2,<0.3` and the `afca22…` hash |
| The lockfile pins three module commits and verifies them | L0–L1 | `release 2026.11.1`; `verify_lock --module-root` reads `VERSION` and `capability.yaml` at each pinned commit; 94 tests |
| The public system API version is defined and checked | L0 | `configs/api.yaml` `api_version 0.1.0`; module `system_api` ranges validated by `verify_lock` |
| Three organization reusable workflows are implemented | L0 | contract-check, security and release; checkout + shell only; local shell checks pass |
| The mock system has no bypass publisher and rejects invalid motion | L3 | S1–S17: 15 scenarios pass, 2 skipped, 0 required failures |
| Read-only integration does not write to the robot | L5 | 30-minute run, `writes=0`, independent bus reads |
| Supervised single-joint and gripper motion completes with bus verification | L5 | 505 vs 512 pulses; gripper 183→645 / 647→183 |
| A stop request latches and rejects new commands | L5 | `ABORTED`/`STOP_LATCHED`; hold 0.266 ms |
| G8 decision replay matches the baseline | L4 | 21/21 decisions |
| Real MoveIt accepts the plan-only contract without execution | L5 | `SUCCESS`, 8-point plan, 0 controller servers, no command topics |
| The rebuilt 7.1 GB image preserves the robot workload and survives reboot | L5 | deploy acceptance 2026-11-25 |
| The frozen baseline meets its recorded G8 and trial results | L5 | `jcheng-manipulation` `ACCEPTANCE.md` |
| The mobile capability starts no hardware path and passes a static `/scan`/`/odom`/`/map` bring-up | L0–L5 | `jcheng-mobile/ACCEPTANCE.md` |
| The perception edge produces timestamp-matched fused targets and a single dual-view run | L3–L5 | `jcheng-perception/ACCEPTANCE.md` |
| The operations guards are installed and observe the robot | L5 | 2026-11-24 verification; `status.json` green |
| The learning, teleop, simulation, studio, applications, benchmark and research repositories pass their declared offline/L0 gates | L0–L2 | their `ACCEPTANCE.md` reports |

## 4. Not verified

| Item | Reason | Risk |
|---|---|---|
| M5.2 S7 stale-state injection | Not run on hardware | Stale state may not be rejected as designed |
| M5.2 S9 runtime unauthorized publisher | Not run on hardware | Publisher guard is not proven at runtime |
| M6 S14 hardware base | Not executed | Base intent path unproven on hardware |
| M6 full G8 re-run and landing evidence | Not executed | End-to-end ecosystem path unproven |
| Mobile motion, mount pose and navigation | Mount/footprint provisional; static only | No motion or navigation claim |
| Perception multi-pose accuracy and motion TF | Single static pose; no moving-target accuracy | Poses are not cleared for motion |
| Perception dual-view repeatability | Wrist depth DDS reader wedged at 7.5 s in run 10 | Full dual-view window not repeatable |
| Operations watchdog real trigger | No wedge reproduced; no synthetic kernel stall | Trigger path correct by design only |
| Operations reboot with drop-ins | Vendor boot sequence moves the arm; needs an operator | OOM settings take effect after restart only |
| New L3/L4/BENCH/research hardware or motion claims | These repositories are offline/mock/scaffold only | No hardware or motion claim is made for them |
| Ecosystem v1.0 acceptance | Not run | No v1.0 release claim |
| Organization reusable CI adoption | The interfaces pilot (PR #15) references `@v1`; no merged repository uses the workflows yet | Reuse is not proven until the pilot merges; gate logic is still duplicated |
| Perception contract adoption | No runtime imports of `jcheng_interfaces`; explicit waiver recorded | Perception is outside the v0.2.0 contract by declaration, not by adoption |
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
- The mobile mount/footprint values are provisional; motion is not accepted.
- Perception now uses aligned external depth (ADR 0004), but only one dual-view
  run exists and the wrist depth reader can still wedge.
- Learning, simulation, studio, applications, benchmark and research are
  offline/mock/scaffold repositories; none has a hardware or motion acceptance.
- The ecosystem is not safety-certified and claims no SIL/PL compliance.
- License status is not uniform: `jcheng-mobile` carries an MIT `LICENSE`,
  retained pending review, while the other new repositories have no `LICENSE`
  and grant no reuse until the review closes.
- The lockfile pins three modules (teleop, applications, studio) for the ArmPi
  combination; `jcheng-mobile` and `jcheng-perception` are intentionally outside
  it.
- Three of seven reusable workflows are implemented; the interfaces pilot
  (PR #15) references `@v1`, but each product repository still keeps its own
  gate until the pilot merges.
- The workspace is canonical at `/home/jerichocheng/01_Projects/jcheng-robotics`;
  the `~/jcheng` compatibility symlink is restored so the older documented paths
  keep working.
- `jcheng-perception` does not consume the interface contract at runtime; this
  is recorded as an explicit waiver in its `ROADMAP.md` and `ACCEPTANCE.md`.

## 6. Sign-off

| Role | Name | Date |
|---|---|---|
| Operator | JerichoCheng | 2026-11-27 |
| Reviewer | pending | — |

A signed acceptance requires a second reviewer and, for any L5 claim, the
operator's per-session authorization. This status report does not substitute
for either.

## 7. Machine-readable report

[`acceptance/ecosystem-2026-11-27.json`](acceptance/ecosystem-2026-11-27.json)
follows `acceptance-report.v1` and validates against
[`acceptance-report.v1.schema.json`](https://github.com/JCHENG-Robotics/jcheng-interfaces/blob/main/schemas/acceptance-report.v1.schema.json).
Its `reviewer` is `pending` and its `result` is `inconclusive`; it is a status
record, not a signed acceptance. The 2026-11-26, 2026-11-25 and 2026-11-24
reports are kept as history. Per-repository reports, when produced, must use the
same schema.

The 2026-11-27 snapshot was generated before the same-day merges of the lockfile
modules (PR #37), the public API version (PR #39), the probe and publisher pins
(PRs #38, #8), the perception waiver (PR #20) and the reusable CI workflows
(PR #18). The tables above are the current status; the JSON remains the
point-in-time record.
