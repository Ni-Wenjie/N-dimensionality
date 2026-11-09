# Changelog

本项目所有值得注意的变更记录于此，格式参考 Keep a Changelog。
版本号以 `package.json` 为准。

## [Unreleased] — NDL TEST PROFILE 全流程测试改动

### Added

- `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`SUPPORT.md`、
  `CHANGELOG.md`：补齐 GitHub 社区规范文件。
- `.github/ISSUE_TEMPLATE/bug_report.yml`、`.github/ISSUE_TEMPLATE/feature_request.yml`、
  `.github/PULL_REQUEST_TEMPLATE.md`：结构化 issue 与 PR 模板。
- `.github/workflows/ndl-community.yml`：社区规范齐备性 CI 门禁。
- `src/parse-length.test.ts`：`parse()` 100/101 字符边界回归测试。
- `docs/parse-length-fix.md`、`docs/parse-length-test.md`、
  `docs/ndl-community-workflow.md`：与代码改动一一对应的 MD 说明。

### Fixed

- `src/index.ts`：`parse()` 抛出的错误文案由 `length between 1 and 99`
  修正为 `length between 1 and 100`，与 `str.length > 100` 守卫保持一致；
  不改变任何数值解析行为。

## [4.0.0] — 基线快照

- 来源：`vercel/ms` @ `main`，codeload tarball 快照
  `a58dc34e09984fe05f1a7064e23f0cca36fcd7f4e01004503c527d12359f9c34`。
- 基线内容：Tiny millisecond conversion utility，TypeScript，4 个测试文件、
  167 个用例，`pnpm run test:nodejs` 全部通过，覆盖率 100%。
- 该快照未附带发布日期信息，故此处不记录日期。
