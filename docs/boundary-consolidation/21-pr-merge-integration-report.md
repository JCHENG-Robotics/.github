# PR Merge & Integration Report

> Status: **partial (2026-11-27)**. No merge was performed by this agent in this
> round. Three PRs were merged during the concurrent window by the Board/owner;
> the remaining PRs fail at least one merge gate. No branch protection,
> required check or approval was bypassed.

## 1. Merge records (verified)

| PR | Head (audited) | Merge SHA | Main after merge | CI | Approval | Merged at (UTC) | Method |
|---|---|---|---|---|---|---|---|
| `.github` #27 | `f523540` | `e441b2d` | `b66966c` (after #24) | `m1-gate` success | `JerichoSwaine` | 2026-11-27T13:23:30Z | squash |
| `jcheng-interfaces` #19 | `3e17add` | `1e6ecd0` | `1e6ecd0` | contract/m1/security success | `JerichoSwaine` | 2026-11-27T14:52:40Z | squash; **proposal only** |
| `jcheng-learning` #5 | `2d4ea30` | `6997825` | `6997825` | `learning-gate` success | `JerichoSwaine` | 2026-11-27T14:54:48Z | squash |

`#19` merging does not publish a runtime contract: the `BaseIntent`/lease-holder
document remains a proposal; no IDL, schema or contract hash changed.

## 2. Gate status of open PRs

| PR | Head | Mergeable | Required review | QA covers final head | Verdict |
|---|---|---|---|---|---|
| `.github` #28 | `847f7c5` | true | **dismissed / none** | **no** (merge commit `847f7c5` not QA'd) | **BLOCKED** |
| `jcheng-devices` #2 | `9026c16` | true | **none** | prior phase | **BLOCKED** |
| `jcheng-scenarios` #1 | `6ee7928` | true | **none** | prior phase | **BLOCKED** |
| `jcheng-system` #41 | `220b0ce` | **false (dirty)** | dismissed | yes (`220b0ce`) | **BLOCKED: conflict** |
| `jcheng-studio` #10 | `ce7199b` | **false (dirty)** | approved | yes (`ce7199b`) | **BLOCKED: conflict** |
| `jcheng-mobile` #6 | `9cee52d` | true | none | no (superseded) | **superseded by port branch** |

Gate failures:

1. **#28**: a `Merge origin/main` commit was pushed after QA; review dismissed.
   The final commit is not QA-covered. Re-QA + re-approval required.
2. **#2/#1**: no approving review; branch protection requires one.
3. **#41/#10**: conflicts with `main` (`mergeable=false`, `dirty`). CGO
   prohibits rebase/cherry-pick/force; the batch is paused.
4. **#6**: now contains a `Merge origin/main` commit (`9cee52d`) on the old
   branch. A new branch from `main` is being prepared per Decision 2; the
   original PR/branch is preserved.

## 3. Cross-repository order check

| Dependency | Check | Result |
|---|---|---|
| #27 → #28 | #28 is stacked on the boundary baseline | #27 merged; #28 retargeted to main |
| #19 → system/mobile | proposal only; system uses a repo-local envelope | no runtime contract dependency |
| #2/#1 → nothing | offline declaration repos | independent |
| #5 → nothing | docs/evidence | independent |
| system → mobile | mobile intent is consumed by system base intake | system must merge before/with mobile |
| system → studio | studio forwards to system `/v1` | system must merge before/with studio |

No order inversion was found, but the system/mobile/studio chain cannot complete
while #41/#10 are conflicted and #6 is superseded.

## 4. Required Board action

1. Approve #2 and #1 (or provide a second reviewer).
2. Re-approve #28 after re-QA of `847f7c5`.
3. Decide the system #41 and studio #10 conflict path: merge the base branch
   first, or authorize a manual port onto `main` (same method as Decision 2).
4. Approve the mobile replacement PR once QA passes; then close #6 as
   superseded.

Do not merge by bypassing protection; this agent will not use admin override or
fabricate an approval.

## 5. No merge/no release statement

No merge, auto-merge, tag or release was created by this agent. No deployment
was changed. The three merged PRs were completed outside this agent's session;
their records above were verified from the GitHub API.

## Related

- [Git operation log](14-git-operation-log.md)
- [Remote delivery report](19-remote-delivery-report.md)
- [Independent QA](18-independent-qa-report.md)
