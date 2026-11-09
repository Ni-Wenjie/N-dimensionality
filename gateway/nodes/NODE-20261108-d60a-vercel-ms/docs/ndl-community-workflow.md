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
