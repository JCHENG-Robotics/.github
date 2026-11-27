# Runtime Authority Hardening — 整改设计（待审查，未实施）

> Status: **v1.0 (2026-11-27)**. 本文件是 Phase 1 设计交付，**不包含实现修改**。
> 设计审查通过后才可改代码；所有验证先在 Mock / 离线 / 隔离仿真完成。
> 不启动实机、不恢复运动权限、不发送真实运动、不修改生产部署。
> 事实依据见 [`02-runtime-authority-audit.md`](02-runtime-authority-audit.md)。

## 0. 设计原则

1. **单一硬件权威**：只有 `jcheng-system` 能调用硬件桥（机械臂 `/servo_controller`、
   底盘 `/ros_robot_controller/set_motor_speeds`）。
2. **纵深防御**：域隔离、命名空间、QoS 都是层，不是唯一安全机制；每一层都要能
   独立失败关闭。
3. **失败关闭**：租约丢失、心跳超时、状态过期、进程退出、未知命令 → 停止/零输出
   并锁存，不自动重试。
4. **不同设备可有不同动作契约**：机械臂用 `ExecuteMotion`，底盘用 `BaseIntent`；
   但共享同一个租约、仲裁、deadman 与停止锁存。
5. **不依赖声明仓在线**：system 保留独立部署实例与安全覆盖。
6. **不破坏现有接口**：新契约走 `jcheng-interfaces` proposal；旧路径保留一个
   兼容窗口，默认关闭。

## 1. 目标架构

```text
                        ┌──────────────────────────────┐
  mobile Nav2 ─────────►│ /jcheng/intent/base (42)     │
  teleop ──────────────►│ /jcheng/intent/teleop (42)   │
  applications/studio ─►│ HTTP /v1/motion/* (loopback) │
                        └──────────────┬───────────────┘
                                       ▼
                        ┌──────────────────────────────┐
                        │ jcheng-system Authority      │
                        │ lease + holder + deadman     │
                        │ + arbiter + stop latch       │
                        │ + limits + state freshness   │
                        └──────┬───────────────┬───────┘
                               ▼               ▼
                    ArmExecutor          BaseExecutor
                    /servo_controller    set_motor_speeds
                    (domain 0)           (domain 0)
                               │               │
                               └───────┬───────┘
                                       ▼
                              HardwareBridge（唯一）
```

- 意图平面：域 42，只有 intent 话题；无直接电机/舵机话题。
- 硬件平面：域 0，只有 system 的桥进程发布/调用。
- 特权平面：域 41（目标态）；DDS Action 仅内部可用，默认不部署。

## 2. Mobile 整改设计

### 2.1 现状与冲突

| 事实 | 证据 |
|---|---|
| Nav2 发布 `/cmd_vel`，launch 未固定 `ROS_DOMAIN_ID` | `jcheng-mobile/.../mobile_nav.launch.py:138-155`；`nav2_params.yaml:86-128,312-325` |
| capability 声明域 42，但无运行时强制 | `jcheng-mobile/capability.yaml:20-22` |
| 厂商 `mecanum` 订阅绝对 `/cmd_vel`，直接发布电机转速 | 厂商 `controller/mecanum.py:63-72` |
| 厂商无超时/看门狗 | 同上；`ros_robot_controller_node.py:58,113-119` |
| system 无 `/cmd_vel` 订阅，且只读白名单禁止 | `jcheng-system/configs/readonly.yaml:19-25`；`docs/SAFETY.md:47` |

### 2.2 目标设计

1. **话题与域**
   - 删除默认 `/cmd_vel` 直连；mobile 发布 `/jcheng/intent/base`，固定域 42。
   - launch 设置 `ROS_DOMAIN_ID=42`（或显式参数），启动时断言；不是只写文档。
   - 命名空间 `/jcheng`；`use_sim_time` 与 QoS 显式声明。
   - 兼容期可保留 `/cmd_vel` remap 到 intent 话题，但默认关闭，且不得直连厂商。
2. **契约**
   - `jcheng-interfaces` 新增 `BaseIntent.msg`（建议字段：`header`、`lease_id`、
     `holder`、`command_id`、`seq`、`linear_x/linear_y/angular_z`、`duty_limit`、
     `deadman_ms`、`source`）。
   - 新增 `BaseState.msg`（速度、duty、零输出原因、latch 状态）供 studio/ops 只读。
   - 版本：interfaces minor bump；`system_api` 同步；consumers 更新 pin。
