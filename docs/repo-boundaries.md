# 生态职责边界规范

> Status: **v1.0 (2026-11-27)**. 适用于 `JCHENG-Robotics` 全部仓库。
> 本文件定义"谁拥有什么事实、谁拥有什么权限、什么格式可以跨仓"。
> 与 [`repo-taxonomy.md`](repo-taxonomy.md)（分层与依赖方向）和
> [`documentation-standard.md`](documentation-standard.md)（文档与验收词汇）
> 共同构成治理基线；三者冲突时，安全相关以 `jcheng-system/docs/SAFETY.md`
> 与硬件工作流为准，其余以本文件为准。
>
> 本文件只定义边界，不迁移实现。已知偏差登记在附录 B，迁移方案见
> [`boundary-consolidation/04-migration-plan.md`](boundary-consolidation/04-migration-plan.md)。

## 0. 目的

生态的失败模式不是"代码写错"，而是**同一事实有多份真源、同一动作有多条路径、
同一格式有多个定义**。本规范用四条不变量约束仓库之间的职责：

- **一个概念只有一个声明真源（declarative source of truth）。**
- **一个动作只有一个执行点（execution point）。**
- **一个跨仓格式只有一个契约位置（contract location）。**
- **一个结论只有一个测量者（measurement owner）。**

## 1. 术语与消歧

以下词在跨仓文档中必须按本表使用；禁止用同义词互换。

| 术语 | 定义 | 所有者 | 禁止混用 |
|---|---|---|---|
| **scenario（场景）** | 一个可复述的作业情境：环境、语义、任务、约束、评测规格的声明集合 | `jcheng-scenarios` | 不得指代 perception 的 `scene_state` |
| **scene（现场/观测场景）** | 某一时刻感知到的物理现场状态（实例、位姿、关系） | `jcheng-perception` | 不得写成"场景" |
| **task（任务）** | 场景内的目标、前置条件、成功/失败条件；不是执行计划 | `jcheng-scenarios` | 不得写进 recipe 作为成功判据 |
| **recipe（配方）** | 任务的可执行编排：步骤顺序、分支、重试、步骤守卫 | `jcheng-applications` | 步骤守卫 ≠ 任务成功条件 |
| **conformance case（一致性用例）** | 验证系统安全/控制行为的固定用例（租约、限位、停止锁存等） | `jcheng-system` | 不得计入任务成功率 |
| **suite（基准套件）** | 预注册的测量方法：指标种类、聚合、最小样本、阈值 | `jcheng-benchmark` | 不得定义任务成功语义 |
| **evaluation spec（评测规格）** | 生态/业务层面的指标定义与阈值策略 | `jcheng-scenarios` | benchmark 不得自创业务阈值 |
| **device profile** | 设备型号的声明式描述：身份、运动学、声明限位、能力、provenance | `jcheng-devices` | 不是部署配置 |
| **robot profile（部署实例）** | 某台已部署机器人的运行时配置与安全覆盖 | `jcheng-system` | 不是设备目录 |
| **repo manifest** | 仓库的能力/权限声明（`capability.yaml`） | 各仓自己 | 不是设备能力 profile |
| **evidence class** | `L0`–`L5` 验收证据等级 | `documentation-standard.md` | 引用时必须写"证据等级 Lx" |

## 2. 十条总则

