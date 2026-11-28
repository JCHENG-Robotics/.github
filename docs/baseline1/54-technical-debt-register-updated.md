# Technical Debt Register — Baseline 1 Update

> Summary of the open debt after the Baseline 1 sprint. The canonical register
> remains `.github/docs/boundary-consolidation/32-technical-debt-register.md`;
> this page records the final disposition without opening a new programme.

## 1. Closed or narrowed

| Item | Previous | Now |
|---|---|---|
| TD-17 artifact schema/hash | High, main | **closed on main** (#36 merged; devices/scenarios hash split and role attributes merged) |
| TD-18 cell composition | High, main | **closed on main** for reference; mock task on PR #20 |
| TD-19 device vs algorithm split | Medium, main | **closed on main**; algorithm owners required |
| TD-11 pyarrow env | Low | closed (learning frozen-env 68 tests) |
| Studio B4 | Critical | waived until 2026-12-31, default-disabled; not resolved |

## 2. Open debt (non-blocking for Baseline 1 unless noted)

| ID / area | Severity | Status | Note |
|---|---|---|---|
| Deployment blockers (base bridge, lease sharing, deployed tree, watchdog, DDS authority, bench) | Blocker for deployment | **Open** | Deployment NOT READY; not a Baseline 1 offline blocker |
| Interfaces proposal approval / vocabulary `local_draft` | High for criterion 2 | **Open** | PR #20; no interface-owner approval yet |
| ArmPi reach/payload/aperture/camera resolution | Medium | **Unverified** | no measured device facts; explicitly reported |
| AR5 local SDK/URDF/calibration/unit | Medium | **Missing** | vendor-public facts only; `data_status: partial` |
| PiPER X hardware/runtime adapter | Medium | **Missing** | registration/simulation only |
| Gazebo runtime / ore_sorting world asset | Medium | **Not verified** | offline asset check only |
| Boundary findings B5/B7/B8/B10/B11 | Medium/High | **Open (25) + 1 waived** | schema ownership, device-fact copies, manifest shape; report 48 |
| Deployed contract 0.1.0 vs dev 0.3.0 | Blocker | **Open** | deployment evidence R10 |
| Accidental recreated remote branches | Low | **Open** | retained because remote deletion needs owner approval |
| Old PRs #4/#5/#3/#32/#33/#34/#35 | Low | **Closed/superseded** | #4 closed by #7; handover #32 to be superseded |
| 200 ms freshness / 300 ms deadman | Medium | **Provisional** | bench validation still required |

## 3. Not debt, by design

- Unverified ArmPi capability facts are an honest outcome, not a software
  interoperability failure.
- Mock success is not a real grasp result.
- Benchmark INCONCLUSIVE is a valid observed result.
- No release/tag is intentional.

## 4. Rule retained

Debt is recorded here and in the boundary report; it does not authorize a new
architecture programme or a real-robot test.
