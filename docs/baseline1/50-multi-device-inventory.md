# Multi-Device Inventory

> Registration/offline assets only. No PiPER X or AR5 runtime adapter, motion,
> deployment or hardware test is included. Source of truth:
> `jcheng-devices/docs/DEVICE_ASSET_INVENTORY.md`.

## 1. Models

| Arm | Device ID | DOF | Status | Local data | Capabilities |
|---|---|---|---|---|---|
| Hiwonder ArmPi Ultra | `hiwonder.armpi-ultra` | 5 | **reference** | profiles, system overlay, simulation, private vendor tree/manual | `arm.position_control`, `arm.joint_feedback` |
| AgileX PiPER X | `agilex.piper-x` | 6 | **candidate** | public URDF/ROS (MIT), pyAgxArm (LGPL), external cache; no hardware | `arm.position_control`, `arm.joint_feedback` |
| Rokae AR5 | `rokae.ar5` | 7 | **planned, partial** | vendor-public facts only; no SDK/URDF/calibration/unit | `arm.position_control` (planned) |

## 2. Model vs instance

- Device ID = model (`vendor.model`). It never encodes DOF.
- A real unit is an instance, e.g. `hiwonder.armpi-ultra@armpi-lab-01`; instance
  metadata is deployment data and is not part of the registry ID.
- DOF is an attribute from kinematics; AR5 reports 7 because the vendor page
  states 7, not because of the model name.

## 3. AR5 re-verification

The official ROKAE AR-series page
(<https://www.rokae.com/en/product/show/595/>, accessed 2026-11-28) states:

- 7 DOF, 5 kg rated payload, 683 mm operating radius;
- EtherCAT, joint torque sensors standard;
- joint ranges axis1 ±178°, axis2 ±120°, axis3 ±178°, axis4 -60…145°,
  axis5 ±178°, axis6 ±60°, axis7 ±90°.

The vendor-public facts are recorded with `verification: unverified`,
`data_status: partial` and `workspace.verified: false`. No local SDK, URDF,
calibration or measured unit exists; these limits must not be used for planning
or safety until checked on the real controller.

## 4. Assets and licenses

| Category | ArmPi | PiPER X | AR5 |
|---|---|---|---|
| Public repo assets | declarative profiles | declarative profiles | declarative profile with cited vendor facts |
| Vendor SDK/URDF/mesh/manual | private, not committed | external cache/vendor repos, licenses retained | none found |
| Calibration | private | none | none |
| Datasets | private perception datasets | private cache | none |

No vendor SDK, URDF, mesh, manual, calibration, dataset, token or absolute
private path is committed or pushed.

## 5. Availability

- ArmPi: full reference path (profiles + system overlay + simulation +
  mock/real deployment evidence of the old tree); device limits still
  unverified.
- PiPER X: profile/URDF/simulation only; no runtime adapter or hardware.
- AR5: registration only; no runtime, no simulation, no hardware.

## 6. Non-goals

No interchangeability claim; each arm has a different kinematic and control
model. No second/third arm integration into the ore-sorting reference task.
