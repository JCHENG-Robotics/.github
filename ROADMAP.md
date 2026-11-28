# JCHENG ecosystem roadmap

> Status: **Baseline 1 technical acceptance complete (2026-11-28)**; final
> record #40 pending Board approval/merge. Contract v0.2.0 runtime and the
> separate offline artifact contract 1.0.0 are in use. M6 hardware items and
> deployment remain open. No v1.0 release claim; no release/tag.
> English canonical. Repository-local roadmaps live in each repository.

## Current state

| Item | State | Evidence |
|---|---|---|
| **Baseline 1 offline integration** | **Technically complete; record #40 pending** | `docs/baseline1/ratification/`; real CLI cell + 8-case mock task + benchmark; 15-repo regression |
| **Offline artifact contract 1.0.0** | **Accepted** (offline only) | interfaces #20/#21 `426f371`; scenarios #5 `1c21885`; golden vectors |
| **Device registration** | 9 profiles | ArmPi 5, PiPER X 6, AR5 family + **AR5L/AR5R** 7; devices #7/#8 |
| Organization and three founding repositories | Complete (M1) | 111/111 API checks; `jcheng-ecosystem-bootstrap/M1-VERIFICATION.json` |
| Contracts `jcheng-interfaces` v0.2.0 | Complete (R5, 2026-11-27) | Contract hash `sha256:afca22a4…35b1c`; signed tag `v0.2.0` verified; 7/8 runtime consumers adopted |
| Mock system runtime `jcheng-system` | Complete (M3) | 15 scenarios pass, 2 skipped, 0 required failures; `main` `40a74ba` |
| Read-only robot integration | Complete (M4) | 30 min, 1799/1799 `measured`, `writes=0` |
| Mock ROS transport (lease, safety, ExecuteMotion, stop latch) | Complete (M5.1) | 5 ROS tests; CI `m5-mock` |
| Supervised hardware single-joint / gripper | Complete, core (M5.2) | joint1 505 vs 512 pulses; gripper 183→645/647→183; stop hold 0.266 ms |
| Replay and plan-only verification | In progress (M6) | S13 21/21; S17 plan-only and real MoveIt pass; S14 base and full G8 pending |
| ArmPi Ultra runtime image | Complete (2026-11-25) | `armpi-ultra:flatten-20261125`, 7.1 GB, `linux/arm64`; 20 nodes / 60 topics preserved; `jcheng-system/deploy/armpi-ultra/` |
| Frozen experimental baseline | Frozen | `jcheng-manipulation` `v1.0.0` at `b3411e4`; full G8 acceptance |
| Mobile capability | Experimental | `jcheng-mobile` v0.1.0; static `/scan`, `/odom` and `/map` pass; motion, mount pose and navigation unverified |
| Perception capability | Experimental | `jcheng-perception` v0.1.0; ADR 0004 aligned depth, split edge, one dual-view run and offline ore-scene S0/S1 (93 tests); repeatability, real-ore accuracy, multi-pose and motion unverified |
| Operations | Deployed | `jcheng-ops` v0.1.0; four robot guards and Studio watchdog installed and verified |
| Benchmark harness | Experimental | `jcheng-benchmark` v0.1.0; offline read-only harness and synthetic self-test only; no recorded or hardware result |
| Operator console | Experimental | `jcheng-studio` v0.7.0; ported console, read-only REST/WS, sessions, intent path and replay; no hardware acceptance |
| Application orchestration | Experimental | `jcheng-applications` v0.1.0; M2 read-only transport, M3 supervised run on the mock, S3 branches/tree/WAITING/derived-plan; no hardware |
| Learning | Experimental | `jcheng-learning` v0.2.0; M1 offline dataset infrastructure and capture boundary; no runtime node, policy or hardware |
| Teleoperation | Experimental | `jcheng-teleop` v0.3.0; M0 design and M1 ROS-free core complete; system mock intake and test-only ArmPi/Gate-2 simulation bridge pass L3; no hardware |
| Device library | Experimental | `jcheng-devices` v0.1.0; offline registry (6 devices / 7 capabilities), `device-profile.v1` / `capability-profile.v1`, validator and CI; no adapter, runtime or hardware |
| Simulation | Experimental | `jcheng-simulation` v0.1.0; offline multi-robot plant on domain 43; mock verified, Gazebo partial; no hardware |
| Research workspace | Experimental | `jcheng-research` v0.1.0; public; draft reports (Ultralytics, RLinf/PiPER X) and SAM3/AGX Orin experiments recorded, review pending; no product/hardware claim |
| Scenario catalog | Experimental | `jcheng-scenarios` v0.1.0; SCEN-layer declarative catalog, eight repository-local schemas, offline validation and the `ore_sorting` reference; no consumer integration, evaluation or hardware |
| License | Pending for most repositories | Frozen baseline and `jcheng-mobile` carry MIT (mobile retained pending review); `jcheng-interfaces`, `jcheng-system`, `jcheng-perception`, `jcheng-ops`, `jcheng-learning`, `jcheng-teleop`, `jcheng-devices`, `jcheng-simulation`, `jcheng-scenarios`, `jcheng-research`, `jcheng-benchmark`, `jcheng-studio`, `jcheng-applications` and `.github` have no `LICENSE` |

