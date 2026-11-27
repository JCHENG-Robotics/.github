# Migration Plan — 边界收束（仅设计，不实施）

> Status: **v1.0 (2026-11-27)**. 本文件只设计迁移，不修改任何现有仓库实现。
> 每项迁移须单独提交方案并获批准后执行；本文件不是执行授权。
> 约束：不直接删除设备配置副本；不机械迁移所有 Schema；不未经语义分析迁移
> Perception 状态机；不未经兼容性验证统一契约版本。

## 总览

| ID | 主题 | 风险 | 前置 | 建议批次 |
|---|---|---|---|---|
| MIG-01 | 设备事实唯一化 | High | devices 准入 | 1 |
| MIG-02 | 场景/任务语义收束 | High | scenarios 准入 | 1 |
| MIG-03 | Schema 归属登记与提升 | Medium | MIG-01/02 | 2 |
| MIG-04 | 契约版本统一 | High | interfaces 0.3.0 发布 | 2 |
| MIG-05 | Manifest 方言统一 | Medium | MIG-04 | 2 |
| MIG-06 | Studio 执行旁路移除 | Critical | 执行权限审计批准 | 0（安全前置） |
| MIG-07 | Mobile `/cmd_vel` 收口 | Critical | 执行权限审计批准 | 0（安全前置） |
| MIG-08 | Perception 任务状态机 | High | 语义评审 | 3 |
| MIG-09 | Research plant 移交 | Low | 无 | 3 |
| MIG-10 | Benchmark 实机采集隔离 | Medium | 无 | 3 |

---

## MIG-01 设备事实唯一化

| 字段 | 内容 |
|---|---|
| 当前证据 | devices `registry/devices/*.yaml`；system `configs/robots/*/profile.yaml`；interfaces `schemas/robot-profile.v1` + `tests/fixtures/robot_profile.yaml`；simulation `robots/*/robot.yaml`；learning `profiles/armpi_ultra.yaml`；studio `configs/joint_mapping.yaml`、`takeover.yaml`；applications `model.py:464-465`；teleop `examples/.../profile.yaml` |
| 语义与职责 | devices 拥有设备**声明事实**（身份、运动学、声明限位、能力、provenance）；system 拥有**部署实例 + 安全覆盖**（可收紧、不可放宽）；simulation 拥有 plant 参数；learning/studio/apps/teleop 只读引用 |
| 现有消费者 | system 运行时（profile）、simulation（plant）、learning（适配）、studio（旧运动路径）、applications（gripper 范围） |
| 目标归属 | devices 为声明源；system 为部署快照（生成或比对）；其余引用 |
| 迁移方式 | ① 给 devices profile 增加稳定 `profile_version` 与字段级 provenance；② system 增加生成脚本：`device_profile + safety_overlay → robot-profile.v1`，写入 `source_device: id@version#sha256`；③ CI 比对重叠字段，不一致即失败；④ 逐仓替换手写副本为引用/生成；⑤ 最后才删除副本（保留一个 minor 的兼容期） |
| 兼容性影响 | `robot-profile.v1` 字段不变；新增 `source_device` 为可选；旧 profile 仍可读。system 部署不依赖 devices 在线 |
| 回归测试 | devices gate；system `test_lockfile`/`test_readonly`/profile 校验；simulation robot.yaml 校验；逐字段 diff（限位/gripper/workspace） |
| 回滚 | 保留旧 profile；生成脚本产出新文件，失败即回退旧文件；不改 tag |
| 风险 | **High**：数值不一致会导致实机限位变化；任何放宽必须人工评审 |

## MIG-02 场景/任务语义收束

