# Quick Start Verification

> Verified offline on 2026-11-28. No robot, DDS graph, Gazebo runtime or
> production deployment was used.

## 1. Files exist and are coherent

| File | Result |
|---|---|
| `~/jcheng/QUICKSTART.md` | present, commands match the current entries |
| `~/jcheng/DEVELOPER_GUIDE.md` | present, readiness and counts updated |
| `.github/dev/baseline1-acceptance.sh` | present, executable (`100755`) |
| `~/jcheng/dev/baseline1-acceptance.sh` | workspace symlink to the tracked entry |
| `~/jcheng/dev/TASK_ore_target_localization_20261128.md` | present, task definition only |
| `~/jcheng/jcheng.code-workspace` | present |

## 2. Commands actually run

| Command | Result |
|---|---|
| `dev/env-check.sh` | DEVELOPMENT READY with optional gaps |
| `dev/validate-device.sh` | 9 devices / 7 capabilities on merged main |
| `dev/validate-scenario.sh` | 1 scenario / 6 profiles / 0 errors |
| `dev/build.sh interfaces` | one package finished |
| `dev/test.sh interfaces` | 22 tests, gate OK |
| `dev/test.sh applications` | 218 + 5 skipped, gate OK |
| `dev/mock-launch.sh dev-token 8766` | `/v1/health` 200; contract 0.2.0; DISARMED |
| `dev/sim-launch.sh` | `/sim/*` topics on domain 43, mock backend |
| `.github/dev/baseline1-acceptance.sh` | exit 0; reference + 8 cases + benchmark |

## 3. Unavailable or limited

| Item | Reason |
|---|---|
| Gazebo runtime (`gz`) | CLI not installed; no ore_sorting world asset; mock backend is the verified path |
| Nav2 / slam_toolbox | not installed; AMR navigation is out of Baseline 1 scope |
| ROS 2 Humble build | robot target only; not installed locally |
| AR5 L/R motion | no local SDK/URDF/calibration/variant kinematics; registration only |
| PiPER X motion | no hardware/runtime adapter |
| Real perception/grasp | not implemented; first human-led task |

No command above starts the robot or sends motion. `dev/baseline1-acceptance.sh`
is loopback/synthetic only.
