<div align="center"><span style="color:#05070E;background:#22E1D0;padding:4px 12px">F1 F3 F4 F5 ✓ 闭环</span> <span style="color:#05070E;background:#FFB547;padding:4px 12px">F2 本地演练 ✓</span> <span style="color:#05070E;background:#FF3D9A;padding:4px 12px">F2 真实发布 BLOCKED_AUTH</span></div>

# NDL 全流程测试报告 · 2026-11-08

> 节点：`NODE-20261108-d60a-vercel-ms` ｜ 路线：`ROUTE-20261108-3f43` ｜ 计划：`PLAN-20261108-fa6c`
> 测试性质：**TEST PROFILE**（按用户「自行建立测试节点、流通整个项目、完成全流程测试」授权实例化）
> 结果：**F0→F1→F3→F4→F5→F2(演练)→F3(迭代) 全部跑通；真实 GitHub 发布按规范返回 `BLOCKED_AUTH`**

## 1. 一句话结论

项目从零骨架到可交付闭环已经跑通并留痕：12/12 计划任务通过、169/169 测试通过、契约校验 0 错误、20 条实时日志、`git status` 干净、本地 Fork PR 推送 5/5 断言通过。**唯一未做的是真实 GitHub 推送**——缺凭据，按规范写 `BLOCKED_AUTH`，没有伪造成功。

## 2. 三个资料库附件的核验结果（重要）

| 附件 | 实际类型 | 正文 | 私钥/Token/公钥 |
|---|---|---|---|
| `SPEC.md` | WorkBuddy 空间页 HTML 骨架，12,355 B | 无 | 0 处 |
| `N维度` | 同一 HTML 骨架，12,341 B | 无 | 0 处 |
| `N维度.pub` | 同一 HTML 骨架，12,341 B | 无 | 0 处 |

三者与上一轮的 `GitHub key` 仅标题/空间 ID 不同。因此：

- `docs/SPEC.md` 与 `docs/contracts/` 是按项目指令中 NDL-SPEC-0001 v2.0 **内联条款实例化的 TEST PROFILE**，已在文件顶部明确标注，**不冒充原始唯一事实来源**；取得原始 SPEC 后应覆盖并重新校验。
- 无凭据可用，故 F2 真实发布必然 `BLOCKED_AUTH`，这与上一轮环境体检结论一致。

## 3. 环境与通道实测

| 项 | 结果 |
|---|---|
| 工具链 | git 2.43.0 / gh 2.86.0 / node 22.13.1 / python 3.11.1 / pnpm 10.28.2 |
| `https://github.com` git-http | 超时 30s（不可用） |
| `ssh github.com:22` | TCP 与 SSH 握手通，但 `Permission denied (publickey)`（无密钥） |
| `codeload.github.com` | 200，实测拉取 `vercel/ms@main` 59,156 B 成功 |
| `registry.npmjs.org` | 200，`pnpm install --frozen-lockfile` 413 包 4.2s 成功 |
| `api.github.com` | 403，匿名共享 IP 触发 rate limit |

→ F1 走 codeload，F2 走本地 bare 远端演练，均未依赖被阻断的通道。

## 4. 全流程阶段与真实数据

| 阶段 | 做了什么 | 关键产物/断言 |
|---|---|---|
| F0 骨架 | 三层空间 + contracts + REGISTRY + 两级日志器 | `docs/SPEC.md`、`docs/contracts/{route,plan}.schema.yaml`、`data/lab/REGISTRY.yaml` |
| F1 建节点 | 真实拉取 `vercel/ms@main` | sha256 `a58dc34e…7f9c34`，基线提交 `c391baa`，`F1-CLONE.md` |
| F3 检测 | 客观检测 + 9 findings + 策略路线 | 基线 167/167 通过、覆盖率 100%；`F3-DETECTION.md`、9 份 `findings/F-00X.md`、`route.yaml` |
| F4 计划 | 12 个原子任务，每条含 `verify`/`rollback`/`md_note` | `plan.yaml`，契约 0 错误 |
| F5 实操 | 补齐 7 项社区规范、修 1 处真实缺陷、加 2 个边界测试、加 CI 门禁 | 169/169 通过；提交 `996db25`，分支 `ndl/NODE-20261108-d60a-vercel-ms/community-and-parse-fix` |
| F2 闸门 | 前置 PASS、脱敏 0 命中、认证探测 `BLOCKED_AUTH`、本地 Fork PR 演练 5/5 PASS | `F2-GATE.md`、`F2-PR-DRAFT.md` |
| F3 迭代 | 复检对比，验证闭环 | `F3-ITERATION.md`：缺失 7→0、parse 不一致 True→False、用例 167→169 |