1. **声明与执行分离。** 声明设备、场景、配方、评测的仓库不执行、不测量、不访问硬件。
2. **执行点唯一。** 实机运动只由 `jcheng-system` 的 `ExecuteMotion` 产生；其余仓库只产生意图或观测。
3. **跨仓契约唯一。** 只有 `jcheng-interfaces` 能定义跨仓格式；仓库内 Schema 默认只是仓库内文档。
4. **测量者唯一。** 生态级实验评测由 `jcheng-benchmark` 执行并出报告；仓库只声明自己的验收。
5. **声明事实唯一。** 设备事实归 `jcheng-devices`，场景/任务事实归 `jcheng-scenarios`；其他仓库只能引用。
6. **运行时自主。** `jcheng-system` 必须保有独立的部署实例与安全覆盖配置，不得依赖任何声明仓的在线可用性。
7. **副本必须可追溯。** 允许生成式副本、部署快照和测试 Fixture，但必须有 provenance、版本、哈希与一致性校验，且只读、不得手改。
8. **阈值分级。** 安全阈值归 `jcheng-system`；业务验收阈值归 `jcheng-scenarios`；benchmark 不得自创阈值；仓库内部阈值必须标明"内部"。
9. **失败关闭。** 声明之间出现不一致时，构建/发布失败；运行时采用更严格的已部署安全值。
10. **冻结即证据。** 冻结基线以 tag + commit SHA + 证据为准，不以当前 HEAD 为准。

## 3. Repository Ownership Matrix

| 仓库 | 层 | 独占职责 | 明确不负责 | 允许依赖 | 禁止行为 |
|---|---|---|---|---|---|
| `.github` | L0 | 治理、模板、复用 CI、生态级文档、注册表 | 产品代码、设备/场景数据、密钥 | 无（CI 可读所有仓） | 承载运行时逻辑或机器人配置 |
| `jcheng-interfaces` | L1 | 跨仓 IDL、HTTP/WS、公共 Schema、错误码、契约哈希 | 节点、业务逻辑、设备实例、场景实例 | 无 | 打开设备、定义业务判据、保存设备/场景数据 |
| `jcheng-system` | L2 | 安全状态机、租约、仲裁、执行、硬件桥、网关、部署实例、安全覆盖 | 业务任务语义、设备目录、场景目录、生态评测 | L1 | 运行时依赖 L3/L4；从声明仓在线读取安全配置 |
| `jcheng-manipulation` | L3 冻结 | `v1.0.0` 实验基线、历史证据、参考实现 | 新功能、新契约、运行时依赖 | 无（被引用方） | 改 tag/历史；被新系统运行时依赖 |
| `jcheng-mobile` | L3 | 激光里程计、SLAM、地图、Nav2、底盘意图 | 设备驱动、电机桥、伪里程计、任务语义 | L1 + L2 客户端 | 打开串口/设备、发布厂商话题、伪造里程计 |
| `jcheng-perception` | L3 | 采集、检测、深度/TF、融合、场景观测、建议位姿 | 运动、任务阶段判定、任务成功判定、训练 | L1 + L2 客户端 | 发布运动命令、打开相机设备、伪造深度/TF |
| `jcheng-learning` | L3 | 数据集契约、校验、训练、离线评测、策略产物 | 运行时节点、设备、直接运动、生态评测 | L1 | 训练时访问设备、把模型指标当生态结论 |
| `jcheng-teleop` | L3 | 操作员输入调理、`TeleopCommand` 意图、采集/回放、监督授权 | 输入设备驱动、租约签发、运动执行、数据集契约 | L1 + L2 客户端 | 打开设备、发布厂商话题、直接运动、自建租约 |
| `jcheng-devices` | L3 DEV | 设备身份、运动学、声明限位、能力、provenance、离线校验 | 运行时 I/O、部署配置、安全覆盖、运动 | 无（离线） | 打开设备、加入 DDS、发布话题、替换部署实例 |
| `jcheng-simulation` | SIM | 虚拟 plant、world、mock、域 43、truth 标签 | 任务成功判定、设备目录、真实运动 | L1（只读） | 加入域 0/41/42、向真实系统发运动、声称硬件验证 |
| `jcheng-scenarios` | SCEN | 场景注册表、环境/语义/任务/约束/评测声明、场景校验 | 执行、编排、测量、仿真、设备目录 | 无（离线） | 加入 DDS、启动节点、执行任务、发布意图、虚构结果 |
| `jcheng-studio` | L4 | 观察、诊断、会话/轨迹/实验记录、意图转发、停止代理 | DDS、设备访问、租约持有、运动分发、设备/感知/统计算法 | L2 HTTP/WS + L1 | 自建 LeaseManager、调用 `/motion/dispatch`、执行运动 |
| `jcheng-applications` | L4 | 配方校验、确定性规划、失败关闭的意图序列、运行记录 | 任务成功语义、测量、设备描述、运动执行 | L1 + L2 HTTP/WS | 加入 DDS、打开设备、直接执行运动、内嵌成功判据 |
| `jcheng-benchmark` | BENCH | suite 执行、聚合、阈值评估、provenance 报告 | 任务语义、业务阈值来源、数据生成、实机采集 | 只读数据集/规格文件 | 采集/回填数据、自创阈值、把 mock 当硬件、ssh 实机采集 |
| `jcheng-ops` | OPS | 部署、探活、看门狗、systemd 自愈、运维记录 | 业务逻辑、场景判定、运动、租约、设备 | HTTP 健康端点 + systemd | 加入 DDS、发送运动、访问设备、读取业务数据 |
| `jcheng-research` | RESEARCH | 文献、根因、实验设计、报告与决策 | 运行时代码、硬件、运动、第二套 plant | 无（离线） | 被运行时代码导入、声称产品验收 |
| `jcheng-mobile-bench` | BENCH 沙箱 | 台架材料沙箱 | 发布、被依赖、版本化 | 无 | 被能力仓或运行时依赖、部署到机器人 |

