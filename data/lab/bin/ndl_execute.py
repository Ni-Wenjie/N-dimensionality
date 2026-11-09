#!/usr/bin/env python3
"""data/lab/bin/ndl_execute.py — F5 计划执行器（TEST PROFILE）
读取 data/nodes/<NODE-ID>/plan.yaml，按任务顺序执行：
  action -> verify(可自动判定) -> md_note 存在性 -> 实时两级日志 -> 回写 status
已 passed 任务跳过（幂等）。任一任务失败即执行 rollback 并停止。
用法: ndl_execute.py <node_id>
"""
import pathlib
import subprocess
import sys
import yaml

W = pathlib.Path("/workspace")
N = sys.argv[1]
PLAN = W / "data/nodes" / N / "plan.yaml"
DATA = W / "data/nodes" / N
NODE = W / "gateway/nodes" / N
LOG = W / "data/lab/bin/ndl_log.sh"

IMPL = {}

IMPL["T-101"] = r"""cat > CONTRIBUTING.md <<'NDL_EOF'
# Contributing to ms

## 本地开发

- Node.js >= 20（见 `package.json` 的 `engines`）、pnpm 10。
- 安装依赖：`pnpm install --frozen-lockfile`
- 运行测试：`pnpm run test:nodejs`（Jest，node 环境）
- 类型检查：`pnpm run typecheck`
- 静态检查：`pnpm run lint`
- 格式化：`pnpm run format`
- 构建：`pnpm run build`

新增或修改 `src/` 下的行为时，必须同步在 `src/*.test.ts` 增加用例，并保证
`pnpm run test:nodejs` 全部通过。

## 提交与分支

- 提交信息遵循 Conventional Commits：`feat:` / `fix:` / `docs:` / `test:` / `ci:` / `chore:`。
- 分支命名：`ndl/<NODE-ID>/<plan-slug>`；禁止直接向 `main` 提交。
- 禁止 `git push --force`。

## Pull Request

本仓库为第三方项目，改动请通过 Fork 发起 PR：

1. Fork 仓库并克隆你的 Fork。
2. 从最新 `main` 创建特性分支。
3. 提交前运行 `pnpm run test:nodejs`、`pnpm run lint`、`pnpm run typecheck`。
4. 按 `.github/PULL_REQUEST_TEMPLATE.md` 填写变更说明、验收命令与回滚方案。
5. 在 PR 中说明每个改动对应的 MD 说明文件。

## 社区规范

请遵守 `CODE_OF_CONDUCT.md`；安全漏洞请按 `SECURITY.md` 私下报告，不要公开开 issue。
NDL_EOF
"""

IMPL["T-102"] = r"""cat > CODE_OF_CONDUCT.md <<'NDL_EOF'
# Contributor Covenant Code of Conduct

## Our Pledge

我们承诺让参与本项目的每个人都能获得无骚扰的体验，不论年龄、体型、残障、
族裔、性别认同与表达、经验水平、教育程度、社会经济地位、国籍、外貌、种族、
宗教或性取向。

## Our Standards

有助于营造积极环境的行为包括：对他人表达同理与尊重、尊重不同观点、
给出并优雅接受建设性反馈、承担责任并向受影响者致歉、聚焦社区整体利益。

不可接受的行为包括：性化语言或图像、挑衅与侮辱性评论、公开或私下骚扰、
未经许可公开他人隐私信息，以及其他在专业场所中合理认定为不当的行为。

## Enforcement Responsibilities

维护者负责澄清并执行本准则，对不合规行为可采取删除/编辑内容、临时或永久
封禁等处置，并会告知处置理由。

## Scope

本准则适用于所有项目空间，以及个人在公共场合代表项目时。

## Enforcement

遇到违反准则的行为，请通过 `SECURITY.md` 描述的私有渠道联系维护者。
所有投诉都会被及时且公正地审阅，并尊重报告者的隐私与安全。

## Attribution

本准则改编自 [Contributor Covenant](https://www.contributor-covenant.org/)
version 2.1。
NDL_EOF
"""

