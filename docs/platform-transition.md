# Platform transition — ArmPi Ultra to the fixed PiPER cell

> Status: **approved 2026-11-28; publication in progress.** English canonical.  
> This is a public summary of the approved platform-pivot record and ADR-0007.
> It records decisions; it does not change controls, contracts, deployment units
> or evidence. The source record remains authoritative.

## 1. Decision summary

| ID | Decision | Value | Reason |
|---|---|---|---|
| **D1** | ArmPi Ultra status | `Frozen`, not `Archived` | The read-only demo and rollback path stay available; evidence and deployment records are retained |
| **D2** | Deployment shape | Fixed cell first; mobile later | Remove chassis, navigation and mobile calibration from the first production path |
| **D3** | PiPER X role | Production execution arm: teach → record → replay → supervised execution | The leader stays out of the control loop; the safety case is smaller |
| **D4** | AR5 role | Second-phase dual arm; backend only after the identity gate | No local SDK, URDF, calibration or unit; vendor/controller facts are unconfirmed |
| **D5** | Contract change | `v0.3.0`: robot-profile v2, `chain_id`, gripper ranges without constants | v1 is servo-shaped and cannot express CAN/EtherCAT or dual arms |
| **D6** | Evidence rule | Re-establish evidence per platform; ArmPi `Verified` does not migrate | Different hardware, interface and calibration |

**What is frozen is the platform, not the repositories.** `jcheng-system`,
`jcheng-perception`, `jcheng-applications` and the other product repositories
continue to evolve. `jcheng-manipulation` stays `Frozen` at `v1.0.0`.

## 2. Current platform state

| Surface | State | Note |
|---|---|---|
| ArmPi Ultra platform | **Frozen** (2026-11-28) | Read-only demo retained; no new ArmPi feature PRs |
| Motion authority | **Revocation pending operator action** | Do not restart the vendor container; its startup check moves the arm |
| Read-only `/v1` gateway | Retained | Demo and rollback surface |
| `jcheng-system/deploy/armpi-ultra/` | Frozen banner | Files and image lock retained |
| `jcheng-ops` ArmPi probes | `legacy` | No new installs |
| `jcheng-mobile` | `Experimental`, dormant | No chassis work in P0–P6; P7 is deferred |
| PiPER X | **P2 read-only in progress** | Two CAN channels; leader read-only; follower not commanded |
| AR5 | **Planned / identity gate** | No backend, URDF or calibration work before P4 |

## 3. What the ArmPi freeze retains

These results are hardware results on the ArmPi Ultra. They stay valid for this
platform and are **not** transferred to PiPER X or AR5.

| Item | Result | Evidence |
|---|---|---|
| M4 read-only telemetry | 30 min, 1799/1799 `measured`, `writes=0` | `docs/ecosystem/evidence/m4-readonly-20261123/` |
| M5.2 supervised joint | `joint1` 505 vs 512 pulses | `docs/ecosystem/evidence/m52-final-20261124/` |
| M5.2 gripper | 183→645 close, 647→183 open | same |
| M5.2 stop | 0.266 ms software stop | same |
| M6 S13 replay | 21/21 decisions | `docs/ecosystem/evidence/m6-s13-20261124/` |
| M6 S17 plan-only | MoveIt 2.5.10, `SUCCESS`, 8-point plan, 0 controller servers | `docs/ecosystem/evidence/m6-s17-20261125/` |
| Runtime image | `armpi-ultra:flatten-20261125`, 7.1 GB arm64, 20 nodes / 60 topics | `jcheng-system/deploy/armpi-ultra/` |

The platform claim level is **partially verified**: the listed scopes passed, but
the platform as a whole was never validated end to end. The frozen baseline's own
full G8 is a separate result and remains valid for the baseline.

## 4. What was never verified

These stay `Not started` or `Unverified`. They are retired with the platform, not
deferred:

| Item | State |
|---|---|
| M6 S14 chassis pulse on hardware | Not started |
| Ecosystem G8 re-run (locate → grasp → lift → place) | Not started |
| S7 stale-state injection | Unverified |
| S9 runtime publisher detection | Unverified |
| Teleoperation with hardware streaming | Unverified |
| M7 first external module pilot | Not started |
| Functional safety (e-stop, brake, encoder, self-collision) | Not claimed |

