# Contract & Regression Report — Phase 4 只读调查

> Status: **v1.0 (2026-11-27)**. 只读调查与方案；未安装依赖、未改仓库、未跑
> Humble/Gazebo/实机。补齐 Learning 证据的命令仅作为待批准方案。

## 1. 版本关系（部署树 / 开发树 / 生态锁）

| 平面 | 版本 | Contract hash | 证据 |
|---|---|---|---|
| interfaces 已发布 v0.1.0 | 0.1.0 | `0b8d72ce…` | tag `v0.1.0` |
| interfaces 已发布 v0.2.0 | 0.2.0 | `afca22a4…` | tag `v0.2.0` / `b03a054` |
| interfaces `main` | 0.3.0（未发布） | `8120c502…` | `VERSION`、`interface_manifest.json` |
| system 开发树 | 0.3.0-dev0 | `afca22a4…` | `configs/contract.yaml:10` |
| system 部署 R10 | **0.1.0** | **`0b8d72ce…`** | `deploy/armpi-ultra/evidence/20261127-r10/contract.json` |
| 生态锁 | 0.2.0 | `afca22a4…` | `jcheng-system/locks/ecosystem.lock.yaml` |

**结论**：三平面不一致，部署树最旧（0.1.0），开发树与锁为 0.2.0，interfaces
主线已到 0.3.0 未发布。"部署门禁完整"的结论只对 0.1.0 成立；升级到 0.2.0/0.3.0
后的实机行为没有证据。

## 2. 生产者 / 消费者矩阵

| 契约 | 生产者 | 消费者 | 当前状态 |
|---|---|---|---|
| ROS IDL / HTTP / WS / 公共 Schema | interfaces | system、applications、studio、teleop、devices、scenarios | system/devices/scenarios pin 0.2.0；四个 L4/L3 仍 pin 0.1.0 |
| `robot-profile.v1` | interfaces（schema）/ system（实例） | system 运行时 | 部署实例 SHA-256 已锁 |
| `capability-manifest.v1` | interfaces | 全部产品仓 | 7 仓 v1；perception/ops/benchmark legacy；system/interfaces 无 |
| device/capability profile | devices（repo-local） | 本仓；simulation/learning/studio 计划中 | 未跨仓消费 |
| scenario/task/evaluation | scenarios（repo-local） | 本仓；apps/sim/bench/perception 计划中 | 未跨仓消费 |
| `TeleopCommand` | teleop（test-only publisher） | system intake（mock） | 生产 lease adapter 未实现 |
| gateway `/health`、`/v1` | system | studio、ops、applications | ops 未登记为契约 |
| benchmark report v1 | benchmark（repo-local） | 本仓 | 未跨仓消费 |

## 3. Learning 缺失 pyarrow：根因与隔离环境方案

### 根因

- `jcheng-learning/pyproject.toml:12` 把 `pyarrow==24.0.0` 列为**必需**运行时依赖。
- `uv.lock` 已锁定 `pyarrow 24.0.0`（87 个包，`requires-python >=3.12`）。
- 宿主 Python 3.12 环境**未安装**该依赖；`import pyarrow` 失败，导致
  `tests/test_cli.py`、`test_export_features.py`、`test_import.py` 等 5 个模块
  在收集阶段失败。
- 这不是代码缺陷，也不是 lock 漂移；是"直接在系统 Python 跑测试"导致的环境缺失。

### 待批准的隔离环境方案（不改仓库）

```bash
cd <workspace>/jcheng-learning
export UV_PROJECT_ENVIRONMENT="$PWD/.venv-ci"
uv sync --frozen --python 3.12          # 严格使用 uv.lock，不解析新版本
uv run --frozen --python 3.12 pytest tests
```