**真实代码缺陷（F-008）**：`src/index.ts` 的 `parse()` 守卫是 `str.length > 100`（允许 1..100），错误文案却写 `length between 1 and 99`。修正为 100，并新增 100/101 字符边界回归测试。只改文案，不触碰任何数值解析路径。

**幂等验证**：T-111 首次因验收器只搜 stdout（Jest 摘要实际写 stderr）失败，日志 `L-015` 如实记录并执行 rollback；修正验收器后复跑，T-101..T-110 全部 `SKIP`、T-111/T-112 通过——这是真实验证过的幂等，不是设计宣称。

## 5. 最终一致性校验

| 校验项 | 结果 |
|---|---|
| `route.yaml` / `plan.yaml` jsonschema 契约错误数 | 0 / 0 |
| `plan.tasks` 状态 | 12 / 12 `passed` |
| `pnpm run test:nodejs` | 5 suites，169 passed / 169 total，覆盖率 100% |
| `git status --porcelain` | 空 |
| 提交信息 Conventional Commits | `fix: align parse() length message with guard and complete community baseline` |
| 未直推 main / 未用 `--force` / 保留 MIT LICENSE | 全部满足 |
| 脱敏扫描（节点 + data + logs） | 0 命中 |
| 日志 | `MAIN.md` 20 条（L-001..L-020）+ 节点日志同步；STATUS BLOCK 为唯一覆写区 |

## 6. 产物清单（`/workspace`）

```
NDL-FULLFLOW-TEST-REPORT-20261108.md     本页
NDL-ENV-AUDIT-20261108.md                上一轮环境体检
docs/SPEC.md                             TEST PROFILE 规范实例
docs/contracts/route.schema.yaml         策略层契约
docs/contracts/plan.schema.yaml          执行层契约
data/lab/REGISTRY.yaml                   NODE-ID 唯一来源
data/lab/bin/{ndl_detect,ndl_verify,ndl_execute}.py, ndl_log.sh
data/nodes/NODE-20261108-d60a-vercel-ms/
  F1-CLONE.md  F3-DETECTION.md  route.yaml  plan.yaml
  F5-ACCEPTANCE.md  F5-COMMIT.md  F2-GATE.md  F2-PR-DRAFT.md  F3-ITERATION.md
  findings/F-001.md ... F-009.md
logs/MAIN.md  logs/NODE-20261108-d60a-vercel-ms.md
gateway/nodes/NODE-20261108-d60a-vercel-ms/   唯一代码区（13 新增 + 1 修改）
```

## 7. 阻塞项与下一步

| 阻塞 | 原因 | 解除方式 |
|---|---|---|
| `BLOCKED_AUTH` | 无 SSH Ed25519 私钥、无 PAT、`gh` 未登录；三个附件均为空壳 | 经环境变量注入 Ed25519 私钥并注册公钥；第三方仓库 `vercel/ms` 走 Fork PR |
| 原始 SPEC 缺失 | 资料库附件无正文 | 提供原始 `docs/SPEC.md` 与 `docs/contracts/`，覆盖 TEST PROFILE 后重新校验 |

下一轮迭代入口已就绪：以 `F3-ITERATION.md` 的复检结果生成新路线，已 `passed` 的任务会自动跳过。
