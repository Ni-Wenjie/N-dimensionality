<div align="center"><span style="color:#05070E;background:#22E1D0;padding:4px 12px">架构 / 规范</span> <span style="color:#05070E;background:#FFB547;padding:4px 12px">流程 / 迭代</span> <span style="color:#05070E;background:#FF3D9A;padding:4px 12px">风险 / 待办</span></div>

# GitHub_N维实验室 · 项目详细说明

> 文档版本：2026-11-09（依据当前工作区真实状态编写，所有数据均可由命令复验）
> 适用对象：项目维护者、后续接手的开发者、审计与复现人员
> 唯一事实来源：`NDL-SPEC-0001 v2.0`。本文为**说明性文档**，不替代规范与契约。

---

## 1. 项目是什么

**GitHub_N维实验室**不是从零开发的业务项目，而是一套「对既有 GitHub 仓库做 AI 辅助二次开发」的流水线。它把指定仓库转化为一条完整闭环：

```
检测 → 路线 → 计划 → 实操 → 发布 → 回到检测迭代
F1   → F3   → F4   → F5   → F2   → F3
```

最终交付三类东西，且全过程可追溯：

1. **AI 优化后的可运行项目**（在节点空间内，能安装依赖、能跑测试）
2. **符合 GitHub 社区规范的代码文件**（README / LICENSE / CONTRIBUTING / CoC / SECURITY / SUPPORT / CHANGELOG / .gitignore / issue 模板 / PR 模板 / CI）
3. **一一对应的 MD 说明文件**（每个代码改动都有独立说明，记录证据、断言、影响、回滚）

## 2. 规范状态声明（重要）

| 项 | 状态 |
|---|---|
| 原始 `docs/SPEC.md` / `docs/contracts/` | **未取得**。资料库附件经核验均为 WorkBuddy 空间页 HTML 骨架，无正文 |
| 当前 `docs/SPEC.md` | 按项目指令中 NDL-SPEC-0001 v2.0 **内联条款实例化的 TEST PROFILE**，已在文件顶部标注「非原始唯一事实来源」 |
| 影响 | 取得原始规范后，须覆盖本文件并用 `docs/contracts/` 原字段重新校验 `route.yaml` / `plan.yaml` |

**本文与所有 YAML 契约、日志、代码均保持纯文本，不加视觉样式**；霓虹配色只用于本报告页眉一类人可读呈现层。

## 3. 三层空间架构

终端空间（`/workspace`）下分三个 L1 空间，L2 节点空间是**唯一可写代码区**。

| 空间 | 路径 | 职责 | 可写代码 |
|---|---|---|---|
| 网关空间 L1 | `gateway/` | 登记与路由，不存源码 | 否 |
| 数据空间 L1 | `data/` | 实验室自身配置 + 各节点报告/路线/计划 | 否 |
| 日志空间 L1 | `logs/` | 总日志 `MAIN.md` + 节点专属日志 | 否 |
| 节点空间 L2 | `gateway/nodes/<NODE-ID>/` | 作业空间，克隆仓库与全部改动都在这里 | **是** |
| 文档空间 | `docs/` | 规范与 YAML 契约 | 否 |

```
/workspace
├── docs/
│   ├── SPEC.md                      # TEST PROFILE 规范实例
│   └── contracts/
│       ├── route.schema.yaml        # 策略层（优化路线）契约
│       └── plan.schema.yaml         # 执行层（优化计划）契约
├── data/
│   ├── lab/
│   │   ├── REGISTRY.yaml            # NODE-ID 唯一来源
│   │   └── bin/                     # 检测/验收/执行/日志 4 个工具
│   └── nodes/<NODE-ID>/             # 每节点的报告、路线、计划、findings
├── logs/
│   ├── MAIN.md                      # 总日志（append-only + STATUS BLOCK）
│   └── <NODE-ID>.md                 # 节点日志（append-only）
├── gateway/
│   └── nodes/<NODE-ID>/             # 唯一代码区（含 .git）
└── NDL-*.md                         # 环境体检 / 全流程 / F2 发布 报告
```

**硬规则**：跨空间引用一律用 `NODE-ID`（`NODE-<YYYYMMDD>-<4hex>-<repo-slug>`），从 `data/lab/REGISTRY.yaml` 读取，禁止遍历目录猜测；被克隆仓库自带的配置（`.npmrc`、`biome.json`、`tsconfig.json` 等）留在节点空间，**禁止复制进 `data/`**。

## 4. 工作阶段

保留原始编号，但**执行顺序以下表为准**：

| 阶段 | 名称 | 输入 → 输出 |
|---|---|---|
| F1 | 克隆建节点 | `repo_url` → 节点空间 + `REGISTRY.yaml` 登记 + `F1-CLONE.md` |
| F3 | 检测 / 说明报告 / 优化路线 | 节点源码 → `F3-DETECTION.md` + `findings/F-XXX.md` + `route.yaml` |
| F4 | 优化计划 | `route.yaml` → `plan.yaml`（执行层任务清单） |
| F5 | 实操 + 实时日志 | `plan.yaml` → 代码改动 + MD 说明 + 验收报告 + 提交 |
| F2 | 认证上传（**发布闸门**） | F5 全通过且 `git status` 干净 → 特性分支 / PR |
| → F3 | 迭代 | 复检结果 → 新一轮路线 |

