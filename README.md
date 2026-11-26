# JCHENG-Robotics/.github

Organization governance repository: the organization profile, community health
files, issue/PR templates, reusable CI workflows, composite Action skeletons,
and the ecosystem-level README, ROADMAP, CHANGELOG and acceptance report.
**It contains no product code, robot configuration or secrets.**

Organization profile: [English](profile/README.md) | [简体中文](profile/README.zh-CN.md)
(English is canonical; the Chinese page is a translation.)

## Current state (2026-11-24)

- M1–M5.2 are complete; the offline part of M6 is merged (S13 replay 21/21,
  S17 plan-only). The real-robot part of M6 awaits separate authorization.
- Ecosystem repositories: `.github`, `jcheng-interfaces`, `jcheng-system`,
  `jcheng-manipulation` (frozen baseline), `jcheng-mobile`, `jcheng-perception`
  and `jcheng-ops`. `jcheng-mobile-bench` is an explicitly labelled bench
  sandbox and is not released.
- `jcheng-benchmark` is a BENCH-layer, offline read-only benchmark harness
  (v0.1.0, experimental). It is outside the runtime dependency graph and has no
  recorded or hardware result yet.
- Documentation standard: every product repository carries `README.md`,
  `README.zh-CN.md`, `ROADMAP.md`, `CHANGELOG.md` and `ACCEPTANCE.md`. See
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
| [acceptance/ecosystem-2026-11-25.json](acceptance/ecosystem-2026-11-25.json) | Current machine-readable acceptance (schema v1; reviewer pending) |
| [acceptance/ecosystem-2026-11-24.json](acceptance/ecosystem-2026-11-24.json) | Previous machine-readable acceptance (history) |
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