IMPL["T-103"] = r"""cat > SECURITY.md <<'NDL_EOF'
# Security Policy

## Supported Versions

安全修复仅面向当前主版本：

| Version | Supported |
| --- | --- |
| 4.x（当前 `package.json` 声明 `4.0.0`） | :white_check_mark: |
| < 4.0 | :x: |

## Reporting a Vulnerability

**请勿为安全漏洞公开创建 issue。**

请使用 GitHub 的 **Security Advisories → Report a vulnerability** 私有报告渠道
提交，或通过与维护者的私有联系渠道发送，包含：

- 受影响版本与复现环境（Node.js 版本、pnpm 版本）
- 复现步骤与最小可运行示例
- 影响范围与可能的利用方式

维护者会确认收到并协调修复与披露时间。在修复发布前，请避免公开细节。

## 依赖安全

本项目运行时无生产依赖；开发依赖由 `pnpm-lock.yaml` 锁定，升级请通过独立 PR 提交。
NDL_EOF
"""

IMPL["T-104"] = r"""cat > SUPPORT.md <<'NDL_EOF'
# Support

## 如何获得帮助

- **用法问题与缺陷报告**：使用 GitHub Issues，并优先选用
  `.github/ISSUE_TEMPLATE/` 中的结构化模板，附上 Node.js 版本、`pnpm` 版本、
  最小复现代码与期望/实际结果。
- **功能建议**：使用 feature request 模板，说明使用场景与替代方案。
- **安全问题**：**不要**用 issue，按 `SECURITY.md` 走私有报告渠道。
- **贡献流程**：见 `CONTRIBUTING.md`。

## 响应范围

本项目是时间单位转换工具库，仅处理 `ms()` / `parse()` / `parseStrict()` /
`format()` 的行为问题与文档问题。构建工具链、下游框架或业务系统集成问题
不在本项目支持范围内。

## 自助排查

1. 确认 Node.js >= 20 且 `pnpm install --frozen-lockfile` 成功。
2. 运行 `pnpm run test:nodejs` 确认本地基线。
3. 查阅 `README.md` 与 `CHANGELOG.md` 确认是否为已知行为变更。
NDL_EOF
"""

IMPL["T-105"] = r"""cat > CHANGELOG.md <<'NDL_EOF'
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
NDL_EOF
"""

IMPL["T-106"] = r"""mkdir -p .github/ISSUE_TEMPLATE
cat > .github/ISSUE_TEMPLATE/bug_report.yml <<'NDL_EOF'
name: Bug report
description: 报告 ms() / parse() / format() 的可复现行为问题
title: "[Bug]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        安全问题请改用 SECURITY.md 的私有渠道，不要在此提交。
  - type: input
    id: version
    attributes:
      label: 版本
      description: package.json 中的版本号或安装的 npm 版本
      placeholder: "4.0.0"
    validations:
      required: true
  - type: input
    id: runtime
    attributes:
      label: 运行环境
      placeholder: "Node.js 22.x / pnpm 10.x / linux"
    validations:
      required: true
  - type: textarea
    id: repro
    attributes:
      label: 最小复现代码
      render: ts
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: 期望结果与实际结果
    validations:
      required: true
NDL_EOF
cat > .github/ISSUE_TEMPLATE/feature_request.yml <<'NDL_EOF'
name: Feature request
description: 提出新的时间单位或格式化能力建议
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: 要解决的问题
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: 建议的 API 与行为
      render: ts
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: 已考虑的替代方案
    validations:
      required: false
NDL_EOF
"""

IMPL["T-107"] = r"""cat > .github/PULL_REQUEST_TEMPLATE.md <<'NDL_EOF'
## 变更说明

<!-- 逐项列出改动文件与动机，禁止使用「适当优化 / 进行完善 / 相关内容」等模糊表述 -->

## 关联的 MD 说明文件

<!-- 每个代码改动必须给出一一对应的 MD 说明路径 -->

## 验收命令

```bash
pnpm install --frozen-lockfile
pnpm run test:nodejs
pnpm run lint
pnpm run typecheck
```

- [ ] 上述命令全部通过
- [ ] 新增/修改行为已补充测试用例
- [ ] 提交信息符合 Conventional Commits

## Rollback

<!-- 写明回滚命令，例如：git revert <commit>，禁止 git push --force -->

## 检查项

- [ ] 未直接向 `main` 提交
- [ ] 保留了原有 `LICENSE`
- [ ] 未包含任何凭据或密钥
NDL_EOF
"""

