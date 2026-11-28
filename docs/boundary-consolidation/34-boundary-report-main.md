# Boundary Report — Actual Main Baseline

> Status: **main integration snapshot (2026-11-28)**. Report-only; static
> checks are not runtime safety proof. This supersedes the development-branch
> counts for the main plane; the branch report remains for history.

## 1. Snapshot

| Repository | `main` SHA |
|---|---|
| `.github` | `94b4cd5` |
| `jcheng-devices` | `86c721c` |
| `jcheng-scenarios` | `6dbedad` |
| `jcheng-learning` | `6997825` |
| `jcheng-interfaces` | `1e6ecd0` |
| `jcheng-system` | `72b2ce2` |
| `jcheng-studio` | `40c002b` |
| `jcheng-mobile` | `f96cfee` |

Checker: `check_boundaries.py --root /tmp/eib1-workspace --mode report`
(exit 0). Result: **12 open + 1 waived**, 0 open Critical.

## 2. Findings

| Rule | Severity | Repo | Evidence | Status | Note |
|---|---|---|---|---|---|
| B5 | High | interfaces | no `capability.yaml` | Open | add manifest |
| B7 | Medium | interfaces | 7 schemas no ownership | Open | add `SCHEMA_OWNERSHIP.md` |
| B5 | High | system | no `capability.yaml` | Open | add manifest |
| B6 | High | system | R10 deployed contract 0.1.0/`0b8d72…` vs dev 0.2.0/`afca22…` | Open | deployment blocker |
| B7 | Medium | learning | 1 schema no ownership | Open | add ownership table |
| B8 | High | learning | `profiles/armpi_ultra.yaml` device copy | Open | Phase 2 |
| B10 | Medium | learning | copy has no provenance | Open | Phase 2 |
| B4 | Critical | studio | `legacy_motion.py` `/motion/dispatch` | **Waived** `W-2026-11-27-01` until 2026-12-31 | default-disabled |
| B6 | Medium | studio | `capability.yaml` 0.8.0 vs lock 0.7.0 | Open | release/lock update |
| B8 | High | studio | `joint_mapping.yaml` device copy | Open | Phase 2 |
| B8 | High | studio | `takeover.yaml` device copy | Open | Phase 2 |
| B10 | Medium | studio | `joint_mapping.yaml` no provenance | Open | Phase 2 |
| B10 | Medium | studio | `takeover.yaml` no provenance | Open | Phase 2 |

## 3. Change vs development branch

| Item | Dev branch | Main |
|---|---|---|
| open findings | 28 | **12** |
| waived | 1 | 1 |
| mobile B4 `/cmd_vel` | eliminated | **eliminated on main** |
| system holder/deadman/DDS | resolved | **resolved on main** |
| studio legacy | default-disabled | **default-disabled/waived** |
| device copies | open | open (Phase 2) |

Findings were not reduced by deleting rules; the drop is from merged fixes.

## 4. Classification

- **Resolved on main**: mobile direct `/cmd_vel`, deadman default, holder,
  DDS privileged-service gate, base tick latch.
- **Mitigated**: studio legacy default-disabled.
- **Waived**: studio B4 (not resolved).
- **Open**: B5/B7 manifests/ownership, system deployment tree, studio lock
  skew, device-fact copies (Phase 2).

## 5. Limits

- Static only; no DDS/ROS runtime, no device, no hardware.
- 0 open Critical does **not** mean real-robot ready; deployment blockers
  remain (base bridge, cross-process lease, deployed tree, bench validation).
- The checker runs from `.github` main and reads repo-local files; it cannot
  prove runtime topic/QoS/subscriber behavior.

## Related

- [Status model](31-status-model.md)
- [Technical debt](32-technical-debt-register.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
