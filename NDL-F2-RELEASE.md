# F2 真实发布记录 · NODE-20261108-d60a-vercel-ms

- 发布时间: 2026-11-09 17:12:05 +0800
- 认证方式: SSH Ed25519（经进程内 ssh-agent 注入，未写入任何文件/日志/commit）
- 认证探测: `Hi Ni-Wenjie! You've successfully authenticated`
- 目标仓库: `git@github.com:Ni-Wenjie/N-dimensionality.git`（用户自有仓库，非第三方）
- 发布分支: `ndl/NODE-20261108-d60a-vercel-ms/fullflow-release`
- base: `main` @ `340e0f8`
- 未直推 main: 是
- 未使用 --force: 是
- Conventional Commits: 是
- 保留目标仓库原有 LICENSE / README: 是（README 未改动）
- 脱敏扫描: 私钥/Token 特征 0 命中

## 发布内容

三层空间骨架（`gateway/` 登记、`data/` 实验室配置与节点产物、`logs/` 两级日志）、
`docs/SPEC.md`（TEST PROFILE）与 `docs/contracts/` 契约、路线/计划 YAML、
F3 检测报告与 9 份 findings MD、F5 验收与提交说明、F2 闸门结论与 PR 草案、
F3 迭代复检、两份全流程/环境报告，以及节点工作区源码（13 新增 + 1 修改）。

## 与用户给定命令的差异

| 用户命令 | 本次执行 | 原因 |
| --- | --- | --- |
| `git init` 从零建仓 | 克隆已有 `main` 后建特性分支 | 目标仓库已存在；本项目不对新建业务项目做从零创作 |
| `git push -u origin main` | `git push origin ndl/NODE-20261108-d60a-vercel-ms/fullflow-release` | 硬性约束：禁止直推 main |
| `https://github.com/...` remote | `git@github.com:...` | 本沙箱 git-http 超时；凭据为 SSH Ed25519 |
| `first commit` | `docs: publish NDL full-flow test deliverables (TEST)` | Conventional Commits |