| 字段 | 内容 |
|---|---|
| 当前证据 | scenarios 8 Schema + `ore_sorting`；system `scenarios.py` S1–S17；benchmark `suites/`；simulation `worlds/*.sdf`（table/target_cube）；applications recipe `at_least_rad`；perception `types.py:27-34` Phase；learning `docs/m2/suites` |
| 语义与职责 | scenarios 拥有任务、成功/失败条件、指标定义、业务阈值策略；system 的 S1–S17 是**一致性用例**；benchmark 只执行评测；simulation 只消费环境；applications 只保留步骤守卫；perception 只输出观测 |
| 现有消费者 | applications（未来）、simulation（未来）、benchmark（未来）、devices（能力匹配，未来） |
| 目标归属 | scenarios 声明；其余引用 `scenario_id@version` / `task_id@version` / `evaluation_id@version` |
| 迁移方式 | ① 把 S1–S17 重命名为 conformance cases（文档与报告字段，不改行为）；② applications recipe 增加可选 `scenario_id`/`task_id`，守卫改名 `step_guard`；③ benchmark suite 增加 `evaluation_ref`，阈值为空即 inconclusive；④ simulation 增加 environment 适配器（只读）；⑤ perception Phase 降级为 advisory hint 或迁出（见 MIG-08） |
| 兼容性影响 | recipe/suite 为新增可选字段，旧文件继续有效；报告 schema 需新增字段（走 interfaces 或 repo-local v2） |
| 回归测试 | scenarios gate；applications recipe 校验；benchmark suite 校验；system S1–S17 报告仍全绿；simulation 域 43 测试 |
| 回滚 | 新增字段均可忽略；保留旧 suite 格式；不删除 S1–S17 |
| 风险 | **High**：把"任务成功"错接到一致性用例会污染统计；需人工语义评审 |

## MIG-03 Schema 归属登记与提升

| 字段 | 内容 |
|---|---|
| 当前证据 | 17 个仓内 JSON Schema（scenarios 8、perception 6、devices 2、learning 1）+ teleop 13 个代码内 Schema；interfaces 7 个公共 Schema |
| 语义与职责 | interfaces 只收跨仓契约；repo-local 允许，但必须登记 owner/consumers/status |
| 现有消费者 | 多数仅本仓；studio 读 teleop status；未来 apps/sim/bench 读 scenarios；sim/learning/studio 可能读 devices |
| 目标归属 | 保持 repo-local；**只有出现第二个消费者才提案上移**，不批量搬迁 |
| 迁移方式 | ① 两新仓已建 `SCHEMA_OWNERSHIP.md`；② 其余仓按同一模板补登记（单独 PR）；③ `check_boundaries` B7 报告未登记项；④ 逐项评审提升，不机械迁移 |
| 兼容性影响 | 纯文档/门禁，无运行时变化 |
| 回归测试 | 各仓 gate；B7 report-only |
| 回滚 | 删除新增登记文件即可；不改 Schema |
| 风险 | **Medium**：错误提升会把内部格式冻结成契约 |

## MIG-04 契约版本统一

| 字段 | 内容 |
|---|---|
| 当前证据 | interfaces 0.2.0/`afca22…` 已签名，0.3.0/`8120c5…` 未发布；6 仓仍 pin 0.1.0/`0b8d72…`；生态锁 modules 写 `>=0.2,<0.3`；部署证据为 0.1.0/`0b8d72…` |
| 语义与职责 | interfaces 发布契约；system 是运行时消费者；L4 客户端与 teleop 需握手；离线仓只声明 |
| 现有消费者 | system、applications、studio、teleop、devices、scenarios；mobile/simulation/learning 声明性 pin |
| 目标归属 | 统一到 interfaces 已发布的 tag；system 保持兼容窗口 |
| 迁移方式 | ① interfaces 收口 0.3.0（pyproject/README/manifest），打 tag；② system 升级并补 `system_api` 版本源；③ applications/studio/teleop 握手更新；④ 离线仓更新声明；⑤ 最后更新锁。禁止先改锁 |
| 兼容性影响 | 0.2.0→0.3.0 为 minor（新增 class），无 IDL 破坏；但握手测试会拒绝旧 hash |
| 回归测试 | interfaces manifest check + schema check；system contract/lease/stop 测试；L4 握手测试；部署树升级后再跑 L5（需另行授权） |
| 回滚 | 保留 0.2.0 tag 与旧 manifest；消费仓可回退 pin；不改已签名 tag |
| 风险 | **High**：部署树仍是 0.1.0；未对齐前不得声称实机门禁完整 |

