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
