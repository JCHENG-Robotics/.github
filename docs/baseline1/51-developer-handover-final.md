# Developer Handover — Final

> **DEVELOPMENT READY: YES.** Human development can start now; it does not wait
> for Baseline 1 merge or deployment readiness.

## 1. Authoritative files in the workspace

| Purpose | Path |
|---|---|
| Start here | `~/jcheng/QUICKSTART.md` |
| Full guide | `~/jcheng/DEVELOPER_GUIDE.md` |
| VS Code workspace | `~/jcheng/jcheng.code-workspace` |
| Dev entries | `~/jcheng/dev/*.sh` |
| Unified acceptance entry | `.github/dev/baseline1-acceptance.sh` (workspace symlink `~/jcheng/dev/baseline1-acceptance.sh`) |
| First task | `~/jcheng/dev/TASK_ore_target_localization_20261128.md` |
| Handover report | `.github` PR #32 content, superseded by this delivery |

## 2. Answers to the eight handover questions

1. **Which directory?** `~/jcheng`; open `jcheng.code-workspace`; edit
   `~/jcheng/jcheng-*`. Do not edit `.worktrees/`.
2. **Which ROS 2 environment?** `/opt/ros/jazzy` only; Humble is not installed.
3. **Which terminal/commands?** See `QUICKSTART.md`: `dev/env-check.sh`,
   `dev/build.sh`, `dev/test.sh`, `dev/mock-launch.sh`, `dev/sim-launch.sh`,
   `dev/validate-device.sh`, `dev/validate-scenario.sh`,
   `dev/reference-integration.sh`, `dev/baseline1-acceptance.sh`.
4. **Which repo for what?** `.github/docs/repo-boundaries.md`; perception for
   scene/localization, applications for task orchestration, system for runtime
   authority, devices/scenarios for declarations.
5. **How to run/debug a ROS node?** `source /opt/ros/jazzy/setup.bash`; use
   `ros2 run --prefix 'gdb -ex run --args' <pkg> <exe>` or `dev/debug.sh`.
6. **Where are the three arms?** See 50 and
   `jcheng-devices/docs/DEVICE_ASSET_INVENTORY.md`; private material under
   `~/03_Resources/robotics/` (read-only).
7. **Where are simulation/datasets/experiments/assets?** Simulation
   `~/jcheng/jcheng-simulation`; datasets `~/jcheng/perception_datasets`;
   experiments `~/jcheng/phase2` and `~/02_Areas/robotics-lab/experiment-data`;
   private vendor assets `~/03_Resources/robotics/`.
8. **Which paths are forbidden?** `/media/jerichocheng/{bootfs,rootfs}`,
   vendor assets, vendor container, production systemd units, real hardware
   output and motion.

## 3. Validated entries

| Entry | Last result |
|---|---|
| `dev/env-check.sh` | DEVELOPMENT READY with optional gaps |
| `dev/build.sh interfaces` | one package finished |
| `dev/test.sh interfaces/devices/scenarios/applications/system` | pass (counts in 48) |
| `dev/mock-launch.sh` | `/v1/health` 200, contract 0.2.0, DISARMED |
| `dev/sim-launch.sh` | `/sim/*` topics on domain 43, mock backend |
| `dev/validate-device.sh` | 7 devices / 7 capabilities |
| `dev/validate-scenario.sh` | 1 scenario / 6 profiles / 0 errors |
| `dev/reference-integration.sh` | `matched_with_unverified` on main |
| `dev/baseline1-acceptance.sh` | reference + 8 cases + benchmark, exit 0 |

## 4. First task

`~/jcheng/dev/TASK_ore_target_localization_20261128.md`: ore target
localization and grasp-target generation on synthetic data. Inputs, draft
`jcheng.ore_grasp_targets.v1` contract, entry paths, metrics, experiment method
and acceptance criteria are specified; the core algorithm is intentionally not
implemented.

## 5. Known gaps

- Humble, Nav2, slam_toolbox and `gz` CLI are absent; Gazebo runtime not verified.
- AR5 has no local SDK/URDF/calibration; PiPER X has no hardware.
- ArmPi reach/payload/aperture/camera resolution unverified.
- Real perception/grasp and deployment remain out of scope.
