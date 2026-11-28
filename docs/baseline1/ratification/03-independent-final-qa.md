# Independent Final QA Report — Ratified Main

> Reviewer: independent read-only QA agent, separate from implementation.
> Date: 2026-11-28. No tracked file was modified; no commit/push/merge/tag; no
> robot, DDS/ROS graph or hardware was accessed.

## 1. Verdict

**Substantive ratification: PASS.** The contract, vocabulary, AR5L/R
registration and post-merge acceptance are confirmed on main.

The final record PR #40 needed corrections before approval: it still referenced
closed PR #39, contained contradictory COMPLETE/INCOMPLETE text, and its QA
section described the pre-merge state. Those P1 record-integrity findings are
fixed in this revision. After #40 is approved and merged, Baseline 1 may be
marked COMPLETE; the record itself is the publication step.

## 2. Verified on main

| Item | Result |
|---|---|
| interfaces `426f371` | contract **Accepted** in `CONTRACT.md`; offline scope only; docs-only diff; no schema/IDL |
| scenarios `1c21885` | `vocabulary_status: contracted`; approval reference corrected; no schema/IDL |
| devices `c4be897` | **9 devices / 7 capabilities**; `rokae.ar5l`/`rokae.ar5r`; 123 tests; gate OK |
| applications `0be306e` | 218 + 5 skipped; unchanged |
| interfaces / scenarios | 22 / 116 tests; gates OK |
| Boundary | 25 open + 1 waived |
| Ratified-main acceptance | `/tmp/b1-evidence/final-main-ratified`: `matched_with_unverified`; 8/8 cases; benchmark inconclusive/pass/fail; requirements `36151275…` / `d79dae2f…`; AR5L `ad97bc5f…/f94e376d…`; AR5R `166bd3c5…/31f9b10a…` |
| Freeze record #38 | merged `bf866d6`; it contains the earlier pre-ratification text |
| Record #40 | clean main-based docs-only commit; this revision fixes the QA findings |

## 3. P1 findings and disposition

| ID | Finding | Disposition |
|---|---|---|
| P1-1 | #40 referenced closed #39 as the remaining record | **Fixed**: all references now #40 |
| P1-2 | #40 declared COMPLETE while saying the record must merge before COMPLETE | **Fixed**: status is "COMPLETE, effective on merge of this record"; the publication language no longer contradicts it |
| P1-3 | 03 described #21/#5/#8 as unmerged | **Fixed**: this post-merge report |
| P1-4 | 01 said vocabulary "not on main yet" | **Fixed**: vocabulary is contracted on main |

## 4. P2/P3 notes

- `02` now points to `/tmp/b1-evidence/final-main-ratified`.
- `04` records `.github bf866d6` and explains `f9e77eb` as the pre-record
  source baseline; no self-referential hash.
- Main `.github bf866d6` still carries #38's earlier INCOMPLETE text until #40
  merges; this is expected and is the reason #40 exists.
- `NO_DEVICE_FOR_ROLE` is manually verified; no new automated test was added in
  this record-only PR.
- Studio backend 222 requires the out-of-tree main venv; learning needs
  `UV_PROJECT_ENVIRONMENT` outside the repo.
- AR5 family/unit distinction remains prose-only; the family entry is not a
  deployable unit.

## 5. No-modification statement

The reviewer modified no tracked files, made no remote change, and did not
start a robot, send motion, join a DDS/ROS graph or access hardware. No secret
was printed.
