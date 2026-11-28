# Developer Handover Report

> Status: **DEVELOPMENT READY** (offline; optional tool gaps). **OFFLINE
> INTEGRATION READY: no. DEPLOYMENT READY: no.**
> Handover date: 2026-11-28. No robot, production deployment or real hardware
> output was touched. **Update:** TD-17/18/19 converged on development branches
> the same day; the real cell now completes with `matched_with_unverified`.
> `main` remains NO until #5/#3/#19 merge; see [40](40-td-contract-convergence-report.md).

## 1. Environment (measured)

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS, kernel 7.0.0-44 |
| CPU / RAM / disk | 16 cores / 27 GiB / 238 GiB free on `/home` |
| ROS 2 | **Jazzy only** at `/opt/ros/jazzy`; Humble not installed |
| MoveIt 2 | `moveit_core`, `moveit_ros_planning` present |
| Nav2 / slam_toolbox | **missing** (optional for current offline tasks) |
| Gazebo | `ros_gz_sim` present; `gz` CLI missing; use `backend:=mock` |
| Toolchain | g++ 13.3.0, cmake 3.28.3, make 4.3, Python 3.12.3, uv 0.13.8, colcon |
| Tools | VS Code 1.145.2, GDB 15.1, Git 2.43.0, Docker 29.9.3, no Podman |

`dev/env-check.sh` → `DEVELOPMENT READY with optional gaps`.

## 2. Workspace plan

| Area | Path | Rule |
|---|---|---|
| Official development | `~/jcheng/jcheng-*` | edit here; branch from `origin/main` for new work |
| VS Code workspace | `~/jcheng/jcheng.code-workspace` | multi-folder, Jazzy, build dirs excluded |
| Agent temporary | `~/jcheng/.worktrees/*`, `.git-safety/` | do not edit; PR/audit work |
| Experiments | `~/02_Areas/robotics-lab/experiment-data`, `~/jcheng/phase2` | results/data |
| Simulation | `~/jcheng/jcheng-simulation` | domain 43 only |
| Vendor assets | `~/03_Resources/robotics/` | **read-only** |
| Datasets | `~/jcheng/perception_datasets` (1.5G), `~/.local/share/jcheng/assets/piper_x` | private; do not commit |
| Frozen baseline | `~/jcheng/jcheng-manipulation@v1.0.0` | read-only |
| Developer entries | `~/jcheng/dev/` | scripts |
| Guide | `~/jcheng/DEVELOPER_GUIDE.md` | start here |

No file was deleted or migrated. Existing branches/worktrees/build dirs remain.

## 3. Validated entry points

| Entry | Command | Result |
|---|---|---|
| Environment | `dev/env-check.sh` | DEVELOPMENT READY + optional gaps |
| Workspace status | `dev/workspace-status.sh` | 18 checkouts, 26 worktree dirs, data sizes |
| Devices | `dev/validate-device.sh` | **7 devices / 7 capabilities** |
| Scenarios | `dev/validate-scenario.sh` | **1 scenario / 6 profiles / 0 errors** |
| Build | `dev/build.sh interfaces` | 1 package finished |
| Test | `dev/test.sh system` | 191 passed + gate |
| Test | `dev/test.sh devices` | 58 passed + gate |
| Test | `dev/test.sh scenarios` | 114 passed + gate (phase2 branch) |
| Mock gateway | `dev/mock-launch.sh dev-token 8788` | `/v1/health` 200: status ok, contract 0.2.0, DISARMED |
| Simulation mock | `dev/sim-launch.sh` | 4 `/sim/*` topics on domain 43 |
| Reference | `dev/reference-integration.sh` | **fail-closed** (TD-17/18/19) |

## 4. Multi-device registration

| Arm | DOF | Status | Assets |
|---|---|---|---|
| HiWonder ArmPi Ultra | 5 | **reference** | profiles, system overlay, simulation, private vendor tree/manuals |
| AgileX PiPER X | 6 | candidate, unverified | public profiles/URDF/ROS (MIT), pyAgxArm (LGPL), external cache |
| Rokae AR5 | 7 | **planned, data_missing** | no SDK/URDF/limits/calibration found; placeholder only |

- Device model IDs are `vendor.model`; instance IDs (`model@instance`) are
  separate. DOF is an attribute, never the ID.
- AR5 uses `data_status: missing` and no invented kinematics/limits.
- Private vendor assets are not committed or pushed.
- Device asset inventory: `<workspace>/jcheng-devices/docs/DEVICE_ASSET_INVENTORY.md`
  (in the devices repository).

## 5. First manual task

`<workspace>/dev/TASK_ore_sorting_20261128.md`: offline ore instance recognition
→ visible 3D geometry → grasp target → mock execution. Inputs, outputs, entry
points, acceptance criteria and non-goals are specified; the core
implementation is intentionally left to you.

## 6. Readiness

| State | Result | Meaning |
|---|---|---|
| DEVELOPMENT READY | **YES** (optional gaps) | edit/build/test/debug/mock/validate/experiment offline |
| OFFLINE INTEGRATION READY | **NO on main** / **YES on convergence branches** | real artifacts complete with `matched_with_unverified` on #5/#3/#19; main awaits merge/QA (40) |
| DEPLOYMENT READY | **NO** | deployed tree, base bridge, lease sharing, bench/hardware absent |

You can start development now; do not wait for DEPLOYMENT READY.

## 7. Forbidden actions

- Start/ssh the robot for motion, send motion, enable real hardware output.
- Modify `/media/jerichocheng/{bootfs,rootfs}`, `~/03_Resources/robotics/`, the
  vendor container or production systemd units.
- Commit vendor SDK/manual/mesh/calibration/datasets/tokens/absolute paths.
- Enable `ARMPI_HARDWARE_MOTION`, legacy studio motion or `gz` hardware paths.

## 8. Known gaps

- Humble/Nav2/slam_toolbox/`gz` CLI absent locally (CI/container needed).
- AR5 has no vendor data; PiPER X has no hardware.
- Cross-repo artifact schema/vocabulary and the ArmPi reference remain open.
- 200 ms freshness / 300 ms deadman remain provisional.

## Related

- Developer guide: `<workspace>/DEVELOPER_GUIDE.md`
- [Status model](31-status-model.md)
- [Deployment readiness](36-deployment-readiness-updated.md)
