# Frozen Baseline 1 Manifest

> **Conditional freeze.** The source SHAs below are the fixed main baseline at
> 2026-11-28. The contract/vocabulary/AR5L-R PRs are unmerged, so this manifest
> is not yet the final COMPLETE freeze. No artifact hash is computed over this
> report itself, so the manifest commit cannot create a self-reference.

## 1. Fixed source revisions

| Repository | main SHA | Version |
|---|---|---|
| `.github` | `f9e77eb8b309ab705c20f08a34bb28be68ff8ce7` | n/a |
| interfaces | `a142641b4fb256aa2368abe778bb6c5b010d1c23` | 0.2.0 |
| devices | `a006f5f2a3e71522f23b8aa6af6a363d0bd57174` | 0.1.0 |
| scenarios | `eac6dda1e7cdd8a80063fe8365518cf20bf2f65a` | 0.1.0 |
| applications | `0be306e7d7ebf7b8a7e6b47aa5fb0c518358d90c` | 0.1.0 |
| system | `72b2ce25266d3463d4590e871f6a2905fd938704` | 0.3.0-dev0 |
| mobile | `f96cfee2a3330d6a830f9807f92dc0539ee5d7be` | 0.1.0 |
| studio | `40c002b02131e56b1a4923c8a5f75a2beb26909c` | 0.8.0 |
| perception | `343e621298518f8dbc7c02873f11885bb9de2fa4` | 0.1.0 |
| learning | `69978259f8d6bbfa21f472a4d139bd6798a6f10b` | 0.2.0 |
| teleop | `984b12f5c96d39462b6f6ecf33d4c914bdd75684` | 0.3.0 |
| simulation | `40c250d93fdb72a5088e2c71f3dcb263c791eb0c` | 0.1.0 |
| benchmark | `bfaeac9ee4cb9f5cd5b555b21ec08e1e8d9645e7` | 0.1.0 |
| ops | `4d365f6bd354a1a6cefc676da92d648d73c973c3` | 0.1.0 |
| research | `58858ecea618fb0dd12bda84d39db49bf0ded2b6` | 0.1.0 |
| manipulation | `v1.0.0` = `b3411e43ad31c09f396cdd2db0fdfda8f09853dd` | 1.0.0 frozen |

## 2. Pending ratification heads (not in main)

| Repository | PR | Head | Effect |
|---|---|---|---|
| devices | #8 | `0bbbc18` | AR5L/AR5R units; 9 devices |
| scenarios | #5 | `d73e998` | vocabulary `contracted`; new requirements hash |
| interfaces | #21 | `f656d69` | contract Accepted/1.0.0 record |
| `.github` | freeze PR | recorded in PR | this manifest and reports |

After merge, the merge SHAs replace these heads and the manifest must be
regenerated once (without hashing itself).

## 3. Artifact contract

| Item | Value |
|---|---|
| Offline contract | `jcheng.offline-artifact-contract.v1`, 1.0.0 |
| Approval | real owner approval on interfaces #20; ratification record in #21 |
| Main status | **Proposed** until #21 merges |
| Vocabulary | `local_draft` on main; `contracted` in scenarios #5 |
| Interfaces runtime contract | 0.2.0; not changed by this ratification |

## 4. Artifact hashes on current main

| Artifact | Version | source_hash | content_hash |
|---|---|---|---|
| `hiwonder.armpi-ultra` | 0.1.0 | `sha256:f3c0c1b5…` | `sha256:602e211e…` |
| `hiwonder.armpi-ultra-gripper` | 0.1.0 | `sha256:7077e9b2…` | `sha256:079af9c0…` |
| `intel.realsense-d435i` | 0.1.0 | `sha256:31939225…` | `sha256:f5942741…` |
| `agilex.piper-x` | 0.1.0 | `sha256:b97de34e…` | `sha256:07081ad0…` |
| `rokae.ar5` family | 0.2.0 | `sha256:36cf6bad…` | `sha256:949a0170…` |
| `ore_sorting` requirements | 0.1.0 | `sha256:5e540ccf…` (scenario source) | `sha256:ca9d9f03…` |

Full hashes are in `docs/baseline1/42-baseline1-manifest.md` and the evidence
directories. `42` records the pre-ratification source SHAs; this manifest
supersedes its source section. After scenarios #5 merges, the requirements
hashes necessarily change (vocabulary field is hashed); regenerate and record
the new values.

## 5. Build/dependency environment

- Ubuntu 24.04.5 LTS, Python 3.12.3, g++ 13.3.0, CMake 3.28.3, colcon.
- ROS 2 Jazzy only; MoveIt 2 present; Nav2/slam_toolbox absent.
- Gazebo: `ros_gz_sim` present, `gz` CLI absent; runtime not verified.
- Learning: `uv` 0.13.8 frozen environment outside the repo.
- No network service or hardware is required for acceptance.

## 6. Acceptance commands

```bash
.github/dev/baseline1-acceptance.sh          # unified reference + 8 cases + benchmark
dev/test.sh <repo>                           # repo tests/gates
python3 -m pytest -q                         # per-repo main worktree
python3 scripts/check_boundaries.py --root <16-repo-workspace> --mode report
```

## 7. Waiver, debt, unverified, limits

| Item | Status |
|---|---|
| Studio B4 waiver `W-2026-11-27-01` | active until 2026-12-31; not resolved |
| Boundary findings | 25 open + 1 waived; non-blocking, recorded |
| TD-20 contract ratification | open until #21 merges |
| TD-21 Gazebo/world | open; offline asset check only |
| TD-22 AR5 local data | open; L/R units missing variant data |
| TD-24 mock task | closed: applications #20 merged |
| ArmPi reach/payload/aperture/resolution | unverified; no real grasp claim |
| PiPER X hardware | absent; registration/simulation only |
| AR5 L/R runtime | absent; no adapter/motion |
| Deployment | NOT READY: deployed 0.1.0, base bridge, lease sharing, watchdog, DDS holder, bench evidence |
| Real motion/hardware | not authorized |

## 8. Freeze rule

Do not call this the final frozen manifest until #8/#5/#21 and this freeze PR
are merged and the post-merge acceptance rerun passes. No self-referential hash
is used.
