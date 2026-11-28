# Remote Delivery Report

> Status: **partial (2026-11-27)**. Three PRs are merged to `main`; six remain
> open and fail at least one merge gate. No merge was performed by this agent
> in this round. No branch protection, required check or approval was bypassed.
> No release, tag or deployment change.

## 1. Delivery table

| Repository | Branch | HEAD | PR | CI | QA | Delivery |
|---|---|---|---|---|---|---|
| `.github` | `docs/boundary-consolidation-20261127` | `f523540` | [#27](https://github.com/JCHENG-Robotics/.github/pull/27) | ✅ | n/a | **merged** `e441b2d` |
| `jcheng-interfaces` | `docs/base-intent-proposal-20261127` | `3e17add` | [#19](https://github.com/JCHENG-Robotics/jcheng-interfaces/pull/19) | ✅ | n/a | **merged** `1e6ecd0` (proposal only) |
| `jcheng-learning` | `feat/regression-20261127` | `2d4ea30` | [#5](https://github.com/JCHENG-Robotics/jcheng-learning/pull/5) | ✅ | n/a | **merged** `6997825` |
| `.github` | `feat/controlled-git-20261127` | `847f7c5` | [#28](https://github.com/JCHENG-Robotics/.github/pull/28) | ✅ | ❌ final head not QA'd | **blocked: review dismissed** |
| `jcheng-devices` | `feat/admission-20261127` | `9026c16` | [#2](https://github.com/JCHENG-Robotics/jcheng-devices/pull/2) | ✅ | prior | **blocked: no approval** |
| `jcheng-scenarios` | `feat/admission-20261127` | `6ee7928` | [#1](https://github.com/JCHENG-Robotics/jcheng-scenarios/pull/1) | ✅ | prior | **blocked: no approval** |
| `jcheng-system` | `feat/authority-hardening-20261127` | `220b0ce` | [#41](https://github.com/JCHENG-Robotics/jcheng-system/pull/41) | ✅ 12/12 | ✅ PASS | **blocked: conflict with `main`** |
| `jcheng-studio` | `feat/authority-hardening-20261127` | `ce7199b` | [#10](https://github.com/JCHENG-Robotics/jcheng-studio/pull/10) | ✅ 3/3 | ✅ PASS | **blocked: conflict with `main`** |
| `jcheng-mobile` | `feat/authority-hardening-20261127` | `9cee52d` | [#6](https://github.com/JCHENG-Robotics/jcheng-mobile/pull/6) | ✅ 3/3 | earlier | **superseded by #7** |
| `jcheng-mobile` | `feat/authority-hardening-port-20261127` | `dc93f4b` | [#7](https://github.com/JCHENG-Robotics/jcheng-mobile/pull/7) | ✅ 3/3 | ✅ PASS (port tree = `9cee52d`) | **delivered for review; no approval** |
| `.github` | `docs/baseline-1-reports` | `0696c27` | [#29](https://github.com/JCHENG-Robotics/.github/pull/29) stacked on #28 | ✅ m1-gate | n/a (reports) | **delivered for review** |

## 2. Mobile conflict resolution (Decision 2)

- Original #6 and its branch/evidence are preserved. The branch now contains a
  `Merge origin/main` commit `9cee52d`; it was not rewritten.
- New branch `feat/authority-hardening-port-20261127` was created from
  `origin/main` `0972e4b`; the 19-file hardening delta was ported manually into
  one commit `dc93f4b`.
- `git diff dc93f4b 9cee52d` is **empty** — the port tree is identical to the
  audited conflict-resolved tree.
- 50 tests, colcon build, independent QA: PASS.
- PR #7 links #6 and explains the conflict/port/equivalence. Close #6 only
  after #7 is merged, marked "superseded by #7".

## 3. CI notes

- Merged PRs: `m1-gate`, contract/security, `learning-gate` all green.
- #28: `m1-gate` green, but a merge commit was added after QA and the review
  was dismissed; it needs re-QA and re-approval.
- #2/#1: checks green; no approving review.
- #41/#10: checks green; `mergeable=false` against `main`.
- #7: `mobile-gate`, `contract + no-hardware`, `ros build (humble)` green.
- No PR has been merged by bypassing protection.

## 4. Merge and release

**No merge, no auto-merge, no tag, no release, no deployment by this agent.**
The Board/owner merged #27, #19 and #5 concurrently. The remaining merges need
Board decisions:

1. Re-approve #28 after re-QA of the final head.
2. Approve #2 and #1.
3. Decide the system/studio conflict path (merge base branch first, or
   authorize a manual port onto `main`).
4. Approve #7; then close #6 as superseded.

## 5. Rollback

| Repository | Rollback suggestion |
|---|---|
| merged #27/#5/#19 | new reverting commit if needed; no history rewrite |
| `.github` #28 | close PR |
| devices/scenarios | close PR |
| system #41 / studio #10 | close PR or Board-approved port |
| mobile #7 | close PR; #6 remains as evidence |

## Related

- [PR merge report](21-pr-merge-integration-report.md)
- [Git operation log](14-git-operation-log.md)
- [Baseline manifest](25-ecosystem-integration-baseline-1-manifest.md)
