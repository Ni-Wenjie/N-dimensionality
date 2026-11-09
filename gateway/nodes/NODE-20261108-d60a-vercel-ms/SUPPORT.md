# Support

## 如何获得帮助

- **用法问题与缺陷报告**：使用 GitHub Issues，并优先选用
  `.github/ISSUE_TEMPLATE/` 中的结构化模板，附上 Node.js 版本、`pnpm` 版本、
  最小复现代码与期望/实际结果。
- **功能建议**：使用 feature request 模板，说明使用场景与替代方案。
- **安全问题**：**不要**用 issue，按 `SECURITY.md` 走私有报告渠道。
- **贡献流程**：见 `CONTRIBUTING.md`。

## 响应范围

本项目是时间单位转换工具库，仅处理 `ms()` / `parse()` / `parseStrict()` /
`format()` 的行为问题与文档问题。构建工具链、下游框架或业务系统集成问题
不在本项目支持范围内。

## 自助排查

1. 确认 Node.js >= 20 且 `pnpm install --frozen-lockfile` 成功。
2. 运行 `pnpm run test:nodejs` 确认本地基线。
3. 查阅 `README.md` 与 `CHANGELOG.md` 确认是否为已知行为变更。