## 5. Pins and image

| Item | Value |
|---|---|
| Contract | `v0.2.0`, commit `b03a054a59f70c24741fce37ebe1bb03978d9021` |
| Contract hash | `sha256:afca22a42f7163e0351d185d5a8577b0b51f2f3da4b92278f161a4a7d2c35b1c` |
| Runtime image tag | `armpi-ultra:flatten-20261125` |
| Runtime image digest | `ghcr.io/jcheng-robotics/armpi-ultra@sha256:d4e6f3901f1c43e08f4018ff7f7b55dec21b2955dba8b98404a440a1f89df15f` |
| Baseline | `jcheng-manipulation` `v1.0.0`, `b3411e4`, unchanged |

**Contract release note.** `jcheng-interfaces` v0.3.0 was released on 2026-11-28
after the freeze record was written. It adds robot-profile v2, `chain_id` and
gripper units; the manifest hash is `sha256:8bc92d18…`. The ArmPi deployment
remains on the signed v0.2.0 pin (`afca22…`), and the runtime consumers still
declare `>=0.2,<0.3`; migration is in progress. The v0.3.0 tag is annotated; the
v0.2.0 tag remains the signed pin. P1 is **in progress**, not complete.

## 6. Target fixed cell

```text
Fixed cell (no chassis)
├── PiPER X follower   ← production execution arm; the only commanded object
├── PiPER X leader     ← teach input; read-only; never receives a command
├── D435i external camera ← fixed-base calibration
├── (optional) wrist camera ← PiPER link6 hand-eye; deferred
└── host (Orin or workstation) ← domain 0 vendor / 41 privileged / 42 capability
```

P2 has already recorded the following at rest:

| Arm | Role | CAN interface | Firmware state |
|---|---|---|---|
| Right | leader, teach input only | `can_leader1` | `ctrl_mode 0x02` teaching; free to hand-guide |
| Left | follower, motion output | `can_follower1` | `ctrl_mode 0x01` CAN control; holds position |

The read-only decoder opens `CAN_RAW` sockets only to receive. It has no send
method, no torque enable and no motion path. `tx_packets` on both interfaces stays
zero in the read-only probe.

## 7. Teach → replay → supervised execution

The production path is **not** real-time leader–follower:

```text
leader (PiPER) ── read-only ──▶ teach capture (operator side)
                                  │ joint trajectory + provenance + seal
                                  ▼
                            offline replay (SafetySupervisor; S13 decisions)
                                  │ decision agreement 100%
                                  ▼
              ExecuteMotion ─▶ arbiter ─▶ lease ─▶ follower (PiPER)
```

- The leader is never enabled and never receives a motion command.
- Capture runs on the operator side; it is not part of `jcheng-system`.
- Replay reuses the S13 decision pattern; it does not execute motion by itself.
- Execution uses `JOINT_TRAJECTORY`; every frame is confirmed on CAN; a stop
  aborts the in-flight frame.
- A production recipe produces the same `JOINT_TRAJECTORY` and shares the
  executor with replay.

Real-time teleoperation is a separate P3.5 project: it needs `intent_source`, a
streaming executor, deadman tuning and its own safety case. It does not block
P0–P3.

## 8. AR5 identity gate

AR5 stays `planned` until all six facts have a source:

1. Vendor and model (Rokae AR5 or another vendor).
2. Controller topology (one controller for two arms, or two controllers).
3. SDK and license (Rokae ROS 2 packages, dependency terms).
4. EtherCAT master and real-time performance (host, RT kernel, cycle).
5. URDF, joint signs and limits.
6. Gripper model, stroke and control interface.

If any fact is unknown, AR5 remains `planned`; do not write the backend, change
the `rokae.ar5*` registry entries or claim dual-arm capability.

## 9. Phase plan

