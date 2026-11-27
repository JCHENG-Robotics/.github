# Architecture Boundary Check Report — report-only

> Status: **v1.0 (2026-11-27)**. `check_boundaries` 已实现为 report-only；未接入 CI、
> 未阻断任何构建、未提交。全生态只读运行一次；本报告给出结果、误报/漏报评估与
> CI 接入方案。静态门禁不能证明运行时安全。

## 1. 实现与证据

| 项 | 内容 |
|---|---|
| 脚本 | `.github/scripts/check_boundaries.py`（未 commit） |
| 测试 | `.github/scripts/test_check_boundaries.py`，**17 passed** |
| 运行 | `python3 .github/scripts/check_boundaries.py --root . --mode report` |
| 输出 | `evidence/20261127_boundary/boundary-report.json` / `.md` |
| 范围 | 16 个仓（含 `.github`）；只解析 AST/YAML/git 只读，不 import 目标仓 |
| 退出码 | report 模式恒为 0 |
| 运行时间 | < 10 s（本地） |

规则覆盖：B1 依赖方向、B2 硬件访问、B3 运行时面、B4 运动执行旁路、B5 manifest
合规、B6 契约版本/锁/部署树、B7 Schema 所有权、B8 设备/场景事实源、B9 冻结基线、
B10 生成式副本 provenance、B11 Git 审计。

## 2. 结果摘要

> 本节是**加固前**快照（31 open / 2 Critical）。加固后的重跑见 §9
> （29 open / 1 Critical，mobile B4 已消除，studio B4 已登记豁免）。

| 严重度 | 数量 |
|---|---|
| Critical | 2 |
| High | 14 |
| Medium | 13 |
| Low | 2 |
| **合计** | **31** |

### Critical

| 规则 | 仓库 | 证据 | 结论 |
|---|---|---|---|
| B4 | `jcheng-mobile` | `capability.yaml` 声明 `/cmd_vel` | 无 system base intake；域漂移即可达厂商电机 |
| B4 | `jcheng-studio` | `backend/app/adapters/hardware.py` `/motion/dispatch` | legacy 第二执行权威 |

### High

| 规则 | 仓库 | 证据 | 结论 |
|---|---|---|---|
| B5 | interfaces / system | 无 `capability.yaml` | 准入 manifest 缺失 |
| B6 | system | R10 部署 `0b8d72…` vs 开发 `afca22…` | 部署树与开发树不一致 |
| B6 | teleop / studio / applications | manifest 范围 `>=0.1,<0.2` vs 锁 `>=0.2,<0.3` | 契约范围冲突 |
| B3 | teleop | `publisher.py` 创建 publisher，manifest 空 runtime | 声明与代码不一致 |
| B8 | perception | `types.py` `class Phase` | 任务阶段在 scenarios 之外 |
| B8 | learning / teleop / simulation / studio | 设备 profile 副本无 `device_id`/`source` | 设备事实重复 |
| B8 | applications | `model.py` 硬编码 `2.22` | 夹爪范围重复 |
| B7 | interfaces / perception / learning | 无 `SCHEMA_OWNERSHIP.md` | Schema 归属未登记 |

### Medium / Low

- Medium：B7 三个仓；B5 perception/benchmark/ops legacy manifest；B6 studio 版本
  0.8.0 vs 锁 0.7.0；B10 五个设备副本无 provenance；B11 `.github` 分支上游指向
  `origin/main`。
- Low：B11 manipulation/mobile 历史 merge commit（非本专项产生）。

## 3. 误报评估

| 规则 | 误报 | 处理 |
|---|---|---|
| B4 | 初版把 checker 自身与 `jcheng-manipulation/armpi_ultra_ws_clean/docs/original/` 判为旁路 | 已排除 `.github`、frozen baseline、`docs/original`、`tools/legacy` |
| B9 | 初版把 GitHub `/blob/main/` 文档链接与含 SHA 的 `HEAD a08b8b6` 判为移动引用 | 收紧为 `@main`/`HEAD`/`branch main` 且无 7+ 位 SHA；排除 `.github` |
| B11 | 初版把所有 feature-branch merge commit（多为 `Merge origin/main`）判为 Medium | 过滤 `Merge origin/main`/`remote-tracking`，降为 Low |
| B8 | 初版对所有仓重复报告同一设备副本 | 按 repo 前缀归属 |

当前 31 条中未见明确误报；B11 两条 Low 属于历史操作，不是本轮违规。

## 4. 漏报评估

