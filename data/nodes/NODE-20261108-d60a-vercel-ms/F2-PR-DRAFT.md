# Fork PR 草案（本地演练，未向真实 GitHub 提交）

- **base**: `vercel/ms` → `main`
- **head**: `<your-fork>` → `ndl/NODE-20261108-d60a-vercel-ms/community-and-parse-fix`
- **标题**: `fix: align parse() length message with guard and complete community baseline`
- **提交**: `996db2539cb530ec9514b16533091a5dc87f1da4`（Conventional Commits）
- **状态**: 草案。`BLOCKED_AUTH`，未创建真实 PR。

## 变更摘要

| 类别 | 路径 | 对应 MD 说明 |
|---|---|---|
| 社区规范 | `CONTRIBUTING.md` | `findings/F-001.md` |
| 社区规范 | `CODE_OF_CONDUCT.md` | `findings/F-002.md` |
| 社区规范 | `SECURITY.md` | `findings/F-003.md` |
| 社区规范 | `SUPPORT.md` | `findings/F-004.md` |
| 社区规范 | `CHANGELOG.md` | `findings/F-005.md` |
| 社区规范 | `.github/ISSUE_TEMPLATE/bug_report.yml`、`feature_request.yml` | `findings/F-006.md` |
| 社区规范 | `.github/PULL_REQUEST_TEMPLATE.md` | `findings/F-007.md` |
| 代码修复 | `src/index.ts`（错误文案 99 → 100） | `docs/parse-length-fix.md` |
| 回归测试 | `src/parse-length.test.ts`（100/101 边界，2 用例） | `docs/parse-length-test.md` |
| CI 门禁 | `.github/workflows/ndl-community.yml` | `docs/ndl-community-workflow.md` |

保留原 `LICENSE`（MIT）未改；未修改 `quality.yml` / `release.yml` / `test.yml`；未修改任何依赖配置。

## 验收命令

```bash
pnpm install --frozen-lockfile
pnpm run test:nodejs      # 169 passed / 169 total，覆盖率 100%
pnpm run lint
pnpm run typecheck
python3 data/lab/bin/ndl_verify.py all
```

- [x] `ndl_verify.py all` 退出码 0（17 项静态断言 + 测试套件）
- [x] `git status --porcelain` 为空
- [x] 提交信息符合 Conventional Commits
- [x] 未直推 `main`、未使用 `--force`

## Rollback

```bash
git revert 996db2539cb530ec9514b16533091a5dc87f1da4
```

（禁止 `git push --force`）
