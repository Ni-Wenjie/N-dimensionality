# NDL 实验室 · 环境与配置体检报告

> 报告类型：只读体检（未创建、未修改任何项目结构）
> 检测时间：2026-11-08 21:13 CST (+0800)
> 检测依据：NDL-SPEC-0001 v2.0（三层空间架构）+ 项目硬性约束
> 结论：**不可启动** —— 工具链完整，但项目骨架、契约文件、凭据、Git 身份四项前置条件缺失

---

## 一、总体判定

| 维度 | 状态 | 说明 |
|---|---|---|
| 运行时工具链 | ✅ 就绪 | git 2.43.0 / gh 2.86.0 / node 22.13.1 / python 3.11.1 |
| 数据与校验依赖 | ✅ 就绪 | PyYAML 6.0.3、jsonschema 4.26.0、pandas 3.0.0 |
| 磁盘与写权限 | ✅ 就绪 | 254G 可用；`/workspace` 可写 |
| 网络（GitHub 数据面） | ⚠️ 部分 | `ssh github.com:22` 通、codeload/raw 通；`https://github.com` 与 git-http 超时 |
| 项目骨架（三层空间） | ❌ 缺失 | `gateway/`、`data/`、`logs/`、`docs/` 全部不存在 |
| 契约文件 | ❌ 缺失 | `docs/SPEC.md`、`docs/contracts/`、`data/lab/REGISTRY.yaml` 全无 |
| 凭据 | ❌ 缺失 | 无 SSH 密钥、无 PAT、`gh` 未登录 |
| Git 提交身份 | ❌ 缺失 | `user.name` / `user.email` 均未配置 |

**判定：BLOCKED_NO_ENV** —— 可执行「读取类」工作，但 F1 克隆建节点无法按规范完成。

---

## 二、逐项检测明细

### 1. 运行时与工具链

| 检查项 | 实测结果 | 判定 |
|---|---|---|
| git | 2.43.0 | ✅ |
| gh (GitHub CLI) | 2.86.0 | ✅ 已安装，未认证 |
| node / pnpm / npm | 22.13.1 / 10.28.2 / 11.9.0 | ✅ |
| python3 | 3.11.1（pyenv） | ✅ |
| ssh | OpenSSH_9.6p1 | ✅ |
| ssh-keygen / git-credential-helper | `/usr/bin/ssh-keygen`、`/usr/local/bin/git-credential-helper` | ✅ |
| docker / make / unzip / jq | 均可用 | ✅ |
| yq | 未安装 | ⚠️ 可用 `python3 -c "import yaml"` 替代，但 `docs/contracts/` 若要求 yq 校验则会卡 |
| shellcheck / markdownlint / pre-commit | 均未安装 | ⚠️ 影响 CI 与代码质量门禁，可按需安装 |

### 2. Git 身份与提交能力

```
$ git config --global --list
safe.directory=*
credential.helper=/usr/local/system/bin/git-credential-helper
```

- ❌ `user.name` 缺失 → 任何 `git commit` 会直接失败
- ❌ `user.email` 缺失 → 同上
- ⚠️ `credential.helper` 指向沙箱托管 helper，需确认其是否支持 GitHub 托管凭据注入

### 3. 凭据与认证

| 检查项 | 结果 |
|---|---|
| `~/.ssh` 内容 | 空目录（无任何密钥对） |
| `GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_PAT` / `GIT_SSH_KEY` | 全部 unset |
| `gh auth status` | `You are not logged into any GitHub hosts` |

SSH 通道已实测打通（用一次性探测密钥连接）：

```
$ ssh -T git@github.com
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
git@github.com: Permission denied (publickey).
```

> 这是**好消息**：transport 层已到达 GitHub SSH 服务，只差把公钥注册到账号。注册后 `git clone git@github.com:...` 即可用，无需账号密码（符合硬性约束 1）。

### 4. 网络可达性（关键差异点）

