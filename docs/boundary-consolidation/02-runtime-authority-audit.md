# Runtime Authority Audit — 意图到硬件的执行权限

> Status: **v1.0 (2026-11-27)**. 只读静态审计；**未启动机器人、未发送运动指令、
> 未做任何实机测试**。所有 file:line 均来自本地代码与部署材料。
> 结论中的"可达"区分：**静态可达**（代码存在）、**部署可达**（单元/端口已安装）、
> **默认可达**（无需额外配置）。

## 1. 结论摘要

设计上只有 `jcheng-system` 的 `ExecuteMotion` 是实机执行权威。静态审计发现
**四条平行路径**可以产生实机运动，其中两条在特定配置下默认可达：

| # | 路径 | 默认可达 | 门禁 | 风险 |
|---|---|---|---|---|
| A | system HTTP `/v1/motion/execute` | 手动启动后可达 | token → 租约 → armed → safety → 限位 → 总线确认 | **High**（deadman 未强制、token 暴露） |
| B | system DDS `ExecuteMotion` action | 部署不可达（无 unit），同域可启动 | 租约/safety，但**无 HTTP 鉴权** | **High** |
| C | studio legacy `/api/motion/execute` → `/motion/dispatch` | 默认 mock 不可达；启用即达 | 仅 legacy token + 本地租约（自签、无 deadman） | **Critical（设计）/Medium（当前部署）** |
| D | mobile Nav2 `/cmd_vel` → vendor `mecanum` | **域 0 时可达**（launch 未固定域 42） | **无租约、无 deadman、厂商无超时** | **Critical** |
| E | vendor `start_node.service` 开机 bringup | 开机可达 | 无 jcheng 门禁（厂商 startup check 会动臂） | **Critical（运行纪律）** |

**立即建议：暂停依赖 studio legacy 运动与 mobile 底盘的实机运行；在
`/cmd_vel` 域固定、studio legacy 端点关闭、部署树与审计树对齐之前，不恢复。
system-only 的受监督单关节/夹爪运动也应在重新核对部署版本后再进行。**
本次审计未发送任何运动指令。

## 2. 调用链

### A. system HTTP（设计内唯一硬件写入口）

```text
POST /v1/motion/execute
  jcheng_gateway/gateway.py:285
  → GatewayApp.handle:176            token 校验
  → MotionCommand.from_dict
  → jcheng_system_core/executor.py:197
  → validate:174                     contract hash
  → guard.enforce (guard.py:29)      publisher guard（仅名字比对）
  → authority.check (authority.py:207) 租约、armed、priority
  → safety.validate (safety.py:398)   stop latch、armed、state 新鲜度
  → _check_kind:182                   限位/时长/步长/起始距离
  → safety.begin_motion:241
  → VendorBridge.send_step/send_gripper (bridge.py:164/172)
  → _publish:145 → /servo_controller
  → read_bus:57 → GetBusServoState
  → 脉冲比对 (executor.py:321-357) → evidence
```

部署：`jcheng-gateway-vendor.service` 手动启动，8766 loopback；容器
`--privileged --network host`，token 经 `docker exec -e` 出现在 argv
（`deploy/armpi-ultra/container/run.sh:29-31,50`）。

### B. system DDS `ExecuteMotion`

```text
jcheng_vendor/node.py:167 ActionServer
  → _goal:380 → _execute:405
  → motion_executor.execute (executor.py:197)
  → VendorBridge（同 A 的租约/safety/限位/总线门禁）
```

另有 `/jcheng/safety/arm|reset|acquire_lease` 服务（node.py:107-166），
**无 HTTP token**；同域任意 DDS 参与者可 arm + acquire lease + execute。
无 systemd 单元；`motion_vendor.launch.py` 仅手工启动，故部署不可达。

### C. studio legacy（第二执行权威）

```text
POST /api/motion/execute
  backend/app/api/routes.py:384
  → application/motion_ops.py:190-443   Studio 本地 LeaseManager 检查
  → adapters/hardware.py:1151-1270     dispatch / dispatch_profile
  → POST /motion/dispatch (hardware.py:1270)
  → legacy armpi_debug_gateway server.py:225-237
  → node.py:628 → motion.py:544
  → 厂商运动接口
```

- 本地租约：`backend/app/safety/lease.py:36-115`，`uuid4` 自签、内存单槽、
  TTL 60 s、无 deadman/优先级/撤销调用者。
