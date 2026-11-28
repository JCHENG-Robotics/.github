# Technical Debt Register

> Status: **v1.0 (2026-11-28)**. Non-blocking debt is registered here instead
> of expanding the governance scope. Blocking items are marked **Blocker**.
> No item is closed by deleting a check.

| ID | Debt | Severity | Plane | Owner | Next action | Closure criterion |
|---|---|---|---|---|---|---|
| TD-01 | `jcheng-interfaces` no `capability.yaml` | High | Main | interfaces | add manifest | B5 clean |
| TD-02 | `jcheng-system` no `capability.yaml` | High | Main | system | add manifest | B5 clean |
| TD-03 | interfaces/learning no `SCHEMA_OWNERSHIP.md` | Medium | Main | interfaces/learning | add ownership tables | B7 clean |
| TD-04 | system deployed tree 0.1.0 vs dev 0.2.0/0.3.0 | **Blocker** | Deployment | system | deploy-tree alignment with evidence | R10 evidence matches dev contract |
| TD-05 | studio `capability.yaml` 0.8.0 vs lock 0.7.0 | Medium | Main | studio | update lock on release | B6 clean |
| TD-06 | learning `profiles/armpi_ultra.yaml` device copy | High | Main | learning | Phase 2 generated snapshot/reference | B8/B10 clean |
| TD-07 | studio `joint_mapping.yaml`/`takeover.yaml` device copies | High | Main | studio | Phase 2 generated reference or remove | B8/B10 clean |
| TD-08 | Base hardware bridge unavailable | **Blocker** | Deployment | system | reviewed bridge + bench test | zero/duty verified |
| TD-09 | Cross-process lease sharing | **Blocker** | Deployment | system | shared lease source design/impl | base accepts gateway lease across processes |
| TD-10 | DDS `ExecuteMotion` lacks holder | High | Main | interfaces/system | proposal adds holder | DDS path usable with holder |
| TD-11 | Contract pin skew (six repos 0.1.0) | High | Main | interfaces/consumers | 0.3.0 release + pins | lock/manifests agree |
| TD-12 | 200 ms/300 ms provisional | Medium | Main | system/QA | bench validation | measured distribution + Board acceptance |
| TD-13 | Studio legacy waiver | Medium | Main | studio | remove adapter by 2026-12-31 | B4 eliminated, waiver removed |
| TD-14 | No Humble/Gazebo/hardware regression | High | Deployment | all | container + bench plan | evidence at each layer |
| TD-15 | Stale open PRs (.github #25/#26, devices #1, interfaces #17, studio #3) | Low | Main | Board | close/retire explicitly | no stale PRs |
| TD-16 | Frontend still calls 410 legacy endpoints | Low | Main | studio | frontend copy/disable | UI has no legacy motion affordance |
| TD-17 | Cross-repo artifact schema/hash | High | Main | devices/scenarios/applications | — | **Closed on main** (#6/#4/#19): source hash vs artifact self-hash; stale rejection |
| TD-18 | Cell-level capability composition | High | Main | scenarios/devices/applications | — | **Closed on main**: role composition + `matched_with_unverified` |
| TD-19 | Device vs algorithm capability split | Medium | Main | scenarios | — | **Closed on main**: owner split + `deferred_to` |
| TD-20 | Offline artifact contract ratification not on main; vocabulary `local_draft` on main | High | Main | interfaces/scenarios | merge #21 then #5 | Accepted/1.0.0 + `contracted` on main |
| TD-21 | No ore_sorting Gazebo world; `gz` CLI missing; runtime unverified | Medium | Offline | simulation | add world + runtime check | asset loads and mock/Gazebo evidence |
| TD-22 | AR5L/AR5R units have no local SDK/URDF/calibration; variant kinematics unverified | Medium | Dev branch | devices | merge #8; register local data | variant-specific limits/interface verified |
| TD-23 | Accidental/closed remote branches not deleted | Low | Main | Board | approve cleanup list | branches removed with owner approval |
| TD-24 | Mock ore-sorting task and acceptance gates unmerged (apps #20) | High | Dev branches | applications | review/merge #20 | merged + fixed-main rerun |

## Rules

- This register does not authorize implementation; blockers need separate
  design/approval.
- A waiver is not closure. TD-13 remains until the code is removed.
- A mock pass does not close TD-08/TD-09/TD-14.
- New debt is added here, not by creating a new governance program (Decision 10).

## Related

- [Status model](31-status-model.md)
- [Boundary report](12-architecture-boundary-check-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
