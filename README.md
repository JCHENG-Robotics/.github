# JCHENG-Robotics/.github

**English** | [简体中文](README.zh-CN.md)

Organization governance repository: the organization profile, community health
files, issue/PR templates, reusable CI workflows, composite Action skeletons,
and the ecosystem-level README, ROADMAP, CHANGELOG and acceptance report.
**It contains no product code, robot configuration or secrets.**

Organization profile: [profile/README.md](profile/README.md) | [profile/README.zh-CN.md](profile/README.zh-CN.md)

## Baseline 1 (2026-11-28)

The ecosystem has completed its first **offline integration baseline**:

- **DEVELOPMENT READY: YES.**
- **OFFLINE INTEGRATION READY: YES.**
- **BASELINE 1 COMPLETE: technical conditions met; final record #40 pending
  Board approval/merge** (main still shows the earlier #38 text).
- **DEPLOYMENT READY: NO.**

| Baseline 1 result | Evidence |
|---|---|
| Contract `jcheng.offline-artifact-contract.v1` 1.0.0 **Accepted**; offline vocabulary `contracted` | interfaces PR #20/#21 (`426f371`); scenarios #5 (`1c21885`) |
| Real CLI cell integration | arm + gripper + camera; `matched_with_unverified`; DOF 5≥4; reach/payload/aperture/resolution unverified |
| Eight-case synthetic mock ore-sorting task | 8/8 classifications; only `normal` succeeds; benchmark INCONCLUSIVE / test PASS / test FAIL |
| Three-arm registration | ArmPi Ultra 5-DOF reference; PiPER X 6-DOF candidate; ROKAE **AR5L/AR5R** 7-DOF planned dual-arm pair |
| Final main regression | interfaces 22, devices 123, scenarios 116, applications 218+5, system 191, mobile 50, studio 13+222, perception 107, learning 68, teleop 218, simulation 86+2, benchmark 61, ops 9, `.github` 20 |
| Developer handover | `QUICKSTART.md`, `DEVELOPER_GUIDE.md`, `.github/dev/baseline1-acceptance.sh`, first R&D task |
| Deployment | **NOT READY**; no real motion or hardware output authorized |

The detailed record is in [`docs/baseline1/ratification/`](docs/baseline1/ratification/README.md).
This is not a v1.0 release claim and no release/tag has been created.

## Platform pivot (2026-11-28)

The owner approved a platform pivot on 2026-11-28. It changes the hardware plan,
not the Baseline 1 record:

- **ArmPi Ultra is `Frozen`.** The read-only demo, deployment files, image
  digest and rollback path are retained; motion-authority revocation is pending
  operator action. Do not restart the vendor container.
- **The successor is a fixed-cell PiPER X.** P2 is read-only in progress (two
  CAN channels; leader read-only; follower not commanded). Production execution
  is P3, planned.
- **AR5 is gated** on six identity facts (vendor/model, controller topology, SDK
  and license, EtherCAT/real-time, URDF/joint signs/limits, gripper interface).
- **Mobile manipulation is P7, deferred.** `jcheng-mobile` stays dormant.
- **M6 S14 and the ecosystem G8 re-run are retired** with the platform, not
  deferred. S13/S17 remain valid ArmPi evidence.
- **Contracts:** `jcheng-interfaces` v0.3.0 was released on 2026-11-28
  (robot-profile v2, `chain_id`, gripper units; `8bc92d18…`). The signed v0.2.0
  pin (`afca22…`) remains the deployed contract for the current runtime;
  migration is in progress. The device registry now holds 10 device profiles /
  7 capability profiles.

The public summary is [`docs/platform-transition.md`](docs/platform-transition.md);
the architecture is [`docs/architecture.md`](docs/architecture.md). No dates are
promised.

## Previous state (2026-11-26)

> Historical snapshot. Current platform state is in “Platform pivot” above and
> the current versions are in the repository `VERSION` files.

- M1–M5.2 are complete; M6 S13 replay (21/21) and S17 real MoveIt plan-only
  pass. S14 base and a full G8 re-run remain.
- Ecosystem repositories: `.github`, `jcheng-interfaces`, `jcheng-system`,
  `jcheng-manipulation` (frozen baseline), `jcheng-mobile`, `jcheng-perception`,
  `jcheng-learning`, `jcheng-simulation`, `jcheng-studio`,
  `jcheng-applications` and `jcheng-ops`. `jcheng-research` is a public
  investigation workspace. `jcheng-mobile-bench` is an explicitly labelled
  bench sandbox and is not released.
- `jcheng-learning` (v0.1.0) is an offline dataset/training/policy-artifact
  boundary: no runtime node, policy or hardware access.
- `jcheng-simulation` (v0.1.0) is an offline multi-robot plant engine on domain
  43: deterministic mock verified, Gazebo Harmonic partially verified, no
  hardware access and no motion to the real system.
- `jcheng-benchmark` is a BENCH-layer, offline read-only benchmark harness
  (v0.1.0, experimental). It is outside the runtime dependency graph and has no
  recorded or hardware result yet.
- `jcheng-studio` (operator console, v0.7.0) and `jcheng-applications` (task
  orchestration, v0.1.0) are L4 repositories. Both use the gateway HTTP/WS
  boundary; neither joins a DDS domain, opens a device or executes motion.
  Studio has a ported console, read-only REST/WS, a session store and replay;
  Applications has an offline recipe/planning/runner core and a read-only
  transport. `jcheng-research` (public, v0.1.0) produces reports and
  decisions only; it is outside the runtime graph.
- Documentation standard: every product repository carries `README.md`,
  `README.zh-CN.md`, `ROADMAP.md`, `CHANGELOG.md` and `ACCEPTANCE.md`. The
  language switch is the first line after the H1. See
  [docs/documentation-standard.md](docs/documentation-standard.md).
- This repository has no `LICENSE`. `jcheng-mobile` was initialized with an MIT
  `LICENSE`; the other new repositories have none. The third-party and
  copyright review is pending, and the mobile file is retained pending review
  rather than removed retroactively. See
  [docs/license-review.md](docs/license-review.md).
- The reusable workflows gate M1–M6 in the three original repositories. New
  repositories are admitted under [docs/repo-taxonomy.md](docs/repo-taxonomy.md).

## Documents

| Document | Content |
|---|---|
| [profile/README.md](profile/README.md) | Organization profile (English canonical) |
| [profile/README.zh-CN.md](profile/README.zh-CN.md) | Organization profile (Chinese translation) |
| [profile/assets/README.md](profile/assets/README.md) | Profile SVG/photo provenance and maintenance |
| [docs/architecture.md](docs/architecture.md) | Layers, repository responsibilities, dependency rules and the single motion path |
| [docs/evidence.md](docs/evidence.md) | Status vocabulary, evidence classes, frozen baseline and Baseline 1 |
| [docs/platform-transition.md](docs/platform-transition.md) | ArmPi freeze, PiPER X, AR5 gate and P0–P7 |
| [docs/safety-and-limitations.md](docs/safety-and-limitations.md) | Safety non-claims, limitations, license and governance |
| [docs/baseline1/ratification/README.md](docs/baseline1/ratification/README.md) | Baseline 1 acceptance, manifest, QA, freeze record |
| [ROADMAP.md](ROADMAP.md) | Ecosystem milestones M0–M8, Baseline 1 and current state |
| [CHANGELOG.md](CHANGELOG.md) | Ecosystem-level change record |
| [ACCEPTANCE.md](ACCEPTANCE.md) | Ecosystem acceptance status and evidence |
| [acceptance/ecosystem-2026-11-26.json](acceptance/ecosystem-2026-11-26.json) | Current machine-readable acceptance (schema v1; reviewer pending) |
| [acceptance/ecosystem-2026-11-25.json](acceptance/ecosystem-2026-11-25.json) | Previous machine-readable acceptance (history) |
| [acceptance/ecosystem-2026-11-24.json](acceptance/ecosystem-2026-11-24.json) | Earlier machine-readable acceptance (history) |
| [docs/documentation-standard.md](docs/documentation-standard.md) | Document standard and status vocabulary |
| [docs/repo-taxonomy.md](docs/repo-taxonomy.md) | Repository layers, dependency direction and admission checks |
| [docs/templates/](docs/templates/) | README / ROADMAP / CHANGELOG / ACCEPTANCE templates |

## Layout

```text
profile/README.md                 Organization profile (English)
profile/README.zh-CN.md           Organization profile (Chinese translation)
profile/assets/                   Self-contained SVG and photo assets
ROADMAP.md                        Ecosystem roadmap
CHANGELOG.md                      Ecosystem changelog
ACCEPTANCE.md                     Ecosystem acceptance report
acceptance/                       Machine-readable acceptance reports (schema v1)
CONTRIBUTING.md                   Contribution process
SECURITY.md                       Vulnerability and secret handling
GOVERNANCE.md                     Roles, review and release authority
CODEOWNERS.template               Copied into each repository
.github/workflows/                Reusable workflows + organization health check
actions/                          Composite Actions
ISSUE_TEMPLATE/                   Issue, feature, design and config templates
docs/                             Organization policies, architecture, evidence,
                                  platform transition, safety and templates
```

## Constraints

- Every real-robot motion requires separate, explicit authorization; this
  repository contains no motion code.
- Third-party Actions are pinned to a full commit SHA; reusable workflows use
  the organization tag `v1`.
- Tokens, private keys, real site IPs and robot credentials are never committed.
- The policy is no `LICENSE` until the review closes. `jcheng-mobile` predates
  that policy with an MIT `LICENSE`; no further `LICENSE` is added and no MIT
  grant is claimed for the other repositories.
- Documents are English-canonical; product repositories carry a Chinese
  `README.zh-CN.md` translation.
