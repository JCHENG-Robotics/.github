# Simulation Asset Validation Report

> Scope: offline asset availability and parse checks only. No Gazebo runtime was
> launched or claimed.

## 1. Environment

| Item | Status |
|---|---|
| `ros_gz_sim` | present |
| `gz` CLI | **missing** |
| Gazebo runtime | **not verified** |
| Mock backend | available and previously exercised on domain 43 |
| Simulation repo main | `40c250d93fdb72a5088e2c71f3dcb263c791eb0c` |

## 2. Repository checks

`jcheng-simulation` on main: **86 passed, 2 skipped**, gate OK. The tests cover
the profile loader, controller configuration, mock plant and scan/truth paths.

| Asset | Result |
|---|---|
| `robots/armpi_ultra/robot.yaml` | loads; URDF/controller references resolve |
| `robots/armpi_ultra/urdf/jcheng_armpi_sim.urdf.xacro` | referenced and parsed by the profile check |
| `robots/piper_x/` | profile/URDF present; no runtime adapter claimed |
| ore_sorting world/scene asset | **not found** |
| scenario `simulation_assets` | none declared; reference records `not_checked` |

## 3. Scenario environment profile

`jcheng-scenarios` validates `ore_sorting` (1 scenario, 6 profiles, 0 errors).
The environment profile declares frames (`cell`, `camera_optical`,
`robot_base`) and stations (`pick_surface`, `ore_bin`, `gangue_bin`) as design
data. It does not declare a Gazebo world, mesh or scene file, so there is no
ore_sorting simulation asset to load.

## 4. Conclusion

- Offline asset validation: **PASS for the assets that exist** (ArmPi robot
  profile + controller; simulation test suite).
- Ore_sorting Gazebo environment: **not available / not verified**.
- The reference correctly reports simulation `not_checked`; it does not fake a
  Gazebo run.

This satisfies the allowed offline-only scope in Decision 5. Installing Gazebo
or creating a world asset is future work, not a Baseline 1 blocker.
