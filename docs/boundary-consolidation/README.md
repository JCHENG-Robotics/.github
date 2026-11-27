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

## 审批状态

| 项 | 状态 |
|---|---|
| 治理文档与注册更新 | 已落地（本地分支，未 push） |
| 两新仓准入修复 | 已落地（本地分支，未 push） |
| Git 操作审计 | 完成；本会话只提供 diff，不再 add/commit/push |
| Phase 1 整改设计 | **待审查**；未修改 mobile/studio/system 实现 |
| Phase 2 事实源收束 | 未开始（等待 Phase 1 离线验收） |
| Phase 3 check_boundaries | **report-only 已实现并运行**；17 tests；因 M1 禁 Python 规则，待批准 allowlist 后才能提交/接入 CI |
| Phase 4 契约/回归补全 | 只读调查完成；pyarrow 隔离环境待批准执行 |
| Phase 5 独立 QA | 未开始（等待整改落地） |

## 安全提示

审计发现两条 P1 级执行旁路（studio legacy、mobile `/cmd_vel`）。
在整改获批并验证前，建议暂停相关实机运行；本次审计未发送任何运动指令。
详见 [`02-runtime-authority-audit.md`](02-runtime-authority-audit.md) §5。
