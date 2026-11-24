# JCHENG-Robotics/.github

组织级治理仓库：组织主页、社区健康文件、issue/PR 模板、可复用 CI 工作流、
复合 Action 骨架，以及生态级 README、ROADMAP、CHANGELOG 与验收报告。
**不包含产品代码、机器人配置或密钥。**

组织主页：[English](profile/README.md) | [简体中文](profile/README.zh-CN.md)
（英文为主文档，中文为对照译文。）

## 当前状态（2026-11-24）

- M1–M5.2 已完成；M6 离线部分已合并（S13 回放 21/21、S17 plan-only），
  实机部分待单独授权。
- 生态仓库：`.github`、`jcheng-interfaces`、`jcheng-system`、
  `jcheng-manipulation`（冻结基线）、`jcheng-mobile`、`jcheng-perception`、
  `jcheng-ops`。`jcheng-mobile-bench` 为明确的台架沙箱，不参与发布。
- 文档标准：所有产品仓库必须有 `README.md`、`README.zh-CN.md`、`ROADMAP.md`、
  `CHANGELOG.md`、`ACCEPTANCE.md`；规范见
  [docs/documentation-standard.md](docs/documentation-standard.md)。
- 本仓库没有 `LICENSE`；策略是审查完成前不添加 `LICENSE`。`jcheng-mobile` 是初始化时
  的例外（MIT），其余仓库不添加、不宣称 MIT。许可证审查见
  [docs/license-review.md](docs/license-review.md)。
- 复用工作流已用于三个仓库的 M1–M6 门禁；新增仓库按
  [docs/repo-taxonomy.md](docs/repo-taxonomy.md) 准入。

## 文档

| 文档 | 内容 |
|---|---|
| [profile/README.md](profile/README.md) | 生态主页（英文主文档） |
| [ROADMAP.md](ROADMAP.md) | 生态里程碑 M0–M8 与当前状态 |
| [CHANGELOG.md](CHANGELOG.md) | 生态级变更记录 |
| [ACCEPTANCE.md](ACCEPTANCE.md) | 生态级验收状态与证据 |
| [docs/documentation-standard.md](docs/documentation-standard.md) | 文档标准与状态词汇 |
| [docs/repo-taxonomy.md](docs/repo-taxonomy.md) | 仓库分层、依赖方向与准入检查 |
| [docs/templates/](docs/templates/) | README / ROADMAP / CHANGELOG / ACCEPTANCE 模板 |

## 目录

```text
profile/README.md                 组织主页（英文）
profile/README.zh-CN.md           组织主页（中文对照）
ROADMAP.md                        生态路线图
CHANGELOG.md                      生态变更日志
ACCEPTANCE.md                     生态验收报告
CONTRIBUTING.md                   贡献流程
SECURITY.md                       漏洞与密钥处理
GOVERNANCE.md                     角色、评审、发布权限
CODEOWNERS.template               各仓库复制后生效
.github/workflows/                可复用工作流 + 组织健康检查
actions/                          复合 Action
ISSUE_TEMPLATE/                   问题/特性/设计/配置模板
docs/                             组织级策略、文档标准与模板
```

## 约束

- 任何实机运动必须有单独、明确的授权；本仓库不包含运动代码。
- 第三方 Action 使用完整 commit SHA；复用工作流用组织标签 `v1`。
- 不提交令牌、私钥、真实站点 IP、机器人凭据。
- 许可证审查完成前，不添加 `LICENSE`，不宣称 MIT。
- 文档语言：英文为主文档；产品仓库的 `README.zh-CN.md` 为中文对照。