| Phase | Scope | State | Exit evidence |
|---|---|---|---|
| **P0** | ArmPi freeze; motion-authority revocation | **In progress** | Freeze record; read-only demo; publisher set recorded |
| **P1** | Contracts v0.3.0: robot-profile v2, `chain_id`, gripper ranges | **In progress** — v0.3.0 released 2026-11-28; consumer migration in progress | v1/v2 load; all gates green; mock runs a v2 profile |
| **P2** | PiPER X read-only: two CAN channels, zero writes | **In progress** | 30 min read-only; `writes=0`; SDK agreement |
| **P3** | PiPER X production: teach → replay → supervised execution | **Planned** | One pick-place; per-frame CAN confirmation; stop ≤100 ms |
| **P4** | AR5 identity gate: six facts | **Planned** (parallel with P1–P3) | Every fact sourced or explicitly unknown |
| **P5** | AR5 read-only and dual-arm | **Gated** | Dual-arm read-only; plan-only; single-arm L5 |
| **P6** | Fixed-cell close: lock, evidence, release notes | **Planned** | Per-platform evidence and a new lock |
| **P7** | Mobile manipulation | **Deferred** | Separate project charter |

No dates are promised. Phases are ordered by dependency, not calendar.

## 10. Ore-sorting disposition

| Stage | Platform coupling | Disposition after the pivot |
|---|---|---|
| S0 research and design | None | Transfers unchanged |
| S1 offline segmentation | None (ROS-free, no device) | Transfers; synthetic and public baseline stay partially verified; real-ore accuracy unverified |
| S1.5 depth backend | None (laptop GPU) | Transfers; no hardware claim |
| S2 instance 3D | Camera and depth calibration | Re-run on the fixed cell; new mount calibration |
| S3 scene state | Offline schema | Transfers; a cross-repo contract still needs an interfaces proposal |
| S4 multi-view | External and wrist cameras | Re-plan for a fixed external camera and optional wrist camera |
| S5 active perception | Arm model and simulation | Re-derive in PiPER simulation; motion stays system-owned |
| S6 graspability | 5-DoF ArmPi assumption | Re-derive for 6-DoF and a parallel prismatic gripper |
| S7 integration | Contracts only | Unchanged; scenario declarations remain the input |
| S8 closed-loop sorting | Full cell and supervised execution | Blocked on P2/P3/P6; no ArmPi result transfers |

## 11. Stop conditions and risks

The pivot records three stop conditions. If any occurs, stop the real arm and
return to the previous phase:

| ID | Risk | Mitigation |
|---|---|---|
| R31 | Two vendor stacks online, dual authority returns | One motion authority at a time; record the publisher set on every switch |
| R32 | The leader is connected as a motion source | Read-only adapter; static and runtime zero-command proof; do not approve `intent_source` |
| R33 | A v1 profile is made to look like CAN/EtherCAT hardware | v2 schema; review rejects invented `servo_id`/pulses; tests assert it |

Other recorded risks include AR5 vendor/model uncertainty, EtherCAT real-time
limits, pyAgxArm/Rokae license questions, unmeasured PiPER gripper direction and
limits, calibration invalidation, and an ArmPi that is still powered. See the
source record for the full register.

## 12. Publication status

The platform-pivot record, ADR-0007 and the ArmPi freeze record were approved on
2026-11-28. The freeze record states that the record and design documents are on
a local branch and that push/PR are pending owner confirmation. This document is
a public summary prepared for the organization profile; it does not claim that
the source record is already public.

Until the source record is merged:

- cite the decision as **approved 2026-11-28; publication in progress**;
- do not link a non-existent organization design repository;
- keep the ArmPi evidence paths unchanged;
- keep all real-robot work behind separate, explicit authorization.

## 13. Sources

- `jcheng-manipulation` design record: `docs/ecosystem/17-platform-pivot.md`,
  `docs/ecosystem/adr/0007-fixed-cell-piper-first.md`,
  `docs/ecosystem/evidence/armpi-freeze-20261128/`.
- `jcheng-system/deploy/piper-cell/README.md` and
  `jcheng-system/ros2_ws/src/jcheng_vendor/jcheng_vendor/piper_readonly.py`.
- `jcheng-scenarios/docs/PLATFORM_PIVOT_20261128.md`.
- `jcheng-ops/README.md` (ArmPi probes marked legacy).
- [`architecture.md`](architecture.md), [`evidence.md`](evidence.md),
  [`safety-and-limitations.md`](safety-and-limitations.md).