## MIG-05 Manifest 方言统一

| 字段 | 内容 |
|---|---|
| 当前证据 | 7 仓 v1；perception/ops/benchmark legacy；system/interfaces/research/scenarios(已改 v1) 无或不同；两新仓已统一 v1 |
| 语义与职责 | manifest 是准入声明，不是设备能力 profile；离线仓用 `class: offline` + 空 runtime |
| 现有消费者 | 组织 admission 检查、CI、锁 |
| 目标归属 | 全部产品仓使用 `capability-manifest.v1`；离线语义用 vacuous 字段并在注释/文档说明 |
| 迁移方式 | ① 先补 system/interfaces 的 manifest（暂无）；② perception/ops/benchmark 逐仓转 v1（单独 PR）；③ 保留 `runtime_roles` 等信息到 README/ARCHITECTURE；④ CI 校验 schema |
| 兼容性影响 | 纯声明变化；不改变运行时 |
| 回归测试 | 各仓 gate；B5 report-only |
| 回滚 | 保留旧 manifest 副本一个 minor |
| 风险 | **Medium**：`requires_lease: true` 等 vacuous 字段易被误读为真实权限 |

## MIG-06 Studio 执行旁路移除

| 字段 | 内容 |
|---|---|
| 当前证据 | `backend/app/service.py:111` 自建 `LeaseManager`；`api/routes.py:384` `/api/motion/execute`；`adapters/hardware.py:1270` POST `/motion/dispatch`；`ARMPI_HARDWARE_MOTION` 默认 0 |
| 语义与职责 | Studio 只观察 + 转发意图 + 停止代理；不得自持租约或分发运动 |
| 现有消费者 | G7/G8 legacy runners、旧 gateway |
| 目标归属 | system 独占执行；studio 只走 `jcheng-gateway.v1` |
| 迁移方式 | ① 默认禁用并加启动期硬阻断；② 把 legacy 代码移入 `tools/legacy/`，不可被 backend 导入；③ G7/G8 runner 改为 gateway v1 + operator 提供的 lease id；④ 删除前保留一个版本的只读记录 |
| 兼容性影响 | 旧实验脚本失效；新路径需 system gateway 可达 |
| 回归测试 | studio 13 项单测 + 新增"无本地 lease/无 /motion/dispatch"静态测试；gateway v1 意图测试 |
| 回滚 | 保留 legacy 分支/tag；不删除历史 |
| 风险 | **Critical**：当前启用即形成第二执行权威 |

## MIG-07 Mobile `/cmd_vel` 收口

| 字段 | 内容 |
|---|---|
| 当前证据 | mobile launch 未设 `ROS_DOMAIN_ID`；capability 声明域 42；厂商 `mecanum.py:63-67` 订阅绝对 `/cmd_vel` 并发布 `/ros_robot_controller/set_motor_speeds`，无超时/门禁；system `readonly.yaml` 禁 `/cmd_vel` |
| 语义与职责 | mobile 只发布底盘意图；system 消费并执行；厂商电机桥归 system |
| 现有消费者 | 厂商底盘节点（域 0） |
| 目标归属 | system 的 base intake；mobile 不再直连厂商 |
| 迁移方式 | ① 立即在 mobile launch 固定域 42（或独立域）并加启动断言；② system 增加 base intent 订阅 + 租约/deadman + 电机桥；③ 厂商 `controller/mecanum` 从 `start_node.service` 移除或由 system 接管；④ 台架验证失流停车 |
| 兼容性影响 | 底盘运动从"直连"变为"system 门禁"；旧 Nav2 配置需 remap |
| 回归测试 | mobile 静态测试；system base intake mock 测试；台架 L5（需授权） |
| 回滚 | 保留旧 launch 分支；不删除厂商代码 |
| 风险 | **Critical**：默认域 0 时意图可直达电机，无 deadman |