**F2 是闸门**，不是普通阶段：前置条件不满足返回 `BLOCKED_NO_VALIDATED_PLAN`；鉴权失败写 `BLOCKED_AUTH`。本次实测两种状态都出现过，且都被如实记录。

## 5. 六条硬性约束

1. **凭据**：只用 SSH Ed25519 / Fine-grained PAT / GitHub App / GCM；仅由环境变量注入，绝不写入文件、日志或 commit；写入前脱敏扫描。
2. **提交**：Conventional Commits；分支 `ndl/<NODE-ID>/<plan-slug>`；禁止直推 main、禁止 `--force`；第三方仓库走 Fork PR；保留目标仓库原有 LICENSE。
3. **日志**：两级 + append-only。每个原子任务结束前依次「写节点日志 → 向 `MAIN.md` 追加摘要 → 覆写 STATUS BLOCK」；STATUS BLOCK 是**唯一允许覆写**的区域；禁止批量补记与事后追记；时间戳取系统 `date`。
4. **AI 可读产物**：路线/计划必须是符合 `docs/contracts/` 的 YAML；验收断言必须可由命令或测试自动判定；每任务含 `verify` 与 `rollback`；已 `passed` 任务重复执行时跳过（幂等）。路线＝策略层，计划＝执行层。
5. **语言**：禁止「适当优化 / 进行完善 / 尽快 / 相关内容」等模糊表述，一律写成「路径 + 动作 + 可自动判定的断言」；禁止编造节点数据、时间戳或检测结果；不得修改计划声明范围之外的文件。
6. **疑义即停**：缺 `repo_url` / `NODE-ID` / `PLAN-ID`，或存在多个候选时，列出缺失项等待补充，不得猜测。

## 6. 四个 laboratory 工具

| 脚本 | 作用 | 复现命令 |
|---|---|---|
| `data/lab/bin/ndl_detect.py` | 客观检测节点空间（文件清单、社区规范齐备性、CI、测试数、源码断言一致性），输出 JSON | `python3 data/lab/bin/ndl_detect.py gateway/nodes/<NODE-ID>` |
| `data/lab/bin/ndl_verify.py` | 可自动判定的验收器，支持 `community` / `parse-msg` / `parse-runtime` / `ci-gate` / `all` | `python3 data/lab/bin/ndl_verify.py all` |
| `data/lab/bin/ndl_execute.py` | 计划执行器：逐任务 `action → verify → md_note → 实时日志 → 回写 status`，失败即 rollback | `python3 data/lab/bin/ndl_execute.py <NODE-ID>` |
| `data/lab/bin/ndl_log.sh` | 两级日志写入器，自动递增 `L-NNN` 编号并覆写 STATUS BLOCK | `ndl_log.sh <NODE-ID> <task-id> <status> <summary>` |

契约校验方式：

```bash
python3 -c "import yaml; from jsonschema import Draft202012Validator; \
s=yaml.safe_load(open('docs/contracts/plan.schema.yaml')); \
d=yaml.safe_load(open('data/nodes/<NODE-ID>/plan.yaml')); \
print(len(list(Draft202012Validator(s).iter_errors(d))))"   # 期望 0
```

## 7. 本次测试节点完整档案

| 字段 | 值 |
|---|---|
| NODE-ID | `NODE-20261108-d60a-vercel-ms` |
| 目标仓库 | `https://github.com/vercel/ms.git` @ `main`（第三方公开仓库） |
| 拉取通道 | `codeload.github.com` tarball（`https://github.com` git-http 在本沙箱超时 30s） |
| 快照 sha256 | `a58dc34e09984fe05f1a7064e23f0cca36fcd7f4e01004503c527d12359f9c34`（59,156 B） |
| 基线提交 | `c391baa` — `chore: baseline snapshot vercel/ms@main (TEST)` |
| ROUTE-ID | `ROUTE-20261108-3f43` |
| PLAN-ID | `PLAN-20261108-fa6c` / slug `community-and-parse-fix` |
| 节点分支 | `ndl/NODE-20261108-d60a-vercel-ms/community-and-parse-fix` @ `996db25` |
| 发布仓库 | `git@github.com:Ni-Wenjie/N-dimensionality.git`（用户自有） |
| 发布分支 | `ndl/NODE-20261108-d60a-vercel-ms/fullflow-release` |
| 发布提交 | `bc73616` → `8dc2722`（两次 Conventional Commits） |
| 远端 `main` | `340e0f8`（未改动） |
| REGISTRY 状态 | `published_test_branch` |

## 8. 检测结论与优化结果

