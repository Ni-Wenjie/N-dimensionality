# F3 迭代复检 · F2 后回到 F3（闭环验证）

> 检测脚本：`data/lab/bin/ndl_detect.py`
> 基线对象：`/tmp/msprobe/ms-main`（F1 tarball 原始解压，未装依赖）
> 复检对象：`gateway/nodes/NODE-20261108-d60a-vercel-ms/`
> 统一口径：排除 `.git` / `node_modules` / `coverage`（coverage 是 jest 生成的测试产物，已被 `.gitignore` 忽略，故 git status 仍干净）

| 指标 | F3 基线 | F3 迭代复检 | 变化 |
|---|---|---|---|
| 文件数（同口径） | 23 | 36 | +13 |
| 社区规范缺失项 | 7 | **0** | ✅ 全部消除 |
| CI 工作流 | 3 | 4 | +`ndl-community.yml` |
| `parse()` 文案/守卫不一致 | `True` | **`False`** | ✅ 已修正 |
| 测试文件 | 4 | 5 | +`parse-length.test.ts` |
| 测试用例 | 167 | **169** | +2（100/101 边界） |
| `pnpm run test:nodejs` | 167/167 通过 | 169/169 通过，覆盖率 100% | ✅ |

## 新增的 13 个文件（全部在计划声明范围内）

```
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/ndl-community.yml
CHANGELOG.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
SECURITY.md
SUPPORT.md
docs/ndl-community-workflow.md
docs/parse-length-fix.md
docs/parse-length-test.md
src/parse-length.test.ts
```

`src/index.ts` 为修改（1 处文案），不在新增清单内。无消失文件。

## 迭代结论

复检证明 F3 → F4 → F5 的改动确实消除了全部 9 个 findings，且未引入测试回归。下一轮迭代可直接从本复检结果生成新的路线 YAML；当前 `route.yaml` 的 9 个 findings 已全部关闭，无需重复执行（计划 `status: passed` 的任务具备幂等跳过能力）。