## MIG-08 Perception 任务状态机

| 字段 | 内容 |
|---|---|
| 当前证据 | `jcheng_perception_core/types.py:27-34` `Phase(SEARCH/COARSE/ACQUIRE/FINE/DROP_RECHECK)`；`FusedTarget.msg` 常量；`node.py:380` `drop_recheck` Trigger |
| 语义与职责 | 任务阶段属于 applications/scenarios；perception 只输出观测与建议 |
| 现有消费者 | perception 内部流水线；可能被旧 studio 使用 |
| 目标归属 | applications（阶段决策）或 scenarios（阶段定义）；perception 保留 `observation_phase` 作为 hint |
| 迁移方式 | ① 先做语义评审：阶段是"任务状态"还是"观测置信度阶段"；② 若是任务状态，迁 applications，perception 只发置信度/建议；③ 消息字段保留但改名/标 deprecated；④ 不机械迁移 |
| 兼容性影响 | 消息字段变化需 interfaces 提案；旧消费者需适配 |
| 回归测试 | perception 122 项；applications 阶段测试；契约握手 |
| 回滚 | 保留旧字段一个 minor |
| 风险 | **High**：误迁会改变抓取时序 |

## MIG-09 Research plant 移交

| 字段 | 内容 |
|---|---|
| 当前证据 | `jcheng-research/experiments/20261126-piper-x-gazebo-plant/` 完整 plant 生成器/URDF/SDF |
| 语义与职责 | 实验代码可留在 research，但不得成为第二套产品 plant |
| 现有消费者 | 仅 research 报告 |
| 目标归属 | simulation（若继续使用）或标记参考实现并退役 |
| 迁移方式 | ① 报告标注"实验副本，非产品 plant"；② 若 simulation 需要，迁入并加测试；③ 否则归档到 `experiments/` 只读 |
| 兼容性影响 | 无运行时影响 |
| 回归测试 | research gate；simulation gate（若迁移） |
| 回滚 | 保留原目录只读 |
| 风险 | **Low** |

## MIG-10 Benchmark 实机采集隔离

| 字段 | 内容 |
|---|---|
| 当前证据 | `jcheng-benchmark/tools/live/` 经 ssh 采集主机/DDS；capability 声明"no network path" |
| 语义与职责 | 采集属于 ops/studio 或受监督会话；benchmark 只读文件 |
| 现有消费者 | 无生产调用 |
| 目标归属 | 移出 benchmark 或隔离为不可导入工具 |
| 迁移方式 | ① 把 `tools/live` 标记 quarantine，CI 断言不被导入；② 需要实机采集时由 ops/studio 提供 JSONL；③ 不在 benchmark 内保留 ssh 路径 |
| 兼容性影响 | 无；仅工具位置 |
| 回归测试 | benchmark 61 项 + no-network 静态测试 |
| 回滚 | 保留目录只读 |
| 风险 | **Medium** |

## 执行顺序与门槛

1. **安全前置**：MIG-06、MIG-07 先做只读审计与运行暂停建议；实机整改需单独授权。
2. **批次 1**：MIG-01、MIG-02（声明收束；不改运行时数值）。
3. **批次 2**：MIG-04 → MIG-05 → MIG-03（先契约，再方言，再登记）。
4. **批次 3**：MIG-08、MIG-09、MIG-10（语义评审后）。
5. 每项迁移独立 PR、独立回滚、独立回归证据；不得合并提交。

## Related

- [边界规范](../repo-boundaries.md)
- [Source of Truth Matrix](01-source-of-truth-matrix.md)
- [契约兼容矩阵](03-contract-compatibility-matrix.md)
- [执行权限审计](02-runtime-authority-audit.md)
