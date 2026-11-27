# JCHENG Robotics

**English** | [简体中文](README.zh-CN.md)

**Reproducible, safety-bounded robot manipulation.**  
From a measured 5-DoF manipulation baseline to an independently versioned robotics ecosystem.


**Status:** M1–M5.2 complete · M6 in progress · 2026-11-25 · English canonical  
**Start here:** [Ecosystem roadmap](https://github.com/JCHENG-Robotics/.github/blob/main/ROADMAP.md) ·
[Acceptance report](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md) ·
[Frozen baseline](https://github.com/JerichoCheng/jcheng-manipulation)

**Contents:** [Overview](#overview) · [Why](#why-this-exists) · [Method](#method) ·
[Status](#status-at-a-glance) · [Evidence](#evidence-foundation) · [Architecture](#architecture) ·
[Safety](#safety-model-and-non-claims) · [Quality](#quality-and-reproducibility) ·
[Repositories](#repository-map) · [Roadmap](#roadmap) · [Acceptance](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md) ·
[Governance](#governance) · [Limitations](#limitations-and-threats-to-validity) · [License](#license)

---

## Overview

JCHENG Robotics is an engineering organization for reliable, auditable robot manipulation on
low-cost hardware. It grew out of a project-based master's research project on a five-degree-of-freedom
ArmPi Ultra platform and is being developed into a multi-repository ecosystem with explicit contracts,
versioning, safety boundaries and reproducible evidence.

The work is guided by two commitments:

1. **Every claim is traceable to evidence.** Results are reported with commands, logs, datasets or
   machine-readable reports; unmeasured quantities are labelled as such.
2. **Every real-robot motion passes one boundary.** Motion intents are validated and arbitrated before
   any hardware command is published. New modules do not receive a second path to the actuators.

The program is organized around three questions:

1. **Measurement.** What accuracy and reliability are achievable when every transform, joint limit,
   camera frame and failure mode is measured rather than assumed?
2. **Reliability.** Which corrections and interventions survive pre-registered, paired real-robot
   trials rather than a single successful demonstration?
3. **Architecture.** How can new capabilities be added without creating a second path to the
   actuators or weakening the evidence chain?

This README is written as an engineering portfolio: problem definition, method, evidence, limitations
and reproducibility are stated explicitly. The English version is canonical; the Chinese version is a
translation.

## Why this exists

Low-cost 5-DoF arms are capable enough for table-top grasping, but their integration surfaces are
fragile. In the frozen `v1.0.0` baseline, the same platform had **six distinct motion write paths**,
four limit profiles with different runtime consumers, and at least four places where joint limits or
servo mappings were duplicated. The safety supervisor vetoed the MoveIt CLI path only; the fast path
was documented as bypassing it by design; the command cache could be mistaken for measured state.

The baseline solved the scientific question — what accuracy and reliability are achievable when every
transform, limit and failure mode is measured rather than assumed. The ecosystem addresses the
engineering question that follows: **how can new capabilities be added without weakening the safety,
reproducibility or evidence boundaries that made the baseline trustworthy?**

## Method

The baseline and the ecosystem follow the same measurement-first method:

- **Measure the platform before modelling it.** Joint stops, TF frames, camera extrinsics, gripper
  travel and bus behaviour were surveyed on the physical robot.
- **Prefer independent checks.** Checkerboard hand–eye validation, AprilTag scale checks, bus-register
  completion and a separate front camera are used instead of trusting a single source.
- **Pre-register comparisons.** The paired trials fixed the hypothesis, sample size and analysis
  before data collection; protocol deviations are recorded rather than hidden.
- **Report failed bounds.** The 6 mm error-budget bound is reported as failed instead of being
  reframed through a more favourable statistic.
- **Freeze the evidence.** `v1.0.0` is an immutable baseline; new work is versioned separately and
  cannot rewrite its tags, evidence or experimental history.
- **Separate plan from execution.** Planning, validation and execution are distinct stages with
  separate owners and evidence.

The new ecosystem adds one more rule: **the architecture itself must be testable**. The M3 mock stack
and the S1–S17 scenarios exist to prove the no-bypass boundary before any supervised hardware work.

## Status at a glance

| Item | Status |
|---|---|
| Experimental baseline | `jcheng-manipulation v1.0.0`, commit `b3411e4`, frozen; full G8 acceptance recorded |
| Ecosystem milestones | **M1–M5.2 complete**; M6 S13 and S17 real MoveIt verified; S14 base and full G8 pending |
| Contracts | `jcheng-interfaces` v0.1.0: 14 msg / 10 srv / 1 action, seven schemas, pinned contract hash |
| System runtime | `jcheng-system` 0.3.0-dev: 13 ROS packages; M4 read-only, M5.2 core, M6 S13 + S17 real verified; S14/G8 pending |
| Runtime image | `armpi-ultra:flatten-20261125`, 7.1 GB arm64; 20 nodes / 60 topics preserved and reboot persistent |
| Capability repositories | `jcheng-mobile` v0.1.0 static `/scan`/`/odom`/`/map`; `jcheng-perception` v0.1.0 aligned depth + split edge + one dual-view run + offline ORE S0/S1; `jcheng-ops` v0.1.0 deployed |
| Learning / simulation | `jcheng-learning` v0.2.0 M1 offline dataset infrastructure; `jcheng-simulation` v0.1.0 offline multi-robot plant on domain 43 (mock verified, Gazebo partial) |
| Teleoperation | `jcheng-teleop` v0.3.0 M0 design + M1 ROS-free core; system mock intake and ArmPi/Gate-2 simulation bridge pass L3; no hardware |
| Device library | `jcheng-devices` v0.1.0 offline registry (6 devices / 7 capabilities), device/capability schemas, validator and CI; no device access, runtime or motion |
| Operator / orchestration | `jcheng-studio` v0.7.0 console + read-only REST/WS + sessions/replay; `jcheng-applications` v0.1.0 M3 mock run + S3 branches/tree/WAITING/derived; no DDS or motion |
| Research | `jcheng-research` v0.1.0, public; draft reports and SAM3/AGX Orin experiments recorded, review pending |
| Benchmark | `jcheng-benchmark` v0.1.0 experimental; offline, read-only harness and synthetic self-test only; no recorded or hardware result |
| Real-robot motion in the new ecosystem | Supervised single-joint and gripper motions passed (M5.2); M6 S17 real plan-only passed without execution; full G8 re-run pending |
| Documentation | Unified README / ROADMAP / CHANGELOG / ACCEPTANCE set; English canonical, Chinese README |
| License | **Pending** for most new repositories; `jcheng-mobile` carries MIT from initialization; the review must resolve the exception |

## Evidence foundation

The following results are reported in the frozen baseline. They are **baseline results**, not results
of the new ecosystem, which does not yet execute motion.

| Evaluation | Reported result | Interpretation |
|---|---|---|
| Hand–eye calibration | 2.94 mm / 0.39° across 14 poses; hold-out 3.29 mm / 0.43° | Independent checkerboard validation, not vendor defaults |
| Paired fixed-site trial | 12/24 vs **24/24**, McNemar p = 0.00049 | Constant low-configuration correction, pre-registered |
| Random-placement trial | 9/24 vs **24/24**, McNemar p = 6.1 × 10⁻⁵ | Free placement, wrist/front-camera locate, base approach |
| Error budget | Translation RSS **13.325 mm** vs a 6 mm bound (fails); empirical placement mean **3.080 mm** | The bound is not met; the empirical mean is inside 6 mm |
| Fast motion | Grasp + put-back **11.67 s → 8.94 s**; G8 fast landing **2.27 mm** | S-curve 4.0 rad/s / 20 rad/s², bus-verified |

The baseline also records repeatability (0.449 mm RMS / 1.017 mm max), backlash (1.117 mm), a
±9 mm gripper tolerance envelope, and a full failure-mode taxonomy. The evidence index is in
[`jcheng-manipulation`](https://github.com/JerichoCheng/jcheng-manipulation).

**Critical reading:** the 6 mm error-budget bound is *not* satisfied by the RSS aggregation. The
reported placement mean is inside 6 mm, but that is a different statistic. The fast path was validated
in one direction. None of these results constitute a safety certification.

## Architecture

The target architecture separates **contracts**, **privileged execution**, **capabilities** and
**applications**:

```text
L4  Applications        task orchestration · operator UI · evidence review
L3  Capabilities        manipulation · teleop · learning · mobile
L2  System              authority · safety · motion · gateway · telemetry · guard
L1  Contracts           ROS IDL · OpenAPI/WS · configuration and evidence schemas
L0  Governance          org profile · templates · reusable CI · branch protection

Hardware plane          one publisher, vendor DDS domain 0
```

The founding repositories were deliberately small; the ecosystem has since
added independently versioned capability, operations and benchmark repositories:

| Repository | Responsibility | Current state |
|---|---|---|
| [`JCHENG-Robotics/.github`](https://github.com/JCHENG-Robotics/.github) | Governance, templates, reusable CI, ecosystem documents | M1 complete; documentation standard v1.0 |
| [`JCHENG-Robotics/jcheng-interfaces`](https://github.com/JCHENG-Robotics/jcheng-interfaces) | Contracts, schemas, contract hashes | v0.1.0, signed tag |
| [`JCHENG-Robotics/jcheng-system`](https://github.com/JCHENG-Robotics/jcheng-system) | Privileged runtime, safety, arbitration, gateway | 0.3.0-dev; M6 S13 + S17 real |
| [`JCHENG-Robotics/jcheng-mobile`](https://github.com/JCHENG-Robotics/jcheng-mobile) | L3 mobile base | v0.1.0; static bring-up |
| [`JCHENG-Robotics/jcheng-perception`](https://github.com/JCHENG-Robotics/jcheng-perception) | L3 perception | v0.1.0; aligned depth + single dual-view run |
| [`JCHENG-Robotics/jcheng-ops`](https://github.com/JCHENG-Robotics/jcheng-ops) | Cross-layer operations | v0.1.0 deployed |
| [`JCHENG-Robotics/jcheng-learning`](https://github.com/JCHENG-Robotics/jcheng-learning) | L3 learning: datasets, training, policy artifacts (offline) | v0.1.0; no runtime or policy |
| [`JCHENG-Robotics/jcheng-teleop`](https://github.com/JCHENG-Robotics/jcheng-teleop) | L3 teleoperation: operator input to bounded, lease-gated intent (offline) | v0.1.0; admission only |
| [`JCHENG-Robotics/jcheng-devices`](https://github.com/JCHENG-Robotics/jcheng-devices) | L3 device library: declarative profiles, capability model and offline validation | v0.1.0; offline registry only |
| [`JCHENG-Robotics/jcheng-simulation`](https://github.com/JCHENG-Robotics/jcheng-simulation) | Offline multi-robot plant on domain 43 | v0.1.0; mock verified, Gazebo partial |
| [`JCHENG-Robotics/jcheng-studio`](https://github.com/JCHENG-Robotics/jcheng-studio) | L4 operator console | v0.7.0 |
| [`JCHENG-Robotics/jcheng-applications`](https://github.com/JCHENG-Robotics/jcheng-applications) | L4 task orchestration | v0.1.0 |
| [`JCHENG-Robotics/jcheng-research`](https://github.com/JCHENG-Robotics/jcheng-research) | Public investigation workspace | v0.1.0; outside runtime graph |
| [`JCHENG-Robotics/jcheng-benchmark`](https://github.com/JCHENG-Robotics/jcheng-benchmark) | Cross-layer read-only benchmark harness | v0.1.0 experimental; synthetic self-test only |

### The single motion path

```text
capability module
  → acquire lease
  → ExecuteMotion (contract + lease + idempotency checks)
  → safety validation
  → motion executor
  → hardware bridge (the only publisher)
  → bus-verified result + evidence record
```

Design decisions that follow from this boundary:

- **A lease, not a UI session, grants control.** Leases carry scope, priority, TTL, deadman and
  revocation semantics; they can be audited and preempted.
- **The safety supervisor vetoes; it does not execute.** It validates state freshness, joint limits,
  trajectory rates, start state, workspace and table clearance, and latches a stop on violation.
- **The hardware bridge is the only publisher.** Capability modules join an unprivileged DDS domain;
  the vendor domain is reachable only through the bridge.
- **MoveIt plans; the arbiter executes.** The controller execution chain is not exposed as a second
  motion entry.
- **Measured state is not command echo.** `GetBusServoState` is the completion authority; cached
  `/joint_states` is labelled `commanded`.
- **Failure is fail-closed.** A missing safety heartbeat, stale measured state, bus-read failure or
  unknown outcome latches a stop; it is not retried automatically.

## Safety model and non-claims

The platform has **no hardware e-stop, brake, independent encoder, torque sensing or self-collision
model**. The base is open-loop with no odometry. A software stop is a hold/zero command, not a
safety-rated stop.

Consequently:

- All real-robot work is supervised and requires **separate, explicit authorization** per session.
- The UI and documentation say “software stop” or “stop request”, never “emergency stop”.
- Vendor container restarts can move the arm (`startup_check`); the system does not restart the vendor
  container automatically.
- The new ecosystem is not safety-certified and does not claim SIL/PL compliance.

The runtime now exists, so the boundary is enforced rather than only declared.
M4 proved that the read-only path publishes telemetry and no commands
(`writes=0`, 30 minutes). M5.1 exercised lease, safety and stop semantics over
ROS services/actions against the mock stack; M5.2 connected the same path to
the supervised hardware bridge for one joint and the gripper. S7 (stale-state
injection) and S9 (runtime publisher detection) remain unverified on hardware,
and every real-robot session still requires separate, explicit authorization.

## Quality and reproducibility

| Gate | Current state |
|---|---|
| Repository checks | M1 **111/111** API checks; M2–M6 CI gates in the three founding repositories |
| Branch protection | PR + CODEOWNERS + per-repository required checks; admins restricted; no force-push/delete |
| Contract integrity | Contract hash + `interface_manifest.json`, v0.1.0, verified tag |
| Dependency locking | `ecosystem.lock.yaml` pins commits, contract hash, profile hash and interfaces v0.1.0 |
| Test levels | L0 contract → L1 unit → L2 mock integration → L3 mock E2E → L4 replay → L5 supervised hardware |
| No-bypass verification | S1–S17: 15 scenarios pass, 2 skipped, 0 required failures; M5.1 adds 5 ROS transport tests |
| Hardware evidence | M4 read-only 1799/1799 `measured`, `writes=0`; M5.2 joint/gripper with bus verification and stop latch; M6 S17 real MoveIt `SUCCESS`; 7.1 GB image preserves 20 nodes / 60 topics |
| Evidence | Per-run records with versions, hashes, commands, observations and limitations |
| Documentation | Standard v1.0; every product repository carries the four-document set |

Current status and evidence are aggregated in the
[ecosystem roadmap](https://github.com/JCHENG-Robotics/.github/blob/main/ROADMAP.md) and
[acceptance report](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md). The M1
verification JSON is kept in the local staging archive `jcheng-ecosystem-bootstrap/M1-VERIFICATION.json`;
the design record is in `jcheng-manipulation` branch `design/ecosystem-v1` (`docs/ecosystem/`).

## Repository map

| Repository | Role | State |
|---|---|---|
| `.github` | Organization governance, templates, reusable CI, ecosystem documents | M1 complete; documentation standard v1.0 |
| `jcheng-interfaces` | ROS IDL, HTTP/WS schemas, contract hashes | v0.1.0 |
| `jcheng-system` | Safety, authority, motion, hardware bridge, gateway | 0.3.0-dev; M6 S13 + S17 real |
| `jcheng-manipulation` | Frozen `v1.0.0` experimental baseline and evidence | Read-only reference |
| `jcheng-mobile` | Mobile-base capability (M10, SLAM, Nav2 intent) | v0.1.0; static `/scan`/`/odom`/`/map`; motion unverified |
| `jcheng-perception` | Distributed edge/GPU perception | v0.1.0; aligned depth, split edge, one dual-view run; repeatability unverified |
| `jcheng-ops` | Unattended operations, watchdog and recovery | v0.1.0 deployed |
| `jcheng-benchmark` | Cross-layer read-only benchmark harness and evidence reports | v0.1.0 experimental; no recorded or hardware result |
| `jcheng-simulation` | Offline multi-robot plant on domain 43 | v0.1.0; mock verified, Gazebo partial |
| `jcheng-learning` | Datasets, training and policy artifacts (offline) | v0.1.0; no runtime or policy |
| `jcheng-research` | Public investigation workspace: reports and decisions | v0.1.0; outside runtime graph |
| `jcheng-mobile-bench` | Bench material split out of `jcheng-mobile` | Sandbox; not released |
| `jcheng-teleop` | Teleoperation intent: operator input to bounded, lease-gated intent | Experimental; v0.1.0 admission-only scaffold |
| `jcheng-devices` | Device library: declarative device/capability profiles and offline validation | Experimental; v0.1.0 offline registry |
| `jcheng-studio` | Operator console: debug, diagnostics and experiment records | Experimental; v0.7.0 console, REST/WS, sessions, replay |
| `jcheng-applications` | Task orchestration: recipe validation, deterministic planning and fail-closed intent sequencing | Experimental; v0.1.0 offline core + read-only transport |

## Roadmap

| Milestone | Scope | State |
|---|---|---|
| M0 | Architecture review and approval | Complete |
| M1 | Organization, three repositories, templates, CI skeleton | **Complete** |
| M2 | Contract audit; `jcheng-interfaces` v0.1.0 | **Complete** |
| M3 | `jcheng-system` mock stack; lease, safety, arbitration, gateway | **Complete** |
| M4 | Read-only robot integration (no motion) | **Complete** |
| M5 | Supervised single-joint and gripper execution | **Complete** (M5.1 mock, M5.2 hardware core) |
| M6 | Baseline replay and G8 re-validation | **In progress** — S13 21/21, S17 plan-only and S17 real MoveIt pass; S14 base and full G8 pending |
| M7 | First integrated capability module | **In progress** — mobile static bring-up; perception split edge/dual-view; learning, teleop, simulation, studio and applications scaffolds admitted |
| M8 | Ecosystem v1.0 release with lockfile, SBOM and acceptance report | Planned |

M6 is the current gate. The decision replay matches the baseline (21/21), and
the S17 plan-only contract now passes against real MoveIt 2.5.10 without
execution; what remains is the S14 base, a full G8 re-run and landing evidence.
Each requires separate, explicit authorization. M5.2 also leaves S7
(stale-state injection) and S9 (runtime publisher detection) unverified.

## Governance

- `main` is protected on every repository: pull request, independent review, CODEOWNERS, linear
  history, no force-push or deletion. Required checks are per repository — `m1-gate` for governance
  and perception, `m1-gate` + `m2-contract` for interfaces, five gates for the system runtime,
  `ops-gate` for operations, and `benchmark-gate` for the benchmark harness.
- The single-account phase ended with a second reviewer (`@JerichoSwaine`), who has maintain access
  and is a CODEOWNER on every repository. `main` changes require one author and one reviewer;
  a documented break-glass procedure is not the default.
- Any real-robot motion requires the operator's explicit authorization; CI and automation never
  trigger motion.
- Security reports follow [`SECURITY.md`](https://github.com/JCHENG-Robotics/.github/blob/main/SECURITY.md);
  do not disclose exploit details or credentials publicly.
- Contributions follow [`CONTRIBUTING.md`](https://github.com/JCHENG-Robotics/.github/blob/main/CONTRIBUTING.md)
  and the design-change template.

## Limitations and threats to validity

- **Single platform and site.** Results come from one ArmPi Ultra, one table setup and a small number
  of supervised sessions. They are not a population-level reliability claim.
- **No hardware safety chain.** No e-stop, brake, independent encoder, torque sensing or odometry.
- **TCP-only geometric guards.** Workspace and table checks use the tool point; link and gripper
  collision are outside the model.
- **Open-loop base.** Any base motion invalidates the table calibration; the base has no odometry.
- **Fast path scope.** The 4.0/20 profile is bus-verified but was validated in one direction.
- **Error-budget bound.** The 6 mm RSS bound is not met; the empirical placement mean is a different
  statistic and should not be read as passing the bound.
- **New ecosystem maturity.** M6 is incomplete: S14 and a full G8 re-run remain,
  and S7/S9 are unverified. Mobile has only a static bring-up; perception has
  one dual-view run and a wrist depth reader that can still wedge. No motion
  claim is made for either capability.
- **Operations coverage.** The watchdog has never fired in a real wedge; the
  reboot path has not been exercised because the vendor boot sequence moves the
  arm.
- **License status.** The baseline and `jcheng-mobile` carry MIT; the other new
  repositories have no `LICENSE` and grant no reuse until the review closes.
  The mobile file is retained pending review, not a precedent.

## License

The frozen `jcheng-manipulation v1.0.0` baseline is MIT-licensed. `jcheng-mobile`
was initialized with an MIT `LICENSE`. The other new repositories (`.github`,
`jcheng-interfaces`, `jcheng-system`, `jcheng-perception`, `jcheng-ops`,
`jcheng-benchmark`) have **no
`LICENSE` file**: the third-party dependency and copyright review is pending.
Until that review is approved, no MIT grant is made for those repositories, and
vendor assets are not redistributed. The `jcheng-mobile` file is **retained
pending the review** (see its `LICENSE-REVIEW.md`); it is not a precedent for
adding licenses elsewhere. See
[`license-review.md`](https://github.com/JCHENG-Robotics/.github/blob/main/docs/license-review.md).

## Citation

If you reference the experimental baseline, please cite:

```bibtex
@software{jcheng_manipulation_2026,
  author  = {Cheng, Kewei (Jericho)},
  title   = {JCHENG Manipulation: A ROS 2-Based Robotic Manipulation System with Quantitative Reliability Evaluation},
  year    = {2026},
  version = {1.0.0},
  url     = {https://github.com/JerichoCheng/jcheng-manipulation}
}
```

## Contact

- Design and contract questions: open a `design` issue in the relevant repository.
- Security: follow `SECURITY.md`; do not open a public exploit issue.
- Real-robot work: coordinated with the operator; no remote motion requests.

The baseline evidence index, failure taxonomy and full experimental record remain the authoritative
reference for the platform's measured behaviour.
