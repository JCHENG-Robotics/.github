# Status Model — Development / Main / Deployment

> Status: **v1.0 (2026-11-28)**. Required by Decision 6. A finding can be
> resolved on a development branch while still open on `main` or in the
> deployed image. No finding is called "resolved" across planes without
> evidence at that plane.

## 0. Readiness states

| State | Result | Basis |
|---|---|---|
| **DEVELOPMENT READY** | **YES** (optional gaps) | env check, build interfaces, system/devices/scenarios tests, mock gateway health, simulation mock topics; see [39](39-developer-handover-report.md) |
| **OFFLINE INTEGRATION READY** | **NO** | real device/scenario artifacts fail closed (TD-17/18/19) |
| **DEPLOYMENT READY** | **NO** | deployed tree, base bridge, lease sharing, bench/hardware absent |

Human development proceeds under DEVELOPMENT READY; it does not wait for
deployment readiness.

## 1. Planes

| Plane | Meaning | Snapshot |
|---|---|---|
| **Development** | feature/work branch under test | branch HEAD recorded per finding |
| **Main** | merged `origin/main` | `.github 94b4cd5`, devices `86c721c`, scenarios `6dbedad`, learning `6997825`, interfaces `1e6ecd0`, system `72b2ce2`, studio `40c002b`, mobile `f96cfee` |
| **Deployment** | robot image / deployed tree | `armpi-ultra:flatten-20261125`; R10 evidence contract 0.1.0/`0b8d72…` |

## 2. Finding status

| Finding | Dev | Main | Deployment | Severity | Closure criterion |
|---|---|---|---|---|---|
| Mobile `/cmd_vel` direct path | **Resolved** (intent channel, 50 tests) | **Resolved** (`f96cfee`) | **Open** (not deployed) | Critical | deployed mobile uses intent + system intake |
| Studio legacy motion | **Mitigated/Waived** (default 410, two switches) | **Mitigated/Waived** (`40c002b`, waiver) | **Open** (not removed) | Critical | legacy removed; B4 eliminated |
| Deadman not enforced | **Resolved** (default 300 ms) | **Resolved** (`72b2ce2`) | **Open** (0.1.0) | High | deployed image enforces deadman |
| DDS privileged services | **Resolved** (default-deny) | **Resolved** (`72b2ce2`) | **Open** (not deployed) | High | deployed image gates services |
| Holder bypass | **Resolved** (required) | **Resolved** (`72b2ce2`) | **Open** (0.1.0) | High | deployed image requires holder |
| Base tick shared latch | **Resolved** (tick checks latch) | **Resolved** (`72b2ce2`) | **Open** | Medium | deployed image verified |
| Base hardware bridge | **Open** (fail-closed stub) | **Open** | **Open** | Blocker | reviewed bridge + bench test |
| Cross-process lease sharing | **Open** (`lease_source=none`) | **Open** | **Open** | Blocker | shared lease source design/impl |
| Deployed tree vs dev | — | **Open** (0.1.0 vs 0.2.0/0.3.0) | **Open** | Blocker | deploy 0.2.0/0.3.0 + evidence |
| Contract pin skew | **Open** (six repos 0.1.0) | **Open** | **Open** | High | interfaces 0.3.0 + consumer pins |
| Device fact duplication | **Open** (learning/studio) | **Open** (B8/B10) | **Open** | High | Phase 2 generated snapshots |
| Scenario duplication | **Open** (system/bench/sim/apps) | **Open** | **Open** | High | Phase 2 references |
| Learning pyarrow env | **Resolved** (isolated 68) | **Resolved** (`6997825`) | n/a | Low | keep CI isolated env |
| 200/300 ms parameters | **Provisional** | **Provisional** | n/a | Medium | bench validation, Board acceptance |
| Studio legacy waiver | **Waived** until 2026-12-31 | **Waived** | n/a | Medium | remove code / renew with review |
| Stale open PRs | **Open** (.github #25/#26, devices #1, interfaces #17, studio #3) | n/a | n/a | Low | close/retire explicitly |

## 3. Rules

1. **Development Resolved ≠ Main Resolved.** Only a merged `main` SHA counts
   for the main plane.
2. **Main Resolved ≠ Deployment Resolved.** The deployed image is 0.1.0; every
   hardening item is Open there until a separately authorized deployment.
3. **Static no-Critical ≠ ready.** 12 open boundary findings on main, plus the
   deployment blockers, mean real-robot use remains NOT READY.
4. **Waived ≠ Resolved.** Studio B4 remains waived until 2026-12-31; it is not
   counted in resolved totals.
5. Every row needs repository, commit/snapshot, check time, evidence and a
   closure criterion before a status change.

## 4. Current totals (main)

| Status | Count (main findings) |
|---|---|
| Resolved | 0 deployment; hardening items resolved on main only |
| Mitigated | studio legacy (default-disabled) |
| Waived | 1 (studio B4) |
| Open | 12 boundary findings + deployment blockers |

## Related

- [Boundary report](12-architecture-boundary-check-report.md)
- [Technical debt register](32-technical-debt-register.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
