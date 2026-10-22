---
status: evergreen
type: how-to
last-verified: 2026-10-22
verified-by: DOC-08 改 12 仓口径，逐项回实仓取证 —— ① checkout 集与同级约束（`tellurion-agent:go.mod`
  的 `replace tellurion => ../tellurion`、core `docker-compose.yml` 的 `context: ../tellurion-agent`）；
  ② `go.work` 在 12 仓 `.gitignore` 里各有一条（本机 `Get-ChildItem -Recurse -Filter go.work` 实测 0 个）；
  ③ core 今天**不 require** 两个库仓（`tellurion:go.mod` 无 `github.com/ruoxizhnya/*` 行），
  故单仓 `go build ./...` 就够；④ 各仓测试文件数实测（core 438 / agent 89 / contracts 23 / kit 29 /
  ui 38 vitest + 23 e2e spec）；⑤ **实测到一处真阻断**：core 的 `Dockerfile.service` 仍在
  `go build ./cmd/strategy`，而该目录 REV-16 已删 —— `docker run golang:1.25-alpine … go build
  ./cmd/strategy` 实测 `directory not found`；⑥ agent 的 `cmd/ai` 读 `config/ai-service.yaml`
  且 `LoadConfig` 缺文件即 Fatal，而 agent 仓没有 `config/` 目录 —— 必须给 `CONFIG_PATH`；
  ⑦ Go 侧无 dotenv 加载器（`grep godotenv` 零命中），`.env` 只由 compose 读，而
  `pkg/storage.BuildDSN` 在密码为空时返回 `ErrEmptyDBPassword` ⇒ 原生跑法必须 `export
  DATABASE_PASSWORD`（原文「cp .env 然后 go run」跑不起来）；⑧ `Makefile` 的 `build` 目标
  现在只含 `build-analysis` / `build-data`（`git grep '^build' Makefile` 实测），原文
  「`make build` 会失败因为仍在 build 已删目录」已不成立 —— 真正的障碍是本机没装 `make`。
---

# 本地开发指南（12 仓）