3. **System BaseAuthority**
   - 新模块 `jcheng_system_core/base.py`（ROS-free）+ `jcheng_base` thin node。
   - 订阅 `/jcheng/intent/base`（域 42），校验：
     contract hash → lease（scope `base` + holder）→ command_id 幂等 → 时间戳新鲜
     → 限速/限 duty → deadman → stop latch。
   - 通过 `HardwareAuthority` 调用硬件桥，发布
     `/ros_robot_controller/set_motor_speeds`（域 0）。
   - 指令超时：`intent_timeout_ms`（默认 200 ms）→ 零输出。
   - 失流停车：独立 `jcheng_base_watchdog` 进程（见 2.4）。
4. **厂商栈**
   - 从 `start_node.service` 的底盘 bringup 移除 `controller/mecanum`；只保留
     `ros_robot_controller`（电机板接口）。
   - 该变更属于部署变更，**本阶段不执行**；先在设计审查中批准。
5. **不把域隔离当唯一安全机制**
   - 即使域错误，system 仍是唯一发布电机命令者；厂商 `mecanum` 不再订阅意图话题。
   - 启动断言 + CI 静态检查双保险。

### 2.3 调用链（目标）

```text
Nav2 controller_server/velocity_smoother
  → /jcheng/intent/base (42, reliable, depth 1, deadline 200ms)
  → jcheng_base intake (ROS-free core)
      contract/lease/holder/idempotency/deadman/limits/stop
  → HardwareAuthority.submit_base(...)
  → VendorBridge.publish_motor_speeds (domain 0)
  → ros_robot_controller
  → 电机板
```

### 2.4 异常与失流

| 事件 | 行为 |
|---|---|
| 租约过期/心跳丢失 | 零输出 + latch + 审计事件 |
| intent 超时 | 零输出（保持 latch 直到新有效 intent + 租约） |
| 状态过期/总线失败 | 零输出 + latch |
| base intake 进程退出 | `jcheng_base_watchdog` 在 100 ms 内零输出 |
| 主机/容器崩溃 | 硬件 watchdog（已有）重启；重启后默认零输出 |
| 停止请求 | 立即零输出 + latch；仅授权 reset 可清除 |

### 2.5 验证（离线）

- 单元：lease scope/holder、deadman、timeout、idempotency、限速/限 duty、未知命令。
- Mock 集成：mobile 发 intent → 假 motor bridge 记录；断言正常/异常序列。
- 隔离仿真：域 42/43，不启动厂商栈；用 mock base plant（若 simulation 无底盘，
  新增最小 mock plant，仅测试）。
- 故障注入：kill intake、停心跳、状态过期、总线失败、stop、lease revoke。
- **不运行实机**。

### 2.6 文件影响（设计）

| 仓库 | 文件 | 变更 |
|---|---|---|
| interfaces | `msg/BaseIntent.msg`、`msg/BaseState.msg`、manifest、CHANGELOG | 新契约 |
| system | `jcheng_system_core/base.py`、`jcheng_base/` node、`authority.py`、`safety.py`、`models.py`、`configs/`、`tests/`、launch/systemd | 新入口 + 门禁 |
| system | `jcheng_hardware`/`jcheng_vendor` bridge | 增加 base 发布方法（唯一出口） |
| mobile | `launch/mobile_nav.launch.py`、`config/nav2_params.yaml`、`capability.yaml`、`tests/` | remap/域/意图 |
| deploy | `start_node.service` 或等价 bringup | 移除厂商 mecanum（待批准） |
| .github | 边界规范、迁移计划 | 记录 |

### 2.7 回滚

- 新 base 模块默认关闭（`base_intake_enabled: false`）；保留旧 launch 一个版本。
- 厂商 mecanum 移除前保留可恢复 unit；回滚即恢复旧 unit + 关闭 intake。
- 契约新增字段为 additive；回滚不需要数据迁移。

### 2.8 风险

| 风险 | 缓解 |
|---|---|
| QoS/ deadline 不兼容 | 显式 QoS + 集成测试；兼容期保留可靠传输 |
| 电机零输出语义不明确 | 台架验证（后续授权）；代码层先发零 + 断言 |
| 进程死亡窗口 | 独立 watchdog + 硬件 watchdog 双层 |
| 域设置遗漏 | launch 断言 + CI 静态检查 + 运行时 `/jcheng/health` 报告域 |
| 厂商节点仍被手工启动 | 文档/ops 检查 + B4 门禁告警 |

## 3. Studio 整改设计