## 4. Source of Truth Matrix（SOM）

| 概念 | 唯一声明真源 | 允许的副本 | 一致性校验 |
|---|---|---|---|
| 场景/任务/成功失败条件 | `jcheng-scenarios/scenarios/<id>/` | simulation 的 world 引用、applications 的 `scenario_id` 引用、benchmark 的 `scenario_id` 引用 | `scenario_id@version` + 注册表校验 |
| 业务评测指标与阈值策略 | `jcheng-scenarios/.../evaluation.yaml` | benchmark suite 的 `evaluation_id` 引用 | 指标 ID/单位/方向一致；阈值为空即 inconclusive |
| 设备身份/运动学/声明限位/能力 | `jcheng-devices/registry/` | system 的部署实例（生成式快照）、simulation 的 plant 引用、learning/studio 的只读引用 | `device_id@profile_version#sha256`；重叠字段不一致即阻断发布 |
| 某台机器人的部署配置与安全覆盖 | `jcheng-system/configs/robots/<robot>/` | 无（运行时只读本地） | `robot-profile.v1` schema + profile SHA-256 |
| 配方/步骤编排/重试 | `jcheng-applications/recipes/` | 测试 Fixture | recipe schema + contract hash |
| 现场观测/scene_state | `jcheng-perception` 的 ROS 消息/输出 | 离线数据集（带 provenance） | 时间戳/TF/来源标签 |
| 底盘里程计/地图/路径 | `jcheng-mobile` | 无 | 来源必须为真实 scan matching |
| 数据集契约/训练/策略 | `jcheng-learning/docs/m1/` | teleop 的 capture 适配器、perception 的导出器 | `dataset_id` + `SHA256SUMS` |
| 操作员意图/遥操作捕获 | `jcheng-teleop` | studio 的只读状态 | `TeleopCommand` 契约 + capture manifest |
| 虚拟 plant/world/truth | `jcheng-simulation` | research 的实验副本（必须标注并退役） | 域 43 + `/sim/truth/source=simulated` |
| 实机运动/租约/仲裁/停止 | `jcheng-system` | 无 | `ExecuteMotion` + 租约 + 停止锁存 |
| 跨仓通信格式/错误码 | `jcheng-interfaces` | 无（只允许生成绑定） | contract hash + manifest |
| 生态级测量结果 | `jcheng-benchmark` | 无 | suite + dataset 哈希 + provenance |
| 部署单元/探活/自愈 | `jcheng-ops` | 无 | systemd unit + 健康端点 |
| 冻结基线 | `jcheng-manipulation@v1.0.0`（`b3411e4`） | 无 | tag + commit SHA + 证据路径 |