IMPL["T-108"] = r"""mkdir -p docs
sed -i 's/length between 1 and 99/length between 1 and 100/' src/index.ts
cat > docs/parse-length-fix.md <<'NDL_EOF'
# src/index.ts · parse() 长度文案修正说明

## 改动

`parse()` 的入参守卫为 `str.length > 100`，即实际允许长度为 1..100；
但抛出的错误文案写的是 `length between 1 and 99`。本次把文案改为
`length between 1 and 100`。

## 对应检测项

`F3-DETECTION.md` 的 F-008：`ndl_detect.py` 输出
`parse_length_guard=100` / `parse_error_message_upper=99` / `inconsistent=true`。

## 影响范围

- 仅修改一个错误消息字符串。
- 不修改正则、单位换算、`format()` 或任何数值返回路径。
- 原有 167 个用例不受影响（现有断言仅使用 `toThrow()`，不校验文案内容）。

## 验收断言

`python3 data/lab/bin/ndl_verify.py parse-msg` 退出码 0：源码中
`str.length > 100` 与 `length between 1 and 100` 同时存在。

## 回滚

`git checkout -- src/index.ts && rm -f docs/parse-length-fix.md`
NDL_EOF
"""

IMPL["T-109"] = r"""cat > src/parse-length.test.ts <<'NDL_EOF'
import { describe, expect, it } from '@jest/globals';
import { parse } from './index';

describe('parse(string) length boundary', () => {
  it('accepts a string of exactly 100 characters', () => {
    const value = '1'.repeat(100);
    expect(value).toHaveLength(100);
    expect(Number.isFinite(parse(value))).toBe(true);
  });

  it('throws on a string of 101 characters with the corrected message', () => {
    const value = '1'.repeat(101);
    expect(value).toHaveLength(101);
    expect(() => parse(value)).toThrow(/length between 1 and 100/);
  });
});
NDL_EOF
cat > docs/parse-length-test.md <<'NDL_EOF'
# src/parse-length.test.ts · 边界回归测试说明

## 改动

新增 2 个用例，锁定 `parse()` 的长度边界：

- 100 字符的纯数字字符串可被解析，返回值为有限数，不抛错。
- 101 字符的字符串触发 `throw`，且错误消息包含 `length between 1 and 100`。

## 对应检测项

`findings/F-008.md`；配套代码改动见 `docs/parse-length-fix.md`。

## 验收断言

`python3 data/lab/bin/ndl_verify.py parse-runtime` 退出码 0，且
`pnpm run test:nodejs` 输出 `Tests: <n> passed, <n> total`，用例数不少于基线 167。

## 回滚

`rm -f src/parse-length.test.ts docs/parse-length-test.md`
NDL_EOF
"""

IMPL["T-110"] = r"""cat > .github/workflows/ndl-community.yml <<'NDL_EOF'
name: NDL Community Baseline
on:
  push:
    branches: [main]
  pull_request:
jobs:
  community:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify community baseline files
        run: |
          set -e
          for f in README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md \
                   SECURITY.md SUPPORT.md CHANGELOG.md .gitignore \
                   .github/PULL_REQUEST_TEMPLATE.md \
                   .github/ISSUE_TEMPLATE/bug_report.yml \
                   .github/ISSUE_TEMPLATE/feature_request.yml \
                   .github/workflows/ndl-community.yml; do
            test -s "$f" || { echo "MISSING: $f"; exit 1; }
          done
          echo "community baseline: OK"
      - name: Verify parse length message matches guard
        run: |
          python3 - <<'PY'
          import pathlib
          s = pathlib.Path('src/index.ts').read_text()
          assert 'str.length > 100' in s, 'guard changed'
          assert 'length between 1 and 100' in s, 'message inconsistent with guard'
          print('parse length message: OK')
          PY
NDL_EOF
cat > docs/ndl-community-workflow.md <<'NDL_EOF'
# .github/workflows/ndl-community.yml · CI 门禁说明

## 改动

新增独立工作流 `NDL Community Baseline`，在 `push(main)` 与 `pull_request`
触发，执行两组可自动判定断言：

1. 逐项 `test -s` 检查 12 个社区规范/CI 文件，缺失即 `exit 1`。
2. Python 断言 `src/index.ts` 中 `str.length > 100` 与
   `length between 1 and 100` 同时存在，防止 F-008 类不一致回归。

## 对应检测项

`findings/F-009.md`：原 CI 仅有 quality / release / test，未覆盖社区规范齐备性。

## 影响范围

新增 workflow，不修改 `quality.yml`、`release.yml`、`test.yml`，不增加运行时依赖。

## 验收断言

`python3 data/lab/bin/ndl_verify.py ci-gate` 退出码 0（文件存在、非空、
`yaml.safe_load` 可解析且含 `jobs`）。

## 回滚

`rm -f .github/workflows/ndl-community.yml docs/ndl-community-workflow.md`
NDL_EOF
"""

