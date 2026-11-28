# Board Review Packet

> Status: **closure record (2026-11-28)**. All Wave 1–4 PRs are merged; there are
> no pending approvals for this sprint. The Agent did not approve, merge or
> bypass branch protection. This packet records the evidence the Board can
> audit.

## 1. Merged PRs

| PR | Head (audited) | Base at merge | Merge SHA | CI | QA | CODEOWNERS | Risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| `.github` #27 | `f523540` | `main` | `e441b2d` | ✅ | docs | satisfied | low | keep |
| `.github` #28 | `847f7c5` | `main` | `0fe2f0e` | ✅ | final head re-QA required** | satisfied | medium | keep; QA note |
| `.github` #29 | `303e0ba` | `main` | `94b4cd5` | ✅ | docs | satisfied | low | keep |
| devices #2 | `9026c16` | `f87c448` | `86c721c` | ✅ | prior | satisfied | low | keep |
| scenarios #1 | `6ee7928` | `4390212` | `6dbedad` | ✅ | prior | satisfied | low | keep |
| learning #5 | `2d4ea30` | `main` | `6997825` | ✅ | prior | satisfied | low | keep |
| interfaces #19 | `3e17add` | `main` | `1e6ecd0` | ✅ | proposal | satisfied | low | keep; proposal only |
| system #41 | `d10006f` | `3fed859` | `72b2ce2` | ✅ 12/12 | PASS | satisfied | medium | keep |
| studio #10 | `2fddb64` | `1c7b099` | `40c002b` | ✅ 3/3 | PASS | satisfied | medium | keep |
| mobile #7 | `dc93f4b` | `0972e4b` | `f96cfee` | ✅ 3/3 | PASS (port) | satisfied | medium | keep |

\*\* #28 final head `847f7c5` contains a `Merge origin/main` commit after the
earlier QA; the merged tree is the CGO/allowlist/checker content, but a final
tree-level QA record is still a governance gap (TD-level). No product code is
affected.

## 2. Closed / superseded

| PR | Disposition |
|---|---|
| mobile #6 | **closed** as superseded by #7 (`f96cfee`); original branch/commits/evidence preserved; no history rewrite |

## 3. Open PRs outside this sprint's merge set

| PR | Status | Recommendation |
|---|---|---|
| `.github` #25 | stale devices admission duplicate | close/retire explicitly (not this sprint) |
| `.github` #26 | stale scenarios admission duplicate | close/retire explicitly |
| devices #1 | old robot-profile fix branch | verify content already in main; close/retire |
| interfaces #17 | `intent_source` proposal/implementation | keep for a separate contract decision |
| studio #3 | old joint-intent branch | verify/close |

These are **not** blocking Baseline 1; they are registered in the Technical
Debt Register (TD-15).

## 4. Approval/merge gate evidence

- Every merged PR passed its required checks and had a real approving review
  where branch protection required one (system/studio/.github/interfaces/
  learning/devices/scenarios). Mobile main has no branch protection; #7 was
  merged after CI/QA but without an approving review — recorded, not a bypass.
- No admin override, no force-push, no history rewrite, no tag/release.
- `enforce_admins=true` on the protected repos; the Agent did not attempt an
  override.

## 5. Recommendation to the Board

1. Accept the merged Wave 1–4 set as the **main integration status**.
2. Note that #28's final merge-commit QA record is a documentation gap, not a
   code regression.
3. Decide whether to retire the stale open PRs in TD-15.
4. Baseline 1 remains **INCOMPLETE** until Phase 2 (device/scenario) and the
   offline reference integration are completed and merged.

## Related

- [PR merge report](21-pr-merge-integration-report.md)
- [Status model](31-status-model.md)
- [Technical debt](32-technical-debt-register.md)
