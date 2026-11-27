# Regression Baseline

> Status: **v1.0 (2026-11-27 19:38 +0800)**. 稳定快照与测试基线。用于迁移前后对比；
> 不包含实机、Gazebo 或 Humble 容器运行。

## 1. 工作区快照

| 项 | 值 |
|---|---|
| 工作区 | `/home/jerichocheng/jcheng`（多仓，无根 git） |
| git 检出 | 18 |
| 产品仓 | 15：applications、benchmark、devices、interfaces、learning、manipulation、mobile、ops、perception、research、scenarios、simulation、studio、system、teleop |
| 重复检出 | 3：`jcheng-design`（manipulation 的第二个 checkout）、`jcheng-system-r5`、`jcheng-system-v020` |
| 非 git 目录 | `jcheng-mobile-bench`（BENCH 沙箱）、`jcheng-ecosystem-bootstrap`（M1 staging） |
| 并发写入 | 两新仓最后写入 19:20；本快照取 19:29–19:38，期间无新写入 |
| 主机 | Linux，Python 3.12，ROS 2 Jazzy；无 Humble 容器、无 Gazebo 运行、无实机 |

## 2. 本次变更的可回滚点

| 仓库 | 当前分支 | HEAD | 变更前基线 |
|---|---|---|---|
| `.github` | `docs/boundary-consolidation-20261127` | `cfef7c0` | `origin/main` `c298efb` |
| `jcheng-devices` | `feat/admission-20261127` | `9026c16` | `029991f`（`fix/robot-profile-boundary-20261127`） |
| `jcheng-scenarios` | `feat/admission-20261127` | `6ee7928` | `4390212`（`main`） |

回滚方式：切回基线 SHA 或删除本地分支；未 push、未改 tag、未改历史。

## 3. 测试基线（本次实际运行）

| 仓库 | 命令 | 结果 | 说明 |
|---|---|---|---|
| `.github` | `bash scripts/check_org_files.sh` | **pass** | 结构、无产品代码、无 LICENSE |
| `jcheng-interfaces` | `python3 -m pytest` | **16 passed** | 契约/Schema 校验 |
| `jcheng-system` | `python3 -m pytest` | **93 passed** | ROS-free 核心套件；未跑 `tests_ros`、Gate-2/MoveIt |
| `jcheng-devices` | `bash scripts/check_repo_gate.sh` | **57 passed** | 含新增 schema ownership 测试 |
| `jcheng-scenarios` | `bash scripts/check_repo_gate.sh` | **62 passed** | 含新增 manifest/ownership 测试 |
| `jcheng-perception` | `python3 -m pytest tests` | **122 passed** | 离线/单元；未跑 ROS 图与硬件 |
| `jcheng-mobile` | `python3 -m pytest tests` | **10 passed** | 静态契约 |
| `jcheng-learning` | `python3 -m pytest tests` | **collection error** | 缺 `pyarrow`；5 个测试模块无法收集，未改动 |
| `jcheng-teleop` | `python3 -m pytest` | **214 passed** | ROS-free 核心 |
| `jcheng-simulation` | `python3 -m pytest tests` | **86 passed, 2 skipped** | 未启动 Gazebo |
| `jcheng-studio` | `python3 -m pytest tests` | **13 passed** | 后端单元 |
| `jcheng-applications` | `python3 -m pytest` | **186 passed, 5 skipped** | 离线核心 |
| `jcheng-ops` | `bash scripts/check_repo_gate.sh` | **pass**（5 tests） | 无实机探针 |
| `jcheng-benchmark` | `python3 -m pytest` | **61 passed** | 合成自测 |
| `jcheng-research` | `bash scripts/check_repo_gate.sh` | **pass** | 文档/链接/资产 |
| `jcheng-manipulation` | 未运行 | **not run** | 冻结基线；ROS/Humble 依赖，未在本机执行 |
| `jcheng-system-r5` / `-v020` | 未运行 | **not run** | 重复检出，不属于产品矩阵 |

## 4. 未纳入基线的部分（必须在迁移验证时补）

- ROS 2 **Humble** 构建与 `tests_ros`（本机只有 Jazzy）。
- Gazebo Harmonic 仿真（simulation 仅跑离线单测）。
- 实机 L5：任何运动、总线读、相机、底盘；本次明确未执行。
- `jcheng-learning` 的完整套件：安装 `pyarrow` 后重跑。
- 部署树 0.1.0 与审计树 0.3.0-dev0 的差异（见契约矩阵 §3）。

## 5. 两新仓准入后的状态

| 项 | devices | scenarios |
|---|---|---|
| 版本 | 0.1.0 | 0.1.0 |
| 测试 | 57 passed | 62 passed |
| Gate | pass | pass |
| CI | `ci.yml`，merge queue + SHA pin | `ci.yml`，merge queue + SHA pin |
| Manifest | `capability-manifest.v1`，class `offline` | 同左（本次统一） |
| Schema ownership | `SCHEMA_OWNERSHIP.md` + 门禁测试 | 同左 |
| 硬件/DDS/运动 | 无 | 无 |
| 四件套 + LICENSE-REVIEW | 齐 | 齐 |

## Related

- [新仓准入验收报告](06-admission-report.md)
- [迁移方案](04-migration-plan.md)
- [边界规范](../repo-boundaries.md)
