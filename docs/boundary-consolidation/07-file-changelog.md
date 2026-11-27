# 文件变更清单与测试证据

> Status: **v1.0 (2026-11-27)**. 本专项只修改：
> ① `.github` 治理文档与注册信息；② `jcheng-devices` 与 `jcheng-scenarios` 准入修复；
> ③ 工作区 `AGENTS.md`（非 git）。**其他现有仓库的实现代码未修改。**

## 1. git 仓库

### `.github`（分支 `docs/boundary-consolidation-20261127`）

| 提交 | 内容 |
|---|---|
| `3ef9b36` | 并入 devices 准入注册（原 `docs/devices-admission-20261127`） |
| `f7fd1e5` | 并入 scenarios 准入注册（原 `docs/scenarios-admission-20261127`；解决 taxonomy/ROADMAP 冲突，保留两仓） |
| `6a2e5fd` | 新增 `docs/repo-boundaries.md` v1.0；更新 `docs/repo-taxonomy.md`、`profile/README.md`、`profile/README.zh-CN.md`、`CHANGELOG.md`、`ROADMAP.md` |
| `cfef7c0` | 更新组织主页架构图：声明平面 / 意图平面 / 执行平面 |
| `dd76f18` | 新增 `docs/boundary-consolidation/01…06、08` 与 `CHANGELOG` 条目 |
| `d9a5f91` | 新增交付索引 `README.md`；边界规范补充非产品检出说明 |

> 之后的提交只做元数据对齐（本表与回滚引用的 SHA），不改变交付内容；
> 可回滚点仍以 `05-regression-baseline.md` §2 为准。

新增文件：

- `docs/repo-boundaries.md`
- `docs/boundary-consolidation/01-source-of-truth-matrix.md`
- `docs/boundary-consolidation/02-runtime-authority-audit.md`
- `docs/boundary-consolidation/03-contract-compatibility-matrix.md`
- `docs/boundary-consolidation/04-migration-plan.md`
- `docs/boundary-consolidation/05-regression-baseline.md`
- `docs/boundary-consolidation/06-admission-report.md`
- `docs/boundary-consolidation/07-file-changelog.md`
- `docs/boundary-consolidation/08-check-boundaries-design.md`

修改文件：`docs/repo-taxonomy.md`、`profile/README.md`、`profile/README.zh-CN.md`、
`ROADMAP.md`、`CHANGELOG.md`。

### `jcheng-devices`（分支 `feat/admission-20261127`，`9026c16`）

| 文件 | 变更 |
|---|---|
| `SCHEMA_OWNERSHIP.md` | 新增：2 个 Schema 的 owner/status/consumers/promotion trigger |
| `tests/test_contract.py` | 文档清单加入 `SCHEMA_OWNERSHIP.md`；新增 `test_every_schema_is_declared_in_schema_ownership` |
| `README.md` / `README.zh-CN.md` | 目录树加入 `SCHEMA_OWNERSHIP.md`；Related 链接边界规范 |
| `CHANGELOG.md` | Unreleased Added 记录 |

未改：`capability.yaml`（已是 `capability-manifest.v1`）、registry、validator、
CI（已含 merge queue 与 SHA pin）。

### `jcheng-scenarios`（分支 `feat/admission-20261127`，`6ee7928`）

| 文件 | 变更 |
|---|---|
| `capability.yaml` | 改为 `capability-manifest.v1`：`schema_version`、`contract`、`safety{class: offline}`、`hardware_access: none`、空 `runtime` |
| `SCHEMA_OWNERSHIP.md` | 新增：8 个 Schema 的归属与消费方 |
| `tests/test_contract.py` | 加入 `SCHEMA_OWNERSHIP.md`；manifest 测试改为断言完整 v1 形状；新增 ownership 门禁测试 |
| `tests/test_no_hardware.py` | manifest 断言收紧到 `class/scopes/runtime` |
| `docs/ARCHITECTURE.md` | §7 改为“Capability manifest”，删除“故意偏离”表述 |
| `README.md` / `README.zh-CN.md` | manifest 描述、目录树、Related 链接 |
| `CHANGELOG.md` | Unreleased Added/Changed |
| `.github/workflows/ci.yml` | 增加 `merge_group`；`actions/setup-python` 固定 SHA |

未改：8 个 JSON Schema、`ore_sorting` 内容、registry、CLI/loader/validator。

### 工作区 `AGENTS.md`（非 git）

- 状态段加入 `jcheng-scenarios`。
- Repository map 加入 `jcheng-scenarios`（SCEN）；simulation 条目改指
  `jcheng_testkit` 的一致性用例与 scenarios 的任务场景。
- Layer rules 加入 scenarios 的离线边界；devices 段保留。
- Build/test 表加入 scenarios。
- Contracts 段从 v0.1.0/`0b8d72…` 更正为 v0.2.0/`afca22…`，并登记 0.3.0
  未发布与六仓旧 pin。
- Read-before list 的 `.github` 条目加入 `repo-boundaries.md`。

## 2. 未修改（明确声明）

以下仓库的实现代码、配置、Schema、CI 均未改动：

`jcheng-system`、`jcheng-interfaces`、`jcheng-perception`、`jcheng-mobile`、
`jcheng-teleop`、`jcheng-learning`、`jcheng-simulation`、`jcheng-benchmark`、
`jcheng-studio`、`jcheng-applications`、`jcheng-ops`、`jcheng-research`、
`jcheng-manipulation`、`jcheng-system-r5`、`jcheng-system-v020`。

Studio legacy、mobile `/cmd_vel`、system DDS 等只做只读诊断，整改方案在
`02-runtime-authority-audit.md` 与 `04-migration-plan.md`，需单独批准。

## 3. 测试证据

| 仓库 | 命令 | 结果 | 证据 |
|---|---|---|---|
| `.github` | `bash scripts/check_org_files.sh` | pass | 本地 2026-11-27 |
| `jcheng-devices` | `bash scripts/check_repo_gate.sh` | 57 passed | `evidence/20261127_scaffold/` + 本地 |
| `jcheng-scenarios` | `bash scripts/check_repo_gate.sh` | 62 passed | `evidence/20261127_scaffold/` + 本地 |
| 其余 12 仓 | 见 `05-regression-baseline.md` | 全绿，learning 缺 pyarrow | 本地 2026-11-27 |

未运行：ROS 2 Humble 构建、Gazebo、任何实机测试。

## 4. 可回滚点

见 `05-regression-baseline.md` §2。未 push、未改 tag、未改历史。

## Related

- [新仓准入验收报告](06-admission-report.md)
- [回归基线](05-regression-baseline.md)
- [边界规范](../repo-boundaries.md)