- legacy 网关只校验 `X-Armpi-Token` 与本机 motion 配置，**不校验租约**
  （`armpi-debug-studio/ros2_gateway/.../server.py:84-91,220-237`）。
- 停止不联通：`/api/motion/stop` → legacy `/motion/stop`，只发 0.1 s hold，
  不锁存；`/api/teleop/stop` → system `/v1/motion/stop`，system latch 停不了
  legacy 运动。
- 默认可达性：`ARMPI_MODE=mock`、`ARMPI_HARDWARE_MOTION=false`、
  `armpi-gateway-pose` 已于 2026-11-27 mask。满足
  `ARMPI_MODE=hardware + ARMPI_HARDWARE_MOTION=1 + URL/token` 并启动
  `--enable-motion` 的 legacy gateway 即可达。
- 另一条新路径 `/api/session/intent/*`（`routes.py:262-282` →
  `session_ops.py:337-400` → `gateway_v1_intent.py:109-127`）是**设计内**：
  只转发操作员提供的 lease id，不签发租约。但 `_intent_client` 未检查
  `settings.mode`（`session_ops.py:222-235`）；mock 模式下若配置了 v1
  URL/token，仍可向真实 system 提交意图（P2）。

### D. mobile `/cmd_vel`（无 system 门禁）

```text
Nav2 controller_server / behavior_server / velocity_smoother
  jcheng-mobile/.../config/nav2_params.yaml:86-128,278,312-325
  → /cmd_vel（capability 声明域 42，launch 未设置 ROS_DOMAIN_ID）
  → 厂商 controller/mecanum.py:63-67  订阅绝对 /cmd_vel
  → /ros_robot_controller/set_motor_speeds (mecanum.py:69-72)
  → 电机板（无超时/看门狗，失流保持最后占空比）
```

- mobile 侧无 lease/deadman 代码；`capability.yaml:15-17` 仅声明。
- 厂商节点默认域 0（设计记录）；若 mobile launch 在默认环境运行，
  话题名/类型匹配，**意图直达电机**。若显式 `ROS_DOMAIN_ID=42`，厂商在 0，
  无 relay/bridge，不可达。
- 厂商 `bringup.launch.py` 在 `CHASSIS_TYPE=Mecanum` 时同时启动底盘与
  `ros_robot_controller`；`start_node.service` 开机运行 bringup。

### E. vendor 开机与 legacy 网关

- `start_node.service`（开机启用）运行厂商 bringup，startup check 会动臂；
  这不是 jcheng 指令，但属于无门禁的硬件运动。
- `armpi-gateway.service`（8765，开机启用，LAN）为 legacy 读网关，但
  `POST /motion/dispatch` 在 `--enable-motion` 时存在；`armpi-gateway-pose`
  （8766 运动）已安装但未 enable，2026-11-27 为 R10 停止并 mask。

## 3. 可达性矩阵

| 路径 | 静态 | 部署 | 默认 | 到硬件 | 租约 | deadman | 停止锁存 |
|---|---|---|---|---|---|---|---|
| A system HTTP | 是 | 手动 unit | 否 | 是 | 是 | **否（未强制）** | 是 |
| B system DDS | 是 | 无 unit | 否 | 是 | 是 | 否 | 是 |
| C studio legacy | 是 | pose 已 mask | 否 | 是（启用后） | **本地自签** | 否 | **否** |
| C' studio v1 intent | 是 | 需 v1 env | 否 | 经 system | system | system | system |
| D mobile `/cmd_vel` | 是 | 需启动 | **域 0 时是** | 是 | **无** | **无** | **无** |
| E vendor boot | 是 | 开机 | 是 | 是（startup check） | 无 | 无 | 无 |

## 4. 风险登记

### P1 — Critical（安全前置）

1. **mobile `/cmd_vel` 无门禁直达电机**
   - 证据：`nav2_params.yaml:86-128,312-325`、`capability.yaml:20-22`、
     厂商 `mecanum.py:63-72`、`mobile_nav.launch.py` 无域设置。
   - 影响：Nav2 意图可在无租约、无 deadman、无超时的情况下驱动底盘；
     失流保持最后占空比。
   - 整改：launch 固定域 42 + 启动断言；system 增加 base intake（租约 +
     deadman + 电机桥）；厂商 mecanum 从开机 bringup 移除或由 system 接管；
     台架验证失流停车（需单独授权）。

