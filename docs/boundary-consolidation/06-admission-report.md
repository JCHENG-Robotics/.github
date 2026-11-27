# 新仓准入验收报告：jcheng-devices / jcheng-scenarios

> Status: **v1.0 (2026-11-27)**. 结论：两仓达到准入条件（Experimental），
> 无实机、无 DDS、无运动路径。评审人签署：**pending**。
> 本报告只覆盖两个新仓；其他仓库的实现变更未获批准，未修改。

## 1. 验收依据

- [`docs/repo-boundaries.md`](../repo-boundaries.md) §9 准入检查
- [`docs/repo-taxonomy.md`](../repo-taxonomy.md) 新仓库准入检查
- [`docs/documentation-standard.md`](../documentation-standard.md)
- 用户 2026-11-27 批准的 Phase 2 要求

## 2. jcheng-devices

| 检查项 | 证据 | 结果 |
|---|---|---|
| 职责唯一 | 设备声明库；system 保留部署实例；`docs/INTEGRATION.md` §3.1 | pass |
| 无硬件/DDS/运动 | `capability.yaml`：`hardware_access: none`、`class: offline`、空 runtime；`tests/test_no_hardware.py` | pass |
| Manifest | `capability-manifest.v1` 形状；`>=0.2,<0.3` + `afca22…`；测试断言 | pass |
| Schema ownership | 新增 `SCHEMA_OWNERSHIP.md`（2 个 Schema、owner、consumers、promotion trigger）；`tests/test_contract.py::test_every_schema_is_declared_in_schema_ownership` | pass |
| 四件套 + 版本 | README/README.zh-CN/ROADMAP/CHANGELOG/ACCEPTANCE/VERSION 齐；版本 0.1.0 四处一致 | pass |
| CI | `.github/workflows/ci.yml`：merge queue、SHA pin、`check_repo_gate.sh` | pass |
| 依赖审查 | `docs/DEPENDENCY_REVIEW.md`；无运行时依赖 | pass |
| 测试 | **57 passed**；gate OK | pass |
| 消费方声明 | `SCHEMA_OWNERSHIP.md` 列出 planned consumers（simulation/learning/studio/applications） | pass |
| 硬件证据 | 不适用（无运动）；未声称硬件验证 | pass |

边界声明：`jcheng-system/configs/robots/<robot>/profile.yaml` 仍是运行时权威；
devices 的 profile 只用于规划、能力匹配、仿真配置，不导出运行配置。该声明由
`docs/INTEGRATION.md` 与 README 双重记录。

## 3. jcheng-scenarios

| 检查项 | 证据 | 结果 |
|---|---|---|
| 职责唯一 | 场景/任务/成功条件/评测规格声明；不执行、不测量 | pass |
| 无硬件/DDS/运动 | 统一后的 `capability.yaml`：`class: offline`、空 scopes/runtime、`hardware_access: none`；`tests/test_no_hardware.py` | pass |
| Manifest 统一 | 由自定义 offline profile 改为 `capability-manifest.v1`；测试断言 7 个顶层键、范围与哈希 | pass |
| Schema ownership | 新增 `SCHEMA_OWNERSHIP.md`（8 个 Schema、owner、consumers、promotion trigger）；门禁测试覆盖 | pass |
| 四件套 + 版本 | 五件文档齐；版本 0.1.0（VERSION / pyproject / `__version__` / manifest / registry / profile 一致） | pass |
| CI | 新增 `merge_group`；`actions/setup-python` 固定到 SHA `a26af69…`；gate 绿 | pass |
| 依赖审查 | `docs/DEPENDENCY_REVIEW.md`；仅 PyYAML/jsonschema/pytest | pass |
| 测试 | **62 passed**；gate OK | pass |
| 内容规则 | `ore_sorting` ID/版本/provenance 齐；无执行计划、无设备兼容结论、无评测结果 | pass |
| 硬件证据 | 不适用（无运动） | pass |

## 4. 未弱化标准的证明

- 没有删除任何测试。
- `test_capability_manifest_is_offline_scen` 被**替换为更严格的**
  `test_capability_manifest_is_canonical_offline`：从"断言自定义字段"改为
  "断言完整 `capability-manifest.v1` 形状、契约范围与哈希"。
- 新增两个门禁测试（每仓一个），Schema 文件未登记即失败。
- `test_no_hardware.py` 的 manifest 断言同步收紧到 `class/scopes/runtime`。
- 两仓 gate 均重新通过；测试数为 57 / 62。

## 5. 已知限制

- 两仓均为 `Experimental`；没有实机证据，也不声称硬件验证。
- `jcheng-learning` 的测试基线缺 `pyarrow`，与本次变更无关，未修改。
- `jcheng-interfaces` 0.3.0 未发布；两仓 pin 0.2.0/`afca22…`，与 system 一致。
- 两仓未 push、未开 PR；分支与 SHA 见回归基线。

## Related

- [回归基线](05-regression-baseline.md)
- [文件变更清单](07-file-changelog.md)
- [边界规范](../repo-boundaries.md)
