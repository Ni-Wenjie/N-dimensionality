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