**副本规则。** 生成式副本、部署快照和 Fixture 必须同时满足：
① 标注来源 `repo@version#sha256`；② 只读；③ 有生成/校验脚本；④ 校验失败即构建失败；
⑤ 不得成为第二个手写真源。system 的 `robot-profile.v1` 是"部署实例"，不是设备目录：
它可以收紧声明限位，但不得放宽或静默改写设备身份。

## 5. Runtime Authority Matrix（RAM）

| 动作/资源 | 唯一权威 | 输入 | 门禁 | 备注 |
|---|---|---|---|---|
| 机械臂/夹爪运动 | `jcheng-system` `ExecuteMotion` | applications/teleop 的意图 | 租约 + deadman + 限位 + 停止锁存 | 唯一实机执行点 |
| 底盘运动 | `jcheng-system`（目标态） | mobile 的 `/cmd_vel` 意图 | 同上 | 现状：`/cmd_vel` 不得接到电机驱动 |
| 停止 | `jcheng-system` 停止锁存 | 任何客户端 | 立即锁存 | studio 仅可代理 `POST /v1/motion/stop` |
| 租约签发/续期/撤销 | `jcheng-system` | 操作员/客户端请求 | 单一持有者 + 租约争用规则 | 其他仓不得自建租约 |
| 执行限位/安全覆盖 | `jcheng-system` | 部署实例 | 更严格者优先 | 不依赖 devices 在线 |
| 安全状态 | `jcheng-system` | 总线读数/状态机 | 失败关闭 | `/joint_states` 不是测量值 |
| 遥操作意图 | `jcheng-teleop` | 输入调理 | 限速/范围/来源 | 只提案，不执行 |
| 任务意图 | `jcheng-applications` | 配方 → 计划 | 确定性 + 失败关闭 | 只提交，不执行 |
| 感知建议 | `jcheng-perception` | 相机/深度/TF | 时间匹配失败即丢弃 | advisory only |
| 虚拟运动 | `jcheng-simulation` | 域 43 | 域隔离 | 永不驱动真实系统 |
| 部署/重启 | `jcheng-ops` | HTTP 健康端点 | 连续失败 + 运动态检查 | 无业务逻辑 |
| 设备描述 | `jcheng-devices` | 注册表 | 离线校验 | 无运行时权限 |
| 场景声明 | `jcheng-scenarios` | 注册表 | 离线校验 | 无运行时权限 |

## 6. Schema Ownership Matrix（SCH）

**契约 Schema（只允许在 `jcheng-interfaces`）**

| Schema | 消费者 | 变更方式 |
|---|---|---|
| `capability-manifest.v1` | 全部产品仓 | interfaces proposal + tag |
| `robot-profile.v1` | system（部署实例） | interfaces proposal + tag |
| `safety-profile.v1` | system | interfaces proposal + tag |
| `lockfile.v1` / `evidence-record.v1` / `acceptance-report.v1` | system / 各仓 | interfaces proposal + tag |
| `messages.v1`、`openapi/jcheng-gateway.v1`、`ws/jcheng-ws.v1`、错误码表 | 运行时仓 | interfaces proposal + tag |

**仓库内 Schema（repo-local，必须登记）**

| Schema | 所在仓 | 当前消费者 | 目标状态 | 提升触发条件 |
|---|---|---|---|---|
| scenario/task/environment/semantics/capability-requirements/operational-constraints/evaluation/registry（8 个） | scenarios | 仅本仓 | repo-local v1 | applications/simulation/benchmark/perception 任一实际解析即触发 |
| device-profile.v1 / capability-profile.v1 | devices | 仅本仓 | repo-local v1 | simulation/learning/studio 任一实际解析即触发 |
| ore_dataset / ore_dual_view_dataset / ore_evaluation / scene_association / scene_state v1/v2 | perception | 仅本仓与证据 | repo-local v1 | 与其他仓交换实例即触发 |
| dataset-quality-report.v1 | learning | 仅本仓 | repo-local v1 | benchmark 或其他仓消费即触发 |
| teleop capture/dataset/status/export（代码内 13 个） | teleop | studio 读 status | repo-local v1 | studio 或其他仓解析即触发 |
| suite/sample/report v1 | benchmark | 仅本仓 | repo-local v1 | 其他仓消费报告格式即触发 |

