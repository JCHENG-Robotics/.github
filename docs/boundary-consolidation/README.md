# Boundary Consolidation — 交付索引

> Status: **v1.0 (2026-11-27)**. 本目录是 Ecosystem Boundary Consolidation
> 专项的证据与设计交付；只读诊断 + 治理文档，不含其他仓库的实现修改。

| 文件 | 交付物 | 说明 |
|---|---|---|
| [`../repo-boundaries.md`](../repo-boundaries.md) | Repo Boundary Specification | 10 节规范 + 6 张矩阵 + D-01…D-10 决策 |
| [`01-source-of-truth-matrix.md`](01-source-of-truth-matrix.md) | Source of Truth Matrix | 概念 × 声明源 × 运行时权威 × 已知副本 |
| [`02-runtime-authority-audit.md`](02-runtime-authority-audit.md) | Runtime Authority Audit | 意图→硬件调用链、可达性、风险与整改 |
| [`03-contract-compatibility-matrix.md`](03-contract-compatibility-matrix.md) | Contract Compatibility Matrix | 契约版本、pin、锁、部署证据 |
| [`04-migration-plan.md`](04-migration-plan.md) | Migration Plan | MIG-01…MIG-10，9 项字段/项 |
| [`05-regression-baseline.md`](05-regression-baseline.md) | Regression Baseline | 快照、测试结果、回滚点 |
| [`06-admission-report.md`](06-admission-report.md) | 新仓准入验收报告 | devices / scenarios |
| [`07-file-changelog.md`](07-file-changelog.md) | 文件变更清单及测试证据 | 变更范围与未变更声明 |
| [`08-check-boundaries-design.md`](08-check-boundaries-design.md) | 边界门禁设计 | report-only，B1–B12 |
| [`09-git-operation-audit.md`](09-git-operation-audit.md) | Git Operation Audit | 本会话全部 Git 写操作、commit/merge、HEAD 归因与合规判定 |
| [`10-authority-hardening-design.md`](10-authority-hardening-design.md) | Runtime Authority Hardening Design | Mobile/Studio/System 整改设计（待审查，未实施） |
| [`11-contract-regression-report.md`](11-contract-regression-report.md) | Contract & Regression Report | 版本关系、pyarrow 根因、分层回归方案 |
| [`12-architecture-boundary-check-report.md`](12-architecture-boundary-check-report.md) | Architecture Boundary Check Report | report-only 运行结果、误报/漏报、CI 接入方案 |
| [`13-deployment-readiness-preliminary.md`](13-deployment-readiness-preliminary.md) | Deployment Readiness Assessment | **NOT READY**；实机恢复前置条件清单 |
| [`14-git-operation-log.md`](14-git-operation-log.md) | Git Operation Log | 受控 Git 操作、commit、push、PR、CI |
| [`15-m1-allowlist-test-report.md`](15-m1-allowlist-test-report.md) | M1 Allowlist Test Report | 8/8 allowlist cases；checker 20 tests；gate OK |
| [`16-learning-regression-report.md`](16-learning-regression-report.md) | Learning Regression Report | 隔离环境 68 passed；PR #5 |
| [`17-authority-hardening-implementation-report.md`](17-authority-hardening-implementation-report.md) | Runtime Authority Implementation | System/Mobile/Studio 实现、状态机、16 项故障矩阵 |
| [`18-independent-qa-report.md`](18-independent-qa-report.md) | Independent QA Report | **PASS**；Rework 关闭；可 push/PR，不可 merge |
| [`19-remote-delivery-report.md`](19-remote-delivery-report.md) | Remote Delivery Report | 9 个 PR；mobile #6 冲突阻塞；未 merge |
| [`20-file-changes-and-rollback.md`](20-file-changes-and-rollback.md) | File Changes & Rollback | 文件/测试/回滚 SHA 汇总 |
| [`21-pr-merge-integration-report.md`](21-pr-merge-integration-report.md) | PR Merge & Integration Report | 3 merged；6 blocked；门禁与依赖核查 |
| [`22-safety-parameter-validation-plan.md`](22-safety-parameter-validation-plan.md) | Safety Parameter Validation Plan | 200 ms / 300 ms provisional；台架验证方法 |
| [`23-studio-waiver-verification.md`](23-studio-waiver-verification.md) | Studio Waiver Verification | 默认不可达、过期检查、移除计划 |
| [`24-phase2-source-of-truth-design.md`](24-phase2-source-of-truth-design.md) | Phase 2 Device/Scenario Design | MIG-01/02 + ArmPi×ore_sorting 设计（未实施） |
| [`25-ecosystem-integration-baseline-1-manifest.md`](25-ecosystem-integration-baseline-1-manifest.md) | Baseline 1 Manifest | **INCOMPLETE**；main SHA/版本/风险 |
| [`26-post-merge-regression-report.md`](26-post-merge-regression-report.md) | Post-Merge Regression | 实际 main 基线 + 分支证据；Baseline 未达成 |
| [`27-mobile-conflict-resolution-report.md`](27-mobile-conflict-resolution-report.md) | Mobile Conflict Resolution | #6 → 新 main 分支移植；树等价；QA PASS；PR #7 |
| [`28-phase2-implementation-status.md`](28-phase2-implementation-status.md) | Phase 2 Implementation Status | 设计完成；实现在本轮启动 |
| [`29-system-conflict-resolution-report.md`](29-system-conflict-resolution-report.md) | System Conflict Resolution | #41 已合并；本地树=main；191 tests |
| [`30-studio-conflict-resolution-report.md`](30-studio-conflict-resolution-report.md) | Studio Conflict Resolution | #10 已合并；本地树=main；13+222 tests |
| [`31-status-model.md`](31-status-model.md) | Status Model | Development / Main / Deployment 三平面 |
| [`32-technical-debt-register.md`](32-technical-debt-register.md) | Technical Debt Register | 16 项；blockers 与 closure |
| [`33-board-review-packet.md`](33-board-review-packet.md) | Board Review Packet | 全部 Wave PR 已合并；无 pending approval |
| [`34-boundary-report-main.md`](34-boundary-report-main.md) | Boundary Report — Main | 12 open + 1 waived；0 open Critical |
| [`35-baseline-manifest-updated.md`](35-baseline-manifest-updated.md) | Baseline Manifest Updated | **INCOMPLETE**；main SHAs/tests |
| [`36-deployment-readiness-updated.md`](36-deployment-readiness-updated.md) | Deployment Readiness Updated | **NOT READY**；deployment FAIL |
| [`37-armpi-ore-sorting-reference-result.md`](37-armpi-ore-sorting-reference-result.md) | ArmPi × ore_sorting Reference Result | 组件通过；真实工件 fail-closed；Baseline 未达成 |

## 审批状态

| 项 | 状态 |
|---|---|
| Wave 1–4 PRs | **已合并**（#27/#28/#29/#2/#1/#5/#19/#41/#10/#7；#6 closed superseded） |
| Main 集成 QA | **PASS**（Development/Main；Deployment FAIL） |
| Phase 2 MIG-01/02 | 组件实现完成（Draft PR devices #3、scenarios #2、applications #18） |
| ArmPi × ore_sorting | fixture 路径通过；真实 CLI 工件 fail-closed（37） |
| Baseline 1 | **INCOMPLETE**（artifact schema/vocabulary 未收敛） |
| 实机/部署 | **NOT READY / 未授权** |

## 安全提示

审计发现两条 P1 级执行旁路（studio legacy、mobile `/cmd_vel`）。
在整改获批并验证前，建议暂停相关实机运行；本次审计未发送任何运动指令。
详见 [`02-runtime-authority-audit.md`](02-runtime-authority-audit.md) §5。
