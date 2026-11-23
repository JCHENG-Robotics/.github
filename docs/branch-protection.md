# 分支保护基线

`main` 必须保持以下配置（实际配置并由 `scripts/verify_m1.sh` 验证）：

| 项 | 值 |
|---|---|
| 直接 push | 禁止 |
| force-push | 禁止 |
| 删除分支 | 禁止 |
| PR 批准 | ≥1 |
| CODEOWNERS 批准 | 必需 |
| 必需检查 | `m1-gate`（或实际 check run 名称） |
| 管理员受限 | 是 |
| 对话解决 | 必需 |
| 线性历史 | 必需 |
| 合并方式 | 仅 squash |
| 合并后删分支 | 是 |

发布标签：受保护、签名、不可移动；禁止 force-push 已发布标签。

变更本基线需要 Owner 批准，并更新 `settings/branch-protection.json` 与
`scripts/verify_m1.sh`。
