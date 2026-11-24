# <仓库名称>

<一段话：本仓库是什么，一句话范围，一句话边界。>

> 状态：**<实验性 | 已部署 | 冻结>**，截至 <YYYY-MM-DD>。
> 版本 <x.y.z>。<最重要的限制。>
> 本文为英文主文档的中文对照；如有歧义，以 [README.md](README.md) 为准。

## 范围与边界

| 项 | 本仓库 |
|---|---|
| 层 | L<0–4> |
| 输入 | <话题 / API / 文件> |
| 输出 | <话题 / API / 文件> |
| 硬件访问 | `<none | camera_readonly | ...>`（`capability.yaml`） |
| 拥有设备 | <无，或确切设备> |
| 禁止 | <设备访问、运动话题、厂商代码> |

## 仓库结构

```text
<repo>/
├── capability.yaml
├── VERSION
├── README.md
├── README.zh-CN.md
├── ROADMAP.md
├── CHANGELOG.md
├── ACCEPTANCE.md
└── <源码树>
```

## 依赖

- <操作系统 / ROS 发行版>
- <运行时依赖>
- <硬件（如有）>

## 快速开始

```bash
<构建>
<测试>
<无硬件运行>
```

## 验证状态

| 结论 | 状态 | 证据 |
|---|---|---|
| <结论> | <已验证 | 部分验证 | 未验证> | <路径> |

完整报告：[ACCEPTANCE.md](ACCEPTANCE.md)。

## 相关仓库

- [`jcheng-interfaces`](https://github.com/JCHENG-Robotics/jcheng-interfaces) — 契约来源。
- [`jcheng-system`](https://github.com/JCHENG-Robotics/jcheng-system) — 特权运行时。
- [`jcheng-ops`](https://github.com/JCHENG-Robotics/jcheng-ops) — 运维。
- [`.github`](https://github.com/JCHENG-Robotics/.github) — 生态路线图、变更日志与验收。

## 许可

许可证审查进行中；本仓库没有 `LICENSE`，默认版权保留。
详见 [LICENSE-REVIEW.md](LICENSE-REVIEW.md)。