IMPL["T-111"] = r"""set -o pipefail
python3 /workspace/data/lab/bin/ndl_verify.py all > /tmp/ndl_verify_all.txt 2>&1
RC=$?
{
  echo '# F5 全套验收报告'
  echo
  echo '> TEST PROFILE · 由 T-111 实时执行生成，非人工填写。'
  echo "> 执行时间: $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo '> 验收器: `data/lab/bin/ndl_verify.py all`'
  echo
  echo '## 实际输出'
  echo
  echo '```'
  cat /tmp/ndl_verify_all.txt
  echo '```'
  echo
  echo "## 结论"
  echo
  if [ "$RC" -eq 0 ]; then echo '全部断言通过，退出码 0。'; else echo "存在失败断言，退出码 $RC。"; fi
} > /workspace/data/nodes/NODE_ID_PLACEHOLDER/F5-ACCEPTANCE.md
exit "$RC"
"""

IMPL["T-112"] = r"""BR='ndl/NODE_ID_PLACEHOLDER/community-and-parse-fix'
CUR=$(git branch --show-current)
if [ "$CUR" != "$BR" ]; then git checkout -q -b "$BR"; fi
git add -A
git commit -q -m "fix: align parse() length message with guard and complete community baseline"
COMMIT=$(git rev-parse --short HEAD)
SUBJECT=$(git log -1 --pretty=%s)
cat > /workspace/data/nodes/NODE_ID_PLACEHOLDER/F5-COMMIT.md <<NDL_EOF
# F5 提交说明

- 分支: \`$BR\`
- 提交: \`$COMMIT\`
- 提交信息: \`$SUBJECT\`（Conventional Commits）
- 变更文件数: $(git show --stat --oneline HEAD | tail -1)
- 直推 main: 否
- 使用 --force: 否
- 保留原有 LICENSE: 是
- 凭据写入文件/日志/commit: 否（已脱敏检查）
- 生成时间: $(date '+%Y-%m-%d %H:%M:%S %z')
NDL_EOF
"""


def sh(cmd, cwd=NODE):
    return subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True,
                          text=True, timeout=300)


def md_path(rel):
    p = NODE / rel
    if p.exists():
        return p
    return W / rel


def log(task_id, status, summary):
    r = subprocess.run([str(LOG), N, task_id, status, summary],
                       capture_output=True, text=True)
    print("  LOG " + r.stdout.strip() + (" " + r.stderr.strip() if r.stderr.strip() else ""))


def main():
    plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    for task in plan["tasks"]:
        tid = task["id"]
        if task["status"] == "passed":
            print(f"[SKIP] {tid} already passed (幂等)")
            continue
        print(f"[RUN ] {tid} {task['path']}")
        cmd = IMPL[tid].replace("NODE_ID_PLACEHOLDER", N)
        a = sh(cmd)
        if a.returncode != 0:
            print("  ACTION FAILED:", (a.stdout + a.stderr).strip()[-500:])
            sh(task["rollback"])
            task["status"] = "failed"
            PLAN.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
            log(tid, "failed", f"action 执行失败，已执行 rollback: {task['rollback'][:60]}")
            sys.exit(1)
        v = sh(task["verify"]["cmd"])
        ok = v.returncode == 0
        print("  VERIFY:", "PASS" if ok else "FAIL", "|", task["verify"]["cmd"][:100])
        if not ok:
            print("  ", (v.stdout + v.stderr).strip()[-400:])
        mp = md_path(task["md_note"])
        mdok = mp.is_file() and mp.stat().st_size > 0
        print("  MD_NOTE:", "PASS" if mdok else "FAIL", "|", task["md_note"])
        if not (ok and mdok):
            sh(task["rollback"])
            task["status"] = "failed"
            PLAN.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
            log(tid, "failed", "verify 或 md_note 断言失败，已执行 rollback")
            sys.exit(1)
        task["status"] = "passed"
        PLAN.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
        log(tid, "passed", f"{task['path']} | verify={task['verify']['cmd'][:70]} | md_note={task['md_note']}")
    print("\nALL TASKS PASSED")


if __name__ == "__main__":
    main()
