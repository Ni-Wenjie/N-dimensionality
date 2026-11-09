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
