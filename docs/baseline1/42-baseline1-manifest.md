# Baseline 1 Manifest

> Fixed at 2026-11-28. `main` SHAs are the regression base; candidate SHAs are
> the unmerged implementation under review. No release/tag was created.

## 1. Repositories on main

| Repository | main SHA | Version |
|---|---|---|
| `.github` | `b1e07067462f06339e4f2a58ccb664b3008d6eb0` | n/a |
| `jcheng-interfaces` | `1e6ecd03122809cf02f2ad81a3cb3218ca107ae2` | 0.2.0 |
| `jcheng-devices` | `b82f273e9124be99c3579b8b506ca571e47f6e9e` | 0.1.0 |
| `jcheng-scenarios` | `eac6dda1e7cdd8a80063fe8365518cf20bf2f65a` | 0.1.0 |
| `jcheng-applications` | `02ed6151a33dde86a309f058d1d1ba0eda51a42d` | 0.1.0 |
| `jcheng-system` | `72b2ce25266d3463d4590e871f6a2905fd938704` | 0.3.0-dev0 |
| `jcheng-mobile` | `f96cfee2a3330d6a830f9807f92dc0539ee5d7be` | 0.1.0 |
| `jcheng-studio` | `40c002b02131e56b1a4923c8a5f75a2beb26909c` | 0.8.0 |
| `jcheng-perception` | `343e621298518f8dbc7c02873f11885bb9de2fa4` | 0.1.0 |
| `jcheng-learning` | `69978259f8d6bbfa21f472a4d139bd6798a6f10b` | 0.2.0 |
| `jcheng-teleop` | `984b12f5c96d39462b6f6ecf33d4c914bdd75684` | 0.3.0 |
| `jcheng-simulation` | `40c250d93fdb72a5088e2c71f3dcb263c791eb0c` | 0.1.0 |
| `jcheng-benchmark` | `bfaeac9ee4cb9f5cd5b555b21ec08e1e8d9645e7` | 0.1.0 |
| `jcheng-ops` | `4d365f6bd354a1a6cefc676da92d648d73c973c3` | 0.1.0 |
| `jcheng-research` | `58858ecea618fb0dd12bda84d39db49bf0ded2b6` | 0.1.0 |
| `jcheng-manipulation` | tag `v1.0.0` = `b3411e43ad31c09f396cdd2db0fdfda8f09853dd` | 1.0.0 (frozen) |

`jcheng-design` and `jcheng-ecosystem-bootstrap` are not Baseline 1 runtime or
artifact consumers.

## 2. Candidate PR heads

| Repository | PR | Head SHA | Base | Status |
|---|---|---|---|---|
| devices | #7 | `dbf933b55b29a677f46b3a0ac7426092fa22a8de` | `b82f273` | open, CI green, review required |
| applications | #20 | `bc6dc5b98a6373d89b0ed89053eea2444225e722` | `02ed615` | open, CI green, review required |
| interfaces | #20 | `bdd0e59a6f30a3e1abe52b43e04e855f91c142ee` | `1e6ecd0` | open, CI green, review required |
| `.github` | this PR | recorded in the merge commit | `b1e0706` | open, review required |
| `.github` handover | #32 | `584168d` | older main | content superseded by this delivery |

## 3. Artifact hashes (candidate device tree)

| Artifact | Version | source_hash | content_hash |
|---|---|---|---|
| `hiwonder.armpi-ultra` | 0.1.0 | `sha256:f3c0c1b5373066599e46f85a63055a7a0cd3cd53f96c939bd4e101413551aeb9` | `sha256:602e211ed6be27823154c1cd7ac06a97af9db95c45c844531408cfc0f729dbeb` |
| `hiwonder.armpi-ultra-gripper` | 0.1.0 | `sha256:7077e9b2ecb496510acd06a3a7aed5ea09d0dbfd132ea5cb03beb49d73d4e535` | `sha256:079af9c0e9e92543b3b8c3b56f0afaa095446f6271f9bc5a924b6058191028ae` |
| `intel.realsense-d435i` | 0.1.0 | `sha256:319392259245ccdc9247897f585a0146a387839c31aff913c65c9ba0a62308a5` | `sha256:f5942741a875bae3247416cfb6e39d7d7a61765c8bc9b04a0fb00551ad5f7451` |
| `agilex.piper-x` | 0.1.0 | `sha256:b97de34e64826a2c093762675d7cfdd1cf3601beb85b4b982f6689780758edfa` | `sha256:07081ad041148dfaa4b6abc8e0d583683b4e298f98ccc8add18399a3cda30ecc` |
| `rokae.ar5` | 0.2.0 | `sha256:36cf6bad959672762420ee3e1d700246628543015d8762666e854cfe7abb583b` | `sha256:949a0170aa218e8094e5101d205ad86e825adb1cc05f1159e34db57a92d499ce` |

Scenario requirements `ore_sorting` 0.1.0:

- `content_hash`: `sha256:ca9d9f032cd2e2c4d9547c3ed23d2a958da26740b03046ca9aad489da18eb323`
- `provenance.scenario_content_hash`: `sha256:5e540ccf3e0d3704c00ae61ed88450ea476d2f95fd6dd6283c966d4d6a9dad10`

The values are pinned to the candidate device tree; regenerating after a
profile or scenario change produces new hashes and requires a new manifest.

## 4. Contracts and vocabulary

| Item | Value |
|---|---|
| Interfaces contract | 0.2.0, `afca22…`; no 0.3.0 release |
| Offline artifact contract | proposal `jcheng.offline-artifact-contract.v1`, version 1.0.0, **Proposed** |
| Device snapshot | `jcheng.device_snapshot.v1` |
| Scenario requirements | `jcheng.scenario_requirements.v1` |
| Capability vocabulary | `local_draft` |
| Compatibility report | `jcheng.device_compatibility.v1` |
| Reference report | `jcheng.applications.reference_report.v1` |
| Mock task result | `jcheng.applications.ore_sorting_task.v1` |

## 5. Known limits

- `matched_with_unverified`: ArmPi DOF matched; reach/payload/aperture/camera
  resolution unverified; three perception requirements deferred.
- AR5: vendor-public 7-DOF/5 kg/683 mm/EtherCAT facts, unverified locally; no
  SDK/URDF/calibration/unit; `data_status: partial`.
- PiPER X: simulation/profile only, no hardware.
- Gazebo runtime unavailable; simulation asset check only.
- Benchmark observed suite INCONCLUSIVE; test thresholds are not business
  acceptance criteria.
- Deployed tree remains 0.1.0; deployment NOT READY.
