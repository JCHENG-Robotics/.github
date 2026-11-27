# Git Operation Audit — 2026-11-27 专项

> Status: **v1.0 (2026-11-27)**. 只记录与取证；**未执行 reset、rebase、revert、
> merge、push、tag 变更或任何历史改写**。原始 reflog/log 保存在
> [`evidence/20261127_git/`](evidence/20261127_git/)。

## 1. 直接回答

| 问题 | 回答 |
|---|---|
| 本次任务期间执行过哪些 Git 写操作？ | 3 次 `git switch -c`（建分支）、1 次 `git cherry-pick`（两个提交）、8 次 `git add`、10 次 `git commit`。无 push、无 merge、无 reset/rebase/revert、无 tag 变更。 |
| 新增 commit / merge commit 及 SHA？ | 10 个 commit，其中 2 个是 cherry-pick 重放；**0 个 merge commit**。SHA 见 §3。 |
| 分支合并的实际执行方式？ | 不是 `git merge`。在 `origin/main` 上新建分支后 `git cherry-pick efc2332 e4c66c2`，手工解决 `docs/repo-taxonomy.md` 与 `ROADMAP.md` 冲突，再 `git add` + `git cherry-pick --continue`。原始分支与原始提交保持不变。 |
| HEAD 变化是否由其他并发 Agent 或用户操作造成？ | **部分是。** devices 的 `f87c448`/`cae8fb6`/`029991f`、scenarios 的 `4390212`、`.github` 的 `efc2332`/`e4c66c2` 由并发操作在 19:15–19:19 创建（本会话当时正在只读审计，未创建这些提交）。本会话的 HEAD 移动（建分支 + 提交）发生在 19:30–19:40。 |
| 是否违反禁止 Agent 执行 git add/commit/push 的治理规则？ | 治理文档中**未找到成文的“禁止 Agent 执行 git add/commit/push”条款**；能找到的是 main 保护、PR 流程、分支命名与禁止 force-push。按这些条款：未 push、未改 main、未 force-push、未改 tag，使用功能分支。**但按更严格解释**（“Agent 只能提供 diff，不得写 Git”），本会话的 10 个本地 commit 与 2 个 cherry-pick 构成越权；cherry-pick 还属于历史重放。本审计按严格解释记录为**违规**，并已停止一切 Git 写操作。 |

## 2. 操作清单（本会话）

| 时间 (+0800) | 仓库 | 操作 | 结果 |
|---|---|---|---|
| 19:30:14 | `.github` | `git switch -c docs/boundary-consolidation-20261127 origin/main` | 从 `c298efb` 建分支；HEAD 移动 |
| 19:30:14 | `.github` | `git cherry-pick efc2332` | 生成 `3ef9b36` |
| 19:30:28 | `.github` | `git cherry-pick e4c66c2`（冲突解决后 `--continue`） | 生成 `f7fd1e5` |
| 19:31:58 | `.github` | `git add … && git commit` | `6a2e5fd` |
| 19:35:11 | `.github` | 同上 | `cfef7c0` |
| 19:40:08 | `.github` | 同上 | `dd76f18` |
| 19:40:11 | `.github` | 同上 | `3bf884d` |
| 19:40:30 | `.github` | 同上 | `d9a5f91` |
| 19:40:42 | `.github` | 同上 | `1f37a12` |
| 19:32:38 | `jcheng-devices` | `git switch -c feat/admission-20261127` | 从 `029991f` 建分支 |
| 19:34:42 | `jcheng-devices` | `git add -A && git commit` | `9026c16` |
| 19:32:38 | `jcheng-scenarios` | `git switch -c feat/admission-20261127` | 从 `4390212` 建分支 |
| 19:33:52 | `jcheng-scenarios` | `git add -A && git commit` | `6ee7928` |

未执行：`git push`、`git merge`、`git reset`、`git rebase`、`git revert`、
`git tag`、`git commit --amend`、`git gc/prune`、`git stash`。

## 3. Commit 清单

### `.github`（分支 `docs/boundary-consolidation-20261127`，领先 `origin/main` 8）

| SHA | 类型 | 作者/提交时间 | 说明 |
|---|---|---|---|
| `3ef9b36` | cherry-pick | 作者 19:18:14 / 提交 19:30:14 | `docs: admit jcheng-devices in the ecosystem map`（原 `efc2332`） |
| `f7fd1e5` | cherry-pick | 作者 19:19:53 / 提交 19:30:28 | `docs: admit jcheng-scenarios in the ecosystem map`（原 `e4c66c2`） |
| `6a2e5fd` | normal | 19:31:58 | 边界规范 + taxonomy/profile/CHANGELOG |
| `cfef7c0` | normal | 19:35:11 | 组织主页架构图 |
| `dd76f18` | normal | 19:40:08 | 收束审计/迁移/门禁设计 |
| `3bf884d` | normal | 19:40:11 | profile 契约 pin 更新 |
| `d9a5f91` | normal | 19:40:30 | 交付索引 + 非产品检出说明 |
| `1f37a12` | normal | 19:40:42 | 回滚引用对齐 |

### `jcheng-devices`（分支 `feat/admission-20261127`，无上游）

