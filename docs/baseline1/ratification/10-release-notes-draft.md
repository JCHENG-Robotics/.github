# Baseline 1 Release Notes — Draft

> **Draft only.** No release or tag was created. The Board decides whether/when
> to release. This is not a deployment authorization.

## Highlights

- Offline multi-repository baseline for ArmPi Ultra × ore_sorting.
- Real CLI artifacts: device snapshots, scenario requirements, role-composed
  cell, capability matching, reference plan, mock gateway and benchmark.
- Explicit semantics: `artifact_valid`, `capability_match_status`,
  `capability_satisfied`, `offline_execution_allowed`, `deployment_ready`,
  `motion_authorized`.
- Eight-case synthetic mock ore-sorting task with stop-once and authorization
  failure coverage.
- Three-arm registration: ArmPi Ultra 5-DOF reference, PiPER X 6-DOF candidate,
  ROKAE AR5L/AR5R 7-DOF planned dual-arm pair.
- Offline artifact contract 1.0.0: hash/unit/vocabulary semantics, golden
  vectors, Proposed→Accepted record.
- Developer handover: quick start, guide, unified acceptance entry and first
  human-led task.

## Known limits

- ArmPi reach/payload/aperture/camera resolution unverified.
- AR5 L/R variant kinematics/SDK/calibration absent; PiPER X no hardware.
- No real perception, IK, grasp or task-accuracy claim.
- Gazebo runtime not verified; simulation is offline asset validation.
- Deployment NOT READY: deployed tree 0.1.0, base bridge, lease sharing,
  watchdog, DDS holder and bench evidence outstanding.
- Studio B4 waiver remains until 2026-12-31; boundary debt remains.

## Safety

No real robot motion, hardware output or production deployment is included or
authorized. Software stop is not an emergency stop.
