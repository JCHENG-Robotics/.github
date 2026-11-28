# Controlled Git Operations (CGO)

> Status: **v1.0 (2026-11-27)**, approved for the
> **Ecosystem Stabilization & Authority Hardening** program only.
> This policy does not grant unlimited Git permission to other tasks.
> It records the 2026-11-27 governance incident and replaces the previous
> "diff-only" rule for this program.

## 1. Purpose and scope

CGO lets an implementation agent complete a reviewed change end to end
(branch → commit → push → PR) without asking the Board for every Git command,
while keeping the Board's final merge/release authority and a complete audit
trail.

Scope: the repositories explicitly named in the current program's task
authorization. A repository without an explicit task authorization must not be
written to, even if it is listed in the ecosystem map.

## 2. Roles

| Role | Owns | Cannot |
|---|---|---|
| **Board (Owner)** | final merge, release, tag, branch protection, high-risk Git operations, acceptance | delegate these silently |
| **Implementation Agent** | branch, add, commit, push to a work branch, PR, CI queries, fixes and follow-up commits within scope | merge, force-push, rewrite history, release, change settings |
| **Independent QA** | independent verification of behavior, tests, claims and Git content | be the implementing agent; self-approval |

Self-check is not independent acceptance. A passing CI or a green local suite is
evidence, not a waiver.

## 3. Authorized operations (no per-command Board approval)

Within the authorized repository and task scope:

- create a work branch that follows the ecosystem naming convention
  (`feat|fix|docs|chore/<topic>-YYYYMMDD`);
- `git add` specific files;
- `git commit` with Conventional Commits;
- `git push` to the **corresponding remote work branch**;
- create or update a Pull Request;
- query remote branches, commit history and CI status;
- fix failures and append commits within the same scope.

## 4. Prohibited without separate Board approval

- push directly to `main` or `master`;
- merge a Pull Request into a protected branch;
- force-push, including `--force-with-lease`;
- `reset`, `rebase`, `revert`, `cherry-pick`, `commit --amend` or any other
  history rewrite/rollback;
- delete a remote branch;
- modify or delete a tag;
- create a formal release;
- change repository visibility, access, branch protection or organization
  security settings;
- bypass CI, required checks or independent QA;
- publish an unaccepted change as a stable release.

If a fix needs history rewriting, stop and ask the Board. Do not "clean up" a
pushed branch.

## 5. Pre-commit quality gate

Before every commit:

1. Inspect `git status`, `git diff`, `git diff --cached`.
2. Confirm every change is inside the current task authorization.
3. Check for other agents' or the user's uncommitted changes; never include
   them silently.
4. Never run `git add .` or `git add -A`; stage explicit paths.
5. Exclude secrets, tokens, personal data, local absolute paths, device
   credentials, private datasets and raw audit evidence.
6. Run the repository gate and the relevant tests.
7. Record test output, known limitations and unverified items.
8. Use Conventional Commits (`feat(scope): …`, `fix(scope): …`, `docs: …`).

If a concurrent change, remote conflict or unexplained file appears, stop
writing to that repository and report. Do not overwrite or merge it.

## 6. Branches, PRs and remote delivery

- One logical change per branch; one PR per logical change.
- Push to a remote branch with an explicit refspec, never to `main`.
- Draft PR is required while the work is WIP or not independently verified.
- Ready-for-review requires: gate green, tests recorded, QA report, scope and
  sensitive-content check.
- The Board performs the merge. The agent does not merge or enable auto-merge.
- Remote delivery is not complete until the push, PR and CI status are
  observed and recorded. A local commit is not a delivery.

Suggested PR body sections: scope, files, tests/evidence, boundary impact,
risk, rollback, known gaps, QA status.

## 7. Sensitive content and audit evidence

- Raw reflogs, full logs and local paths stay local. Remote commits contain
  only redacted reports.
- No tokens, keys, real site IPs, robot credentials, private datasets or
  personal data.
- Absolute workspace paths in committed documents are replaced with
  `<workspace>`.
- Evidence is referenced by relative path, commit SHA or external URL, not by
  a local home directory.

## 8. Concurrency

- Before writing, check `git status` and the branch/upstream.
- A dirty tree owned by another agent/user is not yours to stage.
- If two actors touch the same repository, the agent stops and reports.
- Do not switch branches while another actor's work is uncommitted in that
  worktree.

## 9. Incident handling

1. Stop the affected Git operation; do not rewrite history.
2. Preserve reflogs/logs locally.
3. Record a Governance Incident: what, when, repositories, SHAs, impact,
   whether remote/main/tag was touched, root cause.
4. Report to the Board; the Board decides rollback or retention.
5. Corrective action updates this policy and, if needed, the gate.
6. New authorization does not retroactively change the compliance judgment of
   past operations.

## 10. Audit log requirements

Every delivery records:

| Field | Content |
|---|---|
| Repository | organization/repo |
| Local branch | branch name |
| Remote branch | branch name |
| Commit SHA | full SHA |
| Commit message | Conventional Commit |
| Push status | success/failure + timestamp |
| Pull Request | URL and state |
| CI status | required checks |
| QA status | PASS/FAIL/Rework |
| Known risk | residual |
| Open items | not done |
| Rollback | revert/close PR, no history rewrite |

## 11. Relationship to branch protection and QA

CGO does not weaken branch protection. `main` remains protected; direct push,
force-push and deletion stay forbidden. Required checks and independent QA
remain mandatory. A green CI does not authorize real-robot motion; the
hardware authorization rules in `AGENTS.md` and `docs/hardware-workflow.md`
still apply.

## 12. Quick table

| Operation | Agent | Board |
|---|---|---|
| create work branch | ✅ | — |
| add/commit specific files | ✅ | — |
| push work branch | ✅ | — |
| open/update PR | ✅ | — |
| query CI | ✅ | — |
| fix and append commit | ✅ | — |
| push main | ❌ | ✅ (exceptional) |
| merge PR | ❌ | ✅ |
| force-push / rewrite | ❌ | ✅ (exceptional, documented) |
| tag / release | ❌ | ✅ |
| change protection/settings | ❌ | ✅ |

## Related

- [Governance incident 2026-11-27](incidents/2026-11-27-git-authority.md)
- [Git operation audit](boundary-consolidation/09-git-operation-audit.md)
- [Repository boundary specification](repo-boundaries.md)
- [Documentation standard](documentation-standard.md)