### 3.1 现状与冲突

| 事实 | 证据 |
|---|---|
| legacy `/api/motion/execute` → `/motion/dispatch` | `routes.py:384-406`；`motion_ops.py:190-443`；`hardware.py:1151-1270` |
| 本地 LeaseManager 自签、内存、无 deadman/撤销 | `service.py:111`；`safety/lease.py:36-115` |
| legacy gateway 不校验租约 | `armpi-debug-gateway server.py:220-237` |
| 停止不联通 | `motion_ops.py:445-478`；`hardware.py:1312-1356` |
| `/api/control/acquire` 默认无鉴权 | `routes.py:320-332`；`config.py:99-105` |
| 新 v1 intent 路径设计内，但 mock 模式可提交 | `session_ops.py:222-235` |

### 3.2 目标设计

1. **默认禁用 legacy**
   - `/api/motion/execute`、`/api/chassis/pulse`、`/api/motion/stop` 默认返回
     `410 Gone`，并在响应中给出迁移提示。
   - 仅 `ARMPI_ENABLE_LEGACY_MOTION=1` + `ARMPI_MODE=legacy` 双开关才启用；
     该 profile 不进入发布镜像。
   - legacy 代码移入 `tools/legacy/`，backend 不得 import；CI 静态断言。
2. **移除本地运动租约权威**
   - `LeaseManager` 从 `service.py`/`supervisor.py` 的运动门禁中移除；仅保留
     UI 并发锁，重命名 `/api/session/lock`（acquire/renew/release），不参与运动。
   - 任何运动请求必须携带 **system 签发**的 `lease_id`；studio 不调用
     `/v1/leases`，不签发、不续期、不撤销。
3. **唯一意图路径**
   - `/api/session/intent/joint|gripper` → system `/v1/motion/validate` +
     `/v1/motion/execute`；`lease_id` 原样转发。
   - 仅 `ARMPI_MODE=hardware` + `ARMPI_SYSTEM_INTENT=1` 允许；mock 模式拒绝并
     清理 v1 env（避免 mock 打到真实 system）。
   - 启动断言：若 `ARMPI_MODE=mock` 且 v1 URL/token 非空 → 拒绝启动或清空并告警。
4. **停止**
   - 唯一停止入口 `/api/teleop/stop` → system `/v1/motion/stop`（latch）。
   - 删除 legacy stop；UI 的“停止”按钮只走 system。
5. **废弃策略**
   - v0.9.0：legacy 默认 410 + 文档 + 迁移提示；保留一个 minor 的只读记录。
   - v1.0.0：删除 legacy 代码与配置；capability 保持 `observer`。
6. **能力声明**
   - `capability.yaml` 保持 `class: observer`、`hardware_access: none`、
     `runtime` 空；删除“legacy adapter disabled by default”的模糊表述，改为
     “legacy motion removed / not shipped”。

### 3.3 调用链（目标）

```text
POST /api/session/intent/joint|gripper
  → session_ops（校验 mode/feature flag）
  → GatewayV1IntentClient.validate/execute（operator lease_id）
  → system /v1/motion/*（system 校验 lease/safety）
POST /api/teleop/stop
  → system /v1/motion/stop（latch）
```

### 3.4 验证（离线）

- 路由表测试：legacy 三个端点默认 410；无 `/motion/dispatch` 字符串。
- 静态测试：backend 不 import `tools/legacy`；无本地 `LeaseManager` 运动门禁。
- Mock：v1 intent 只发到 mock gateway；mock 模式拒绝硬件 URL。
- 停止：system stop 覆盖 intent；lease revoke/expiry/异常退出 → 后续请求被拒。
- **不运行实机**。

### 3.5 文件影响（设计）

| 文件 | 变更 |
|---|---|
| `backend/app/api/routes.py` | legacy 410；重命名 control lock |
| `backend/app/application/motion_ops.py` | 删除 legacy dispatch/chassis/stop |
| `backend/app/adapters/hardware.py` | 删除 `/motion/dispatch`、`/chassis/pulse`、`/motion/stop` |
| `backend/app/safety/lease.py`、`supervisor.py`、`service.py` | 移除运动权威；保留 UI 锁 |
| `backend/app/application/session_ops.py` | mode/feature flag；v1 环境清理 |
| `backend/app/config.py` | 双开关；启动断言 |
| `tests/` | 路由/静态/停止/租约测试 |
| `capability.yaml`、`docs/INTEGRATION.md` | 边界更正 |
| `tools/legacy/` | 迁移 legacy（不可 import） |

