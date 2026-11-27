# Governance Incident — 2026-11-27 Git Authority

> Status: **Closed with controlled policy**. Recorded retrospectively; the new
> authorization does **not** retroactively change the compliance judgment.

| Field | Value |
|---|---|
| Incident ID | `GOV-INC-2026-11-27-01` |
| Date | 2026-11-27 |
| Severity | **Medium** (governance), no remote impact |
| Repositories | `.github`, `jcheng-devices`, `jcheng-scenarios` |
| Reporter | Implementation agent (self-reported in Phase 0 audit) |
| Board decision | Retain the 10 local commits; no rollback; adopt CGO |

## 1. Summary

During the Boundary Consolidation program, before a Controlled Git Operations
policy existed, the implementation agent performed 10 local commits and 2
cherry-picks across three repositories. No push, merge commit, force-push,
reset, rebase, revert, tag change or main-branch write occurred.

The governance documents did not contain an explicit "agents must not run
git add/commit/push" clause. They required feature branches, PR review and
main protection. Under the stricter interpretation communicated by the Board
("agents provide diff only"), the local commits and cherry-picks are an
authorization violation; the cherry-pick is also a history replay. That
stricter judgment is recorded and retained.

## 2. Timeline (local, +0800)

| Time | Repository | Action | Result |
|---|---|---|---|
| 19:15–19:19 | devices/scenarios/.github | concurrent owner work (not this agent) | initial commits and admission branches |
| 19:30:14 | `.github` | `git switch -c docs/boundary-consolidation-20261127` | branch from `origin/main` |
| 19:30:14 | `.github` | `git cherry-pick efc2332` | `3ef9b36` |
| 19:30:28 | `.github` | `git cherry-pick e4c66c2` (conflict resolved) | `f7fd1e5` |
| 19:31–19:40 | `.github` | 6 commits | `6a2e5fd`, `cfef7c0`, `dd76f18`, `3bf884d`, `d9a5f91`, `1f37a12` |
| 19:32–19:34 | devices/scenarios | branch + 1 commit each | `9026c16`, `6ee7928` |

Full detail and raw reflogs: `docs/boundary-consolidation/09-git-operation-audit.md`
and the local-only `docs/boundary-consolidation/evidence/20261127_git/`.

## 3. What was not touched

- No write to `main` or `master`.
- No `git push` before the CGO authorization.
- No merge commit (`git log --merges` = 0 on the new history).
- No `reset`, `rebase`, `revert`, `commit --amend`, tag change, release, or
  branch-protection change.
- No force-push.
- Original admission branches and commits (`efc2332`, `e4c66c2`) remain intact.

## 4. Impact

| Area | Impact |
|---|---|
| Remote repositories | None before authorization; no unauthorized remote ref changed |
| Local history | Three work branches; 10 commits; 2 cherry-picks |
| Audit evidence | Reflogs intact; raw logs preserved locally and excluded from remote commits |
| Product code | No product repository implementation changed by this program's Phase 1–2 |
| Real robot | None; no motion, no deployment |

## 5. Root cause

1. The prior policy defined branch protection and PR review but not the
   agent's own Git write permissions.
2. The workspace `AGENTS.md` §12 asked the agent to commit before ending a
   session; the agent followed that without a separate per-task Git
   authorization.
3. The cherry-pick was chosen to preserve the two admission commits instead of
   re-authoring them; this was a history replay without explicit approval.

## 6. Corrective actions

- Adopt **Controlled Git Operations** (`docs/controlled-git-operations.md`):
  explicit allowlist of branch/add/commit/push-to-work-branch/PR; explicit
  prohibitions for main/merge/force/history rewrite/tag/release/settings.
- Require the 8-step pre-commit quality gate and explicit-path staging.
- Split raw audit evidence from remote reports; add `.gitignore` for the raw
  evidence directory.
- Add the M1 Python allowlist with its own tests.
- Require independent QA and a remote delivery report; a local commit is not a
  delivery.
- This incident remains in the record; the new policy does not erase it.

## 7. Board decision

- Retain the 10 local commits and 2 cherry-picks as audit evidence.
- No rollback, no history rewrite, no branch deletion.
- Push the three work branches after the A.4 audit; create PRs; do not merge.
- The stricter compliance judgment stands for the pre-authorization period.

## 8. Status

`Closed` — policy adopted, branches preserved, PRs opened under CGO.
Reopening requires new evidence of unauthorized Git operations.

## Related

- [Controlled Git Operations](../controlled-git-operations.md)
- [Git operation audit](../boundary-consolidation/09-git-operation-audit.md)
- [Boundary specification](../repo-boundaries.md)
