# NDL-SPEC-0001 v2.0 · 测试实例（TEST PROFILE）

> 状态：**TEST PROFILE / 测试用实例化副本**，非原始唯一事实来源。
> 生成原因：2026-11-08 全流程测试请求中，资料库附件 `SPEC.md` 实为 WorkBuddy 空间页 HTML 骨架（无正文），
> 原始 `docs/SPEC.md` 与 `docs/contracts/` 在沙箱与项目网盘均不存在。
> 本文件依据项目指令中给出的 NDL-SPEC-0001 v2.0 内联条款实例化，**仅用于本次全流程测试**，不冒充原始规范。
> 一旦取得原始 SPEC.md，应以原始文件覆盖本文件，并按原始字段重新校验所有产物。

## 1. 三层空间架构

| 空间 | 路径 | 职责 | 是否可写代码 |
|---|---|---|---|
| 网关空间 L1 | `gateway/` | 登记与路由，不存源码 | 否 |
| 数据空间 L1 | `data/` | 实验室自身配置 + 各节点报告/路线/计划 | 否 |
| 日志空间 L1 | `logs/` | `MAIN.md` 总日志 + 节点专属日志 | 否 |
| 节点空间 L2 | `gateway/nodes/<NODE-ID>/` | 作业空间，唯一可写代码区 | 是 |

- 跨空间引用一律使用 `NODE-ID`，格式为 `NODE-<YYYYMMDD>-<4hex>-<repo-slug>`，唯一来源 `data/lab/REGISTRY.yaml`。
- 禁止遍历目录猜测 NODE-ID。
- 被克隆仓库自带配置留在节点空间内，禁止复制进 `data/`。

## 2. 阶段顺序

`F1 克隆建节点 → F3 检测/说明报告/优化路线 → F4 优化计划 → F5 实操+实时日志 → F2 认证上传 → 回到 F3 迭代`

- F2 是发布闸门：仅在 F5 全部验收通过且 `git status` 干净后触发；否则返回 `BLOCKED_NO_VALIDATED_PLAN`。
- 鉴权失败写 `BLOCKED_AUTH`。

## 3. 硬性约束（测试同样适用）

1. 凭据只用 SSH Ed25519 / Fine-grained PAT / GitHub App / GCM；仅由环境变量注入，绝不写入文件、日志或 commit；写入前脱敏扫描。
2. 提交用 Conventional Commits；分支 `ndl/<NODE-ID>/<plan-slug>`；禁止直推 main、禁止 `--force`；第三方仓库走 Fork PR；保留目标仓库原有 LICENSE。
3. 日志两级 + append-only：原子任务结束前依次「写节点日志 → MAIN.md 追加摘要 → 覆写 STATUS BLOCK」；禁止批量补记与事后追记；时间戳取系统 `date`。
4. 优化路线与优化计划必须是符合 `docs/contracts/` 的 YAML；验收断言必须可由命令或测试自动判定；每任务含 `verify` 与 `rollback`；已 `passed` 任务重复执行时跳过。路线＝策略层，计划＝执行层。
5. 禁止模糊表述；禁止编造节点数据、时间戳或检测结果；不得修改计划声明范围之外的文件。
6. 缺 `repo_url` / `NODE-ID` / `PLAN-ID`，或存在多个候选时，列出缺失项等待补充，不得猜测。
   - 本次测试例外：用户显式授权「自行建立测试节点」，故测试 `repo_url` 与 `NODE-ID` 由本实例按规定格式实例化并登记，全程标注 `TEST`。

## 4. 测试实例参数

| 字段 | 值 |
|---|---|
| profile | `TEST` |
| 目标仓库 | `https://github.com/vercel/ms.git`（第三方公开仓库，真实数据） |
| 拉取通道 | `codeload.github.com` tarball（`https://github.com` git-http 在本沙箱超时） |
| 远端演练 | 本地 bare git 仓库，模拟 Fork PR，不向真实 GitHub 推送 |
| 真实发布 | 需凭据；本次预期 `BLOCKED_AUTH`，如实记录，不伪造推送成功 |
| NODE-ID | 见 `data/lab/REGISTRY.yaml` |
| PLAN-ID | 由 F4 生成并登记 |

## 5. 社区规范基线（F3/F5 检查项）

`README.md`、`LICENSE`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`SUPPORT.md`、`CHANGELOG.md`、`.gitignore`、`.github/ISSUE_TEMPLATE/`、PR 模板、CI 必须齐备；每个代码改动都要有对应 MD 说明文件。

## 6. 呈现层风格（仅人可读层）

深空底 `#05070E`；青 `#22E1D0`＝完成/规范，洋红 `#FF3D9A`＝纠错/风险，琥珀 `#FFB547`＝进行中/计划。YAML 契约、日志、代码保持纯文本，不加视觉样式。