### 3.6 回滚

- 双开关默认关闭；回滚恢复旧配置即可，不改数据。
- legacy 代码先移动到 `tools/legacy` 一个版本，确认无调用后再删除。
- 保留 tag/分支；不修改历史。

### 3.7 风险

| 风险 | 缓解 |
|---|---|
| 旧实验脚本失效 | 迁移指南 + 一个 minor 兼容期 |
| 操作员忘记提供 lease id | UI 明确提示；system 拒绝并返回原因 |
| mock 模式误连真实 system | 启动断言 + 清空 env + 测试 |
| 停止路径遗漏 | 路由表枚举 + 每个端点测试 |

## 4. System 整改设计

### 4.1 现状与缺口

| 缺口 | 证据 |
|---|---|
| DDS Action 无 token/鉴权 | `jcheng_vendor/node.py:107-166,167,380-405` |
| deadman 未在硬件路径强制 | `authority.py:121,207-234`；仅 teleop 使用 |
| 租约 DELETE 无 holder 校验 | `gateway.py:253-254`；`authority.py:174-180` |
| PublisherGuard 仅名字比对 | `guard.py:19-33` |
| token 在 docker exec argv；容器 root | `deploy/.../run.sh:29-31,50` |
| expected_profile_hash/require_measured_state 客户端可空 | `models.py:419`；`safety.py:419-422` |
| 部署树 0.1.0 vs 审计树 0.3.0-dev0 | `deploy/.../evidence/20261127-r10/contract.json` |

### 4.2 目标设计

1. **唯一硬件出口**
   - 引入 `HardwareAuthority`（`jcheng_system_core/hardware_authority.py`）：
     所有 arm/base 写入必须经它；`VendorBridge` 只由它持有。
   - 反射/静态检查：除 `hardware_authority.py` 外，任何模块不得直接调用
     `bridge._publish` / `send_step` / `send_gripper` / `publish_motor_speeds`。
2. **DDS Action 授权**
   - 默认：ActionServer 只在域 41（特权）启动，且要求 SROS2；不进入发布镜像。
   - 启动门禁：`JCHENG_ALLOW_DDS_EXECUTE=1` + 域 ∈ {41} + SROS2 已启用，否则拒绝
     启动 ActionServer。
   - 文档明确：HTTP `/v1/motion/*` 是唯一外部入口；DDS 是内部/测试。
   - **不强制**底盘使用 arm 的 action；base 用 intent，arm 用 action，但同一授权。
3. **deadman 强制**
   - 租约字段 `deadman_ms` 进入 `authority.check`；任何 motion 前校验最近心跳
     （monotonic）≤ deadman。
   - 执行期间：每步前 + streaming 循环内检查；watchdog 线程在超时后发 stop/zero。
   - 默认 `require_deadman=True`；只有显式测试 profile 可关，且启动日志告警。
4. **租约 holder 与撤销**
   - `renew`/`DELETE` 校验 `holder` 或 `client_id`；不匹配 403。
   - 管理员撤销需要独立 admin token/scope；记录审计事件。
   - `revoke()` 接入 stop path；撤销即零/停止 + latch。
5. **PublisherGuard 加固**
   - 允许清单（node name + domain + topic）而非仅字符串；启动时枚举并记录。
   - 明确局限：不能发现同域伪装节点；由 DDS 安全/域隔离补足。
6. **统一 arm/base 安全**
   - 同一 `LeaseManager`、`SafetyState`、`stop latch`；scope 区分 `arm/gripper/base/full`。
   - base 零输出 = 停止；arm 停止 = hold + latch。
7. **进程死亡**
   - 新增 `jcheng-safety-watchdog`（Pi host systemd）：监控 gateway 心跳；丢失则
     通过本地接口发 stop/zero；`Restart=always`；不参与正常控制。
   - base 由 `jcheng_base_watchdog` 独立零输出；arm 由 safety watchdog + 总线确认。
8. **部署树对齐**
   - 先完成 0.1.0 → 0.3.0 的部署树对齐与证据；否则所有"实机门禁完整"结论无效。
   - 本阶段只设计，不改部署。

### 4.3 调用链（目标）

```text
HTTP /v1/motion/execute ─┐
DDS ExecuteMotion (41) ──┤
base intent (42) ────────┤
teleop intent (42) ──────┘
        ▼
HardwareAuthority
  contract → lease(holder) → deadman → arbiter → safety → limits → stop latch
        ▼
VendorBridge（唯一） → arm /servo_controller | base set_motor_speeds
        ▼
bus read / zero confirmation → evidence
```