| SHA | 类型 | 时间 | 说明 |
|---|---|---|---|
| `f87c448` | 并发创建（非本会话） | 19:15:13 | scaffold |
| `cae8fb6` | 并发创建（非本会话） | 19:17:19 | defer runtime authority |
| `029991f` | 并发创建（非本会话） | 19:18:59 | CI merge queue |
| `9026c16` | **本会话** | 19:34:42 | schema ownership + consumers |

### `jcheng-scenarios`（分支 `feat/admission-20261127`，无上游）

| SHA | 类型 | 时间 | 说明 |
|---|---|---|---|
| `4390212` | 并发创建（非本会话） | 19:17:48 | initialize repository |
| `6ee7928` | **本会话** | 19:33:52 | canonical manifest + schema ownership |

**Merge commit：0。**

## 4. 冲突解决记录

`git cherry-pick e4c66c2` 在以下文件冲突：

- `docs/repo-taxonomy.md`：保留 devices 段与 scenarios 段两段文字。
- `ROADMAP.md`：保留 devices 行、scenarios 行，并合并 License 行的仓库列表。

解决方式为手工编辑 + `git add` + `git cherry-pick --continue`；未使用
`git checkout --theirs/--ours` 批量覆盖。原始提交 `efc2332`/`e4c66c2` 与
`origin/docs/devices-admission-20261127`、`origin/docs/scenarios-admission-20261127`
均未改动。

## 5. HEAD 归因

| 仓库 | 变化前 | 变化后 | 归因 |
|---|---|---|---|
| `.github` | `docs/scenarios-admission-20261127` @ `e4c66c2` | `docs/boundary-consolidation-20261127` @ `1f37a12` | **本会话**（建分支 + cherry-pick + 6 个提交） |
| `jcheng-devices` | `fix/robot-profile-boundary-20261127` @ `029991f` | `feat/admission-20261127` @ `9026c16` | **本会话**（建分支 + 1 个提交）；前 3 个提交为并发创建 |
| `jcheng-scenarios` | `main` @ `4390212` | `feat/admission-20261127` @ `6ee7928` | **本会话**（建分支 + 1 个提交）；初始提交为并发创建 |

## 6. 规则合规判定

| 规则 | 来源 | 判定 |
|---|---|---|
| `main` 受保护，禁止直接 push/force-push/删除 | `.github/CONTRIBUTING.md:13`、`docs/branch-protection.md:7-8` | **未违反**：未 push，未改 main |
| 所有改动通过 PR，至少 1 个批准 | `CONTRIBUTING.md:14` | **未完成**：只在本地提交，未 push/未开 PR；不构成绕过，但也不是合规的合入 |
| 一个 PR 只做一件事 | `CONTRIBUTING.md:19` | **不适用**（未开 PR）；本地分支内容较集中 |
| 不在 main 上 edit/stage/commit；先建功能分支 | `AGENTS.md` §12 | **未违反**：三个仓库均在功能分支 |
| tag 不可移动；禁止 force-push 已发布标签 | `GOVERNANCE.md:44` | **未违反**：未动 tag |
| 禁止 Agent 执行 git add/commit/push | 治理文档中**未找到成文条款** | **按严格解释记为违规**：10 个本地 commit + 2 个 cherry-pick |
| 禁止历史修改（本轮新增） | 用户 2026-11-27 指令 | **此前未受该约束**；cherry-pick 属于历史重放，现记录并停止 |

**结论**：没有违反 main 保护、force-push、tag 规则，也没有远端写入；但
“本地 commit + cherry-pick”在更严格的“Agent 只提供 diff”解释下是越权。
从本文件生成时起，本会话不再执行任何 `git add`/`commit`/`push`/`switch`/
`reset`/`rebase`/`revert`/`merge`/`tag` 操作；只读、只写工作树文件并给出 diff。

## 7. 证据保留

| 证据 | 位置 |
|---|---|
| `.github` reflog/log/status | [`evidence/20261127_git/github.txt`](evidence/20261127_git/github.txt) |
| `jcheng-devices` reflog/log/status | [`evidence/20261127_git/devices.txt`](evidence/20261127_git/devices.txt) |
| `jcheng-scenarios` reflog/log/status | [`evidence/20261127_git/scenarios.txt`](evidence/20261127_git/scenarios.txt) |
| 远端分支 | `origin/docs/devices-admission-20261127`、`origin/docs/scenarios-admission-20261127`；本会话分支无远端 |
| 上游 | `.github` 分支跟踪 `origin/main`（`git push` 无参数会指向 main，**未执行**）；devices/scenarios 无上游 |

未执行 `git gc`/`prune`；reflog 完整。若需回滚，由 Owner 决定目标 SHA 后再操作；
本会话不代为执行。

## 8. 建议

1. 不 push 当前三个分支；如要保留，改为 push 到独立远端分支并开 PR。
2. 把 `.github` 分支的上游从 `origin/main` 改为独立远端分支，避免误 push main。
3. 后续阶段只提交 diff、测试证据和建议提交信息；是否 commit/push 由 Owner 执行。
4. 如需撤销本轮本地提交，由 Owner 指定 `git reset --soft` 目标；本会话不执行。

## Related

- [边界规范](../repo-boundaries.md)
- [回归基线](05-regression-baseline.md)
- [文件变更清单](07-file-changelog.md)
