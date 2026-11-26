# Ecosystem changelog

All notable ecosystem-level changes are recorded here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the ecosystem follows
[Semantic Versioning](https://semver.org/) per repository.
Repository-local changes stay in their own `CHANGELOG.md`; this file records
events that cross repository boundaries or change the ecosystem baseline.
The ecosystem itself has no version until M8, so entries are dated rather than
versioned.

## [Unreleased]

### Added

- Documentation standard v1.0 (`docs/documentation-standard.md`) and
  templates (`docs/templates/`); all product repositories now carry the same
  README / ROADMAP / CHANGELOG / ACCEPTANCE set.
- Ecosystem-level `ROADMAP.md`, `CHANGELOG.md` and `ACCEPTANCE.md` in this
  repository; the organization profile now reflects the live repository map
  and M6 status.
- `acceptance/ecosystem-2026-11-24.json`: a machine-readable status report that
  validates against `acceptance-report.v1` (reviewer pending; result
  `inconclusive`).
- `jcheng-mobile/LICENSE-REVIEW.md`: the pre-existing MIT file is retained
  pending the organization review instead of being removed retroactively.
- `jcheng-benchmark` v0.1.0: a BENCH-layer, offline read-only benchmark
  harness with pre-registered suite declarations, a strict JSONL runner,
  provenance-labelled reports and a synthetic self-test; no recorded or
  hardware result yet. The organization profile and repository taxonomy now
  include it.
- `jcheng-studio` v0.7.0: the L4 operator console is ported from the frozen
  baseline, with read-only `/v1` REST/WS, the M2a session store, the M2b intent
  path and M3 offline replay. It uses the gateway HTTP/WS boundary only; no DDS
  domain, device access or motion execution. Hardware acceptance is not
  implemented.
- `jcheng-applications` v0.1.0: admission plus an offline L4 task-orchestration
  core (recipe validation, deterministic plans, a fail-closed runner) and an
  M2 read-only HTTP transport. No DDS domain, device access or motion.
- `jcheng-learning` v0.1.0: offline dataset/training/policy-artifact boundary
  with no runtime node, policy or hardware access.
- `jcheng-teleop` v0.1.0: L3 admission-only scaffold for teleoperation intent.
  The reserved `TeleopCommand` stream is documented but not published; there is
  no input adapter, device access, DDS domain or motion. The organization
  profile, roadmap, acceptance and repository taxonomy now include it.
- `jcheng-simulation` v0.1.0: offline multi-robot plant engine on domain 43;
  deterministic mock verified, Gazebo Harmonic partially verified.
- `jcheng-research` v0.1.0: public investigation workspace for reports and
  decisions; outside the runtime dependency graph.
- Language switch standardized in every README: `**English** | [简体中文](README.zh-CN.md)`
  (English) and `**简体中文** | [English](README.md)` (Chinese) as the first line
  after the H1; the status block keeps one canonical sentence without a second
  link. `docs/documentation-standard.md` and both templates updated.

### Changed

- `jcheng-research` is public on GitHub; its README, AGENTS.md, ACCEPTANCE.md,
  LICENSE-REVIEW.md, the repository taxonomy and the organization profile now
  state that instead of claiming a private repository.

## 2026-11-25 — S17 real, image rebuild, static mobile and dual-view perception

### Added

- M6 S17 real MoveIt plan-only in `jcheng-system`: MoveIt 2.5.10, `SUCCESS`,
  8-point plan, 0 controller servers and no command topics.
- ArmPi Ultra runtime image `armpi-ultra:flatten-20261125` (7.1 GB,
  `linux/arm64`, digest
  `sha256:d4e6f3901f1c43e08f4018ff7f7b55dec21b2955dba8b98404a440a1f89df15f`);
  20 nodes / 60 topics preserved and the container survived a host reboot.
- `jcheng-mobile` static bring-up: `/scan`, `/odom` and `/map` pass; motion,
  mount pose and navigation remain unverified.
- `jcheng-perception` ADR 0004 aligned external depth, split-edge ingress/fusion
  and a single 60 s dual-view tag run (cross-view 3.37 mm); run 10 still wedges
  the wrist depth reader, so the full window is not repeatable.
- D435i depth-missing recovery documented in `jcheng-perception`
  `docs/FAILURE_MODES.md`.
- `acceptance/ecosystem-2026-11-25.json`: updated machine-readable status
  report (reviewer pending; result `inconclusive`).

## 2026-11-24 — M5.1/M5.2, M6 offline and capability repositories

### Added

- `jcheng-ops` v0.1.0: unattended operations guards (15 s hardware watchdog,
  30 s health timer with a motion-idle guard, restart policies, OOM protection,
  laptop Studio watchdog) and the 2026-11-24 incident record.
- `jcheng-mobile` v0.1.0: contract-compliant M10 bringup, RTAB-Map ICP laser
  odometry, slam_toolbox and Nav2 MPPI Omni chassis intent; no hardware access
  and no fabricated odometry.
- `jcheng-perception` v0.1.0 hardware bring-up: Pi 5 ARM64 build, wrist Aurora
  data path, bus-measured wrist TF, single static-pose table-plane check and
  the Pi 5 edge → laptop RTX 3060 real-YOLO detection path.
- M5.1 Mock ROS transport in `jcheng-system` (lease, safety, `ExecuteMotion`,
  stop latch); CI `m5-mock` green.
- M5.2 supervised hardware motion in `jcheng-system`: single joint +0.05 rad
  (505 vs 512 pulses) and gripper close/open, both `COMPLETED` and
  `bus_verified`; stop latched in 0.266 ms.
- M6 offline verification merged to `jcheng-system` `main` (`427214b`):
  S13 G8 decision replay 21/21 and S17 MoveIt plan-only goal construction.

### Changed

- The organization profile is no longer an M1 document; it reports M1–M5.2
  complete, M6 in progress and the admitted capability repositories.
- `jcheng-ops` becomes the owner of unattended operations guards; the frozen
  `jcheng-manipulation` baseline keeps only the `start_studio.sh` ordering fix
  and a runbook pointer.

## 2026-11-23 — contracts, mock system and read-only integration

### Added

- M2 contracts: `jcheng-interfaces` v0.1.0 (14 msg / 10 srv / 1 action,
  seven JSON Schemas, OpenAPI `/v1`, WebSocket protocol, contract hash and
  `jcheng_contracts` bindings), signed tag `v0.1.0`.
- M3 mock system runtime: nine ROS packages, S1–S17 scenarios, lockfile and
  `verify_lock.py`; `main` `40a74ba`.
- M4 read-only robot integration: 30 minutes, 1799/1799 `measured` samples,
  `writes=0`; independent bus reads replaced the command-cache `measured`
  source.
- `jcheng-perception` initialization (distributed Pi 5 edge + GPU detector).

### Changed

- The ecosystem baseline remains `jcheng-manipulation v1.0.0` (`b3411e4`);
  no tag, evidence bundle or experiment history was modified.

## 2026-11-23 — design approval and organization initialization

### Added

- M0 architecture approval and design record
  (`jcheng-manipulation` `docs/ecosystem/`).
- M1 initialization: `JCHENG-Robotics` organization, `.github`,
  `jcheng-interfaces` and `jcheng-system` created, `main` protected,
  111/111 API checks passed.
- Bilingual organization profile, governance documents, issue/PR templates,
  reusable CI workflows and composite Action skeletons.

### Security

- Repository rules: PR + CODEOWNERS + `m1-gate`, linear history, no force-push
  or deletion; a second reviewer (`@JerichoSwaine`) holds maintain access.
