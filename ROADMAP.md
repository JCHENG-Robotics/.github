# JCHENG ecosystem roadmap

> Status: **M1–M5.2 complete; M6 in progress** as of 2026-11-26.
> The ecosystem has not reached v1.0 and makes no v1.0 acceptance claim.
> English canonical. Repository-local roadmaps live in each repository.

## Current state

| Item | State | Evidence |
|---|---|---|
| Organization and three founding repositories | Complete (M1) | 111/111 API checks; `jcheng-ecosystem-bootstrap/M1-VERIFICATION.json` |
| Contracts `jcheng-interfaces` v0.1.0 | Complete (M2) | Contract hash `sha256:0b8d72ce…f24b42`; signed tag `v0.1.0` |
| Mock system runtime `jcheng-system` | Complete (M3) | 15 scenarios pass, 2 skipped, 0 required failures; `main` `40a74ba` |
| Read-only robot integration | Complete (M4) | 30 min, 1799/1799 `measured`, `writes=0` |
| Mock ROS transport (lease, safety, ExecuteMotion, stop latch) | Complete (M5.1) | 5 ROS tests; CI `m5-mock` |
| Supervised hardware single-joint / gripper | Complete, core (M5.2) | joint1 505 vs 512 pulses; gripper 183→645/647→183; stop hold 0.266 ms |
| Replay and plan-only verification | In progress (M6) | S13 21/21; S17 plan-only and real MoveIt pass; S14 base and full G8 pending |
| ArmPi Ultra runtime image | Complete (2026-11-25) | `armpi-ultra:flatten-20261125`, 7.1 GB, `linux/arm64`; 20 nodes / 60 topics preserved; `jcheng-system/deploy/armpi-ultra/` |
| Frozen experimental baseline | Frozen | `jcheng-manipulation` `v1.0.0` at `b3411e4`; full G8 acceptance |
| Mobile capability | Experimental | `jcheng-mobile` v0.1.0; static `/scan`, `/odom` and `/map` pass; motion, mount pose and navigation unverified |
| Perception capability | Experimental | `jcheng-perception` v0.1.0; ADR 0004 aligned depth, split edge and one dual-view run; repeatability, multi-pose and motion unverified |
| Operations | Deployed | `jcheng-ops` v0.1.0; four robot guards and Studio watchdog installed and verified |
| Benchmark harness | Experimental | `jcheng-benchmark` v0.1.0; offline read-only harness and synthetic self-test only; no recorded or hardware result |
| Operator console | Experimental | `jcheng-studio` v0.7.0; ported console, read-only REST/WS, sessions, intent path and replay; no hardware acceptance |
| Application orchestration | Experimental | `jcheng-applications` v0.1.0; offline recipe/planning/runner core and M2 read-only transport; no motion |
| Learning | Experimental | `jcheng-learning` v0.1.0; offline dataset/training/policy-artifact boundary; no runtime node, policy or hardware |
| Simulation | Experimental | `jcheng-simulation` v0.1.0; offline multi-robot plant on domain 43; mock verified, Gazebo partial; no hardware |
| Research workspace | Experimental | `jcheng-research` v0.1.0; private, reports and decisions only; no investigation complete |
| License | Pending for most repositories | Frozen baseline and `jcheng-mobile` carry MIT (mobile retained pending review); `jcheng-interfaces`, `jcheng-system`, `jcheng-perception`, `jcheng-ops`, `jcheng-learning`, `jcheng-simulation`, `jcheng-research`, `jcheng-benchmark`, `jcheng-studio`, `jcheng-applications` and `.github` have no `LICENSE` |

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
| M6 | Baseline replay and G8 re-validation | In progress — S13 21/21 and S17 plan-only + real pass; S14 base and full G8 pending | `docs/ecosystem/evidence/m6-s13-20261124/`; `jcheng-system/deploy/armpi-ultra/docs/ACCEPTANCE-20261125.md` |
| M7 | First integrated capability module on the system API | In progress — mobile static bring-up, perception split edge/dual-view; studio/applications/learning/simulation scaffolds admitted | A capability passes L3 and supervised L5 through the system boundary | `jcheng-mobile`, `jcheng-perception`, `jcheng-studio`, `jcheng-applications`, `jcheng-learning`, `jcheng-simulation` roadmaps |
| M8 | Ecosystem v1.0: lockfile, SBOM, signed acceptance report | Planned | All repositories at declared versions; ecosystem acceptance passes | — |

## Next

1. **Finish M6.** S17 real MoveIt plan-only passed on 2026-11-25; S14 base
   acceptance, full G8 re-run and landing evidence remain. Prerequisites:
   separate explicit authorization and an operator present.
2. **Integrate one capability end to end.** Mobile has a static `/scan`,
   `/odom` and `/map` bring-up; perception has aligned depth, split edge and a
   single dual-view run. Both still need their own accuracy/repeatability work,
   then a supervised path through `jcheng-system`.
3. **Close the residual M5.2 items.** S7 stale-state injection and S9 runtime
   publisher detection need a supervised hardware session.
4. **Keep the image lock current.** Re-record
   `jcheng-system/deploy/armpi-ultra/container/image.lock` on every image
   change; the 2026-11-25 digest is the current reference.

## Out of scope

- Functional-safety certification. The platform has no e-stop, brake,
  independent encoder or self-collision model; it does not claim SIL/PL.
- Migration or rewriting of the frozen `jcheng-manipulation v1.0.0` tags,
  evidence or experiment history.
- Runtime dependency from `jcheng-system` on L3 capabilities or L4
  applications.
- Automatic real-robot motion from CI or unattended scripts.

## Dependencies

- `jcheng-interfaces` v0.1.0, contract hash
  `sha256:0b8d72ced7f54d444d6851d8b99a51a78e2bed3f687324f51a15f76557f24b42`.
- `jcheng-system` `>=0.1,<0.4` for capability repositories; system API range
  declared per `capability.yaml`.
- Every real-robot session requires separate, explicit operator authorization.
