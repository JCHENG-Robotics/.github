# Remote Delivery Report

> Status: **partial (2026-11-27)**. All authorized branches are pushed and PRs
> exist. **No PR is merged.** The mobile PR has a remote conflict and is
> stopped under Controlled Git Operations A.3; no automatic resolution was
> attempted.

## 1. Delivery table

| Repository | Local / remote branch | HEAD | PR | CI | QA | Delivery |
|---|---|---|---|---|---|---|
| `.github` | `docs/boundary-consolidation-20261127` | `f523540` | [#27](https://github.com/JCHENG-Robotics/.github/pull/27) | ✅ m1-gate | n/a (docs) | delivered |
| `.github` | `feat/controlled-git-20261127` | `5b0ddd8` | [#28](https://github.com/JCHENG-Robotics/.github/pull/28) stacked on #27 | ✅ m1-gate | n/a (governance) | delivered |
| `jcheng-devices` | `feat/admission-20261127` | `9026c16` | [#2](https://github.com/JCHENG-Robotics/jcheng-devices/pull/2) | ✅ devices-gate | prior phase | delivered |
| `jcheng-scenarios` | `feat/admission-20261127` | `6ee7928` | [#1](https://github.com/JCHENG-Robotics/jcheng-scenarios/pull/1) | ✅ scenarios-gate | prior phase | delivered |
| `jcheng-interfaces` | `docs/base-intent-proposal-20261127` | `3e17add` | [#19](https://github.com/JCHENG-Robotics/jcheng-interfaces/pull/19) | ✅ contract/m1/security | n/a (proposal) | delivered |
| `jcheng-learning` | `feat/regression-20261127` | `2d4ea30` | [#5](https://github.com/JCHENG-Robotics/jcheng-learning/pull/5) | ✅ learning-gate | prior phase | delivered |
| `jcheng-system` | `feat/authority-hardening-20261127` | `220b0ce` | [#41](https://github.com/JCHENG-Robotics/jcheng-system/pull/41) | ✅ all completed checks success | ✅ PASS | delivered for review |
| `jcheng-mobile` | `feat/authority-hardening-20261127` | `64dce1e` | [#6](https://github.com/JCHENG-Robotics/jcheng-mobile/pull/6) | ❌ **no CI: PR conflicts with `main`** | ✅ PASS (local) | **blocked** |
| `jcheng-studio` | `feat/authority-hardening-20261127` | `ce7199b` | [#10](https://github.com/JCHENG-Robotics/jcheng-studio/pull/10) | ✅ studio/console/frontend success | ✅ PASS | delivered for review |

## 2. Mobile conflict — stopped, not resolved

`GET /repos/JCHENG-Robotics/jcheng-mobile/pulls/6` reports
`mergeable=false`, `mergeable_state=dirty`. The hardening branch was based on
`fix/m10-static-validation`; retargeting the PR to `main` exposed a conflict.

Per CGO A.3, the agent **stopped writing to this repository**. No rebase,
cherry-pick, force-push or automatic merge was performed. The branch remains
pushed as evidence. Board options:

1. Merge `fix/m10-static-validation` first, then retarget #6 to `main`.
2. Approve a fresh branch from `main` with the hardening file set applied
   manually (no history rewrite) and a new PR.
3. Accept the feature-branch base and record that no PR CI ran.

## 3. CI notes

- System: `m1-gate`, `m3-mock`, `m4-readonly`, `m5-mock`, `m5-vendor`,
  `m6-replay` all completed success. `mergeable_state=clean`.
- Studio: `studio-gate`, `console-tests`, `frontend-build` success; blocked
  only by the required review.
- Mobile: no checks because the PR base after retarget has a conflict and the
  workflow filters `pull_request` to `main`. Local tests are 50 passed.
- `.github`, devices, scenarios, interfaces and learning checks are green.

## 4. Merge and release

**No merge, no auto-merge, no release.** The Board decides the merge order and
whether to merge the stacked `.github` PR #28 after #27. No tag was created and
no deployment was changed.

## 5. Rollback

| Repository | Rollback suggestion |
|---|---|
| `.github` | close #28, then #27; no history rewrite |
| devices / scenarios | close the PR; branch is isolated |
| interfaces | close #19; proposal only |
| learning | close #5; docs/evidence only |
| system | close #41; Board may revert to `879b4b9` with a new commit |
| mobile | close #6; Board decides the conflict path |
| studio | close #10; Board may revert to `b5c99e8` with a new commit |

Never rewrite a pushed branch or tag. Use a new reverting commit if the Board
chooses to roll back code.

## Related

- [Git operation log](14-git-operation-log.md)
- [Independent QA](18-independent-qa-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
