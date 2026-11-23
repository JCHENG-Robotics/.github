# JCHENG-Robotics/.github

组织级治理仓库：组织主页、社区健康文件、issue/PR 模板、可复用 CI 工作流与
复合 Action 骨架。**不包含产品代码、机器人配置或密钥。**

## M1 状态

- 仓库骨架已准备，等待组织与 API 凭据后推送。
- 没有 `LICENSE`；许可证审查见 [docs/license-review.md](docs/license-review.md)。
- 复用工作流是骨架，M2/M3 再填充真实构建与测试步骤。

## 目录

```text
profile/README.md                 组织主页
CONTRIBUTING.md                   贡献流程
SECURITY.md                       漏洞与密钥处理
GOVERNANCE.md                     角色、评审、发布权限
CODEOWNERS.template               各仓库复制后生效
.github/workflows/                6 个可复用工作流 + 1 个组织健康检查
actions/                          3 个复合 Action 骨架
ISSUE_TEMPLATE/                   问题/特性/设计/配置模板
docs/                             组织级策略
```

## 约束

- 任何实机运动必须有单独、明确的授权；本仓库不包含运动代码。
- 第三方 Action 使用完整 commit SHA；复用工作流用组织标签 `v1`。
- 不提交令牌、私钥、真实站点 IP、机器人凭据。
- 许可证审查完成前，不添加 `LICENSE`，不宣称 MIT。