## Milestones

| Milestone | Scope | State | Exit criterion | Evidence |
|---|---|---|---|---|
| M0 | Architecture review and approval | Complete (2026-11-23) | Design record approved | `jcheng-manipulation` `docs/ecosystem/` |
| M1 | Organization, three repositories, branch protection, templates, CI skeleton | Complete (2026-11-23) | 111/111 checks pass | `jcheng-ecosystem-bootstrap/docs/M1-ACCEPTANCE.md` |
| M2 | Contract audit; `jcheng-interfaces` v0.1.0; CI; signed tag | Complete (2026-11-23) | Audit signed; 15 contract tests pass; tag Verified | `docs/ecosystem/09-m2-execution.md` |
| M3 | `jcheng-system` mock stack, lease, safety, arbitration, gateway | Complete (2026-11-23) | Required S1–S17 failures = 0; no vendor publisher | `docs/ecosystem/10-m3-execution.md` |
| M4 | Read-only robot integration (no motion) | Complete (2026-11-23) | 30 min, `writes=0`, independent bus reads match | `docs/ecosystem/evidence/m4-readonly-20261123/` |
| M5.1 | Mock ROS services/actions, lease, safety, stop latch | Complete (2026-11-24) | 5 ROS tests; `m5-mock` green | `jcheng-system` `tests_ros/` |
| M5.2 | Supervised single-joint and gripper execution | Complete, core (2026-11-24) | `COMPLETED` + `bus_verified`; stop latches | `docs/ecosystem/evidence/m52-final-20261124/` |
| M6 | Baseline replay and G8 re-validation | In progress — S13 21/21 and S17 plan-only + real pass; S14 base and full G8 pending | S13/S17 pass; S14 base and full G8 re-run with landing evidence | `docs/ecosystem/evidence/m6-s13-20261124/`; `jcheng-system/deploy/armpi-ultra/docs/ACCEPTANCE-20261125.md` |
| M7 | First integrated capability module on the system API | In progress — mobile static bring-up, perception split edge/dual-view; studio/applications/learning/teleop/simulation/devices scaffolds admitted | A capability passes L3 and supervised L5 through the system boundary | `jcheng-mobile`, `jcheng-perception`, `jcheng-studio`, `jcheng-applications`, `jcheng-learning`, `jcheng-teleop`, `jcheng-simulation`, `jcheng-devices` roadmaps |
| **B1** | **Baseline 1 offline integration and developer handover** | **Technical complete; #40 approval pending** | Real CLI cell, 8-case mock task, benchmark, regression, independent QA | `docs/baseline1/` |
| M8 | Ecosystem v1.0: lockfile, SBOM, signed acceptance report | Planned | All repositories at declared versions; ecosystem acceptance passes | — |

## Next — Human-Led Robotics R&D

Baseline 1 closes the centralized ecosystem-building phase. The next work is
human-led:

1. **First R&D task:** Ore Target Localization & Grasp Target Generation.
   Start at `jcheng-perception/.../jcheng_perception_scene/types.py`; spec in
   `dev/TASK_ore_target_localization_20261128.md`.
2. **Keep the Baseline 1 record current** after #40 merges; the agent provides
   test/review/documentation support only.
3. **Deployment is separate and NOT READY.** M6 hardware items, base bridge,
   lease sharing, watchdog and bench evidence require explicit authorization.
4. **Do not start Baseline 2** or add a new architecture programme.
5. Non-blocking debt stays in `docs/boundary-consolidation/32-technical-debt-register.md`.

## Out of scope

- Functional-safety certification. The platform has no e-stop, brake,
  independent encoder or self-collision model; it does not claim SIL/PL.
- Migration or rewriting of the frozen `jcheng-manipulation v1.0.0` tags,
  evidence or experiment history.
- Runtime dependency from `jcheng-system` on L3 capabilities or L4
  applications.
- Automatic real-robot motion from CI or unattended scripts.

## Dependencies

- `jcheng-interfaces` v0.2.0, contract hash
  `sha256:afca22a42f7163e0351d185d5a8577b0b51f2f3da4b92278f161a4a7d2c35b1c`.
- `jcheng-system` `>=0.1,<0.4` for capability repositories; system API range
  declared per `capability.yaml`.
- Every real-robot session requires separate, explicit operator authorization.