> 只写**当前确实可用**的步骤。遇到与本文不符的情况，以代码为准并回来更新本文。
>
> 本仓不复制各仓的构建细节：单仓的「怎么构建 / 边界 / 禁止」以**该仓 `AGENTS.md`** 为准，
> 本文只回答分仓之后新出现的问题 —— **同时 checkout 哪些仓、`go.work` 怎么用、
> 跨仓起栈的顺序与坑**。仓名与 module path 的唯一真相源是
> [core `repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md)。

---

## 1. 先决定你要 checkout 几个仓

十二仓不是「全都要」。按你要做的事选最小集：

| 你要做的事 | 必须 checkout | 为什么 |
|---|---|---|
| 改回测引擎 / 后端 API / 存储 | `tellurion`（core） | 自足：core 今天**不 require** 两个库仓，`go build ./...` 单仓就能过 |
| 加前端页面 / 跑 e2e | + `tellurion-ui` | `web/` 与 `e2e/` 只在 ui 仓，core 里没有 |
| 动 AI 实验员 / 工具注册表 | + `tellurion-agent` | 且**必须与 core 同级目录**（见下） |
| 改跨边界类型 / 横切工具 | + `tellurion-contracts` / + `tellurion-kit` | 契约与工具库各自单仓可构建 |
| 用数据 / 策略 / 风控 / 分析 / 编排 / 交易网关六服务 | **不需要** | 六仓今天只有 `go.mod` + `doc.go`（占位），没有实现、不起进程 |
| 改本仓文档 | 只本仓 | 门禁是链接检查 + 跨仓引用检查（见 §6） |

推荐的工作区形态：

```
Workspace/
├── tellurion/              ← core（application）
├── tellurion-agent/        ← AI 实验员
├── tellurion-ui/           ← 前端 + e2e
├── tellurion-contracts/    ← 库：port / DTO / 四契约
├── tellurion-kit/          ← 库：横切工具
└── tellurion-docs/         ← 本仓
```

> ⚠️ **同级不是习惯，是硬约束**，两个机制按相对路径解析：
> ① `tellurion-agent:go.mod` 的 `replace tellurion => ../tellurion`（拆仓过渡态，
> S3 删除，见 `tellurion-agent:docs/adr/0001-编译期依赖-core-是过渡态.md`）；
> ② core `docker-compose.yml` 的 `ai-service.build.context: ../tellurion-agent`
> （镜像内还需要 `additional_contexts: core=.`）。把 agent 放到别处，两处同时断。

---

## 2. `go.work` 怎么用

**今天它是可选的**（这一点和很多「多仓联调」直觉相反，所以写清楚）：

- core 的 `go.mod` 里没有任何 `github.com/ruoxizhnya/tellurion-contracts` / `-kit` 的
  `require` —— S1 的**两个库仓侧**已落码（429 导出符号、13 包），但**core 侧的下游腿
  还没执行**。所以 core 单仓 `go build ./...` / `go vet ./...` 就能过，不需要 `go.work`。
- agent 靠 `replace` 指向本地 core，也不需要 `go.work`。

**什么时候它会变成必需**：core / agent 一旦把两个库仓从伪版本/tag 切进 `require`，
本地要同时改三个仓就得用 workspace：

```bash
cd tellurion
go work init . ../tellurion-contracts ../tellurion-kit
go env GOWORK          # 非空 = 已启用；空 = 没用 workspace
```

三条纪律（跨仓规则 C1/C2，见 ADR-034）：

1. **`go.work` / `go.work.sum` 不入库** —— 十二仓的 `.gitignore` 各有一条。
2. **CI 与 Docker 没有它** —— 它们按 `go.sum` 拉真实版本，这正是「别人机器上构建行为一致」的来源。
3. **`replace` 指向仓外路径 = CI 红**（唯一过渡例外是上面 agent 那条）。要复用的形状进
   `tellurion-contracts`，不要新造 core client。

---

## 3. 环境要求

| 项 | 版本 | 用在哪 |
|---|---|---|
| Go | **1.25** | core / agent / contracts / kit（四仓 `go.mod` 一致） |
| PostgreSQL | **17.5**（宿主机原生） | core（`~/.workbuddy/binaries/postgres/`） |
| Redis | **7.4.11**（宿主机原生） | core（`~/.workbuddy/binaries/redis-7.4.11/`） |
| Node | 22 | `tellurion-ui:web/` 与 `tellurion-ui:e2e/` |
| Python | **3.12+**（`nt-sidecar` 的硬要求）；本仓检查脚本仅标准库、语法下限 3.9 | core 的 `nt-sidecar/`、本仓的检查脚本 |

> ⚠️ **Go 不在 PATH**：本机装在 `C:\Users\ruoxi\sdk\go1.25.0`。跑任何 Go 命令前先：
> ```bash
> export PATH="/c/Users/ruoxi/sdk/go1.25.0/bin:$PATH"
> ```
> PowerShell 里是 `$env:PATH="C:\Users\ruoxi\sdk\go1.25.0\bin;$env:PATH"`。

---

## 4. 起基础设施

数据库与缓存是**宿主机原生安装**，不是容器（2026-09-25 定案，理由见 core
`docker-compose.yml` 文件头）；**应用服务仍然全在容器里**。这条形态没随拆仓改变 ——
变的只是「哪些服务在哪个仓里被构建」。

**今天真正能跑通的是「只起原生那半 + 服务用 `go run`」**（容器那半构建不出来，见下）：

```bash
cd tellurion                 # 下面所有相对路径都以 core 仓根为基准
cp .env.example .env         # 一次性；**只有 compose 会读它**（见下面的注记）
tools/local-infra.sh start   # 原生 PostgreSQL 17.5 + Redis 7.4.11（均显式绑回环）
tools/local-infra.sh status  # 读真实 netstat 断言只绑回环（AUD-13 运行时那一半）
```

> ⚠️ **`.env` 不会自动进 `go run` 的进程环境**：本仓 Go 代码没有任何 dotenv 加载器
> （`grep godotenv` 零命中），`.env` 只由 `docker-compose` 自己读。所以 §5 的原生跑法
> **必须显式 export** 需要的变量，否则 `pkg/storage.BuildDSN` 会以
> `database password is empty` 直接 Fatal（`config/*.yaml` 的 `password` 是空串，这是有意的）。

`tools/local-stack.sh {start|stop|status}` 是「原生 + 容器」整栈的统一入口，它做的四步与
**为什么不能只看 `up` 的退出码**：

1. 探 Docker 引擎**是否真的活着**（Docker Desktop 在本机**会自发退出**，此后所有 docker
   命令都报管道不存在，读起来像路径问题而不是「引擎没了」）；
2. `tools/local-infra.sh start`（原生 PostgreSQL 17.5 + Redis 7.4.11，均显式绑回环）；
3. `docker-compose up -d` —— **今天卡在这一步**，见下面的阻断；
4. **等健康 + 端口体检** —— 判据是 HTTP 探针全通（`up` 返回 0 只代表容器被创建了），
   再读真实 `netstat` 断言三个端口只绑回环（AUD-13 运行时那一半，见 [ADR-025](../adr/adr-025-auth-exposure-publish-layer.md)）。

`docker-compose.yml` 里的服务只有三个：`data-service`(:8081) / `analysis-service`(:8085) /
`ai-service`(:8086)。**`strategy-service`(:8082) 已于 REV-16 删除**；前端 `web`(:8080) 由
`tellurion-ui` 自己的镜像提供，不在 core 的 compose 里。

### ⚠️ 已知阻断：容器那半今天构建不出来

`Dockerfile.service` 第 26 行仍在 `go build -o /app/strategy-service ./cmd/strategy`，
而该目录 REV-16（2026-10-17）已随 ADR-012 关闭删除。**实测**
（`docker run --rm -v "$PWD:/app" -w /app golang:1.25-alpine go build ./cmd/strategy`
→ `stat /app/cmd/strategy: directory not found`）⇒ 同一条 `RUN` 里的
`data-service` / `analysis-service` 两个二进制也一起出不来，`docker-compose up` 在构建阶段
就红。**本机迭代请走 §5 的原生 `go run` 路线**。

> 修这一行是 core 仓的活（删掉那条 `go build` 与对应的 `COPY`），不属于本仓；
> 本仓只负责把「今天实际可用的是哪条路」写清楚。AUD-48 那类「删目录忘了删 Dockerfile
> COPY」的护栏只查 `COPY` 源路径，**查不到 `RUN` 里的 `go build` 目标** —— 这是它漏掉的一次。

---

## 5. 跑服务（原生）

三个仓各自在**自己的仓根**跑，且都要注意配置文件路径（`LoadConfig` 读不到文件是
`Fatal`，不是降级）。

### 5.1 core

```bash
cd tellurion

# 原生跑法不读 .env —— 密码必须显式给，否则 BuildDSN 以 ErrEmptyDBPassword 退出
export DATABASE_PASSWORD=postgres

# analysis：本地 open-access —— AUTH_INSECURE=true + server.host 必须是回环
# （config/analysis-service.yaml 的 server.host 是 0.0.0.0，容器形态需要它，
#   原生跑法必须覆盖成回环，否则拒绝启动）
AUTH_INSECURE=true SERVER_HOST=127.0.0.1 go run ./cmd/analysis   # :8085

go run ./cmd/data        # :8081（TUSHARE_TOKEN 空 → 适配器降级，服务照常起）
go run ./cmd/dualrun -strategy bh   # 双跑对账；需侧车 + 真库，见 nt-sidecar-operations.md §1.2
```

连接串：`postgres://postgres:postgres@127.0.0.1:5432/tellurion?sslmode=disable`
（库名 **`tellurion`**；建表在 `tellurion:pkg/storage/postgres.go` 的
`migrationStatements()`，首次连接时按序执行，**没有**版本表 / down / 执行记录）。

`cmd/dualrun` 是**引擎的验收门**（CI `align-gate`），不是生产服务：它必须在同一进程里
链接 `pkg/backtest` 与 `pkg/backtest/nautilus` 两套内核，所以 2026-10-20 裁决**留 core**，
不迁 `tellurion-orchestration`。**`nautilus.Runner` 没有回退分支**（`tellurion:pkg/backtest/nautilus/runner.go`
文件头写死 fail-closed）—— 侧车不可用时显式报 `kernel "nautilus" unreachable`，不会静默换成
go 内核的结果。

### 5.2 agent（AI 实验员，:8086）

```bash
cd tellurion-agent
export DATABASE_PASSWORD=postgres     # 同 §5.1：agent 也走 BuildDSN，不读 .env
CONFIG_PATH=../tellurion/config/ai-service.yaml go run ./cmd/ai
```

> ⚠️ **`CONFIG_PATH` 不是可选的**：`cmd/ai` 的默认路径是 `config/ai-service.yaml`，
> 而 **agent 仓没有 `config/` 目录**（配置的真相留在 core，理由是它与
> `analysis-service.yaml` 逐值一致 —— 同一个实验不得在两个进程跑出不同结果）。
> `bootstrap.LoadConfig` 读不到文件直接 `Fatal`。容器形态由
> `tellurion-agent:Dockerfile` 用 `COPY --from=core config/ai-service.yaml` 解决，
> 原生跑法就得自己给 `CONFIG_PATH`。
>
> 另外 agent 的 `cmd/ai` 今天仍 `import` core 的 `pkg/*`（`replace` 过渡态），
> 所以 core 必须在其同级目录；S3 删掉 `replace` 之后这一条才会解除。

### 5.3 ui（前端，:5173 dev）

```bash
cd tellurion-ui/web
npm ci                       # 用 ci 而非 install：lockfile 不同步时直接失败
npm run dev                  # :5173，Vite 只代理 /api → http://localhost:8085
```

### 5.4 端口一览

| 端口 | 谁 | 说明 |
|---|---|---|
| 8080 | `tellurion-ui` 的 nginx | SPA + `/api` 反代（`tellurion-ui:deploy/nginx-spa.conf`） |
| 8081 | core `cmd/data` | 数据服务 |
| 8085 | core `cmd/analysis` | 主 API 网关（含风控与执行裁决，进程内） |
| 8086 | agent `cmd/ai` | copilot / pipeline / explore / tools 四族 |
| 5173 | Vite dev server | 仅开发 |
| 9100 | core `nt-sidecar` | Nautilus 侧车，运维见 [nt-sidecar-operations.md](nt-sidecar-operations.md) |
| 5432 / 6379 | 原生 PG / Redis | 无 TimescaleDB（只是 Warn）、Redis 无 `requirepass` |

### 5.5 鉴权：两种姿势，默认 open-access

**① 带鉴权（任何非本机部署都必须）**：`export JWT_SECRET=$(openssl rand -hex 32)`。
生效后 `/api/*` 要 `Authorization: Bearer <access_token>`，token 从 `POST /api/auth/login` 拿。
既不给密钥、也不开 `AUTH_INSECURE` 时服务直接拒绝启动（`auth: JWT secret missing`）。

首个管理员在浏览器里建（[ADR-026](../adr/adr-026-first-admin-bootstrap-and-spa-auth.md)）：
`GET /api/auth/status`（公开）→ `bootstrap_required=true` 时登录页显示「创建首个管理员」→
`POST /api/auth/bootstrap`（公开，**只在 `users` 表为空时可用**）→ 拿 token 进控制台。
**窗口此后永久关闭**，同一端点一律 403；之后建号只走 `POST /api/auth/admin/users`。

**② 无鉴权的本地模式（开发默认）**：必须 `AUTH_INSECURE=true`，**外加**二者之一 ——

```bash
# (a) 原生跑法：进程直接绑回环
AUTH_INSECURE=true SERVER_HOST=127.0.0.1 go run ./cmd/analysis

# (b) 容器跑法：容器必须绑 0.0.0.0 才能被转发，于是判据换成「发布层」
AUTH_INSECURE=true AUTH_INSECURE_EXPOSURE=loopback-published
```

两条都不满足时豁免**无效**（照样拒绝启动）—— 否则等于把回测与下单接口开给整个局域网。
`AUTH_INSECURE_EXPOSURE` 的取值必须**逐字**等于 `loopback-published`：拼错按「没声明」
处理（fail closed）。声明本身不提供保证，保证来自两处机器校验：
core `tools/check_deploy_consistency.py` 的检查 3c（静态）+ `tools/local-stack.sh status`
（运行时 netstat）。决策见 [ADR-025](../adr/adr-025-auth-exposure-publish-layer.md)。

> ⚠️ **`/api/auth/status` 被限流豁免**（与 `/health` 同理），否则前端分不清「被限流」与
> 「未认证」。名单在 `tellurion:pkg/bootstrap/server.go` 的 `RateLimitExemptPaths`
> （`cmd/analysis/setup.go` 以 `rateLimitExemptPaths` 引用它），护栏
> `tellurion:cmd/analysis/rate_limit_exempt_test.go`。**别把 `/api/auth` 前缀整个放开** ——
> `/api/auth/login` 与 `/api/auth/refresh` 必须继续限流（口令爆破的第一道闸）。

### 5.6 e2e 必须是 open-access

`tellurion-ui:e2e/playwright.config.ts` 的 `BACKEND_URL` 默认 `http://localhost:8085`，
Playwright 与 `tellurion-ui:e2e/tests/rbac-open-access.spec.ts` **都不带 token**。所以整套
e2e 只能打一个 open-access 的栈；开了鉴权的形态只成立 `e2e/tests/auth-login-flow.spec.ts`。

限流也要放宽（整套 e2e 从 `127.0.0.1` **一个 IP** 出量，API 密集段必然撞 100/min）：
用 core 的显式覆盖层，**不要**改默认值 ——

```bash
cd tellurion
docker-compose -f docker-compose.yml -f docker-compose.e2e.yml \
  up -d --force-recreate --no-deps analysis-service data-service
```

代价写在该文件头：这个姿势下 e2e **不再覆盖**「限流生效」，那条由
`cmd/analysis/rate_limit_exempt_test.go` 的对照组与 `rate_limit_budget_test.go` 守。

---

## 6. 本地复现 CI（每仓各一套）

十二仓的 CI **互不 checkout**（唯一例外是 core→agent 的编译护栏）。所以「本地复现 CI」
= 在**对应仓根**跑那一套：

| 仓 | 本地同款命令 |
|---|---|
| `tellurion` | `go build ./...` · `go vet ./...` · `GOOS=windows go vet ./...` · `gofmt -l .` · `go test ./... -count=1 -race -coverprofile=coverage.out` + `go run ./tools/coveragegate …` · `python tools/check_doc_links.py` · `python tools/check_deploy_consistency.py` · `python tools/check_repo_autonomy.py --self-test && python tools/check_repo_autonomy.py`；另两条 job：`cd nt-sidecar && python -B -m unittest discover -s tests -t .`、`go run ./cmd/dualrun -strategy bh -gate`（后者要侧车 + 已灌库） |
| `tellurion-agent` | `go build ./...` · `go vet ./...` · `go test ./... -count=1`（要 core 同级；CI 里是 checkout core 后 `go mod edit -replace`） |
| `tellurion-contracts` | `gofmt -l .` · `go build ./...` · `go vet ./...` · `go run ./tools/check_api_surface` · `go run ./tools/check_release_matrix` · `go test ./... -count=1` |
| `tellurion-kit` | 同 contracts，但 `check_api_surface` 换成 `go run ./tools/check_scope`；`check_release_matrix` **两条都在** |
| `tellurion-ui` | `cd web && npm ci && npm run lint && npm run typecheck && npm test`（e2e job 在 CI 里是手动触发） |
| `tellurion-docs`（本仓） | `python tools/check_doc_links.py` · `python tools/check_guide_refs.py` · `python tools/test_check_guide_refs.py` · `python tools/check_repo_docs.py` |

> 两个库仓的「单仓可自证」是 R1/R2 判据：**任何一步需要别的仓的源码目录才过，就是边界画错了**
> —— 停下来修边界，**不要**加 `replace ../xxx` 绕过。
>
> `check_repo_docs.py` 与 `check_guide_refs.py --workspace` 都是**工作区级**工具：它们要看见
> 12 个仓目录，而 CI 只 checkout 自己，所以**不进 CI**（前者已在 DOC-07 登记，后者同此定位）。

---

## 7. 测试

```bash
# core（storage 层需要 PG 在跑，否则会 t.Skip —— 跳过不是通过）
cd tellurion && go test ./... -count=1

# 各仓的 test 文件数（实测快照，2026-10-22；要当前值就自己数）
#   core 438（不含 e2e/2）· agent 89 · contracts 23 · kit 29 · ui 38 vitest / 23 e2e spec
```

> 跑 core 全仓测试前把 Go 的 bin 目录放进 `PATH`，并设 `GOPROXY=off` —— 见
> [TEST.md](../TEST.md) §2.0「本机运行前置」。缺前者会让需要子进程 `go build` 的用例
> 找不到 `go`，缺后者会让它联网解析 import 而挂到超时。

---

## 8. 已知陷阱（会浪费你时间的坑）

| 坑 | 现象 | 处置 |
|---|---|---|
| **容器构建必红** | `docker-compose up` 在 `go build ./cmd/strategy` 处失败 | 见 §4「已知阻断」；用原生 `go run` |
| **在 agent 仓直接 `go run ./cmd/ai`** | `Failed to read config file` 后 Fatal | 给 `CONFIG_PATH=../tellurion/config/ai-service.yaml` |
| **原生跑法报 `database password is empty`** | 拷了 `.env` 却没用 —— Go 侧不加载 dotenv | `export DATABASE_PASSWORD=postgres`（`.env` 只服务 compose） |
| **agent 被放到别处** | 编译期 `replace tellurion => ../tellurion` 解析失败 | 必须与 core 同级 |
| **`web/` 在 core 里找不到** | `cd web` 报目录不存在 | 前端在 `tellurion-ui:web/`，2026-10-09 已拆出 |
| **`pkg/ai` 在 core 里找不到** | 同上 | AI 层在 `tellurion-agent:pkg/ai/` |
| **存储测试"通过"但其实没跑** | 连不上库时 `testStore()` 会 `t.Skip` | 起 Postgres 再跑；`go test -v` 看 SKIP 数 |
| **新库是空的** | 少数依赖预置数据的测试在空库下 `t.Skip` | 起 PG 并跑一次数据同步；多数存储层测试已「自灌自证」 |
| **Windows 特有的测试失败** | 写死 POSIX 路径（`/tmp`）在 Windows 下语义不同 | 新增测试用 `t.TempDir()` |
| **本机没有 `make`** | `make build` 报 `command not found`（Windows + Git Bash 未装 make） | 用 `go build ./...`；跨仓护栏用 `sh tools/ci/agent_compat.sh`。**注意 `Makefile` 本身是好的** —— 它只 build `cmd/analysis` 与 `cmd/data`，两个目录都在（`build-execution` / `build-risk` / `build-strategy` 早已删除，别再照旧文档以为 `make build` 必炸） |
| **容器里连不上数据库/缓存** | 应用日志 `connection refused` 指向 `localhost:5432` | 容器内必须用 `host.docker.internal`；漏注入时 `check_deploy_consistency.py` 检查 3 会报 |
| **服务起不来：`Failed to connect to PostgreSQL`** | 连不上库是 `logger.Fatal()`、**没有重试** | 先 `tools/local-infra.sh status`；容器启动由 `deploy/wait-for-deps.sh` 有界等待 |
| **服务起不来：`auth: JWT secret missing`** | 没密钥就拒绝启动 | 见 §5.5（① 带鉴权 或 ② 本地无鉴权） |
| **`go.work` 混进提交** | CI 的 C2 判据红 | `.gitignore` 已挡，别 `git add -f` |
| **改了文档没跑链接检查** | 本仓 CI 唯一门禁就是它 | `python tools/check_doc_links.py` + `check_guide_refs.py` |

---

## 9. 前端（在 `tellurion-ui`，不在 core）

```bash
cd tellurion-ui/web
npm run dev                      # :5173
npm run typecheck && npm test    # 38 个测试文件 / vitest
```

Dev 下 Vite 只代理 `/api`（`tellurion-ui:web/vite.config.ts`），因此缺少 `/api` 前缀的调用会 404。

**鉴权相关（ADR-026）**：`tellurion-ui:web/src/api/client.ts` 是全前端唯一的 HTTP 出口，
`Authorization: Bearer` 在那里注入一次；**没有 token 时不带头**（这是 open-access 形态与
加鉴权之前「逐字节相同」的依据）。401 的处理是「换令牌 → 重放」，结局分三态
（`refreshed` / `rejected` / `unavailable`）——只有服务端明确拒绝才算会话失效，断网不登出。

**姿势探测也是四态**（`tellurion-ui:web/src/stores/auth.ts`）：`unknown` / `open-access` /
`anonymous` / `unavailable`。后两者**不能合并**：`anonymous` 是「后端**说了**要凭据」，
`unavailable` 是「后端**没说话**」（429 / 5xx / 断网）。合并的后果是一次限流把已登录用户
弹到登录页。

```bash
# ⚠️ Windows 下别直接跑 node_modules/.bin/vitest（POSIX 脚本，报 WinError 193）：
cd tellurion-ui/web && node node_modules/vitest/vitest.mjs run src/api/client.auth.test.ts
```