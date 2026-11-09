# Security Policy

## Supported Versions

安全修复仅面向当前主版本：

| Version | Supported |
| --- | --- |
| 4.x（当前 `package.json` 声明 `4.0.0`） | :white_check_mark: |
| < 4.0 | :x: |

## Reporting a Vulnerability

**请勿为安全漏洞公开创建 issue。**

请使用 GitHub 的 **Security Advisories → Report a vulnerability** 私有报告渠道
提交，或通过与维护者的私有联系渠道发送，包含：

- 受影响版本与复现环境（Node.js 版本、pnpm 版本）
- 复现步骤与最小可运行示例
- 影响范围与可能的利用方式

维护者会确认收到并协调修复与披露时间。在修复发布前，请避免公开细节。

## 依赖安全

本项目运行时无生产依赖；开发依赖由 `pnpm-lock.yaml` 锁定，升级请通过独立 PR 提交。