规则：

1. `contract` 类只能位于 `jcheng-interfaces`；其余一律标 `repo-local`。
2. 每个仓必须维护 `SCHEMA_OWNERSHIP.md`（或等价表），列出 Schema、版本、owner、消费者、
   状态（contract / repo-local）、提升触发条件。
3. **第二个消费者出现即触发 proposal**，不得先消费后补票。
4. 生成绑定/模型代码可以由 interfaces 生成，但不得在消费仓手改。

## 7. Evaluation Ownership Matrix（EOM）

| 产物 | 所有者 | 可以做 | 不可以做 |
|---|---|---|---|
| 任务成功/失败语义 | `jcheng-scenarios` | 声明条件、指标定义、业务阈值策略 | 执行测量、写结果 |
| 安全/控制一致性用例 | `jcheng-system` | 定义并运行 conformance cases | 把用例计入任务成功率 |
| 生态级测量与报告 | `jcheng-benchmark` | 执行 suite、聚合、阈值评估、provenance 报告 | 定义任务成功、自创阈值、生成/回填数据 |
| 仓库自身验收 | 各仓 `ACCEPTANCE.md` | 声明本仓 L0–L5 结果与限制 | 代替 benchmark 的生态结论 |
| 模型开发指标 | perception / learning | mask AP、训练/验证指标、内部消融 | 作为生态评测或硬件验证结论 |
| 证据等级 | `documentation-standard.md` | 定义 L0–L5 | 被重定义为层号或 suite 等级 |

**阈值规则。** 安全阈值只属于 system；业务阈值只属于 scenarios；benchmark 的 suite
阈值为空时只产生 `inconclusive` 报告；仓库内部阈值必须在报告中标注 `internal`。

## 8. 跨仓契约变更流程

1. **提案**：在 `jcheng-interfaces/docs/proposals/` 新增文档，写明动机、字段、兼容性、消费者。
2. **评审**：至少一名 reviewer；涉及运动/安全须引用 `jcheng-system/docs/SAFETY.md`。
3. **发布**：interfaces 更新 `VERSION`、`CHANGELOG.md`、`interface_manifest.json` 和
   `contract_hash`，打 SemVer tag（`vX.Y.Z`）。
4. **消费**：各仓更新 `capability.yaml` 的 `interfaces` 范围与 `contract_hash`、
   生态锁 `locks/ecosystem.lock.yaml`、以及握手测试。
5. **弃用**：旧字段至少保留一个 minor 版本，标注 deprecated；移除必须 major。
6. **禁止**：任何仓 pin 分支或 HEAD；任何仓在消费仓内复制契约并"本地扩展"。

repo-local → contract 的提升走同一流程；提升前，其他仓不得解析该文件。

## 9. 仓库准入与退出机制

**状态机**：`Proposed → Admitted (Experimental) → Deployed / Frozen → Deprecated → Archived`。

**准入检查（全部满足）**

- [ ] 职责不与现有仓重叠，且在 `repo-taxonomy.md` 与 `repo-boundaries.md` 登记。
- [ ] 默认 `hardware_access: none`；无 DDS 域、设备 I/O、运动执行。
- [ ] `capability.yaml` 符合当前 manifest 规范；契约 pin 与生态锁一致。
- [ ] 完整四件套文档 + `LICENSE-REVIEW.md` + `VERSION`。
- [ ] CI 跑 repo gate；gate 含 no-hardware、链接、文档结构检查。
- [ ] `SCHEMA_OWNERSHIP.md` 列出全部 Schema、owner、消费者、状态。
- [ ] 失败语义明确；契约握手测试存在。
- [ ] 涉及运动的仓：有受监督实机证据（L5）或明确声明 `Unverified` 且禁止实机运行。

