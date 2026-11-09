# Contributing to ms

## 本地开发

- Node.js >= 20（见 `package.json` 的 `engines`）、pnpm 10。
- 安装依赖：`pnpm install --frozen-lockfile`
- 运行测试：`pnpm run test:nodejs`（Jest，node 环境）
- 类型检查：`pnpm run typecheck`
- 静态检查：`pnpm run lint`
- 格式化：`pnpm run format`
- 构建：`pnpm run build`

新增或修改 `src/` 下的行为时，必须同步在 `src/*.test.ts` 增加用例，并保证
`pnpm run test:nodejs` 全部通过。

## 提交与分支

- 提交信息遵循 Conventional Commits：`feat:` / `fix:` / `docs:` / `test:` / `ci:` / `chore:`。
- 分支命名：`ndl/<NODE-ID>/<plan-slug>`；禁止直接向 `main` 提交。
- 禁止 `git push --force`。

## Pull Request

本仓库为第三方项目，改动请通过 Fork 发起 PR：

1. Fork 仓库并克隆你的 Fork。
2. 从最新 `main` 创建特性分支。
3. 提交前运行 `pnpm run test:nodejs`、`pnpm run lint`、`pnpm run typecheck`。
4. 按 `.github/PULL_REQUEST_TEMPLATE.md` 填写变更说明、验收命令与回滚方案。
5. 在 PR 中说明每个改动对应的 MD 说明文件。

## 社区规范

请遵守 `CODE_OF_CONDUCT.md`；安全漏洞请按 `SECURITY.md` 私下报告，不要公开开 issue。
