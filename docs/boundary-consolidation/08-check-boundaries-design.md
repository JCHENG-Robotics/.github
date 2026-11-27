# check_boundaries — report-only 治理门禁设计

> Status: **v1.0 (2026-11-27)**. 本文只设计门禁，**不实现脚本、不接入 CI、不阻断
> 任何现有构建**。第一版以 report-only 运行（始终 exit 0），连续两个发布周期
> 零误报后再讨论转为 required。

## 1. 目标

把 [`docs/repo-boundaries.md`](../repo-boundaries.md) §11 的规则变成可重复、
可审计、无误报的自动检查，覆盖：

- 依赖方向
- 事实源重复
- 契约版本
- manifest 合规
- 运动执行权限
- 冻结基线
- 资产 provenance

非目标：不做代码风格检查、不做性能/安全扫描、不执行任何仓库代码、不连接
DDS 或硬件。

## 2. 运行模型

```text
repo manifests (YAML/JSON)
        │
        ▼
check_boundaries.py  ── static readers ──► findings[]
        │                                   │
        ├── boundary-report.json            ├── severity
        └── boundary-report.md              ├── evidence path
                                            └── waiver id (optional)
```

- 入口：`python3 .github/scripts/check_boundaries.py --root <workspace> --mode report`
- 只读：AST 解析、YAML/JSON 解析、git 只读命令；禁止 import 目标仓代码。
- 输出：`boundary-report.json`（机器可读）+ `boundary-report.md`（人读）。
- 退出码：report 模式恒为 `0`；`--mode gate` 预留给未来 required 阶段。
- 运行环境：CI runner 或本机；无网络、无 DDS、无设备。

## 3. 规则目录

| ID | 检查 | 输入 | 判定 | 初始严重度 | 误报处理 |
|---|---|---|---|---|---|
| B1 | 依赖方向 | Python import AST、`package.xml`、`pyproject` | L4 不得 import L3 设备/驱动；L2 不得 import L3/L4；离线仓不得 import 运行时仓 | High | 允许 `jcheng_interfaces`/`jcheng_contracts` |
| B2 | 硬件访问 | manifest `hardware_access` + 静态 token（serial、cv2.VideoCapture、/dev/、pyserial、socketcan、pigpio） | 声明 `none` 的仓不得出现设备访问；perception 的 `camera_readonly` 只允许订阅 | Critical | 测试文件、文档、注释豁免 |
| B3 | 运行时面 | manifest `runtime.ros_domains/publishes/subscribes` + publisher 静态清单 | 声明空 runtime 的仓不得有 `create_publisher`/`create_subscription`/`rclpy` 节点入口 | High | 明确 `test-only` 的 publisher 需在 manifest 注释/文档登记 |
| B4 | 运动权限 | topic/服务清单 + 已知执行入口 | 只有 system 可发布执行命令；`/cmd_vel`、`TeleopCommand`、`/jcheng/intent/*` 必须声明为 intent；不得出现第二 `/servo_controller` 发布者 | Critical | 无（安全规则） |
| B5 | manifest 合规 | `capability.yaml` + interfaces schema | 顶层键、`safety.class`、`hardware_access`、`runtime` 符合 v1；离线仓 `class=offline` + 空 runtime | High | 旧方言仓先记为 waived，限期迁移 |
| B6 | 契约版本 | manifest pin + `locks/ecosystem.lock.yaml` + interfaces tags | pin 的 hash 对应已发布 tag；manifest 范围与锁一致；禁止 pin 分支/HEAD | High | 迁移窗口内 waiver |
| B7 | Schema 归属 | `*.schema.json` + `SCHEMA_OWNERSHIP.md` | 每个 Schema 有 owner/status/consumers；`contract` 类只在 interfaces | Medium | 无 |
| B8 | 事实源重复 | devices registry、system profiles、simulation robot.yaml、learning/studio profiles | 重叠字段值不一致即 fail；缺 `device_id@version#sha256` 引用即 warn | High | 生成式副本带 provenance 可通过 |
| B9 | 评测声明 | `ACCEPTANCE.md`、benchmark 报告 | 非 benchmark 仓不得声明生态级评测结果；mock/synthetic 不得标 `Verified` | Medium | 内部指标标 `internal` 可通过 |
| B10 | 冻结引用 | 文档/代码中的 `jcheng-manipulation` 引用 | 必须是 `repo@tag` + SHA；禁止 `HEAD`/分支 | Medium | 无 |
| B11 | 资产 provenance | `assets/`、模型/数据清单 | 每个资产有来源、版本、哈希；`*.pt/*.onnx/*.engine` 不入树 | Medium | 冻结证据豁免 |
| B12 | 文档与词汇 | 四件套、状态词、相对链接 | 缺文档、非标准状态词、断链 | Low | 旧仓限期 |

