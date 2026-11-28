# Git Operation Log — stabilization program

> Status: **in progress (2026-11-27)**. Controlled Git Operations under
> [`../controlled-git-operations.md`](../controlled-git-operations.md).
> No write to `main`, no merge, no force-push, no tag/release, no history
> rewrite. Pre-authorization operations are recorded in
> [`09-git-operation-audit.md`](09-git-operation-audit.md).

## 1. Pre-authorization (retained as audit evidence)

| Repository | Commits | Note |
|---|---|---|
| `.github` | `3ef9b36`, `f7fd1e5`, `6a2e5fd`, `cfef7c0`, `dd76f18`, `3bf884d`, `d9a5f91`, `1f37a12` | 2 cherry-picks; no merge commit; no push before CGO |
| `jcheng-devices` | `9026c16` | on top of the owner's `f87c448`, `cae8fb6`, `029991f` |
| `jcheng-scenarios` | `6ee7928` | on top of the owner's `4390212` |

Governance incident: [`../incidents/2026-11-27-git-authority.md`](../incidents/2026-11-27-git-authority.md).

## 2. Post-authorization deliveries

| Repository | Local branch | Remote branch | HEAD | Commit | Push | PR | CI | QA | Rollback |
|---|---|---|---|---|---|---|---|---|---|
| `.github` | `docs/boundary-consolidation-20261127` | same | `f523540` | phase-2 audit/design/readiness | ✅ | [#27](https://github.com/JCHENG-Robotics/.github/pull/27) | ✅ m1-gate | n/a (docs) | close PR; no history rewrite |
| `.github` | `feat/controlled-git-20261127` | same | `5b0ddd8` | CGO + allowlist + checker + reports | ✅ | [#28](https://github.com/JCHENG-Robotics/.github/pull/28) (stacked on #27) | ✅ m1-gate | n/a (governance) | close PR |
| `jcheng-devices` | `feat/admission-20261127` | same | `9026c16` | device library admission | ✅ | [#2](https://github.com/JCHENG-Robotics/jcheng-devices/pull/2) | ✅ devices-gate | previous phase | close PR |
| `jcheng-scenarios` | `feat/admission-20261127` | same | `6ee7928` | scenario catalog admission | ✅ | [#1](https://github.com/JCHENG-Robotics/jcheng-scenarios/pull/1) | ✅ scenarios-gate | previous phase | close PR |
| `jcheng-interfaces` | `docs/base-intent-proposal-20261127` | same | `3e17add` | BaseIntent/lease-holder proposal | ✅ | [#19](https://github.com/JCHENG-Robotics/jcheng-interfaces/pull/19) | ✅ contract/m1/security | n/a (proposal) | close PR |
| `jcheng-learning` | `feat/regression-20261127` | same | `2d4ea30` | isolated regression baseline | ✅ | [#5](https://github.com/JCHENG-Robotics/jcheng-learning/pull/5) | ✅ learning-gate | previous phase | close PR |
| `jcheng-system` | `feat/authority-hardening-20261127` | same | `220b0ce` | authority hardening + QA rework | ✅ | [#41](https://github.com/JCHENG-Robotics/jcheng-system/pull/41) | ✅ all checks success | QA PASS | revert branch to `879b4b9` (Board decision) |
| `jcheng-mobile` | `feat/authority-hardening-20261127` | same | `64dce1e` | intent channel + QA rework | ✅ | [#6](https://github.com/JCHENG-Robotics/jcheng-mobile/pull/6) | **blocked: PR conflicts with `main`; CI not run** | QA PASS (local) | Board decision; CGO stop on conflict |
| `jcheng-studio` | `feat/authority-hardening-20261127` | same | `ce7199b` | legacy isolation + QA rework | ✅ | [#10](https://github.com/JCHENG-Robotics/jcheng-studio/pull/10) | ✅ all checks success | QA PASS | revert branch to `b5c99e8` (Board decision) |

## 3. Commit inventory (implementation)

| Repository | Commits |
|---|---|
| `jcheng-system` | `9b00466` core, `b808208` vendor/DDS, `19629bf` gateway holder/stop, `fde2e14` base intake node, `b56cf57` shared lease view, `220b0ce` QA rework |
| `jcheng-mobile` | `b021aaa` intent channel, `dbc2d76` intent surface, `cd491c5` liveness docs, `64dce1e` residual docstring |
| `jcheng-studio` | `fbe132d` legacy default-disable + system intent gate, `f65fd26` deprecation docs, `63266a2` empty-lease + docs, `ce7199b` test tightening |

## 4. Prohibited-operation check

| Operation | Occurred |
|---|---|
| push to `main`/`master` | no |
| merge PR | no |
| force-push / `--force-with-lease` | no |
| reset / rebase / revert / cherry-pick / amend after CGO | no |
| delete remote branch | no |
| modify/delete tag | no |
| create release | no |
| change repo visibility/protection/settings | no |
| bypass CI/QA | no |

## 5. Notes

- The two pre-authorization cherry-picks are retained and are not rewritten.
- `feat/controlled-git-20261127` is stacked on the boundary branch; retarget
  to `main` after #27 merges.
- `jcheng-mobile` PR #6 was retargeted to `main` and reports
  `mergeable=false` / `mergeable_state=dirty`. Per CGO A.3 the agent stopped;
  no rebase, cherry-pick, force-push or automatic resolution was performed.
  The Board decides the conflict path.
- Raw reflog/log evidence stays local (`docs/boundary-consolidation/evidence/`
  is gitignored).
- A local commit is not a delivery; each row requires push + PR + CI evidence.

## Related

- [Controlled Git Operations](../controlled-git-operations.md)
- [Governance incident](../incidents/2026-11-27-git-authority.md)
- [Remote delivery report](19-remote-delivery-report.md) (pending)
