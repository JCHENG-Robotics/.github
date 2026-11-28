# Developer Handover Summary

## 1. Open this workspace

`~/jcheng` — open `~/jcheng/jcheng.code-workspace` in VS Code. Edit only
`~/jcheng/jcheng-*`; do not edit `.worktrees/`, `/media/jerichocheng/{bootfs,rootfs}`,
`~/03_Resources/robotics/` or production units.

Read first:

- `~/jcheng/QUICKSTART.md`
- `~/jcheng/DEVELOPER_GUIDE.md`
- `.github/dev/baseline1-acceptance.sh`

## 2. Environment and commands

```bash
source /opt/ros/jazzy/setup.bash     # Jazzy only; Humble absent
cd ~/jcheng
dev/env-check.sh
dev/build.sh interfaces
dev/test.sh interfaces
dev/test.sh applications
dev/mock-launch.sh dev-token 8766
dev/sim-launch.sh                    # domain 43, mock backend
.github/dev/baseline1-acceptance.sh  # unified offline acceptance
```

Learning tests: set `UV_PROJECT_ENVIRONMENT=/tmp/jcheng-learning-venv`; do not
create `.venv` inside the repo (the repo gate rejects large/broken link files).

## 3. First research task — start here

Task: **Ore Target Localization & Grasp Target Generation**.

Start from:

1. `jcheng-perception/ros2_ws/src/jcheng_perception_scene/jcheng_perception_scene/types.py`
2. `jcheng-perception/ros2_ws/src/jcheng_perception_scene/jcheng_perception_scene/cli.py`
3. `jcheng-perception/scripts/ore_scene.py`
4. `jcheng-perception/docs/ORE_SCENE_UNDERSTANDING.md`

Add localization in a new `targets.py` under `jcheng_perception_scene`; add
task-level target selection in `jcheng-applications` and feed the existing
`scripts/ore_sorting_mock_task.py` via a new `--grasp-targets` input. Do not
implement the core algorithm for the owner; the task spec is at
`~/jcheng/dev/TASK_ore_target_localization_20261128.md`.

## 4. What is currently forbidden

- Starting the robot, ssh motion, or sending any real motion command.
- Setting `ARMPI_HARDWARE_MOTION=1`, enabling legacy studio motion or real
  hardware output.
- Modifying production deployment, vendor container, systemd units or private
  vendor assets.
- DDS domain 0; use 42/43 offline only.
- Committing vendor SDK/URDF/mesh/manual, calibration, datasets, tokens or
  absolute private paths.
- Pushing main, force-pushing, rewriting history or merging without real review.

## 5. Current limits

Gazebo `gz` CLI absent and no ore_sorting world; Nav2/slam_toolbox absent; AR5
L/R variant data missing; PiPER X no hardware; ArmPi capability facts
unverified. Deployment NOT READY.
