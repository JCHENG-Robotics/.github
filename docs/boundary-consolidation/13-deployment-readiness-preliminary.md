# Deployment Readiness — 初步评估（实机恢复前置）

> Status: **NOT READY (2026-11-27)**. 本文件是 Phase 1 设计阶段的初步门禁评估；
> 不是实机授权，也不替代逐会话操作员授权。未启动机器人、未发送运动。

## 1. 结论

当前**不具备恢复实机运动的条件**。原因不是单点缺陷，而是三条同时成立：

1. 两条 P1 执行旁路（studio legacy、mobile `/cmd_vel`）尚未整改。
2. 部署树是 0.1.0/`0b8d72…`，开发树是 0.3.0-dev0/`afca22…`；部署侧门禁未验证。
3. base 没有 system 统一授权入口；DDS Action 无鉴权；deadman 未在硬件路径强制。

system-only 的受监督单关节/夹爪运动也应在部署树对齐、P1 整改完成后再评估。

## 2. 就绪矩阵

| 维度 | 状态 | 阻塞项 |
|---|---|---|
| 契约版本 | ❌ | 部署/开发/锁三平面不一致；六个仓旧 pin |
| 执行权威 | 🟡 | System HardwareAuthority + base intake 已离线实现；base 无真实硬件桥；cross-process 租约共享未实现 |
| 停止覆盖 | 🟡 | studio legacy 默认 410；stop 唯一走 system；未实机验证 |
| 租约 | 🟡 | holder/deadman/revoke 已实现；base 默认 `lease_source=none` fail-closed |
| deadman | 🟡 | 默认强制（300 ms provisional）；显式 opt-out 需 manager flag |
| DDS Action | 🟡 | 特权服务默认不创建；域 41+SROS2 标记门禁；ExecuteMotion 无 holder 字段 → fail-closed |
| watchdog | 🟡 | base/watchdog core 已实现；未部署 systemd、未上机 |
| 测试证据 | 🟡 | system 190 / mobile 50 / studio 13+222 / learning 68；无 Humble/实机 |
| 独立 QA | 🟡 | 首轮 Rework 已修复，re-QA 进行中；Board 签核未完成 |
| 冻结基线 | ✅ | `v1.0.0` tag/SHA 完整；HEAD 不作为基线 |
| 新仓准入 | ✅ | devices/scenarios 57/62 passed |

**2026-11-27 20:40 更新**：Phase 1 离线实现与 QA Rework 已提交（system
`220b0ce`、mobile `cd491c5`、studio `63266a2`）。这不改变 **NOT READY**
结论：base 硬件桥、跨进程租约共享、部署树对齐、Humble/台架验证、re-QA
与 Board 签核仍未完成。

## 3. 恢复实机运行的前置条件（建议清单）

- [ ] P1-1：mobile 固定域 42 + system base intake + 厂商 mecanum 不再直连。
- [ ] P1-2：studio legacy 三个写端点默认 410；本地租约降为 UI 锁；停止唯一走 system。
- [ ] System：HardwareAuthority 唯一出口；DDS Action 默认不部署或加 SROS2/域门禁。
- [ ] System：deadman 强制；DELETE/renew holder 校验；revoke 接入 stop。
- [ ] 部署树：0.1.0 → 0.2.0/0.3.0 对齐，重新生成部署证据与 profile hash。
- [ ] 离线验收：未授权拒绝、租约过期、通信中断、停止不可绕过、异常退出。
- [ ] 独立 QA：由非实施 Agent 验收并签署。
- [ ] 契约：interfaces 0.3.0 发布（或明确 0.2.0 兼容窗口），锁与 manifest 一致。
- [ ] 运维：base watchdog、safety watchdog 上机验证（台架，需单独授权）。
- [ ] 操作员：逐会话书面授权、清场、预检、证据记录。

## 4. 当前可做 / 不可做

| 可做（离线） | 不可做（未批准） |
|---|---|
| mock/单测/隔离仿真 | 启动机器人、恢复运动权限 |
| 静态门禁 report-only | 发送真实运动指令 |
| 契约/设计评审 | 修改生产部署 |
| 文档与证据整理 | 台架/实机测试 |

## 5. 说明

- 本评估基于静态审计与本地测试；运行时域/QoS/进程状态仍需实机确认。
- 任何"通过"都必须有 L2/L3 离线证据；L5 需要单独授权与部署树对齐。
- 本文件不构成安全认证。

## Related

- [执行权限审计](02-runtime-authority-audit.md)
- [加固设计](10-authority-hardening-design.md)
- [契约与回归](11-contract-regression-report.md)
- [边界检查报告](12-architecture-boundary-check-report.md)
