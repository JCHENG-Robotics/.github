# JCHENG Robotics

**可复现、受安全边界约束的机器人操作。**  
从经过实测的五自由度操作基线，走向独立版本化的机器人生态。

[English](README.md) | **简体中文**

> 本文为英文主文档的中文对照；如有歧义，以英文版为准。

**状态：** M1–M5.2 完成 · M6 进行中 · 2026-11-25 · 英文为主文档  
**从这里开始：** [生态路线图](https://github.com/JCHENG-Robotics/.github/blob/main/ROADMAP.md) ·
[验收报告](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md) ·
[冻结基线](https://github.com/JerichoCheng/jcheng-manipulation)

**目录：** [概览](#概览) · [为什么](#为什么做这件事) · [方法](#方法) ·
[当前状态](#当前状态) · [证据基础](#证据基础) · [架构](#架构) ·
[安全](#安全模型与不声称的能力) · [质量](#质量与可复现性) · [仓库](#仓库地图) ·
[路线图](#路线图) · [验收](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md) · [治理](#治理) ·
[局限](#局限与有效性威胁) · [许可证](#许可证)

---

## 概览

JCHENG Robotics 是一个面向低成本硬件、强调可靠性与可审计性的机器人操作工程组织。
它源自一项基于五自由度 ArmPi Ultra 平台的项目制硕士研究，目前正在演化为一个由明确契约、
版本管理、安全边界和可复现证据支撑的多仓库生态。

这项工作遵循两条承诺：

1. **每个结论都可追溯到证据。** 结果附有命令、日志、数据或机器可读报告；未测量的量会明确标注。
2. **每个实机运动都经过同一道边界。** 运动意图先经过校验与仲裁，之后才允许发布硬件命令；
   新模块不会获得第二条通往执行器的路径。

本计划围绕三个问题组织：

1. **测量。** 当每一个变换、关节限位、相机坐标系和失效模式都被实测而不是假设时，
   系统能达到怎样的精度与可靠性？
2. **可靠性。** 哪些修正与干预能通过预注册的配对实机试验，而不是只靠一次成功演示？
3. **架构。** 如何在不新增执行器通路、不削弱证据链的前提下持续增加新能力？

本文按工程作品集的标准组织：问题定义、方法、证据、局限与可复现性都明确写出。
英文版为主文档，中文版为对照译文。

## 为什么做这件事

低成本五自由度机械臂足以完成桌面抓取，但其集成面很脆弱。在冻结的 `v1.0.0` 基线中，
同一平台存在**六条不同的运动写入路径**、四套运行时消费者不同的限幅配置，以及至少四处重复的
关节限位或伺服映射。安全监督器只否决 MoveIt CLI 路径；快速路径被明确记录为设计上绕过它；
命令缓存可能被误认为实测状态。

基线解决了科学问题：当每一个变换、限位和失效模式都被实测而不是假设时，系统能达到怎样的
精度与可靠性。生态要解决随之而来的工程问题：**如何在不削弱安全、可复现性和证据边界的前提下，
持续增加新能力？**

## 方法

基线与生态遵循同一套“测量优先”的方法：

- **先测量平台，再建立模型。** 关节止挡、TF 坐标系、相机外参、夹爪行程与总线行为都在实机上
  普查，而不是沿用默认值。
- **优先独立验证。** 棋盘格手眼、AprilTag 尺度检查、总线寄存器完成判定与独立前视相机，
  用来避免单一来源自证。
- **预注册比较。** 配对试验在采集数据前固定假设、样本量与分析方法；协议偏差被记录，
  而不是被隐藏。
- **如实报告失败的门限。** 6 mm 误差预算门限未通过，就报告为未通过，不用更有利的统计量
  重新表述。
- **冻结证据。** `v1.0.0` 是不可变基线；新工作独立版本化，不能重写它的标签、证据或实验历史。
- **规划与执行分离。** 规划、校验、执行是不同阶段，有不同责任人与证据。

新生态再加一条规则：**架构本身必须可测试。** M3 的 Mock 栈与 S1–S17 场景，是为了在任何
受监督实机工作之前证明“不可绕过”的边界。

## 当前状态

| 项 | 状态 |
|---|---|
| 实验基线 | `jcheng-manipulation v1.0.0`，提交 `b3411e4`，已冻结；完整 G8 验收已记录 |
| 生态里程碑 | **M1–M5.2 已完成**；M6 S13 与 S17 实机 MoveIt 已验证；S14 底盘与完整 G8 待做 |
| 契约 | `jcheng-interfaces` v0.1.0：14 msg / 10 srv / 1 action，7 个 Schema，契约哈希已固定 |
| 系统运行时 | `jcheng-system` 0.3.0-dev：13 个 ROS 包；M4 只读、M5.2 核心、M6 S13 + S17 实机已验证；S14/G8 待做 |
| 运行时镜像 | `armpi-ultra:flatten-20261125`，7.1 GB arm64；20 节点 / 60 话题保持不变，重启后仍生效 |
| 能力仓库 | `jcheng-mobile` v0.1.0 静态 `/scan`/`/odom`/`/map`；`jcheng-perception` v0.1.0 对齐深度 + split edge + 单次双视图；`jcheng-ops` v0.1.0 已部署 |
| 仿真 | `jcheng-simulation` v0.1.0 实验性：确定性 mock + Gazebo Harmonic 机械臂植物，仅域 43；离线验证，无硬件路径 |
| 新生态中的实机运动 | 受监督单关节与夹爪运动已通过（M5.2）；M6 S17 实机 plan-only 通过但未执行；完整 G8 复验待做 |
| 文档 | 统一 README / ROADMAP / CHANGELOG / ACCEPTANCE；英文为主，中文 README 对照 |
| 许可证 | 多数新仓库**进行中**；`jcheng-mobile` 初始化时带有 MIT；审查需解决该例外 |

## 证据基础

以下结果来自冻结基线。它们是**基线结果**，不是新生态的结果；新生态目前还不执行运动。

| 评估 | 报告结果 | 解读 |
|---|---|---|
| 手眼标定 | 14 个位姿 2.94 mm / 0.39°；留出位姿 3.29 mm / 0.43° | 独立棋盘格验证，不依赖厂商默认值 |
| 固定点配对试验 | 12/24 对 **24/24**，McNemar p = 0.00049 | 预注册的低构型常数修正 |
| 随机落点试验 | 9/24 对 **24/24**，McNemar p = 6.1 × 10⁻⁵ | 自由摆放、腕部/前视相机定位、底盘接近 |
| 误差预算 | 平移 RSS **13.325 mm**，6 mm 门限未通过；实测放置均值 **3.080 mm** | 门限未满足；实测均值是另一个统计量 |
| 快速运动 | 抓取+放回 **11.67 s → 8.94 s**；G8 快路径落点 **2.27 mm** | S 曲线 4.0 rad/s / 20 rad/s²，总线确认 |

基线还记录了重复性（0.449 mm RMS / 1.017 mm max）、回差（1.117 mm）、夹爪 ±9 mm 容差包络，
以及完整的失效模式分类。证据索引见
[`jcheng-manipulation`](https://github.com/JerichoCheng/jcheng-manipulation)。

**批判性解读：** RSS 聚合**没有**满足 6 mm 误差预算门限；报告的放置均值在 6 mm 内，但那是不同的
统计量。快速路径只在一个方向上完成验证。以上结果都不构成安全认证。

## 架构

目标架构把**契约**、**特权执行**、**能力模块**与**应用**分开：

```text
L4  Applications        任务编排 · 操作界面 · 证据审阅
L3  Capabilities        操作 · 遥操作 · 学习 · 移动
L2  System              控制权 · 安全 · 运动 · 网关 · 遥测 · 守卫
L1  Contracts           ROS IDL · OpenAPI/WS · 配置与证据 Schema
L0  Governance          组织主页 · 模板 · 复用 CI · 分支保护

Hardware plane          唯一发布者，厂商 DDS 域 0
```

首批仓库有意保持精简；此后生态增加了独立版本化的能力与运维仓库：

| 仓库 | 职责 | 当前状态 |
|---|---|---|
| [`JCHENG-Robotics/.github`](https://github.com/JCHENG-Robotics/.github) | 治理、模板、复用 CI、生态文档 | M1 完成；文档标准 v1.0 |
| [`JCHENG-Robotics/jcheng-interfaces`](https://github.com/JCHENG-Robotics/jcheng-interfaces) | 契约、Schema、契约哈希 | v0.1.0，已签名标签 |
| [`JCHENG-Robotics/jcheng-system`](https://github.com/JCHENG-Robotics/jcheng-system) | 特权运行时、安全、仲裁、网关 | 0.3.0-dev；M6 S13 + S17 实机 |
| [`JCHENG-Robotics/jcheng-mobile`](https://github.com/JCHENG-Robotics/jcheng-mobile) | L3 移动底盘 | v0.1.0；静态 bring-up |
| [`JCHENG-Robotics/jcheng-perception`](https://github.com/JCHENG-Robotics/jcheng-perception) | L3 感知 | v0.1.0；对齐深度 + 单次双视图 |
| [`JCHENG-Robotics/jcheng-ops`](https://github.com/JCHENG-Robotics/jcheng-ops) | 跨层运维 | v0.1.0 已部署 |
| [`JCHENG-Robotics/jcheng-simulation`](https://github.com/JCHENG-Robotics/jcheng-simulation) | 离线仿真被控对象（mock + Gazebo Harmonic） | v0.1.0 实验性；仅离线验证 |

### 单一运动路径

```text
能力模块
  → 申请租约
  → ExecuteMotion（契约 + 租约 + 幂等检查）
  → 安全校验
  → 运动执行器
  → 硬件桥（唯一发布者）
  → 总线确认的结果 + 证据记录
```

由这条边界导出的设计决策：

- **控制权来自租约，而不是 UI 会话。** 租约包含作用域、优先级、TTL、deadman 与撤销语义，
  可审计、可抢占。
- **安全监督器只否决，不执行。** 它校验状态新鲜度、关节限位、轨迹速率、起点、工作空间与桌面
  间隙，并在违规时锁存停止。
- **硬件桥是唯一发布者。** 能力模块加入非特权 DDS 域；厂商域只能通过硬件桥到达。
- **MoveIt 只规划，仲裁器执行。** 控制器执行链路不作为第二条运动入口暴露。
- **实测状态不是命令回显。** `GetBusServoState` 是完成判定的权威；缓存的 `/joint_states`
  标注为 `commanded`。
- **失败关闭。** 安全心跳缺失、实测状态过期、总线读失败或结果未知都会锁存停止，不自动重试。

## 安全模型与不声称的能力

平台**没有**硬件急停、抱闸、独立编码器、力矩传感或自碰撞模型。底盘开环、无里程计。
软件停止是保持/置零命令，不是安全等级停止。

因此：

- 所有实机工作都在监督下进行，并且每次会话都需要**单独、明确**的授权。
- UI 与文档只写“软件停止”或“停止请求”，不写“急停”。
- 厂商容器重启可能移动机械臂（`startup_check`）；系统不会自动重启厂商容器。
- 新生态不是安全认证系统，不声称满足 SIL/PL。

运行时已经存在，因此这条边界是**被执行**的，而不只是声明。M4 证明了只读链路只发布遥测、
不发布命令（`writes=0`，30 分钟）。M5.1 在 Mock 栈上通过 ROS 服务/action 验证了租约、
安全与停止语义；M5.2 把同一条路径接到受监督硬件桥，完成单关节与夹爪运动。S7（状态过期注入）
与 S9（运行时发布者检测）仍未在实机单独验证，每次实机会话仍需单独、明确的授权。

## 质量与可复现性

| 门禁 | 当前状态 |
|---|---|
| 仓库检查 | M1 **111/111** 项 API 检查；三个创始仓库的 M2–M6 CI 门禁 |
| 分支保护 | PR + CODEOWNERS + 各仓库必需检查；管理员受限；禁止 force-push/删除 |
| 契约完整性 | 契约哈希 + `interface_manifest.json`，v0.1.0，标签已验证 |
| 依赖锁定 | `ecosystem.lock.yaml` 固定提交、契约哈希、profile 哈希与 interfaces v0.1.0 |
| 测试层级 | L0 契约 → L1 单元 → L2 Mock 集成 → L3 Mock E2E → L4 回放 → L5 受监督实机 |
| 防绕过验证 | S1–S17：15 个场景通过、2 个按计划跳过、必选失败 0；M5.1 另有 5 项 ROS 传输测试 |
| 实机证据 | M4 只读 1799/1799 `measured`、`writes=0`；M5.2 单关节/夹爪总线复核与停止锁存 |
| 证据 | 每次运行记录版本、哈希、命令、观察与限制 |
| 文档 | 标准 v1.0；每个产品仓库具备四件套 |

当前状态与证据汇总见[生态路线图](https://github.com/JCHENG-Robotics/.github/blob/main/ROADMAP.md)与
[验收报告](https://github.com/JCHENG-Robotics/.github/blob/main/ACCEPTANCE.md)。M1 验证 JSON 保存在
本地暂存归档 `jcheng-ecosystem-bootstrap/M1-VERIFICATION.json`；设计记录位于
`jcheng-manipulation` 的 `design/ecosystem-v1` 分支（`docs/ecosystem/`）。

## 仓库地图

| 仓库 | 角色 | 状态 |
|---|---|---|
| `.github` | 组织治理、模板、复用 CI、生态文档 | M1 完成；文档标准 v1.0 |
| `jcheng-interfaces` | ROS IDL、HTTP/WS Schema、契约哈希 | v0.1.0 |
| `jcheng-system` | 安全、控制权、运动、硬件桥、网关 | 0.3.0-dev；M6 S13 + S17 实机 |
| `jcheng-manipulation` | 冻结的 `v1.0.0` 实验基线与证据 | 只读参考 |
| `jcheng-mobile` | 移动底盘能力（M10、SLAM、Nav2 意图） | v0.1.0；静态 `/scan`/`/odom`/`/map`；运动未验证 |
| `jcheng-perception` | 边云分布式感知 | v0.1.0；对齐深度、split edge、单次双视图；重复性未验证 |
| `jcheng-ops` | 无人值守运维、看门狗与恢复 | v0.1.0 已部署 |
| `jcheng-simulation` | 离线仿真被控对象（mock + Gazebo Harmonic，域 43） | v0.1.0 实验性；仅离线验证 |
| `jcheng-mobile-bench` | 从 `jcheng-mobile` 拆出的台架材料 | 沙箱；不发布 |
| `jcheng-teleop` | 遥操作能力 | 计划中 |
| `jcheng-learning` | 数据集、训练、策略推理 | 计划中 |
| `jcheng-applications` | 任务编排与操作应用 | 计划中 |

## 路线图

| 里程碑 | 范围 | 状态 |
|---|---|---|
| M0 | 架构评审与批准 | 完成 |
| M1 | 组织、三个仓库、模板、CI 骨架 | **完成** |
| M2 | 契约审计；`jcheng-interfaces` v0.1.0 | **完成** |
| M3 | `jcheng-system` Mock 栈；租约、安全、仲裁、网关 | **完成** |
| M4 | 机器人只读接入（不运动） | **完成** |
| M5 | 受监督的单关节与夹爪执行 | **完成**（M5.1 Mock，M5.2 实机核心） |
| M6 | 基线回放与 G8 复验 | **进行中**——S13 21/21、S17 plan-only 与 S17 实机 MoveIt 通过；S14 底盘、完整 G8 待做 |
| M7 | 首个集成能力模块 | **进行中**——mobile 静态 bring-up；perception 对齐深度、split edge 与单次双视图 |
| M8 | 生态 v1.0 发布：锁文件、SBOM、验收报告 | 计划中 |

M6 是当前门禁。决策回放已与基线一致（21/21），S17 plan-only 契约已对真实
MoveIt 2.5.10 通过且未执行；剩下的是 S14 底盘、完整 G8 复跑与落点证据。
每一项都需要单独、明确的授权。M5.2 还留下 S7（状态过期注入）与 S9（运行时发布者检测）未验证。

## 治理

- 所有仓库的 `main` 均受保护：PR、独立评审、CODEOWNERS、线性历史、禁止 force-push 与删除。
  必需检查按仓库配置——治理与 perception 为 `m1-gate`；interfaces 为 `m1-gate` +
  `m2-contract`；系统运行时为五个门禁；operations 为 `ops-gate`。
- 组织已结束单账号阶段：第二评审人 `@JerichoSwaine` 已具备 maintain 权限，并在所有仓库中
  都是 CODEOWNER。`main` 变更需要一名作者与一名评审人；break-glass 不是默认路径。
- 任何实机运动都需要操作员明确授权；CI 与自动化不会触发运动。
- 安全报告遵循 [`SECURITY.md`](https://github.com/JCHENG-Robotics/.github/blob/main/SECURITY.md)；
  不要在公开 issue 中披露利用细节或凭据。
- 贡献流程遵循 [`CONTRIBUTING.md`](https://github.com/JCHENG-Robotics/.github/blob/main/CONTRIBUTING.md)
  与设计变更模板。

## 局限与有效性威胁

- **单一平台与场地。** 结果来自一台 ArmPi Ultra、一张桌面和少量受监督会话，不构成群体级
  可靠性结论。
- **没有硬件安全链。** 无急停、抱闸、独立编码器、力矩传感或里程计。
- **仅 TCP 几何守卫。** 工作空间与桌面检查针对工具点；连杆与夹爪碰撞不在模型内。
- **底盘开环。** 任何底盘运动都会使桌面标定失效；底盘没有里程计。
- **快速路径范围。** 4.0/20 档有总线确认，但只在一个方向上完成验证。
- **误差预算门限。** 6 mm RSS 门限未满足；实测放置均值是另一个统计量，不能解读为通过门限。
- **新生态成熟度。** M6 尚未完成：S14 与完整 G8 复跑待做，S7/S9 未验证。mobile 只有
  静态 bring-up；perception 只有单次双视图，且腕部深度 reader 仍可能卡死。不对两者做运动声明。
- **运维覆盖。** 看门狗尚未在真实卡死中触发；整机重启路径未演练，因为厂商启动序列会移动机械臂。
- **许可证状态。** 基线与 `jcheng-mobile` 为 MIT；其余新仓库（包括
  `jcheng-simulation`）没有 `LICENSE`，审查完成前不授予复用许可。mobile 的文件
  保留待审查，不构成先例。

## 许可证

冻结的 `jcheng-manipulation v1.0.0` 基线为 MIT。`jcheng-mobile` 在初始化时已带有一份
MIT `LICENSE`。其余新仓库（`.github`、`jcheng-interfaces`、`jcheng-system`、
`jcheng-perception`、`jcheng-ops`、`jcheng-simulation`）**没有 `LICENSE`**：第三方依赖
与版权审查仍在进行。
审查批准前，这些仓库不授予 MIT 许可，厂商资产不参与再分发。`jcheng-mobile` 的文件
**保留待审查**（见其 `LICENSE-REVIEW.md`），不构成给其他仓库添加许可证的先例。详见
[`license-review.md`](https://github.com/JCHENG-Robotics/.github/blob/main/docs/license-review.md)。

## 引用

如需引用实验基线，请使用：

```bibtex
@software{jcheng_manipulation_2026,
  author  = {Cheng, Kewei (Jericho)},
  title   = {JCHENG Manipulation: A ROS 2-Based Robotic Manipulation System with Quantitative Reliability Evaluation},
  year    = {2026},
  version = {1.0.0},
  url     = {https://github.com/JerichoCheng/jcheng-manipulation}
}
```

## 联系

- 设计与契约问题：在对应仓库开 `design` issue。
- 安全：遵循 `SECURITY.md`；不要公开提交利用细节。
- 实机工作：与操作员协调；不接受远程运动请求。

基线的证据索引、失效模式分类与完整实验记录，仍是该平台实测行为的权威参考。
