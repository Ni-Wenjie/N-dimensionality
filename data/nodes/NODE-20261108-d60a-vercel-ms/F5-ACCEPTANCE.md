# F5 全套验收报告

> TEST PROFILE · 由 T-111 实时执行生成，非人工填写。
> 执行时间: 2026-11-08 22:28:38 +0800
> 验收器: `data/lab/bin/ndl_verify.py all`

## 实际输出

```
PASS present+nonempty: .github/ISSUE_TEMPLATE/bug_report.yml
PASS present+nonempty: .github/ISSUE_TEMPLATE/feature_request.yml
PASS present+nonempty: .github/PULL_REQUEST_TEMPLATE.md
PASS present+nonempty: .gitignore
PASS present+nonempty: CHANGELOG.md
PASS present+nonempty: CODE_OF_CONDUCT.md
PASS present+nonempty: CONTRIBUTING.md
PASS present+nonempty: LICENSE
PASS present+nonempty: README.md
PASS present+nonempty: SECURITY.md
PASS present+nonempty: SUPPORT.md
PASS parse guard/message consistent
PASS regression test present
PASS ci gate workflow present
PASS ci gate YAML parseable
PASS YAML parseable: .github/ISSUE_TEMPLATE/bug_report.yml
PASS YAML parseable: .github/ISSUE_TEMPLATE/feature_request.yml
PASS pnpm run test:nodejs (169 passed)
      
      Test Suites: 5 passed, 5 total
      Tests:       169 passed, 169 total
      Snapshots:   0 total
      Time:        0.281 s, estimated 1 s
      Ran all test suites.

RESULT mode=all failed=0
```

## 结论

全部断言通过，退出码 0。
