# 真实 PR 草案 · Ni-Wenjie/N-dimensionality

> 状态：**草案，未实际创建 PR**（`gh` 未认证，创建 PR 属外部动作，留待用户确认）
> 创建入口（GitHub 推送时返回）：
> `https://github.com/Ni-Wenjie/N-dimensionality/pull/new/ndl/NODE-20261108-d60a-vercel-ms/fullflow-release`

- **base**: `main` @ `340e0f8`
- **head**: `ndl/NODE-20261108-d60a-vercel-ms/fullflow-release` @ `bc73616`
- **共同祖先**: 有（基于目标仓库 `main` 创建，可正常开 PR）
- **标题**: `docs: publish NDL full-flow test deliverables (TEST)`

## 变更摘要

新增 72 个文件 / 648 KB，均为 NDL 全流程测试的闭环产物：

| 路径 | 内容 |
|---|---|
| `docs/SPEC.md`、`docs/contracts/` | TEST PROFILE 规范实例 + 路线/计划 YAML 契约 |
| `data/lab/REGISTRY.yaml`、`data/lab/bin/` | NODE-ID 登记表、检测器/验收器/执行器/日志器 |
| `data/nodes/NODE-20261108-d60a-vercel-ms/` | F1 说明、F3 检测报告与 9 份 findings、route.yaml、plan.yaml、F5 验收/提交说明、F2 闸门结论与两份 PR 草案、F2 真实发布记录、F3 迭代复检 |
| `logs/MAIN.md` + 节点日志 | 22 条 append-only 日志（含 1 条真实失败与 rollback） |
| `gateway/nodes/NODE-20261108-d60a-vercel-ms/` | 优化后的可运行项目：13 个新增文件 + `src/index.ts` 1 处修正 |
| `NDL-*.md` | 环境体检报告、全流程测试报告、F2 发布记录 |

保留目标仓库原有 `README.md` 与 `.gitignore`，未改动 `main`。

## 验收命令（在节点空间执行）

```bash
python3 data/lab/bin/ndl_verify.py all
pnpm install --frozen-lockfile && pnpm run test:nodejs   # 169 passed / 169 total
```

- [x] `route.yaml` / `plan.yaml` jsonschema 契约错误 0 / 0
- [x] 12 / 12 计划任务 `passed`
- [x] `git status --porcelain` 空（节点空间）
- [x] Conventional Commits
- [x] 未直推 `main`、未使用 `--force`
- [x] 发布前脱敏扫描 0 命中

## Rollback

```bash
git revert bc73616c6754943e0f1d413c151603361e654176
```

（禁止 `git push --force`；如需删除测试分支，在 GitHub 分支页操作即可。）

## 安全事项

本次使用的 Ed25519 私钥已出现在对话文本中，属于已泄露凭据。合并 PR 后请立即在
GitHub Settings → SSH and GPG keys 中删除该公钥并重新生成密钥对。
