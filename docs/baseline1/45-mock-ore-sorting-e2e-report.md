# Mock Ore-Sorting E2E Report

> Candidate: applications PR #20 (`c4d871c`). Evidence:
> `~/jcheng/phase2/baseline1-acceptance-20261128/mock-task/`.
> Every observation, target and sample is `data_source: synthetic`.

## 1. What was executed

The task uses the existing applications runtime, not a second executor:

```text
synthetic observation
  → candidate grasp target (fixed reference poses, not IK)
  → six-step recipe through jcheng_applications.model
  → existing supervised lease + linear runner + loopback mock gateway
  → task result
  → synthetic benchmark samples
```

Recipe: HOME → JOINT_STEP pre-grasp → GRIPPER close → JOINT_STEP transfer →
GRIPPER open → HOME. Scopes: arm + gripper.

## 2. Eight cases

| Case | Status | Run state | Execute | Stop | Success |
|---|---|---|---|---|---|
| normal | SUCCEEDED | SUCCEEDED | 6 | 0 | **true** |
| no-target | NO_TARGET | — | 0 | 0 | false |
| unreachable | UNREACHABLE | — | 0 | 0 | false |
| grasp-failure | GRASP_FAILED | FAILED | 3 | 1 | false |
| timeout | TIMEOUT | INDETERMINATE | 2 | 1 | false |
| authorization-failure | AUTHORIZATION_FAILED | ABORTED | 0 | 0 | false |
| stop-request | STOP_REQUESTED | ABORTED | 2 | 1 | false |
| capability-unmet | CAPABILITY_UNMET | — | 0 | 0 | false |

Only `normal` sets `success: true`; it places `ore-001` in `ore_bin` with
`data_source: synthetic`. No task success threshold or real grasp claim exists.

The summary records `scenario_requirements` (scenario/evaluation IDs and both
hashes), `repository_shas`, `artifact_valid`, `capability_satisfied`,
`offline_execution_allowed`, `deployment_ready` and `motion_authorized`; every
sample carries `scenario_id`, `scenario_version` and `evaluation_id`.

## 3. Safety and authorization checks

- The normal run acquires and releases one lease, executes six mock steps, and
  requests no stop.
- Grasp failure, timeout and stop request each submit exactly one stop.
- Authorization failure acquires a lease but submits **zero** execute requests
  and records `ABORTED`.
- `task_summary.json` states `offline_execution_allowed: true`,
  `deployment_ready: false`, `motion_authorized: false`.
- No DDS/ROS, Gazebo, camera, perception model, IK or hardware is used.

## 4. Benchmark evidence

| Suite | Threshold | Result |
|---|---|---|
| observed | none | **inconclusive** |
| test-pass | success_rate ≥ 0.10 | **pass** |
| test-fail | success_rate ≥ 0.99 | **fail** |

The observed rate is 1/8 = 0.125. The test thresholds are explicitly labelled
as test-only, not business acceptance criteria. The PASS/FAIL/INCONCLUSIVE
discrimination is the evidence that the benchmark harness works.

## 5. Interpretation

This proves task orchestration and interface behaviour on synthetic data. It
does not prove ore recognition, 3D localization, grasp planning, real grasp
success or ore-sorting accuracy. Those remain the human-led R&D task in 53.
