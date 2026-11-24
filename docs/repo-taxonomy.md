# 仓库分类与依赖方向

| 层 | 仓库 | 职责 | 禁止 |
|---|---|---|---|
| L0 | `.github` | 治理、模板、复用 CI、组织策略 | 产品代码、机器人配置、密钥 |
| L1 | `jcheng-interfaces` | ROS IDL、HTTP/WS/配置/证据 Schema、契约哈希 | 节点、硬件访问、厂商依赖 |
| L2 | `jcheng-system` | 安全、仲裁、运动、硬件桥、网关、部署、锁 | 运行时依赖 L3/L4 |
| L3 | `jcheng-manipulation` | 冻结 `v1.0.0` 实验基线（参考） | 被新系统运行时依赖 |
| L3 | `jcheng-perception` | 分布式感知：Pi 5 采集/深度/TF/融合，笔记本 GPU YOLO（建议性输出） | 发布运动命令、独占相机或串口设备、加入厂商硬件域 |
| L3 | `jcheng-teleop` / `jcheng-learning` / `jcheng-mobile` | 能力意图源 | 发布厂商话题、打开串口、加入硬件域 |
| L4 | `jcheng-applications` | 任务编排、操作界面 | ROS 硬件话题、rclpy 直连 |
| OPS | `jcheng-ops` | 运维：健康巡检、硬件看门狗、服务自愈、事故手册（跨层，不参与运行时） | 被运行时仓库导入、发布运动命令、拥有设备 |

依赖方向：L4 -> L2 API；L3 -> L1 + L2 客户端；L2 -> L1；L0 -> 所有（仅 CI）。
`jcheng-ops` 不属于运行时分层：只通过 systemd 与本机 HTTP 接口运维部署，不被任何 L1–L4
仓库导入，也不参与运动路径。

新仓库准入检查：

- [ ] 职责不与现有仓库重叠。
- [ ] 只通过 `jcheng-interfaces` 表达跨仓库契约。
- [ ] 默认 `hardware_access: none`。
- [ ] 有 `capability.yaml`、CI、失败语义、契约握手测试。
- [ ] 首次接入有受监督实机证据（如涉及运动）。