### 4.4 验证（离线）

- 单元：holder 校验、deadman 过期、DDS 启动门禁、publisher allowlist、
  stop/revoke、base 零输出。
- Mock 集成：HTTP + DDS + base intent 三入口，共用租约；断言未授权被拒。
- 故障注入：网关退出、心跳丢失、租约过期、总线失败、状态过期、stop。
- 隔离仿真：域 43 仅用于 plant；不接硬件。
- **不运行实机**。

### 4.5 文件影响（设计）

| 文件 | 变更 |
|---|---|
| `jcheng_system_core/hardware_authority.py`（新） | 唯一出口 |
| `jcheng_system_core/authority.py` | deadman、holder、revoke |
| `jcheng_system_core/safety.py` | 强制状态/停止/限位 |
| `jcheng_system_core/gateway.py` | DELETE/renew holder；admin revoke |
| `jcheng_system_core/models.py` | expected_profile_hash 必填/服务端解析 |
| `jcheng_vendor/node.py`、`bridge.py` | DDS 门禁；受 HardwareAuthority 约束 |
| `jcheng_guard/guard.py` | allowlist |
| `jcheng_base/`（新） | base intake |
| `deploy/.../systemd/` | safety/base watchdog、DDS 域 |
| `tests/`、`docs/SAFETY.md`、`ARCHITECTURE.md` | 覆盖与说明 |

### 4.6 回滚

- 新门禁默认开启（更严格）；回滚仅限显式 legacy profile，且记录告警。
- DDS Action 默认不部署；回滚不影响 HTTP。
- watchdog 独立 unit，失败不影响主路径；可单独 disable。
- 不改 tag/历史。

### 4.7 风险

| 风险 | 缓解 |
|---|---|
| deadman 误杀正常运动 | 默认 TTL 与心跳频率留余量；测试覆盖 |
| DDS 域调整影响现有集成 | 先文档/测试；部署变更单独批准 |
| watchdog 误停 | 只发 stop/zero，不发起运动；双人评审 |
| 进程死亡窗口 | 独立 watchdog + 硬件 watchdog |
| 契约变更影响 L4 | 兼容窗口 + 版本化 |

## 5. 跨仓契约与顺序

| 步骤 | 仓库 | 内容 | 门禁 |
|---|---|---|---|
| 1 | interfaces | `BaseIntent`/`BaseState` proposal；holder 字段；版本 tag | 设计批准 |
| 2 | system | HardwareAuthority + deadman + holder + DDS 门禁（mock） | 离线测试 |
| 3 | system | base intake + watchdog（mock） | 离线测试 |
| 4 | mobile | 域/namespace/remap；不再直连厂商 | mock/sim |
| 5 | studio | legacy 410；移除本地租约；唯一 v1 路径 | mock |
| 6 | deploy | 移除厂商 mecanum、部署树对齐 | **单独批准** |
| 7 | hardware | 台架/实机验证 | **单独批准** |

本阶段只做 1–5 的设计与离线验证；6–7 未批准。

## 6. Phase 1 离线验收标准

- 未授权运动请求（HTTP/DDS/base/teleop）被拒绝，返回明确错误。
- 租约过期、心跳丢失、指令超时、进程退出 → 零/停止 + latch。
- 停止不可被 legacy/其他路径绕过；studio 不再持有运动租约。
- mobile 不能直接发布厂商电机话题；system 是唯一出口。
- 所有测试在 mock/离线/隔离仿真通过；无实机。
- 不破坏现有测试、接口、冻结基线。

## 7. 待批准问题

1. `BaseIntent` 是否作为 interfaces 新契约，还是先 repo-local v0 在 system 内验证？
2. DDS Action 的定位：仅内部域 41 + SROS2，还是保留域 42 但加 token？
3. base watchdog 放在 Pi host 还是容器内？容器内无法在容器死时零输出。
4. legacy studio 的废弃窗口：1 个还是 2 个 minor？
5. 厂商 `mecanum` 移除是否接受为部署变更（需单独批准）？
6. 部署树 0.1.0 → 0.3.0 的对齐是否作为 Phase 1 的前置？

## Related

- [执行权限审计](02-runtime-authority-audit.md)
- [迁移计划](04-migration-plan.md) MIG-06/MIG-07
- [边界规范](../repo-boundaries.md)
- [Git 操作审计](09-git-operation-audit.md)
