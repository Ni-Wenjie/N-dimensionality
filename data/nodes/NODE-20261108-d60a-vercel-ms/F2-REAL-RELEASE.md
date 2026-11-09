# F2 真实发布记录 · NODE-20261108-d60a-vercel-ms

> 时间：2026-11-09 17:13 +0800（系统 `date`；对应 `logs/MAIN.md` 条目 L-021 / L-022）
> 结论：**`BLOCKED_AUTH` 已解除，真实 GitHub 发布完成**。

## 1. 凭据处置

| 项 | 实测 |
|---|---|
| 用户提供 | OpenSSH Ed25519 私钥 + 公钥（`2792816446@qq.com`） |
| 配对验证 | `cryptography` 从私钥导出公钥，与给定公钥**完全一致** |
| 注入方式 | `NDL_SSH_PRIVATE_KEY` 环境变量 → `ssh-add -`（stdin）→ 进程内 `ssh-agent` |
| 是否写入文件 | 否 |
| 是否写入日志 | 否 |
| 是否写入 commit | 否（发布前精确脱敏扫描 0 命中） |
| 用后清理 | `ssh-add -D` + `kill $SSH_AGENT_PID` + `unset NDL_SSH_PRIVATE_KEY` |

**私钥已出现在对话文本中，视为已泄露，请在 GitHub Settings → SSH keys 删除并重新生成。** 本次仅用它完成测试发布。

## 2. 认证与目标仓库探测

```
ssh -T git@github.com  →  Hi Ni-Wenjie! You've successfully authenticated, but GitHub does not provide shell access.
git ls-remote git@github.com:Ni-Wenjie/N-dimensionality.git
  →  340e0f8fe96916929d2a57d622d19659b9897ed8  HEAD
  →  340e0f8fe96916929d2a57d622d19659b9897ed8  refs/heads/main
```

目标仓库为**用户自有仓库**（认证用户名与 owner 一致），已有 `main`，内容仅 `README.md`（`# N-dimensionality`）与 `.gitignore` 两个文件。因此不按用户给的 `git init` 从零建仓，而是基于已有 `main` 建特性分支。

## 3. 实际发布

| 字段 | 值 |
|---|---|
| remote | `git@github.com:Ni-Wenjie/N-dimensionality.git`（SSH） |
| base | `main` @ `340e0f8` |
| 发布分支 | `ndl/NODE-20261108-d60a-vercel-ms/fullflow-release` |
| 提交 | `bc73616c6754943e0f1d413c151603361e654176` |
| 提交信息 | `docs: publish NDL full-flow test deliverables (TEST)` |
| 推送命令 | `git push -q origin <branch>`（无 `--force`，未推 `main`） |
| 发布内容 | 72 个文件 / 648 KB：三层空间骨架、`docs/` TEST PROFILE 与契约、路线/计划 YAML、F3 检测报告与 9 份 findings、F5 验收/提交说明、F2 闸门结论与 PR 草案、F3 迭代复检、两份报告 MD、节点源码（排除 `.git`/`node_modules`/`coverage`） |
| 脱敏扫描 | `-----BEGIN ... PRIVATE KEY-----` / `ghp_*` / `github_pat_*` 0 命中 |

GitHub 返回的 PR 创建入口：
`https://github.com/Ni-Wenjie/N-dimensionality/pull/new/ndl/NODE-20261108-d60a-vercel-ms/fullflow-release`

## 4. 发布断言（4/4 PASS）

| 断言 | 结果 |
|---|---|
| ASSERT-1 远端 `refs/heads/<branch>` 与本地 HEAD 哈希一致 | ✅ PASS |
| ASSERT-2 未直推 `main`（远端 `main` 仍为 `340e0f8`） | ✅ PASS |
| ASSERT-3 提交信息符合 Conventional Commits | ✅ PASS |
| ASSERT-4 push 未使用 `--force` | ✅ PASS |

## 5. 与用户给定命令的差异（逐条）

| 用户命令 | 本次执行 | 依据 |
|---|---|---|
| `echo "# N-dimensionality" >> README.md` | 未执行（README 已有该标题，不重复追加） | 避免污染目标仓库 |
| `git init` | 克隆已有 `main` 后建特性分支 | 仓库已存在；本项目不对新建业务项目从零创作 |
| `git commit -m "first commit"` | `docs: publish NDL full-flow test deliverables (TEST)` | Conventional Commits |
| `git branch -M main` | 保持 `main` 不动，新建 `ndl/<NODE-ID>/<plan-slug>` | 分支命名规范 |
| `git remote add origin https://...` | `git@github.com:...` | 沙箱 `https://github.com` git-http 超时；凭据为 SSH 密钥 |
| `git push -u origin main` | `git push origin <特性分支>` | **硬性约束：禁止直推 main** |

## 6. 状态

`BLOCKED_AUTH` → 已解除；`data/lab/REGISTRY.yaml` 的 `status` 由 `f2_blocked_auth` 更新为 `published_test_branch`。
PR 尚未在 GitHub 上创建（`gh` 无 token，且创建 PR 属于外部动作，留给用户确认）。下一轮迭代可用 `F3-ITERATION.md` 的复检结果生成新路线。