**退出/归档**

- 先在注册表标 `Deprecated`，给出消费者迁移期（≥1 个 minor）。
- 迁移完成、证据归档、CI 停止后标 `Archived`；不得静默删除仓库或 tag。
- 归档仓不得再被运行时依赖；其证据仍可被引用。

## 10. 冻结基线管理规则

- 冻结引用必须写成 `repo@tag` + commit SHA + 证据路径，例如
  `jcheng-manipulation@v1.0.0`（`b3411e43ad31c09f396cdd2db0fdfda8f09853dd`）。
- **当前 HEAD 不是冻结基线。** 冻结后新增的提交不改变基线声明。
- tag 不可移动、不可重写；需要修复时在新仓或新分支进行，旧 tag 保持原样。
- 新仓不得运行时依赖冻结仓；只允许引用证据、文档和只读代码片段。
- 冻结仓的 `ACCEPTANCE.md` 是历史声明，不得追加新的"已验证"结论。

## 11. 边界门禁清单（report-only 优先）

`check_boundaries` 第一版只报告、不阻断（exit 0），连续两个发布周期零误报后再转为 required。

| ID | 检查 | 数据来源 | 初始严重度 |
|---|---|---|---|
| B1 | 依赖方向：L4→L2 API、L3→L1+L2 客户端、L2→L1、OPS→HTTP | import 图 + 仓内配置 | High |
| B2 | 硬件访问：声明 `none` 的仓不得 import serial/cv2/rclpy 设备路径 | capability.yaml + 静态 grep | Critical |
| B3 | 运行时面：manifest 的 domain/topic 必须与代码一致 | capability.yaml + publisher 清单 | High |
| B4 | 运动权限：只有 system 可发布执行命令；intent 发布者必须声明 | topic/publisher 清单 | Critical |
| B5 | manifest 合规：schema_version、class、contract pin | capability.yaml | High |
| B6 | 契约版本：各仓 pin 与 `ecosystem.lock.yaml` 一致 | lock + manifests | High |
| B7 | Schema 所有权：每个 repo-local Schema 都在 OWNERSHIP 中登记 | schema 文件 + 表 | Medium |
| B8 | 事实源重复：已知设备字段/场景 ID 在多仓出现且不符 | 注册表 + 指纹 | High |
| B9 | 评测声明：benchmark 报告之外的仓不得声明生态级结果 | ACCEPTANCE + 报告 | Medium |
| B10 | 冻结引用：必须用 tag+SHA，禁止用 HEAD/分支 | 文档链接扫描 | Medium |
| B11 | 资产 provenance：模型/数据/资产有来源、版本、哈希 | assets/ + 数据集清单 | Medium |
| B12 | 文档与状态词汇：四件套、标准词汇、链接可解析 | 文件系统 + 链接检查 | Low |

输出：`boundary-report.json`（机器可读）+ `boundary-report.md`（人读）；每项给出
仓库、证据路径、判定（pass/fail/waived）、豁免理由。第一版不修改任何仓库。

## 12. 例外与豁免

以下情形允许存在副本或例外，但必须登记：

- **生成式副本**：由脚本从真源生成，带 `repo@version#sha256`，只读。
- **部署快照**：为离线可用而固定，例如 system 的 `robot-profile.v1`；必须带哈希并在 CI 比对。
- **测试 Fixture**：只用于测试，不得被生产代码导入；带来源与哈希。
- **历史证据**：冻结仓与 `evidence/` 下的历史文件；只读，不参与新结论。

豁免必须写入本文件附录 B 或对应仓的 `ACCEPTANCE.md`，并给出到期/复核条件。

## 附录 A：决策记录

