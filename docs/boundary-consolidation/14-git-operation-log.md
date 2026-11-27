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
| `.github` | `feat/controlled-git-20261127` | same | `108b926` | CGO + allowlist + checker + reports | ✅ | [#28](https://github.com/JCHENG-Robotics/.github/pull/28) (stacked on #27) | ✅ m1-gate | n/a (governance) | close PR |
| `jcheng-devices` | `feat/admission-20261127` | same | `9026c16` | device library admission | ✅ | [#2](https://github.com/JCHENG-Robotics/jcheng-devices/pull/2) | ✅ devices-gate | previous phase | close PR |
| `jcheng-scenarios` | `feat/admission-20261127` | same | `6ee7928` | scenario catalog admission | ✅ | [#1](https://github.com/JCHENG-Robotics/jcheng-scenarios/pull/1) | ✅ scenarios-gate | previous phase | close PR |
| `jcheng-interfaces` | `docs/base-intent-proposal-20261127` | same | `3e17add` | BaseIntent/lease-holder proposal | ✅ | [#19](https://github.com/JCHENG-Robotics/jcheng-interfaces/pull/19) | ✅ contract/m1/security | n/a (proposal) | close PR |
| `jcheng-learning` | `feat/regression-20261127` | same | `2d4ea30` | isolated regression baseline | ✅ | [#5](https://github.com/JCHENG-Robotics/jcheng-learning/pull/5) | ✅ learning-gate | previous phase | close PR |
| `jcheng-system` | `feat/authority-hardening-20261127` | pending | `b56cf57` | authority hardening | pending | pending | pending | QA running | revert branch to `879b4b9` (Board decision) |
| `jcheng-mobile` | `feat/authority-hardening-20261127` | pending | `dbc2d76` | intent channel | pending | pending | pending | QA running | revert branch to `89a769f` |
| `jcheng-studio` | `feat/authority-hardening-20261127` | pending | `f65fd26` | legacy isolation | pending | pending | pending | QA running | revert branch to `b5c99e8` |

## 3. Commit inventory (implementation)

| Repository | Commits |
|---|---|
| `jcheng-system` | `9b00466` core (authority/base/watchdog), `b808208` vendor routing + DDS gate, `19629bf` gateway holder/stop, `fde2e14` base intake node, `b56cf57` shared lease view |
| `jcheng-mobile` | `b021aaa` intent channel, `dbc2d76` intent surface + boundary tests |
| `jcheng-studio` | `fbe132d` legacy default-disable + system intent gate, `f65fd26` deprecation docs |

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
- Raw reflog/log evidence stays local (`docs/boundary-consolidation/evidence/`
  is gitignored).
- A local commit is not a delivery; each row requires push + PR + CI evidence.

## Related

- [Controlled Git Operations](../controlled-git-operations.md)
- [Governance incident](../incidents/2026-11-27-git-authority.md)
- [Remote delivery report](19-remote-delivery-report.md) (pending)
