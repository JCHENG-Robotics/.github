# Studio Waiver Verification — W-2026-11-27-01

> Status: **conditional acceptance verified on the implementation branch**.
> Studio PR #10 is still blocked by a `main` conflict; the waiver and the code
> are not merged yet. The waiver is valid only while the legacy path remains
> default-disabled and non-reachable from normal configuration.

## 1. Default reachability

| Check | Evidence | Result |
|---|---|---|
| Default mode is `mock` | `backend/app/config.py:107` (`ARMPI_MODE` default `"mock"`) | pass |
| Legacy switch default false | `backend/app/config.py:85,134` (`legacy_motion_enabled=False`) | pass |
| `MODE=legacy` alone fails startup | `config.py:138` raises unless `ENABLE_LEGACY_MOTION=1` | pass |
| `ENABLE_LEGACY_MOTION=1` alone is ignored | `config.py:143` warning; endpoints stay 410 | pass |
| Three legacy endpoints default 410 | `routes.py:152-166`; `test_legacy_motion_disabled.py::test_legacy_endpoints_answer_410_by_default` | pass |
| No default adapter dispatch | `test_legacy_motion_disabled.py::test_non_legacy_service_calls_never_touch_the_adapter`; static test lists only `legacy_motion.py` containing `/motion/dispatch` | pass |
| Empty/whitespace lease rejected | 400 `BAD_REQUEST`, never dispatched; `test_legacy_empty_lease_is_rejected_and_never_dispatched` (tightened) | pass |
| Stop goes to system | `test_stop_goes_through_the_system_and_never_the_local_adapter` | pass |
| Normal config cannot enable | No deploy/config file sets `ARMPI_MODE=legacy` or `ARMPI_ENABLE_LEGACY_MOTION=1`; only docs/config code mention them | pass |

## 2. Residual import

`routes.py:30` and `motion_ops.py:27` import only `legacy_motion_error` (the
410 response helper), not the dispatch adapter. The module still contains the
adapter, so the B4 static finding remains; it is waived, not eliminated. The
removal plan splits the helper out first, then moves/deletes the adapter.

## 3. Waiver governance

| Requirement | Evidence | Result |
|---|---|---|
| Owner | `owner: jcheng-studio` | pass |
| Expiry | `expires: 2026-12-31` | pass |
| Expiry enforced | `apply_waivers` ignores expired entries; tests `test_expired_waiver_is_ignored`, `test_waiver_evidence_mismatch_is_ignored` | pass |
| Evidence scoped | waiver matches `legacy_motion.py` only, not any future B4 finding in the repo | pass |
| Removal plan | split helper, then move/delete adapter by 2026-12-31 or gateway retirement | pass |
| Closure criteria | B4 eliminated, endpoints permanently 410, tests retained, waiver removed | pass |

## 4. Condition for keeping the waiver

If any normal deployment configuration can enable the legacy path, or if the
legacy path can bypass the system authority without the explicit two-switch
operator mode, **the waiver is void** and the path must be removed or redesigned.
The current evidence shows normal mode (`mock` or `hardware`) cannot reach the
legacy adapter; the explicit `MODE=legacy + ENABLE_LEGACY_MOTION=1` path is
operator-only, not system-authorized, and is documented as scheduled for
removal.

## 5. Current blocker

Studio PR #10 (`ce7199b`) is `mergeable=false` against `main`. The verification
above is on the branch; it becomes effective on merge. Until the conflict is
resolved by the Board-approved path, the waiver is conditional and the code is
not on `main`.

## Related

- [Waiver registry](../../boundary-waivers.yaml)
- [Boundary check report](12-architecture-boundary-check-report.md)
- [Independent QA](18-independent-qa-report.md)