## 4. 数据模型

```json
{
  "schema_version": "check-boundaries.v1",
  "generated_at": "2026-11-27T19:45:00+08:00",
  "root": "/home/jerichocheng/jcheng",
  "mode": "report",
  "repos": [
    {"name": "jcheng-system", "layer": "L2", "manifest": null, "findings": 2}
  ],
  "findings": [
    {
      "id": "B4-motion-publisher",
      "rule": "B4",
      "severity": "Critical",
      "repo": "jcheng-studio",
      "evidence": "backend/app/adapters/hardware.py:1270",
      "message": "legacy /motion/dispatch path can publish motion outside ExecuteMotion",
      "waiver": null,
      "status": "open"
    }
  ],
  "summary": {"critical": 2, "high": 5, "medium": 8, "low": 3, "waived": 0}
}
```

## 5. 豁免机制

- 文件：`.github/boundary-waivers.yaml`（治理仓维护）。
- 每条：`id`、`rule`、`repo`、`reason`、`owner`、`expires`（ISO 日期）、`evidence`。
- 过期自动失效并升级为 fail（gate 模式）。
- 豁免不能覆盖 B2/B4 的 Critical 安全规则；安全例外只能通过人工评审记录。

## 6. 分阶段上线

| 阶段 | 触发 | 行为 | 退出条件 |
|---|---|---|---|
| A. 本地报告 | 手动 | 生成报告，exit 0 | 规则可跑通、无崩溃 |
| B. PR 评论 | PR 打开/更新 | 上传 artifact + 评论摘要，不阻断 | 连续 2 个发布周期误报 ≤ 2% |
| C. main 报告 | push main | 记录趋势，不阻断 | 无未解释的 Critical |
| D. required | 治理评审批准 | 仅对 B2/B4/B6/B8 阻断 | 有豁免流程与回滚 |

## 7. 实现草图（不落地）

```python
# .github/scripts/check_boundaries.py（设计示意）
REPOS = discover_repos(ROOT)                 # git 检出 + 产品仓名单
for repo in REPOS:
    manifest = load_manifest(repo)           # YAML/JSON，缺省 None
    imports = ast_imports(repo)              # 只解析，不 import
    pubs = static_publishers(repo)           # create_publisher / 话题清单
    findings += b1_dependency(repo, imports)
    findings += b2_hardware(repo, manifest)
    findings += b3_runtime(repo, manifest, pubs)
    findings += b4_motion(repo, pubs)
    findings += b5_manifest(repo, manifest)
    findings += b6_contract(repo, manifest, LOCK)
    findings += b7_schemas(repo)
    findings += b8_source_of_truth(repo)
    findings += b9_eval_claims(repo)
    findings += b10_frozen(repo)
    findings += b11_assets(repo)
    findings += b12_docs(repo)
write_json(findings); write_markdown(findings)
sys.exit(0)  # report-only
```

## 8. 验收标准（门禁本身）

- 在 15 个产品仓 + 3 个重复检出上跑通，无崩溃、无网络、无设备。
- 对已知偏差（DEV-01…DEV-10）能给出对应 finding；对已对齐项零误报。
- 报告可复现：同一 commit 两次运行字节一致（排序稳定、无时间戳差异或时间戳可注入）。
- 单次运行 < 30 秒；不写目标仓。

## Related

- [边界规范 §11](../repo-boundaries.md)
- [迁移方案](04-migration-plan.md)
- [回归基线](05-regression-baseline.md)