| 端点 | 结果 | 影响 |
|---|---|---|
| `github.com:22` (TCP) | ✅ 通 | SSH 克隆可用（需密钥） |
| `github.com:443` (TCP) | ✅ 通，但 HTTP 请求 12s 超时 | 网页访问、`gh auth login` 设备流不可用 |
| `git ls-remote https://github.com/...` | ❌ 30s 超时 | **git-http 协议不可用** |
| `api.github.com` | ⚠️ 403，`API rate limit exceeded for 82.157.163.131`（共享出口 IP，60/h 已耗尽） | 认证后可用；匿名几乎不可用 |
| `raw.githubusercontent.com` | ✅ 200 | 可读单文件 |
| `codeload.github.com` | ✅ 200，实测下载 `octocat/Hello-World` tarball 成功（258B，可解压） | **可作为 HTTPS 兜底克隆通道** |
| pip / npm 源 | ✅ 可正常下载（实测 `pip download pyyaml` 成功） | 依赖安装无阻 |

系统时间：`2026-11-08 21:13:20 CST (+0800)` —— 与日志时间戳要求一致 ✅

### 5. 项目骨架（三层空间）

本地 `/workspace` 实测：

```
/workspace
└── .codebuddy          # 空，无任何项目文件
```

| 规范要求路径 | 状态 |
|---|---|
| `gateway/`（登记与路由） | ❌ MISSING |
| `data/`（lab 配置 + 各节点产物） | ❌ MISSING |
| `logs/`（MAIN.md + 节点日志） | ❌ MISSING |
| `docs/SPEC.md` | ❌ MISSING |
| `docs/contracts/`（路线/计划 YAML 契约） | ❌ MISSING |
| `data/lab/REGISTRY.yaml`（NODE-ID 唯一来源） | ❌ MISSING |

全盘 `find` 检索 `ndl-lab`、`SPEC.md`：**零命中**（已排除 `/proc`、`node_modules`）。

项目网盘（tdrive，root `FcJMbReJlZOc`）实测仅两项：

- `系统文件/`（空目录，0 项）
- `资产库使用指南.pdf`（898 KB，平台说明文档，非项目资产）

→ **项目网盘无任何 ndL 项目产物，无历史报告/路线/计划可继承。**

---

## 三、启动前必须补齐的输入（阻塞项）

| 编号 | 阻塞项 | 类型 | 解除方式 |
|---|---|---|---|
| B1 | 缺 `repo_url`（目标 GitHub 仓库） | 信息缺失 | 提供仓库 HTTPS/SSH 地址 |
| B2 | 缺 `NODE-ID` 与 `data/lab/REGISTRY.yaml` | 结构缺失 | 提供节点登记表，或授权按 `NODE-<YYYYMMDD>-<4hex>-<repo-slug>` 规则生成并登记 |
| B3 | 无 GitHub 凭据（SSH 公钥未注册 / PAT 未注入） | 认证 | 注入 Ed25519 私钥或 Fine-grained PAT（仅经环境变量）；公开仓库可先用 codeload 兜底拉取，但 F2 发布闸门仍必须凭据 |
| B4 | 无项目骨架与契约文件（`docs/SPEC.md`、`docs/contracts/`） | 结构缺失 | 需明确：由我按 NDL-SPEC-0001 v2.0 初始化骨架，还是从别处同步现成骨架 |
| B5 | `git user.name` / `user.email` 未配置 | 配置 | 提供提交身份（或授权使用 NDL 机器人身份） |

次要项（不阻塞 F1，但阻塞后续验收）：`yq`、`shellcheck`、`markdownlint`、`pre-commit` 未安装，可按 F5 任务清单按需安装。

---

## 四、结论

**当前环境「可跑」，但项目「不可启动」。**

- 基础设施层面没有硬伤：工具链齐、磁盘足、SSH 与 codeload 两条 GitHub 通道可用、包源通畅。
- 项目层面等于一片空白：三层空间、契约、登记表、凭据、提交身份全部缺失。
- 因此无法进入 F1（克隆建节点）——若强行开始，会违反「禁止遍历目录猜测 NODE-ID」「凭据仅由环境变量注入」两条硬性约束。

**下一步（需你确认）**：补齐 B1/B2 信息 + 授权 B4 的骨架初始化方式 + 注入 B3 凭据 + 确认 B5 提交身份后，即可按 `F1 → F3 → F4 → F5 → F2` 启动。
