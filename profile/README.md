# JCHENG Robotics

**Reproducible, safety-bounded robot manipulation.**  
From a measured 5-DoF manipulation baseline to an independently versioned robotics ecosystem.

[简体中文](README.zh-CN.md) | **English**

**Status:** M1 complete · 2026-11-23 · English canonical  
**Start here:** [Frozen baseline](https://github.com/JerichoCheng/jcheng-manipulation) ·
[Design record](https://github.com/JerichoCheng/jcheng-manipulation/blob/design/ecosystem-v1/docs/ecosystem/README.md) ·
[M1 evidence](https://github.com/JerichoCheng/jcheng-manipulation/blob/design/ecosystem-v1/docs/ecosystem/evidence/org-init-20261123/README.md)

**Contents:** [Overview](#overview) · [Why](#why-this-exists) · [Method](#method) ·
[Status](#status-at-a-glance) · [Evidence](#evidence-foundation) · [Architecture](#architecture) ·
[Safety](#safety-model-and-non-claims) · [Quality](#quality-and-reproducibility) ·
[Repositories](#repository-map) · [Roadmap](#roadmap) · [Governance](#governance) ·
[Limitations](#limitations-and-threats-to-validity) · [License](#license)

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
| Ecosystem initialization (M1) | **Complete** — three repositories created, `main` protected, **111/111** checks passed |
| Contracts | M1 skeleton only; no IDL/Schema yet; the contract audit is the M2 gate |
| System runtime | M1 skeleton only; no ROS packages, nodes or deployment units |
| Real-robot motion in the new ecosystem | **None**; M4/M5 require separate, explicit authorization |
| License | **Pending** third-party and copyright review; no `LICENSE` file has been added |

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

The first three repositories are deliberately small:

| Repository | Responsibility | M1 state |
|---|---|---|
| [`JCHENG-Robotics/.github`](https://github.com/JCHENG-Robotics/.github) | Governance, templates, reusable CI | Complete |
| [`JCHENG-Robotics/jcheng-interfaces`](https://github.com/JCHENG-Robotics/jcheng-interfaces) | Contracts, schemas, contract hashes | Skeleton; IDL after audit |
| [`JCHENG-Robotics/jcheng-system`](https://github.com/JCHENG-Robotics/jcheng-system) | Privileged runtime, safety, arbitration, gateway | Skeleton; M3 implementation |

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

The M1 gate keeps the new repositories free of runtime code and IDL; without a runtime publisher there
is no hardware write path. Safety claims will only be made after the corresponding tests and supervised
hardware evidence exist.

## Quality and reproducibility

| Gate | Current state |
|---|---|
| M1 repository checks | **111/111** API checks passed across three repositories |
| Branch protection | PR + CODEOWNERS + `m1-gate`; admins restricted; no force-push/delete |
| Contract integrity | Contract hash + `interface_manifest.json` (M2) |
| Dependency locking | `ecosystem.lock.yaml` pins commits, contract hash, image digest and robot profile (M2/M3) |
| Test levels | L0 contract → L1 unit → L2 mock integration → L3 mock E2E → L4 replay → L5 supervised hardware |
| No-bypass verification | Planned S1–S17 scenarios, including unauthorized-publisher and missing-lease cases (M3) |
| Evidence | Per-run records with versions, hashes, commands, observations and limitations |

The M1 evidence bundle is available at
[`org-init-20261123`](https://github.com/JerichoCheng/jcheng-manipulation/blob/design/ecosystem-v1/docs/ecosystem/evidence/org-init-20261123/README.md).
The design record is [`08-m1-execution.md`](https://github.com/JerichoCheng/jcheng-manipulation/blob/design/ecosystem-v1/docs/ecosystem/08-m1-execution.md).

## Repository map

| Repository | Role | State |
|---|---|---|
| `.github` | Organization governance, templates, reusable CI | M1 complete |
| `jcheng-interfaces` | ROS IDL, HTTP/WS schemas, contract hashes | M1 skeleton |
| `jcheng-system` | Safety, authority, motion, hardware bridge, gateway | M1 skeleton |
| `jcheng-manipulation` | Frozen `v1.0.0` experimental baseline and evidence | Read-only reference |
| `jcheng-teleop` | Teleoperation capability | Planned |
| `jcheng-learning` | Datasets, training, policy inference | Planned |
| `jcheng-mobile` | Mobile-base capability | Planned |
| `jcheng-applications` | Task orchestration and operator applications | Planned |

## Roadmap

| Milestone | Scope | State |
|---|---|---|
| M0 | Architecture review and approval | Complete |
| M1 | Organization, three repositories, templates, CI skeleton | **Complete** |
| M2 | Contract audit of existing interfaces; `jcheng-interfaces` v0.1 | Next |
| M3 | `jcheng-system` mock stack; lease, safety, arbitration, gateway | Planned |
| M4 | Read-only robot integration (no motion) | Planned |
| M5 | Supervised single-joint and gripper execution | Planned |
| M6 | Baseline replay and G8 re-validation | Planned |
| M7 | First external capability module | Planned |
| M8 | Ecosystem v1.0 release with lockfile, SBOM and acceptance report | Planned |

M2 begins with the contract audit: `arm_interfaces`, the Studio API, the gateway and the safety
execution paths must be mapped before any final IDL is defined. This avoids duplicate definitions and
preserves compatibility with the frozen baseline.

## Governance

- `main` is protected on all three repositories: pull request, independent review, CODEOWNERS,
  required `m1-gate`, linear history, no force-push or deletion.
- The organization currently has a single operating account. GitHub does not allow self-approval, so
  future `main` changes require a second reviewer or a documented break-glass procedure. Adding a
  second maintainer is the recommended next governance step.
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
- **New ecosystem maturity.** M1 is repository and governance initialization. The architecture is not
  yet runtime-validated; no safety or performance claim is made for it.
- **License status.** Reuse is not granted until the third-party and copyright review is complete.

## License

The frozen `jcheng-manipulation v1.0.0` baseline is MIT-licensed. The new repositories are public for
review but **do not yet have a `LICENSE` file**: the third-party dependency and copyright review is
pending. Until that review is approved, no MIT grant is made for the new repositories, and vendor
assets are not redistributed. See
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
