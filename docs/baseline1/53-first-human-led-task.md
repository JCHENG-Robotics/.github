# First Human-Led R&D Task — Ore Target Localization & Grasp Target Generation

> Full specification: `~/jcheng/dev/TASK_ore_target_localization_20261128.md`.
> The core algorithm is **not implemented** by this delivery.

## 1. Goal

From one offline synthetic ore-scene observation, produce ore instance IDs,
visible 2D evidence, a **visible** 3D point with validity, and one deterministic
grasp target per reachable ore. Do not infer hidden geometry.

## 2. Inputs

- Synthetic dataset from `jcheng-perception` (`generate-synthetic`, seed
  20261126; 36 scenes, 3 empty).
- `jcheng.scene_state.v1` from `ore_scene.py run --dataset ...`.
- Camera model from the dataset; cell frame from
  `ore_sorting.environment`; device snapshot from `jcheng-devices`.

Start points:

- `jcheng-perception/ros2_ws/src/jcheng_perception_scene/jcheng_perception_scene/types.py`
- `jcheng-perception/ros2_ws/src/jcheng_perception_scene/jcheng_perception_scene/cli.py`
- `jcheng-perception/scripts/ore_scene.py`
- `jcheng-perception/docs/ORE_SCENE_UNDERSTANDING.md`

## 3. Output contract (draft)

`jcheng.ore_grasp_targets.v1` per scene, with:

- `instance_id`, `class`, `visible_centroid_px`;
- `visible_point_m` + `point_validity`;
- `score`, `confidence_kind`, `unknowns`;
- `grasp_target: {frame, position_m, approach, source}`.

Forbidden fields: `true_centroid`, `volume`, `mass`, `material_composition`,
`ore_grade`, `economic_value`. Unknown points have no coordinates. The target is
derived from visible geometry only; it is not an IK solution and does not
authorize motion.

## 4. Entry paths

- perception: new `targets.py` under `jcheng_perception_scene`;
- applications: new `grasp_targets.py` plus a `--grasp-targets` input to
  `scripts/ore_sorting_mock_task.py`.

Do not edit the frozen `jcheng-manipulation` baseline.

## 5. Data and metrics

Split 24/12 before tuning. Metrics: instance precision/recall at IoU 0.5;
visible-point error median/p95 in mm; empty-scene handling; unknown-discipline
audit; determinism. No real-ore, true-centroid or grasp-success claim is
available from this dataset.

## 6. Method

Generate and hash the dataset → run the unchanged S1 baseline → add only the
target module → run at least one ablation → save commands, code SHA, dataset
hash, environment and raw metrics under
`~/jcheng/phase2/ore-target-localization-YYYYMMDD/`.

## 7. Acceptance

Schema-valid output, no forbidden fields, structured errors for empty/invalid/
missing-depth inputs, metrics with sample counts, mock task accepts targets with
no new executor, `deployment_ready`/`motion_authorized` false, tests and docs.

## 8. Non-goals

YOLO/SAM training, true 3D completion, IK/collision planning, real grasp,
hardware, DDS, Gazebo runtime, deployment or release.
