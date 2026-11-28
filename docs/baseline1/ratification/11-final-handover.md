# Final Handover Report — Baseline 1

> Short handover. Baseline 1 is technically complete; the record publishes on
> merge of this PR. No release/tag, no deployment, no real motion.

## 1. What is ready

| Item | State |
|---|---|
| Offline artifact contract 1.0.0 | Accepted (offline only) |
| Vocabulary | `contracted` |
| Device registration | 9 profiles: ArmPi 5 reference, PiPER X 6 candidate, AR5 family + AR5L/AR5R 7 planned dual-arm |
| Real CLI cell | `matched_with_unverified`; reach/payload/aperture/resolution unverified |
| Mock ore-sorting task | 8/8 cases; only `normal` succeeds; benchmark INCONCLUSIVE with test PASS/FAIL |
| Regression | 15 main repos + frozen manipulation `v1.0.0`; all tests/gates pass |
| Developer handover | Quick Start, guide, unified acceptance entry, first task |

## 2. Open the workspace

`~/jcheng` — `~/jcheng/jcheng.code-workspace`. Key repositories are on `main`.
Do not develop in `.worktrees/` or touch vendor/production assets.

## 3. Commands

```bash
source /opt/ros/jazzy/setup.bash
cd ~/jcheng
dev/env-check.sh
dev/build.sh interfaces
dev/test.sh applications
dev/mock-launch.sh dev-token 8766
dev/sim-launch.sh
.github/dev/baseline1-acceptance.sh
```

## 4. First human-led task

**Ore Target Localization & Grasp Target Generation.** Start at:

`jcheng-perception/ros2_ws/src/jcheng_perception_scene/jcheng_perception_scene/types.py`

Then `cli.py`, `scripts/ore_scene.py`; spec:
`~/jcheng/dev/TASK_ore_target_localization_20261128.md`. The core algorithm is
yours; the agent supports environment, tests, review and documentation.

## 5. Remaining limits

Deployment **NOT READY**; ArmPi capability facts unverified; AR5 L/R variant
data absent; PiPER X no hardware; Gazebo runtime not verified; studio B4 waiver
until 2026-12-31; boundary 25 open + 1 waived. No release/tag; Board decides.

## 6. Forbidden

No robot start, real motion, DDS domain 0, production deployment, hardware
output, vendor asset commit, main push, force-push or unapproved merge.
