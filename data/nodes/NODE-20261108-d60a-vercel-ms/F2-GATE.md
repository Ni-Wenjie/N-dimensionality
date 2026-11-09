# F2 发布闸门结论 · NODE-20261108-d60a-vercel-ms

> 判定时间：L-018 = 2026-11-08 22:30:22 +0800；L-019 = 2026-11-08 22:33:47 +0800（见 `logs/MAIN.md`）
> 结论：**闸门前置条件 PASS，真实发布 BLOCKED_AUTH**；本地 Fork PR 演练 5/5 PASS，闭环完成。

## 1. 闸门前置条件

| 断言 | 实测 | 判定 |
|---|---|---|
| 所有 `task.status == passed` | 12 / 12 | ✅ PASS |
| `git status --porcelain` 为空 | `''` | ✅ PASS |
| 脱敏扫描（节点工作区 + `data/` + `logs/`，排除 `.git`/`node_modules`） | `ghp_` / `github_pat_` / `BEGIN ... PRIVATE KEY` / `ssh-ed25519 AAAA` 命中 **0** | ✅ PASS |
| `F2_PRECONDITION` | `PASS` | ✅ 允许进入认证阶段 |

未返回 `BLOCKED_NO_VALIDATED_PLAN`。

## 2. 真实 GitHub 认证探测（结果为 BLOCKED_AUTH）

| 探测项 | 实测 |
|---|---|
| `GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_PAT` / `GIT_SSH_KEY` | 全部 `unset` |
| `~/.ssh` | 无密钥对（仅 `ssh -T` 探测时写入的 `known_hosts`） |
| `gh auth status` | `You are not logged into any GitHub hosts` |
| `ssh -T git@github.com` | `git@github.com: Permission denied (publickey)` |
| 三个资料库附件（SPEC.md / N维度 / N维度.pub） | 均为空间页 HTML 骨架，私钥/公钥/Token 特征均为 0 处 |

→ **`AUTH_RESULT=BLOCKED_AUTH`**。按硬性约束 1，**未向真实 GitHub 发起任何推送**，未伪造发布成功，未把任何凭据写入文件、日志或 commit。

## 3. 本地 Fork PR 演练（非真实发布）

为完成「流通整个项目」的全流程测试，用本地 bare git 仓库模拟 Fork 远端：

- 远端：`/root/.codebuddy/artifact/ndl-fork-sim-NODE-20261108-d60a-vercel-ms.git`（沙箱临时区，非 GitHub）
- 推送命令：`git push fork-sim HEAD:refs/heads/ndl/NODE-20261108-d60a-vercel-ms/community-and-parse-fix`（无 `--force`）
- 本地 HEAD 与远端 HEAD：`996db2539cb530ec9514b16533091a5dc87f1da4`

| 断言 | 判定 |
|---|---|
| ASSERT-1 本地与远端提交哈希一致 | ✅ PASS |
| ASSERT-2 分支名符合 `ndl/<NODE-ID>/<plan-slug>` | ✅ PASS |
| ASSERT-3 远端无 `refs/heads/main`（未直推 main） | ✅ PASS |
| ASSERT-4 提交信息符合 Conventional Commits（`fix: ...`） | ✅ PASS |
| ASSERT-5 保留目标仓库原有 `LICENSE`（MIT） | ✅ PASS |

演练后 `git status --porcelain` 仍为空。PR 草案见 `F2-PR-DRAFT.md`。

## 4. 解除 BLOCKED_AUTH 所需条件

1. 注入 Ed25519 私钥（经环境变量，不落盘）并把对应公钥注册到 GitHub 账号；或
2. 注入 Fine-grained PAT 到 `GITHUB_TOKEN`（本沙箱 `https://github.com` git-http 超时，PAT 仅够 `api.github.com`，克隆仍须 SSH）。
3. 因目标为第三方仓库 `vercel/ms`，真实发布必须走 Fork PR，不能在原仓库直推。