2. **studio legacy 第二执行权威**
   - 证据：`routes.py:384,418,430`、`motion_ops.py:224,348`、
     `hardware.py:1270`、`lease.py:36-115`、legacy `server.py:220-237`。
   - 影响：启用后可绕过 system 租约/安全/停止锁存；两套停止互不联通。
   - 整改：三个 legacy 写端点默认 410/移除；退役 `--takeover` 与
     `armpi-gateway-pose`；`/api/control/acquire` 明确为 UI 并发锁；
     capability 与实现对齐。

3. **system DDS `ExecuteMotion` 无鉴权**
   - 证据：`jcheng_vendor/node.py:107-166,167,380-405`。
   - 影响：同域参与者可 arm + lease + execute；无 systemd 单元但可手工启动。
   - 整改：DDS 路径加 SROS2/域隔离或显式 token/授权；未启用前在文档中
     标为 test-only，不随部署镜像安装。

### P2 — High

4. **deadman 未在硬件路径强制**（`authority.py:121,207-234`；仅 teleop 使用）。
5. **租约 DELETE 无 holder 校验**（`gateway.py:253-254` → `authority.py:174-180`）。
6. **token 出现在 docker exec argv + 容器内 root**（`run.sh:29-31,50`）。
7. **studio mock 模式可向真实 system 提交意图**（`session_ops.py:222-235`）。
8. **`expected_profile_hash`/`require_measured_state` 由客户端赋值**（`models.py:419`、`safety.py:419-422`）。

### P3 — Medium/Low

9. studio 持有设备描述/感知算法/统计评测（`configs/joint_mapping.yaml`、
   `takeover.yaml`、`domain/locate.py`、`jcheng_stats`），与 devices/perception/
   benchmark 重叠。
10. teleop `core/authority.py` 是离线模式状态机；`supervised/authorization.py`
    是本授权记录，不是租约；当前不可达硬件，语义需在集成时收紧。
11. perception `Phase` 任务状态机（`types.py:27-34`）属于 applications/scenarios。

## 5. 立即建议

1. **暂停**以下实机运行，直到 P1-1/P1-2 关闭：
   - 任何 mobile Nav2 底盘运动；
   - 任何 studio legacy 运动（`/api/motion/execute`、`/api/chassis/pulse`、
     `/api/motion/stop`）；
   - 任何 `--enable-motion` legacy gateway 或 `armpi-gateway-pose` 恢复。
2. **不要**设置 `ARMPI_HARDWARE_MOTION=1`、不要启动 `armpi-gateway-pose`、
   不要在未固定域的情况下启动 mobile bringup。
3. system-only 受监督运动：先核对部署树版本（部署证据为 0.1.0/`0b8d72…`，
   审计树为 0.3.0-dev0/`afca22…`），再按现有逐会话授权流程进行。
4. 在 `check_boundaries` 的 B4 规则中把上述路径列为 Critical finding。
5. 本审计未触发任何运动；以上为静态结论，需台架/实机验证的部分已在 §6 标注。

## 6. 证据缺口（需实机或运行时确认）

- 机器人容器/启动 shell 的实际 `ROS_DOMAIN_ID` 与 RMW。
- `start_node.service`、`CHASSIS_TYPE=Mecanum`、mecanum 节点是否运行。
- `/cmd_vel` 实际发布者数量、QoS、频率（`ros2 topic info -v`）。
- legacy 8765 是否带 `--enable-motion`；`/etc/armpi-gateway/*.env` 内容。
- 电机板失流后是否保持最后占空比（代码显示无看门狗）。
- 部署树 0.1.0 与审计树 0.3.0-dev0 的安全门禁差异。
- 工作区外是否存在主机级 domain bridge/relay。

## 7. 方法与限制

- 只读：代码阅读、静态调用链、配置/部署材料；未 import 目标仓、未运行节点、
  未 ssh、未发送运动。
- 结论强度：调用链为代码级证据；"默认可达"基于 env 默认值与已安装 unit；
  运行时域/QoS/进程状态需实机确认。
- 本报告不构成运动授权，也不替代 `jcheng-system/docs/SAFETY.md`。

## Related

- [边界规范](../repo-boundaries.md)
- [迁移方案](04-migration-plan.md)（MIG-06/MIG-07）
- [回归基线](05-regression-baseline.md)