**F3 检测出 9 个 findings**：7 项社区规范文件缺失（`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`SUPPORT.md`、`CHANGELOG.md`、`.github/ISSUE_TEMPLATE/`、`.github/PULL_REQUEST_TEMPLATE.md`）、1 个真实代码缺陷、1 个 CI 门禁缺失。

代码缺陷（F-008）：`src/index.ts` 的 `parse()` 守卫是 `str.length > 100`（实际允许 1..100），错误文案却写 `length between 1 and 99`。修正为 100，并新增 100/101 字符边界回归测试；**只改文案，不触碰任何数值解析路径**。

**F4 计划 12 个原子任务**，F5 全部 `passed`。迭代复检对比：

| 指标 | 基线 | 复检 |
|---|---|---|
| 社区规范缺失项 | 7 | **0** |
| `parse()` 文案/守卫不一致 | `True` | **`False`** |
| CI 工作流 | 3 | 4（+`ndl-community.yml`） |
| 测试文件 / 用例 | 4 / 167 | 5 / **169**（覆盖率 100%） |
| 同口径文件数 | 23 | 36（+13，全在计划范围内） |

**幂等经真实验证**：T-111 首次失败（验收器只搜 stdout，但 Jest 摘要写 stderr），日志 `L-015` 如实记录并 rollback；修正后复跑 T-101～T-110 全部 `SKIP`。

## 9. 日志与追溯

- `logs/MAIN.md`：**23 条** `L-001`～`L-023`，append-only；含 1 条真实失败（`L-015`）、1 条 `BLOCKED_AUTH`（`L-018`）、解除记录（`L-021`）。
- `logs/<NODE-ID>.md`：节点专属日志，与总日志同步。
- STATUS BLOCK：唯一覆写区，记录当前条目、NODE-ID、最近任务、已通过任务数。
- 所有时间戳由系统 `date` 取得，未硬编码。

## 10. 复现指南（从零到发布）

```bash
# 1. 环境：git / gh / node>=20 / pnpm / python3 + PyYAML + jsonschema
python3 -c "import yaml, jsonschema; print('deps ok')"

# 2. F1：拉取（本沙箱走 codeload）
curl -sSL -o snap.tar.gz https://codeload.github.com/vercel/ms/tar.gz/refs/heads/main
tar xzf snap.tar.gz -C gateway/nodes/<NODE-ID> --strip-components=1

# 3. F3：检测 + 契约校验
python3 data/lab/bin/ndl_detect.py gateway/nodes/<NODE-ID>
python3 -c "import yaml; from jsonschema import Draft202012Validator; ..."   # 见 §6

# 4. F5：执行计划（幂等）
python3 data/lab/bin/ndl_execute.py <NODE-ID>
python3 data/lab/bin/ndl_verify.py all

# 5. F2 前置：所有 task.status == passed 且 git status --porcelain 为空
git -C gateway/nodes/<NODE-ID> status --porcelain

# 6. F2 发布：SSH 认证 → 特性分支 → push（禁止 main / --force）
ssh -T git@github.com
git -C <publish-clone> push origin ndl/<NODE-ID>/<plan-slug>
```

## 11. 当前状态与待办

| 事项 | 状态 |
|---|---|
| F1 → F3 → F4 → F5 → F2 → F3 闭环 | ✅ 已完成，12/12 任务、169/169 测试、契约 0 错误 |
| `BLOCKED_AUTH` | ✅ 已解除，产物已真实推送到 GitHub 特性分支 |
| GitHub PR | ⏳ 草案已备（`F2-PR-DRAFT-REAL.md`），**尚未在 GitHub 创建** |
| SSH 密钥 | ⚠️ 私钥曾出现在对话文本中，**需立即在 GitHub 删除并重新生成** |
| 原始 SPEC / contracts | ⚠️ 仍为 TEST PROFILE 实例，取得原始文件后须覆盖并重新校验 |
| 项目网盘 | 目前仅有系统目录与《资产库使用指南.pdf》，无项目资产 |

## 12. 附录：关键文件索引

| 文件 | 内容 |
|---|---|
| `PROJECT-GUIDE.md` | 本文：项目定位、三层架构、六条约束、工具、节点档案、复现指南与待办 |
| `NDL-ENV-AUDIT-20261108.md` | 首轮环境与配置体检，含网络通道实测 |
| `NDL-FULLFLOW-TEST-REPORT-20261108.md` | 全流程测试总报告（F0～F3 迭代） |
| `NDL-F2-REAL-RELEASE-20261109.md` | F2 真实发布报告与安全提醒 |
| `data/nodes/<NODE-ID>/F3-DETECTION.md` | 9 个 findings 的检测报告 |
| `data/nodes/<NODE-ID>/findings/F-001.md`～`F-009.md` | 一一对应说明（证据/断言/影响/策略） |
| `data/nodes/<NODE-ID>/route.yaml` | 策略层优化路线 |
| `data/nodes/<NODE-ID>/plan.yaml` | 执行层计划（12 任务，含 verify/rollback） |
| `data/nodes/<NODE-ID>/F5-ACCEPTANCE.md` | 自动验收器真实输出 |
| `data/nodes/<NODE-ID>/F2-REAL-RELEASE.md` | 认证、发布与命令差异逐条说明 |
| `data/nodes/<NODE-ID>/F3-ITERATION.md` | 迭代复检对比 |
| `logs/MAIN.md` | 23 条总日志 + STATUS BLOCK |
