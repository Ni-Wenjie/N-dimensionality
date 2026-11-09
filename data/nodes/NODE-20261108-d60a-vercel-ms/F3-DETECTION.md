<div align="center"><span style="color:#05070E;background:#22E1D0;padding:4px 10px">DETECTION / 已完成</span> <span style="color:#05070E;background:#FFB547;padding:4px 10px">ROUTE / 进行中</span> <span style="color:#05070E;background:#FF3D9A;padding:4px 10px">DEFECT / 已定位</span></div>

# F3 检测报告 · NODE-20261108-d60a-vercel-ms

> TEST PROFILE · 检测时间：2026-11-08 22:17 +0800（系统 `date`）
> 检测对象：`https://github.com/vercel/ms.git` @ `main`，codeload tarball 快照
> 检测脚本：`data/lab/bin/ndl_detect.py`（可复现，只读，不写业务文件）
> 复现命令：`python3 data/lab/bin/ndl_detect.py gateway/nodes/NODE-20261108-d60a-vercel-ms`

## 1. 快照与来源

| 字段 | 值 |
|---|---|
| snapshot_sha256 | `a58dc34e09984fe05f1a7064e23f0cca36fcd7f4e01004503c527d12359f9c34` |
| 快照字节数 | 59,156 |
| 解压后文件数 | 23（不含 `.git`） |
| 基线提交 | `c391baa` — `chore: baseline snapshot vercel/ms@main (TEST)` |
| 原始 LICENSE | `LICENSE`（MIT，"The MIT License (MIT) Copyright (c)"），保留未改 |

## 2. 真实检测结果

| 检测项 | 实测值 | 判定 |
|---|---|---|
| 社区规范基线 10 项 | 3 项 present / 7 项 missing | ❌ 不达标 |
| CI 工作流 | `quality.yml`、`release.yml`、`test.yml` | ✅ 存在，但无社区规范门禁 |
| `src/index.ts` 行数 | 244 | — |
| `parse()` 长度守卫 | `str.length > 100` → 实际允许 1..100 | — |
| `parse()` 错误文案 | `"length between 1 and 99"` | ❌ **与守卫不一致** |
| 测试文件 | 4 个（`format` / `index` / `parse-strict` / `parse`） | ✅ |
| 测试用例数 | 167 | ✅ |
| 基线 `pnpm run test:nodejs` | 4 suites / 167 tests 全通过，覆盖率 100% | ✅ |
| `git status --porcelain` | 空（依赖安装后仍干净，`node_modules` 已被 `.gitignore` 覆盖） | ✅ |
| `package.json` | `ms@4.0.0`，`type: module`，scripts 10 项 | — |

社区规范逐项：

| 文件 | 状态 | 文件 | 状态 |
|---|---|---|---|
| README.md | ✅ present | CONTRIBUTING.md | ❌ missing |
| LICENSE | ✅ present | CODE_OF_CONDUCT.md | ❌ missing |
| .gitignore | ✅ present | SECURITY.md | ❌ missing |
| .github/workflows/ | ✅ present | SUPPORT.md | ❌ missing |
| | | CHANGELOG.md | ❌ missing |
| | | .github/ISSUE_TEMPLATE/ | ❌ missing |
| | | .github/PULL_REQUEST_TEMPLATE.md | ❌ missing |

## 3. Findings（9 项，一一对应说明文件）

| ID | 级别 | 路径 | 证据摘要 | 说明文件 |
|---|---|---|---|---|
| F-001 | medium | CONTRIBUTING.md | detector: missing | `findings/F-001.md` |
| F-002 | medium | CODE_OF_CONDUCT.md | detector: missing | `findings/F-002.md` |
| F-003 | high | SECURITY.md | detector: missing | `findings/F-003.md` |
| F-004 | low | SUPPORT.md | detector: missing | `findings/F-004.md` |
| F-005 | medium | CHANGELOG.md | detector: missing | `findings/F-005.md` |
| F-006 | medium | .github/ISSUE_TEMPLATE/ | detector: missing | `findings/F-006.md` |
| F-007 | medium | .github/PULL_REQUEST_TEMPLATE.md | detector: missing | `findings/F-007.md` |
| F-008 | high | src/index.ts:parse() | guard=100 / msg=99，inconsistent=true | `findings/F-008.md` |
| F-009 | medium | .github/workflows/ | 3 个工作流均不校验社区规范齐备性 | `findings/F-009.md` |

## 4. 一一对应 MD 说明文件索引

每个 finding 在数据空间 `data/nodes/NODE-20261108-d60a-vercel-ms/findings/` 下有独立 MD，记录证据、可自动判定断言、影响范围与对应策略。策略层产物为 `data/nodes/NODE-20261108-d60a-vercel-ms/route.yaml`（9 findings / 3 strategies），已通过 `docs/contracts/route.schema.yaml` 的 jsonschema 校验，错误数 0。

## 5. 检测边界（如实声明）

- 未执行 `pnpm run test:edge` 与 `pnpm run build`：本次 F3 仅做检测，避免把依赖构建产物引入基线；F5 将按计划范围执行断言。
- 未访问 GitHub API 做仓库元数据核对：匿名出口 IP 已触发 rate limit（403），故仓库信息以 tarball 内 `package.json` 为准，不推测远端元数据。
- 三个资料库附件（SPEC.md / N维度 / N维度.pub）经核验均为空间页 HTML 骨架，无正文与密钥；本实例的 SPEC 与 contracts 为按内联规范实例化的 TEST PROFILE，已在 `docs/SPEC.md` 顶部标注。
