# 许可证与第三方依赖审查（M1 门禁）

> 状态：**pending，未批准。**
> 规则：审查完成并签字前，三个新仓库**不得添加 `LICENSE` 文件**，不得对外宣称 MIT。
> 公开仓库在无许可证时默认版权保留（all rights reserved），这是临时状态。

## 1. 目标

为 `JCHENG-Robotics` 首批仓库确定：

1. 原创代码/文档的版权持有人与许可证（建议 MIT，待确认）。
2. 第三方依赖的许可证清单与兼容性结论。
3. 是否需要 `THIRD_PARTY_NOTICES.md`、SBOM、源码分发或动态链接说明。
4. 厂商资产、网格、固件、数据的再分发边界。

## 2. 版权

| 项 | 当前事实 | 待确认 |
|---|---|---|
| 原创代码/文档 | `jcheng-manipulation` 现有 `LICENSE` 为 MIT，版权人 `Kewei (Jericho) Cheng` | 新仓库是否沿用同一版权人/年份 |
| 贡献者 | 目前主要为个人项目 | 是否需要 CLA/DCO |
| 厂商代码 | `armpi_ultra_ws_clean` 私有、不发布 | 不得复制进新仓库 |
| 厂商网格/资产 | `THIRD_PARTY_NOTICES.md` 声明不在 MIT 下再许可 | 新仓库不得包含 |
| 文档 | 本设计文档为原创 | 是否与代码同许可证 |

## 3. 第三方依赖清单（待逐项核实）

> 下表来自 v1.0.0 审计与已知技术栈；许可证字段需要以实际版本为准复核，
> 不能仅凭本表对外声明。

| 依赖 | 用途 | 已知/推定许可证 | 分发方式 | 风险 |
|---|---|---|---|---|
| ROS 2 Humble | 运行时 | Apache-2.0 | 系统包/容器 | 低；需保留 notices |
| MoveIt 2 | 规划 | BSD-3-Clause | 系统包/容器 | 低 |
| Pilz industrial motion planner | 规划 | BSD-3-Clause（待核实） | 系统包 | 低 |
| Orocos KDL / PyKDL | 运动学 | LGPL-2.1（待核实） | Python 扩展 | **中**；动态链接/分发需复核 |
| urdf_parser_py | URDF 解析 | BSD-3-Clause（待核实） | Python 包 | 低 |
| xacro | URDF 宏 | BSD-3-Clause（待核实） | Python 包 | 低 |
| OpenCV | 视觉 | Apache-2.0（4.5+） | 系统包 | 低；需保留 notices |
| NumPy | 数值 | BSD-3-Clause | Python 包 | 低 |
| PyYAML | 配置 | MIT | Python 包 | 低 |
| FastAPI | 网关/后端 | MIT | Python 包 | 低 |
| uvicorn | ASGI | BSD-3-Clause | Python 包 | 低 |
| pydantic | 模型 | MIT | Python 包 | 低 |
| React / Vite / TypeScript | 前端 | MIT / MIT / Apache-2.0 | npm 包 | 低 |
| Playwright | E2E | Apache-2.0 | npm 包 | 低；浏览器二进制另计 |
| CycloneDDS | DDS | EPL-2.0 / EDL（待核实） | 系统包/容器 | **中**；容器分发需复核 |
| Eclipse Cyclone DDS | DDS | EPL-2.0（待核实） | 系统包 | 中 |
| Librealsense | D435i | Apache-2.0 | 系统包/补丁 | 低；补丁需保留 |
| SQLite | 事件存储 | Public Domain | Python 标准库 | 低 |
| GitHub Actions（第三方） | CI | 各自许可证 | 仅引用，不 vendoring | 低；固定 SHA |
| 厂商 ArmPi 代码/固件 | 硬件栈 | 厂商许可 | 私有、不发布 | **高**；禁止再分发 |
| Contributor Covenant | 行为准则 | CC BY 4.0 | 未采用；本项目自写 | 低；若采用需署名 |

## 4. 审查问题

- [ ] 新仓库的版权持有人、年份、许可证是否与基线一致？
- [ ] LGPL（PyKDL）是否会被静态链接、随容器分发或被修改？
- [ ] EPL（CycloneDDS）是否随运行时镜像分发？需要哪些 notices？
- [ ] 是否发布 wheel/容器/源码包？不同分发方式触发不同义务。
- [ ] 是否需要 SBOM（CycloneDX）与 `THIRD_PARTY_NOTICES.md`？
- [ ] 厂商资产、标定数据、证据图片是否包含第三方版权？
- [ ] 是否有商标（ArmPi、HiWonder、Aurora、RealSense）使用限制？
- [ ] 是否接受 DCO（Developer Certificate of Origin）而非 CLA？
- [ ] 公开仓库在无许可证期间的临时声明是否足够清晰？

## 5. 结论（待填写）

| 项 | 结论 |
|---|---|
| 原创代码许可证 | 待定（建议 MIT） |
| 文档许可证 | 待定（建议与代码一致） |
| 第三方兼容性 | 待核实 |
| 分发义务 | 待核实 |
| 批准人/日期 | 待填写 |

## 6. 批准后的动作

1. 添加 `LICENSE`（建议 MIT，版权行与基线一致）。
2. 添加 `THIRD_PARTY_NOTICES.md`（如需要）。
3. 更新各仓库 README 的许可证段落。
4. 在 `jcheng-system/docs/evidence/` 记录审查结论。
5. 重新运行 `scripts/verify_m1.sh`，确认许可证状态从 `pending` 变为已批准。

**在完成上述动作前，不得把“MIT”写入仓库元数据或对外说明。**