| 规则 | 漏报/限制 | 后续 |
|---|---|---|
| B1 | 只解析 Python；C++/launch 依赖未覆盖 | 增加 `package.xml`/CMake 解析（后续） |
| B2 | 只看 Python token；YAML 配置中的 `/dev/*` 未扫描 | 增加 config 扫描并豁免只读白名单 |
| B3 | 只检测 `create_publisher/subscription`；DDS action server 未覆盖 | 增加 action/service 检测 |
| B4 | `/cmd_vel` 只从 manifest 检测；launch remap 未覆盖；DDS 实际订阅关系无法静态证明 | 增加 launch 解析 + 明确"静态不可证明" |
| B6 | 无法证明远端 tag 与本地一致；`system_api` 无版本源 | 需 CI 拉取 tag 或锁校验 |
| B7 | 只统计 `*.schema.json`；teleop 13 个代码内 Schema 未计入 | 增加代码内 schema ID 扫描 |
| B8 | system 部署实例被 D-09 允许，不判重复；设备能力语义兼容未校验 | Phase 2 增加语义校验 |
| B9 | 只扫 Markdown；代码/配置中的冻结引用未覆盖 | 增加全文件扫描 |
| B10 | 只覆盖已知设备副本；场景/资产副本未覆盖 | 扩展清单 |
| B11 | 无法检测远端 push（只读本地）；无法归因操作者 | 需 CI 审计日志 + 提交签名 |

**结论**：当前只适合 report-only。B4/B6 的 Critical/High 命中与人工审计一致；
静态检查不能替代运行时验证。

## 5. CI 接入方案（待批准）

| 阶段 | 触发 | 行为 | 退出条件 |
|---|---|---|---|
| A 本地 | 手动 | 生成报告，exit 0 | 已完成 |
| B PR 报告 | `pull_request` | 上传 JSON/MD artifact；PR 评论摘要；不阻断 | 连续 2 个发布周期误报 ≤ 2% |
| C main 报告 | `push main` | 记录趋势 | 无未解释 Critical |
| D required | 治理评审批准 | 仅 B2/B4/B6/B8 阻断 | 有豁免流程与回滚 |

- 工作流放在 `.github/.github/workflows/org-health.yml` 或新 `boundary-report.yml`；
  只用 `actions/checkout`（SHA pin）+ `setup-python`（SHA pin）。
- 依赖：PyYAML；不安装目标仓依赖。
- Artifact：`boundary-report.json`、`boundary-report.md`、运行日志。
- 豁免：`.github/boundary-waivers.yaml`（rule/repo/reason/owner/expiry/evidence）；
  Critical 安全规则不可豁免，只能人工评审记录。
- 不做：不发布、不改产品仓、不执行目标仓代码、不连接 DDS/硬件。

## 6. 推荐首批整改（与 Phase 1 对齐）

1. **B4 mobile**：Phase 1 base intake + 域固定（MIG-07）。
2. **B4 studio**：legacy 410 + 移除本地租约（MIG-06）。
3. **B6 system 部署树**：先对齐 0.1.0 → 0.2.0/0.3.0，再做任何实机结论。
4. **B5 interfaces/system**：补 manifest（不改变运行时）。
5. **B7 interfaces/perception/learning**：补 `SCHEMA_OWNERSHIP.md`。
6. **B8 devices**：MIG-01 的生成式副本 + 引用。

## 7. 治理门禁 allowlist（已批准并实现）

原 M1 gate 禁止 `.github` 中任何 `.py`。Decision C 批准最小 allowlist：
`scripts/check_python_policy.sh` 只放行 `check_boundaries.py` 与其测试，
包括 symlink、嵌套、隐藏文件与近似后缀的拒绝用例。**8/8 allowlist tests、
17 checker tests、`org_gate=0`**；详见
[15-m1-allowlist-test-report.md](15-m1-allowlist-test-report.md)。

`check_boundaries` 仍为 report-only；未接入阻断式产品 CI。

## 8. 实施与交付状态

- 脚本、allowlist 与本报告已提交到 `feat/controlled-git-20261127`，
  PR #28（stacked on #27）。
- 未修改产品仓实现；未接入阻断式 CI；未启动机器人。
- 静态结果不构成运行时安全证明。

## 9. 加固后重跑（2026-11-27）

在 mobile/studio 离线实现提交后重跑：

| 项 | 加固前 | 加固后 |
|---|---|---|
| open findings | 31 | **29** |
| mobile B4 `/cmd_vel` | Critical | **已消除**（发布 `/jcheng/intent/base`） |
| studio B4 | `/motion/dispatch` 主路径 | 仅 `backend/app/legacy_motion.py`（默认 410/隔离） |
| system B6 部署树 | High | High（部署未改，按批准保持） |
| 设备副本 B8/B10 | 5 组 | 5 组（Phase 2 处理） |

studio 的 B4 仍为 Critical 报告：代码仍存在，只是默认不可达；在 legacy
被删除前，静态门禁不会把它当已消除。已登记正式豁免
`W-2026-11-27-01`（`boundary-waivers.yaml`，到期 2026-12-31，owner
`jcheng-studio`），报告状态为 waived，不是 eliminated。运行时可达性由
studio 测试覆盖（410、双开关、stop 走 system）。

## Related

- [门禁设计](08-check-boundaries-design.md)
- [执行权限审计](02-runtime-authority-audit.md)
- [加固设计](10-authority-hardening-design.md)
- [迁移计划](04-migration-plan.md)
