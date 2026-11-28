# 贡献指南

## 范围

本组织维护机器人系统的契约、系统运行时、能力模块与应用。任何改动都应说明：

1. 属于哪个仓库、哪个契约版本、影响哪些模块。
2. 是否改变安全语义、控制权、硬件写入或实机行为。
3. 如何验证；测试与证据在哪里。

## 分支与提交

- `main` 受保护：禁止直接 push、force-push、删除。
- 所有改动通过 PR；至少 1 个批准；安全/契约目录需要 CODEOWNERS 批准。
- 提交信息使用 `type: summary`，例如：
  `feat(interfaces): add ExecuteMotion action`
  `fix(system): latch UNKNOWN on dispatch timeout`
  `docs(governance): clarify hardware authorization`
- 一个 PR 只做一件事；不混合重构与行为变化。
- Agent 在已批准专项内遵循
  [`docs/controlled-git-operations.md`](docs/controlled-git-operations.md)：
  可建分支、add、commit、push 工作分支、开 PR；合并、发布、force-push 与历史
  改写保留给 Board。未经任务授权的仓库不得写入。

## 契约变更

- 任何跨仓库消息、服务、action、HTTP/WS Schema 的改动，先改
  `jcheng-interfaces`，再改消费者。
- 契约变更必须更新 `CHANGELOG.md`、`VERSION` 与 `interface_manifest.json`。
- 不允许在消费者仓库里私自定义“临时消息”绕过契约。

## 文档

- 所有产品仓库遵循
  [`docs/documentation-standard.md`](docs/documentation-standard.md)：`README.md`
  （英文）、`README.zh-CN.md`、`ROADMAP.md`、`CHANGELOG.md`、`ACCEPTANCE.md`。
- 范围、安全语义或验收状态的改动，必须在同一 PR 中同步更新 README 的范围/状态、
  ROADMAP 的里程碑与 ACCEPTANCE 的结论/未验证项。
- 状态只使用标准词汇；合成/Mock 结果不得写成实机验证。

## 安全与实机

- **任何实机运动操作都需要单独、明确的授权。** 不得在 PR、CI 或本地脚本中
  默认执行运动。
- 不得新增绕过 `jcheng_motion` / `jcheng_safety` 的硬件发布路径。
- 不得在仓库中提交令牌、私钥、真实站点 IP、机器人凭据。
- 安全相关改动必须附测试或受监督验收证据。

## 许可证与版权

- 许可证审查完成前，不添加 `LICENSE`，不宣称 MIT。
- 不复制厂商代码、网格、固件或未授权资产。
- 新依赖必须在 PR 中说明用途、版本与许可证；审查通过后合入。
- DCO/CLA 形式待许可证审查时确定。

## 评审清单

- [ ] 变更范围与仓库职责一致。
- [ ] 契约/版本/兼容性已更新。
- [ ] 测试或证据可复现。
- [ ] 没有实机运动默认路径。
- [ ] 没有密钥、站点 IP、厂商资产。
- [ ] 文档为中文（代码标识符、命令保留英文）。
