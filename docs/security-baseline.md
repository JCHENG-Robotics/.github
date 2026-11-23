# 安全基线

## 账户与权限

- 组织成员强制 2FA；基础权限 `read`；仓库创建仅 Owner。
- `main` 受保护；管理员同样受限。
- 环境：`release`（发布）、`robot-lab`（实机，手动/审批）、`nightly`（Mock）。
- 机器人令牌只放 `robot-lab` 环境，短生命周期、定期轮换。

## 供应链

- 第三方 Action 用完整 commit SHA；复用工作流用组织标签 `v1`。
- Dependabot + dependency review；新依赖说明用途、版本、许可证。
- 发布附件含 SBOM（CycloneDX）与校验和。
- 不把令牌、私钥、真实站点 IP 写入仓库或前端构建产物。

## 运行时边界

- 能力模块默认无硬件设备、无厂商 DDS 域、无 host 网络。
- 只有 `jcheng-system` 的特权运动平面可以发布硬件命令。
- SROS2/网络隔离是目标；未达成时发布说明标注 enforcement level。
- 运行时不暴露原始 `set_position`/`SetBusServoState` 写路径。

## 事件响应

密钥泄露：先轮换、后清理历史；记录审计。
安全漏洞：私密报告，不在 issue 公开利用细节。
发现绕过运动入口：停止相关实机使用，按最高优先级修复。
