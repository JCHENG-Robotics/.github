# JCHENG-Robotics/.github

**English** | [简体中文](README.zh-CN.md)

Organization governance repository: the organization profile, community health
files, issue/PR templates, reusable CI workflows, composite Action skeletons,
and the ecosystem-level README, ROADMAP, CHANGELOG and acceptance report.
**It contains no product code, robot configuration or secrets.**

Organization profile: [profile/README.md](profile/README.md) | [profile/README.zh-CN.md](profile/README.zh-CN.md)

## Current state (2026-11-26)

- M1–M5.2 are complete; M6 S13 replay (21/21) and S17 real MoveIt plan-only
  pass. S14 base and a full G8 re-run remain.
- Ecosystem repositories: `.github`, `jcheng-interfaces`, `jcheng-system`,
  `jcheng-manipulation` (frozen baseline), `jcheng-mobile`, `jcheng-perception`,
  `jcheng-learning`, `jcheng-simulation`, `jcheng-studio`,
  `jcheng-applications` and `jcheng-ops`. `jcheng-research` is a private
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
  transport. `jcheng-research` (private, v0.1.0) produces reports and
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
| [ROADMAP.md](ROADMAP.md) | Ecosystem milestones M0–M8 and current state |
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
docs/                             Organization policies, document standard and templates
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
