# Quick Start Guide

> Authoritative workspace copy: `~/jcheng/QUICKSTART.md`. This page is the
> versioned handover summary.

## 1. Open and check

```bash
cd ~/jcheng
code jcheng.code-workspace
source /opt/ros/jazzy/setup.bash
dev/env-check.sh
```

Expected: `DEVELOPMENT READY with optional gaps`. Use ROS 2 Jazzy only; Humble
is not installed.

## 2. Build and test

```bash
dev/build.sh interfaces
dev/build.sh system
dev/build.sh simulation

dev/test.sh interfaces
dev/test.sh devices
dev/test.sh scenarios
dev/test.sh applications
dev/test.sh system
dev/test.sh mobile
dev/test.sh studio
dev/test.sh learning
```

## 3. Validate and run the offline chain

```bash
dev/validate-device.sh
dev/validate-scenario.sh
dev/reference-integration.sh
.github/dev/baseline1-acceptance.sh
```

`.github/dev/baseline1-acceptance.sh` generates real CLI artifacts, runs the cell
reference, the eight-case mock ore-sorting task and the benchmark
discrimination, then asserts the gates. Evidence defaults to
`dev/out/baseline1`; override the `*_ROOT` and `OUT` variables to pin checkouts.

## 4. Mock gateway and simulation

```bash
dev/mock-launch.sh dev-token 8766
curl -s http://127.0.0.1:8766/v1/health | python3 -m json.tool

dev/sim-launch.sh
# another terminal
export ROS_DOMAIN_ID=43
ros2 topic list | grep /sim
```

`gz` CLI is missing; Gazebo runtime is not verified. Do not install it silently.

## 5. Debug and inspect

```bash
dev/debug.sh <package> <executable>
ros2 node list
ros2 topic list
ros2 action list
ros2 service list
```

## 6. First task

Read `~/jcheng/dev/TASK_ore_target_localization_20261128.md`. It defines the
synthetic data, draft output contract, entry paths, metrics and acceptance
criteria; the core algorithm is yours to implement.

## 7. Forbidden

No robot start, real motion, ssh motion, production deployment, hardware output,
vendor asset modification, dataset/token/vendor commit, `main` push,
force-push, history rewrite or merge without a real reviewer approval.
