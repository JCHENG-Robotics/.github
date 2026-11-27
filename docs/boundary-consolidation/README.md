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

## 审批状态

| 项 | 状态 |
|---|---|
| 治理文档与注册更新 | 已落地（本地分支，未 push） |
| 两新仓准入修复 | 已落地（本地分支，未 push） |
| 执行权限审计 | 只读完成；P1 整改待单独批准 |
| 迁移计划 | 设计完成；逐项待批准 |
| check_boundaries | 设计完成；未实现、未接入 CI |

## 安全提示

审计发现两条 P1 级执行旁路（studio legacy、mobile `/cmd_vel`）。
在整改获批并验证前，建议暂停相关实机运行；本次审计未发送任何运动指令。
详见 [`02-runtime-authority-audit.md`](02-runtime-authority-audit.md) §5。
