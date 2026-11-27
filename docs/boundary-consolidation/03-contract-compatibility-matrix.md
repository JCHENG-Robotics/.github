# Contract Compatibility Matrix

> Status: **v1.0 (2026-11-27)**. 只读诊断。记录 `jcheng-interfaces` 已发布契约、
> 各仓 pin、生态锁与部署证据之间的一致性。不修改任何现有仓库实现。

## 1. 已发布契约

| 版本 | Tag / commit | Contract hash | 状态 |
|---|---|---|---|
| v0.1.0 | `v0.1.0`（历史） | `sha256:0b8d72ce…` | 已发布；六个仓仍 pin |
| v0.2.0 | `v0.2.0` / `b03a054a59f70c24741fce37ebe1bb03978d9021` | `sha256:afca22a4…` | **已签名 tag**；system 与两个新仓 pin |
| 0.3.0 | `main`（未打 tag） | `sha256:8120c502…` | 未发布；新增 `intent_source` class |

版本源本身不一致（`jcheng-interfaces`）：`VERSION=0.3.0`、`package.xml=0.3.0`、
`pyproject.toml=0.2.0`、`README` 状态块=v0.2.0、`interface_manifest.json`
version=0.3.0。发布流程要求在打 tag 时同时更新 `VERSION`、`CHANGELOG` 与 tag；
当前 `main` 处于"0.3.0 未发布"的中间态。

## 2. 各仓 pin

| 仓库 | 版本 | manifest 风格 | `interfaces` 范围 | contract hash | 与生态锁 |
|---|---|---|---|---|---|
| `jcheng-system` | 0.3.0-dev0 | 无 `capability.yaml` | 0.2.0（`configs/contract.yaml`） | `afca22…` | 一致（锁：0.2.0） |
| `jcheng-devices` | 0.1.0 | v1 | `>=0.2,<0.3` | `afca22…` | 不在锁的 modules 中（非运行时） |
| `jcheng-scenarios` | 0.1.0 | v1 | `>=0.2,<0.3` | `afca22…` | 不在锁中（非运行时） |
| `jcheng-applications` | 0.1.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | **冲突**：锁写 `>=0.2,<0.3` |
| `jcheng-studio` | 0.8.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | **冲突**：锁写 `>=0.2,<0.3`，锁版本 0.7.0 |
| `jcheng-teleop` | 0.3.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | **冲突**：锁写 `>=0.2,<0.3` |
| `jcheng-learning` | 0.2.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | 未列入锁 |
| `jcheng-mobile` | 0.1.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | 未列入锁 |
| `jcheng-simulation` | 0.1.0 | v1 | `>=0.1,<0.2` | `0b8d72…` | 未列入锁 |
| `jcheng-perception` | 0.1.0 | legacy | 未声明；`contracts.status=provisional_in_repo` | — | 未列入锁 |
| `jcheng-benchmark` | 0.1.0 | legacy | `not_applicable` | — | 未列入锁 |
| `jcheng-ops` | 0.1.0 | legacy | `not_applicable` | — | 未列入锁 |
| `jcheng-research` | 0.1.0 | 无 manifest | — | — | 不在运行时图 |
| `jcheng-interfaces` | 0.3.0 | 无 manifest | — | — | 自身 |

## 3. 部署与审计树不一致

`jcheng-system/deploy/armpi-ultra/evidence/20261127-r10/contract.json`：

```json
{"contract":{"major":0,"minor":1,"patch":0,
 "contract_hash":"sha256:0b8d72ce…"},"system_version":"0.1.0"}
```

而当前审计树 `jcheng-system/configs/contract.yaml` 为 0.2.0 / `afca22…`。
结论：**部署证据来自 0.1.0 树，审计树是 0.3.0-dev0**。任何"部署侧门禁完整"
的结论只对 0.1.0 部署成立；升级到 0.2.0 后的实机行为没有证据。这不是代码缺陷，
但必须在迁移项 MIG-04 中作为前置条件处理。

## 4. 兼容性判定

| 关系 | 判定 | 说明 |
|---|---|---|
| system ↔ devices ↔ scenarios | **兼容** | 同为 0.2.0 / `afca22…`；devices/scenarios 为离线声明，不参与运行时握手 |
| system ↔ applications/studio/teleop | **声明不兼容** | 三者 pin `>=0.1,<0.2`，system 契约已 0.2.0；锁却写 `>=0.2,<0.3`。需要统一，不能靠锁覆盖 manifest |
| mobile/simulation/learning ↔ interfaces | **旧 pin** | `>=0.1,<0.2`；它们不直接消费 IDL（mobile 无消息、simulation 域 43、learning 离线），风险中低，但 manifest 必须随发布更新 |
| perception ↔ interfaces | **未声明** | 仓内 `jcheng_perception_msgs` 7 条 + 6 个 Schema；自述 M2 前提升。当前不可握手 |
| benchmark/ops ↔ interfaces | **不适用** | 无跨仓契约；ops 实际依赖 gateway `/health` 与 studio `/api/health`，应登记为 HTTP 契约而非 `not_applicable` |
| 部署树 ↔ 审计树 | **不一致** | 见 §3；实机验证前必须先对齐 |

## 5. `system_api` 字段

所有 v1 manifest 都声明 `system_api`（如 `>=0.2,<0.4`），但 `jcheng-system`
没有任何系统 API 版本源（无 `api_version`、无握手字段）。因此该字段当前
**不可验证**，只能作为声明。契约变更流程需要补一个 system-side API 版本，
或删除该字段。列为迁移项 MIG-04 的子项。

## 6. 升级顺序（建议）

1. `jcheng-interfaces`：把 0.3.0 收口（更新 `pyproject.toml`、README、manifest），
   打 tag，生成新 hash。
2. `jcheng-system`：升级到 0.3.0 契约 + 补 `system_api` 版本源；保留 0.2.0
   兼容窗口。
3. L4 客户端（applications、studio）与 teleop：改为新 hash，握手测试同步。
4. 离线仓（mobile、simulation、learning、devices、scenarios）：更新声明即可，
   不涉及运行时握手。
5. 最后更新 `locks/ecosystem.lock.yaml` 与 `.github` 注册表。

**禁止**：先改锁再改 manifest、pin 分支或 HEAD、在消费仓本地扩展契约。

## Related

- [Source of Truth Matrix](01-source-of-truth-matrix.md)
- [迁移方案](04-migration-plan.md)
- [边界规范 §8](../repo-boundaries.md)
