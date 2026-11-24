# 仓库分类与依赖方向

| 层 | 仓库 | 职责 | 禁止 |
|---|---|---|---|
| L0 | `.github` | 治理、模板、复用 CI、组织策略、生态级文档 | 产品代码、机器人配置、密钥 |
| L1 | `jcheng-interfaces` | ROS IDL、HTTP/WS/配置/证据 Schema、契约哈希 | 节点、硬件访问、厂商依赖 |
| L2 | `jcheng-system` | 安全、仲裁、运动、硬件桥、网关、部署、锁 | 运行时依赖 L3/L4 |
| L3 | `jcheng-manipulation` | 冻结 `v1.0.0` 实验基线（参考） | 被新系统运行时依赖 |
| L3 | `jcheng-mobile` | 移动底盘：激光里程计、SLAM、Nav2 底盘意图 | 发布厂商话题、打开串口、伪造里程计 |
| L3 | `jcheng-perception` | 边云分布式感知，输出建议位姿 | 发布运动命令、打开相机设备、伪造深度/TF |
| L3 | `jcheng-teleop` / `jcheng-learning` | 遥操作 / 学习（计划中） | 发布厂商话题、打开串口、加入硬件域 |
| L4 | `jcheng-applications` | 任务编排、操作界面（计划中） | ROS 硬件话题、rclpy 直连 |
| OPS | `jcheng-ops` | 无人值守巡检、看门狗、服务自愈 | 发送运动命令、加入 DDS 图、访问设备 |
| BENCH | `jcheng-mobile-bench` | 台架材料沙箱（不发布） | 被能力仓库或运行时依赖 |

依赖方向：L4 -> L2 API；L3 -> L1 + L2 客户端；L2 -> L1；OPS -> 仅 HTTP 健康端点；L0 -> 所有（仅 CI）。
`jcheng-mobile-bench` 不在依赖图中。

## 文档要求

每个产品仓库（L1–L4 与 OPS）必须具备，且结构遵循
[`documentation-standard.md`](documentation-standard.md)：

- [ ] `README.md`（英文主文档）与 `README.zh-CN.md`（中文对照）。
- [ ] `ROADMAP.md`：里程碑、状态、证据链接、下一步与范围外事项。
- [ ] `CHANGELOG.md`：Keep a Changelog 1.1.0 + SemVer，仅英文。
- [ ] `ACCEPTANCE.md`：L0–L5 分层、已验证/未验证、限制与签署；仅英文。
- [ ] 上述文档中的状态只使用标准词汇（Complete / In progress / Planned /
      Not started；Verified / Partially verified / Unverified / Inconclusive）。

`.github` 作为治理仓库维护生态级 `ROADMAP.md`、`CHANGELOG.md`、`ACCEPTANCE.md`
与双语组织主页；`jcheng-mobile-bench` 只需 `README.md` 明确标注沙箱状态。

## 新仓库准入检查

- [ ] 职责不与现有仓库重叠。
- [ ] 只通过 `jcheng-interfaces` 表达跨仓库契约。
- [ ] 默认 `hardware_access: none`。
- [ ] 有 `capability.yaml`、CI、失败语义、契约握手测试。
- [ ] 具备完整四件套文档（见上）。
- [ ] 首次接入有受监督实机证据（如涉及运动）。
