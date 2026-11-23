# 仓库分类与依赖方向

| 层 | 仓库 | 职责 | 禁止 |
|---|---|---|---|
| L0 | `.github` | 治理、模板、复用 CI、组织策略 | 产品代码、机器人配置、密钥 |
| L1 | `jcheng-interfaces` | ROS IDL、HTTP/WS/配置/证据 Schema、契约哈希 | 节点、硬件访问、厂商依赖 |
| L2 | `jcheng-system` | 安全、仲裁、运动、硬件桥、网关、部署、锁 | 运行时依赖 L3/L4 |
| L3 | `jcheng-manipulation` | 冻结 `v1.0.0` 实验基线（参考） | 被新系统运行时依赖 |
| L3 | `jcheng-teleop` / `jcheng-learning` / `jcheng-mobile` | 能力意图源 | 发布厂商话题、打开串口、加入硬件域 |
| L4 | `jcheng-applications` | 任务编排、操作界面 | ROS 硬件话题、rclpy 直连 |

依赖方向：L4 -> L2 API；L3 -> L1 + L2 客户端；L2 -> L1；L0 -> 所有（仅 CI）。

新仓库准入检查：

- [ ] 职责不与现有仓库重叠。
- [ ] 只通过 `jcheng-interfaces` 表达跨仓库契约。
- [ ] 默认 `hardware_access: none`。
- [ ] 有 `capability.yaml`、CI、失败语义、契约握手测试。
- [ ] 首次接入有受监督实机证据（如涉及运动）。
