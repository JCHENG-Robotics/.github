# JCHENG-Robotics/.github

**简体中文** | [English](README.md)

组织级治理仓库：组织主页、社区健康文件、issue/PR 模板、可复用 CI 工作流、
复合 Action 骨架，以及生态级 README、ROADMAP、CHANGELOG 与验收报告。
**不包含产品代码、机器人配置或密钥。**

组织主页：[profile/README.md](profile/README.md) | [profile/README.zh-CN.md](profile/README.zh-CN.md)

## Baseline 1（2026-11-28）

生态已完成第一个**离线集成基线**：

- **DEVELOPMENT READY：YES**
- **OFFLINE INTEGRATION READY：YES**
- **BASELINE 1 COMPLETE：技术条件已满足；最终记录 #40 待 Board 批准/合并**
- **DEPLOYMENT READY：NO**

| Baseline 1 结果 | 证据 |
|---|---|
| 离线工件契约 1.0.0 **Accepted**，vocabulary `contracted` | interfaces #20/#21（`426f371`）；scenarios #5（`1c21885`） |
| 真实 CLI cell 集成 | arm + gripper + camera；`matched_with_unverified` |
| 8 场景合成 Mock 矿石分拣 | 8/8 分类正确；仅 `normal` 成功；benchmark INCONCLUSIVE / test PASS/FAIL |
| 三臂登记 | ArmPi 5-DOF reference、PiPER X 6-DOF candidate、ROKAE **AR5L/AR5R** 7-DOF planned 双臂 |
| 最终 main 回归 | interfaces 22、devices 123、scenarios 116、applications 218+5 等全部通过 |
| 开发交接 | Quick Start、Developer Guide、统一验收入口、首个人工任务 |
| 部署 | **NOT READY**，无真实运动/硬件输出授权 |

详细记录见 [`docs/baseline1/ratification/`](docs/baseline1/ratification/README.md)。
本轮不创建 Release/Tag。

## 上一状态（2026-11-26）

- M1–M5.2 已完成；M6 S13 回放 21/21 与 S17 实机 MoveIt plan-only 已通过；
  S14 底盘与完整 G8 复跑待做。
- 生态仓库：`.github`、`jcheng-interfaces`、`jcheng-system`、
  `jcheng-manipulation`（冻结基线）、`jcheng-mobile`、`jcheng-perception`、
  `jcheng-learning`、`jcheng-simulation`、`jcheng-studio`、
  `jcheng-applications` 与 `jcheng-ops`。`jcheng-research` 是公开调研工作区；
  `jcheng-mobile-bench` 是明确的台架沙箱，不参与发布。
- `jcheng-learning`（v0.1.0）是离线的数据集/训练/策略产物边界：没有运行时节点、
  策略或硬件访问。
- `jcheng-simulation`（v0.1.0）是域 43 上的离线多机器人被控对象引擎：确定性 mock
  已验证，Gazebo Harmonic 部分验证；不访问硬件，也不向真实系统发送运动。
- `jcheng-benchmark` 是 BENCH 层的离线只读基准工具（v0.1.0，实验性），在运行时依赖
  图之外，尚无可记录数据或硬件结果。
- `jcheng-studio`（操作台，v0.7.0）与 `jcheng-applications`（任务编排，v0.1.0）是
  L4 仓库。两者只经网关 HTTP/WS 边界访问机器人；不加入 DDS 域、不打开设备、不执行
  运动。Studio 已迁入控制台、只读 REST/WS、会话存储与回放；Applications 有离线
  配方/规划/运行器核心与只读传输。`jcheng-research`（公开，v0.1.0）只产出报告与
  决策，不在运行时图中。
- 文档标准：所有产品仓库必须有 `README.md`、`README.zh-CN.md`、`ROADMAP.md`、
  `CHANGELOG.md`、`ACCEPTANCE.md`；语言切换固定放在 H1 之后第一行。规范见
  [docs/documentation-standard.md](docs/documentation-standard.md)。
- 本仓库没有 `LICENSE`；策略是审查完成前不添加 `LICENSE`。`jcheng-mobile` 是初始化时
  的例外（MIT），保留待审查，其余仓库不添加、不宣称 MIT。许可证审查见
  [docs/license-review.md](docs/license-review.md)。
- 复用工作流已用于三个仓库的 M1–M6 门禁；新增仓库按
  [docs/repo-taxonomy.md](docs/repo-taxonomy.md) 准入。

## 文档

| 文档 | 内容 |
|---|---|
| [profile/README.md](profile/README.md) | 生态主页（英文主文档） |
| [docs/baseline1/ratification/README.md](docs/baseline1/ratification/README.md) | Baseline 1 验收、Manifest、QA 与冻结记录 |
| [ROADMAP.md](ROADMAP.md) | 生态里程碑 M0–M8、Baseline 1 与当前状态 |
| [CHANGELOG.md](CHANGELOG.md) | 生态级变更记录 |
| [ACCEPTANCE.md](ACCEPTANCE.md) | 生态级验收状态与证据 |
| [acceptance/ecosystem-2026-11-26.json](acceptance/ecosystem-2026-11-26.json) | 当前机器可读验收（schema v1；reviewer pending） |
| [acceptance/ecosystem-2026-11-25.json](acceptance/ecosystem-2026-11-25.json) | 上一版机器可读验收（历史） |
| [acceptance/ecosystem-2026-11-24.json](acceptance/ecosystem-2026-11-24.json) | 更早的机器可读验收（历史） |
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
