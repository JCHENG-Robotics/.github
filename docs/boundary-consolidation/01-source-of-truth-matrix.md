# Source of Truth Matrix — 现状与目标

> Status: **v1.0 (2026-11-27)**. 本文件是 [`docs/repo-boundaries.md`](../repo-boundaries.md)
> §4 的证据化展开：每个概念当前由谁声明、有哪些副本、哪些已经漂移。
> 只做诊断，不迁移实现。

## 1. 快照

- 工作区：`/home/jerichocheng/jcheng`，18 个 git 检出（15 个产品仓 + 3 个重复检出）。
- 两新仓已于 2026-11-27 19:20 前完成并发写入；本矩阵基于 19:30 的稳定快照。
- 判据：`git status`、`capability.yaml`、`registry`、`schema`、文档与代码交叉引用。

## 2. 矩阵

| 概念 | 声明真源（目标） | 运行时权威 | 已知副本（证据） | 漂移 |
|---|---|---|---|---|
| 设备身份/运动学/声明限位/能力 | `jcheng-devices/registry/` | 无（描述） | `jcheng-system/configs/robots/armpi_ultra/profile.yaml`；`jcheng-interfaces/schemas/robot-profile.v1.schema.json` + `tests/fixtures/robot_profile.yaml`；`jcheng-simulation/ros2_ws/src/jcheng_simulation_robots/robots/armpi_ultra/robot.yaml`；`jcheng-learning/src/jcheng_learning/profiles/armpi_ultra.yaml`；`jcheng-studio/configs/joint_mapping.yaml`、`configs/takeover.yaml`；`jcheng-applications/src/jcheng_applications/model.py:464-465`（gripper `[0,2.22]`）；`jcheng-teleop/examples/armpi_ultra_demo/profile.yaml` | **High**：8 处手写；数值一致但无引用关系 |
| 某台机器人的部署配置与安全覆盖 | `jcheng-system/configs/robots/<robot>/` | `jcheng-system` | 无（运行时只读本地） | **对齐**：`robot-profile.v1` + profile SHA-256；但与 devices 声明未建立哈希引用 |
| 场景/任务/成功失败条件 | `jcheng-scenarios/scenarios/<id>/` | 无（声明） | `jcheng-system/ros2_ws/src/jcheng_system_core/jcheng_system_core/scenarios.py`（S1–S17）；`jcheng-benchmark/benchmarks/suites/*.yaml`；`jcheng-simulation/.../worlds/*.sdf`（table、target_cube）；`jcheng-applications/recipes/*.yaml`（`at_least_rad`/`at_most_rad`）；`jcheng-perception/.../types.py:27-34`（Phase）；`jcheng-learning/docs/m2/suites/*.yaml` | **High**：6 处独立语义 |
| 业务评测指标与阈值策略 | `jcheng-scenarios/.../evaluation.yaml` | 无（声明） | `jcheng-benchmark/benchmarks/suites/*.yaml`（metrics/thresholds）；`jcheng-learning/docs/m2/EVAL.md`、`docs/m2/suites/`；`jcheng-perception/.../schemas/jcheng.ore_evaluation.v1.schema.json` | **High**：4 套指标词汇；阈值均未设定 |
| 配方/步骤编排/重试 | `jcheng-applications/recipes/` | 无（提交意图） | 测试 Fixture | **对齐**：recipe schema 在仓内；缺 `scenario_id`/`task_id` 引用 |
| 实机运动/租约/仲裁/停止 | `jcheng-system` | `jcheng-system` | 见 Runtime Authority Audit | **Critical/High**：studio legacy lease/dispatch；mobile `/cmd_vel` |
| 现场观测/scene_state | `jcheng-perception` | 无（advisory） | `jcheng-perception/.../schemas/jcheng.scene_state.v1/v2`；证据 JSONL | **对齐**：但 `Phase` 任务状态机越界 |
| 底盘里程计/地图/路径 | `jcheng-mobile` | 无（意图） | 无 | **对齐**（设备几何描述除外） |
| 数据集契约/训练/策略 | `jcheng-learning/docs/m1/` | 无（离线） | `jcheng-teleop/.../capture`（capture 包，非数据集）；`jcheng-perception/.../ore_dataset`（专用数据集） | **Medium**：数据集契约未上移 interfaces；perception 另立 ore_dataset |
| 操作员意图/遥操作捕获 | `jcheng-teleop` | `jcheng-system` 消费 | `jcheng-studio` 只读状态面板 | **对齐**：manifest 与 publisher 不一致（见审计） |
| 虚拟 plant/world/truth | `jcheng-simulation` | 域 43 | `jcheng-research/experiments/20261126-piper-x-gazebo-plant/`（第二套 plant） | **Medium**：research 副本未标退役 |
| 跨仓通信格式/错误码 | `jcheng-interfaces` | 运行时契约 | 见 Contract Compatibility Matrix | **High**：17 + 13 个仓内 Schema |
| 生态级测量结果 | `jcheng-benchmark` | 无（离线） | `jcheng-learning/docs/m2/suites`；`jcheng-perception` 模型指标；`jcheng-studio` 配对统计 | **Medium**：多套“评测”词汇 |
| 部署单元/探活/自愈 | `jcheng-ops` | `jcheng-ops` | `jcheng-system/deploy/armpi-ultra/systemd/`（system 自管部署） | **Low**：两处 systemd 材料，需登记归属 |
| 冻结基线 | `jcheng-manipulation@v1.0.0`（`b3411e4`） | 无 | system 证据引用 | **对齐**：HEAD 领先 32 提交，不作为基线 |
| 生态治理/注册表 | `.github` | 无 | 各仓 README 状态表 | **Medium**：本次已补齐 devices/scenarios，仍有两处版本声明需随发布更新 |

## 3. 副本判定规则

| 情形 | 允许 | 条件 |
|---|---|---|
| system 部署实例 | 是 | 由 devices profile + 本地安全覆盖生成或比对；带 `device_id@version#sha256`；CI 校验；只读 |
| simulation plant | 是 | 引用 `device_id@version`；只保留 plant 参数；限位冲突时以 system 部署值为准 |
| learning/studio 只读引用 | 是 | 不导出为运行时配置；不手改；标明来源 |
| 文档表格/示例 | 是 | 标注“示例，非真源”；不得进入 CI 判定 |
| 手写第二份设备限位 | 否 | 必须先提案或生成 |
| research 实验 plant | 有条件 | 标注实验副本；实验结束移交 simulation 或标记退役 |

## 4. 待批准决策

1. `jcheng-interfaces/schemas/robot-profile.v1` 是否保留为部署契约（当前是）。若保留，devices 的 `device-profile.v1` 与其字段映射必须在迁移项 MIG-01 中固定。
2. system 的 `profile.yaml` 是否改为“生成式部署快照”（带 devices 引用与哈希）。本文件建议：是，但保留独立安全覆盖。
3. perception 的 `ore_dataset`/`ore_evaluation` 是否保留仓内（建议保留为模型开发专用），不与 learning 的 `jcheng.dataset.v1` 合并。

## Related

- [边界规范](../repo-boundaries.md)
- [契约兼容矩阵](03-contract-compatibility-matrix.md)
- [迁移方案](04-migration-plan.md)