| ID | 决策 | 日期 |
|---|---|---|
| D-01 | **Devices** 是设备声明事实的唯一权威来源。 | 2026-11-27 |
| D-02 | **Scenarios** 是领域场景、业务任务及场景验收规范的唯一权威来源。 | 2026-11-27 |
| D-03 | **Interfaces** 管理跨仓公共契约，不强制收容所有 repo-local Schema。 | 2026-11-27 |
| D-04 | **System** 独占实机运动执行授权、安全仲裁及硬件输出权限。 | 2026-11-27 |
| D-05 | **Applications** 负责任务编排。 | 2026-11-27 |
| D-06 | **Benchmark** 负责生态级实验评测；各仓允许保留内部专项测试与开发评测。 | 2026-11-27 |
| D-07 | **Manipulation** 冻结范围以指定 tag、commit SHA 和对应证据为准，而非当前 HEAD。 | 2026-11-27 |
| D-08 | 允许具有明确 provenance、版本、哈希和一致性校验的生成式副本、部署快照及测试 Fixture。 | 2026-11-27 |
| D-09 | **System** 必须保留独立安全覆盖配置，不得依赖 Devices 的在线可用性。 | 2026-11-27 |
| D-10 | **Scenarios** 可以声明业务验收阈值，但不得覆盖 System 的安全阈值或虚构实验结果。 | 2026-11-27 |

## 附录 B：已知偏差登记（迁移前）

| 编号 | 偏差 | 证据 | 目标 | 迁移项 |
|---|---|---|---|---|
| DEV-01 | 设备事实存在多份手写副本 | system `configs/robots/*/profile.yaml`、devices registry、simulation `robot.yaml`、learning `profiles/`、studio `configs/`、interfaces fixture | devices 声明 + system 部署实例 + 引用 | MIG-01 |
| DEV-02 | 场景/任务语义分散 | system `scenarios.py` S1–S17、benchmark `suites/`、simulation `worlds/`、applications recipe 判据、perception `Phase` | scenarios 声明 + 各仓引用 | MIG-02 |
| DEV-03 | 跨仓 Schema 在 interfaces 之外 | scenarios 8、devices 2、perception 6、learning 1、teleop 13（代码内） | 登记 repo-local；第二次消费前提案 | MIG-03 |
| DEV-04 | 契约 pin 不一致 | 0.1.0/`0b8d72`、0.2.0/`afca22`、interfaces 0.3.0 | 统一到已发布契约 | MIG-04 |
| DEV-05 | manifest 方言不一致 | 7 仓用 `capability-manifest.v1`，perception/ops/benchmark/scenarios 用旧格式 | 统一 manifest 规范 | MIG-05 |
| DEV-06 | Studio 本地运动路径 | `backend/app/service.py:111`、`api/routes.py:384`、`adapters/hardware.py:1270` | 移除/禁用 legacy，只走 gateway v1 | MIG-06 |
| DEV-07 | Mobile `/cmd_vel` 无 system intake | `capability.yaml`、`launch/mobile_nav.launch.py` | system intake 消费后再到硬件 | MIG-07 |
| DEV-08 | perception 任务状态机 | `jcheng_perception_core/types.py:27-34` | 迁 applications 或降为 advisory hint | MIG-08 |
| DEV-09 | research 第二套 plant | `experiments/20261126-piper-x-gazebo-plant/` | 移交 simulation 或标参考并退役 | MIG-09 |
| DEV-10 | benchmark `tools/live` 实机采集 | `tools/live/`（ssh） | 迁 ops/studio 或隔离 | MIG-10 |

## Related

- [仓库分类与依赖方向](repo-taxonomy.md)
- [文档与验收标准](documentation-standard.md)
- [迁移方案](boundary-consolidation/04-migration-plan.md)
- [执行权限审计](boundary-consolidation/02-runtime-authority-audit.md)
- [边界门禁设计](boundary-consolidation/06-check-boundaries-design.md)