- 使用 `uv.lock`（不是 `pip install -e .`），保证与 CI/锁一致。
- 不写入系统 Python；`.venv-ci/` 应被 `.gitignore` 覆盖（需确认）。
- 证据：保存 `uv sync` 日志、`uv pip freeze`、pytest 输出、pyarrow 版本。
- 若 CI 已有等价环境，则不需新增脚本；只需记录 CI 运行 URL。

### 待确认

- `uv.lock` 的 `requires-python` 与宿主 3.12.3 一致。
- `.gitignore` 是否覆盖 `.venv-ci/`；若否，方案改为仓库外目录
  `UV_PROJECT_ENVIRONMENT=/tmp/jcheng-learning-venv`。
- pyarrow 24.0.0 是否在目标平台有 wheel（lock 中有 manylinux x86_64/aarch64）。

## 4. 回归分层与缺口

| 层 | 现有 | 缺口 | 方案 |
|---|---|---|---|
| L0 契约/静态 | 各仓 gate、interfaces schema check | 无统一边界门禁 | Phase 3 `check_boundaries` report-only |
| L1 单元 | system 93、devices 57、scenarios 62、perception 122、teleop 214、applications 186、simulation 86、benchmark 61、studio 13、interfaces 16、mobile 10 | learning 缺 pyarrow | §3 隔离环境 |
| L2 Mock 集成 | system mock stack、apps mock、studio mock、teleop mock | **无 base intent / 统一租约的跨仓集成** | 新增 system+base+mobile mock 集成 |
| L3 Mock 端到端 | system S1–S17、scenarios 校验 | 无 studio 全路径停止覆盖 | 新增 stop/revoke/exit 测试 |
| L4 Replay | system S13、benchmark JSONL | 无设备/场景引用的 replay | 待 MIG-01/02 |
| L5 实机 | 历史证据（manipulation/系统 M4/M5.2） | **部署树 0.1.0**；无 0.2.0/0.3.0 证据 | 需单独授权与版本对齐 |

### 跨仓集成测试（建议新增）

1. **system + applications**：intent → lease → execute → mock bridge；未授权拒绝。
2. **system + studio**：v1 intent/stop；legacy 410；mock 模式拒绝真实 URL。
3. **system + teleop**：TeleopCommand → intake → lease/deadman；无租约拒绝。
4. **system + base（新）**：BaseIntent → lease/base scope → 零输出；超时/失流。
5. **devices + system**：profile 重叠字段一致；不一致阻断（MIG-01）。
6. **scenarios + apps/bench**：`scenario_id`/`evaluation_id` 引用可解析（MIG-02）。

### ROS 2 构建验证

- 目标：`ros:humble-ros-base` 容器，`colcon build` system/perception/mobile/simulation。
- 宿主只有 Jazzy；不能在宿主上冒充 Humble 结论。
- 记录镜像 digest、colcon 日志、测试输出。

### 仿真回归

- 仅域 43；`jcheng_simulation` mock plant；不接硬件。
- base 若 simulation 无底盘模型，新增最小 mock plant 或 system 内 mock bridge。

## 5. 当前不能下的结论

- 不能声称 0.2.0/0.3.0 部署树具备完整实机门禁：部署证据是 0.1.0。
- 不能声称 DDS Action 安全：无 token/SROS2，且默认不部署。
- 不能声称 mobile/base 已受统一授权：base intake 尚不存在。
- 不能声称 learning 测试全绿：环境缺 pyarrow，未在隔离环境重跑。
- 不能声称 check_boundaries 可替代运行时安全：它只是静态报告。

## 6. 本轮未执行

- 未安装 pyarrow/uv sync；未创建 venv；未跑 Humble/Gazebo。
- 未修改任何仓库实现、CI、锁或部署。
- 未启动机器人、未发送运动。

## Related

- [契约兼容矩阵](03-contract-compatibility-matrix.md)
- [回归基线](05-regression-baseline.md)
- [执行权限审计](02-runtime-authority-audit.md)
- [加固设计](10-authority-hardening-design.md)
