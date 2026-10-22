---
status: evergreen
type: how-to
last-verified: 2026-10-22
verified-by: DOC-08 改 12 仓口径，逐项回实仓取证 —— ① 部署资产逐文件定归属（core
  `docker-compose*.yml` / `Dockerfile.service` / `cmd/*/Dockerfile` / `config/*.yaml` /
  `deploy/k8s/*` / `deploy/wait-for-deps.sh`；ui `Dockerfile` + `deploy/nginx-spa.conf`；
  agent `Dockerfile` 依赖命名上下文 `core`）；② `deploy/k8s/` 无 ai-service 清单
  （`ALLOWED_MISSING_IN_K8S` 登记该差异）；③ `check_deploy_consistency.py` 的覆盖面实测
  （只读 core 的 compose ↔ k8s，且只查 `COPY` 不查 `RUN`）；④ **实测阻断**：
  `Dockerfile.service` 仍 `go build ./cmd/strategy`，该目录 REV-16 已删。
---

# 部署配置：改哪里（12 仓）

> 本地开发走 core 的 `docker-compose.yml`，生产走 core 的 `deploy/k8s/`。**两套独立维护**，
> 这是有意的（不引入 Kompose / Helm 那套生成链：为几处配置给单人自托管项目加一整套工具，
> 收益不抵复杂度）。代价是可能漂移，所以有三道护栏 —— 但护栏的**覆盖面只到 core 仓**，
> 分仓之后这条例外必须先说清楚（见 §2）。
>
> **2026-09-25 形态**：本地开发侧，**数据库与缓存改为宿主机原生安装**
> （PostgreSQL 17.5 / Redis 7.4.11，由 core `tools/local-infra.sh` 启停），
> **应用服务仍然全部跑在容器里**。k8s 侧不变（postgres-statefulset + redis-deployment
> 保留 —— k8s 本就不该依赖宿主机数据库）。

---

## 1. 部署资产现在分在三个仓里

这是 DOC-08 之前最容易踩错的一处：文档按单仓写「改 `docker-compose.yml` 和
`deploy/k8s/`」，但**前端镜像、nginx 配置、AI 镜像**的真相已经不在 core 里了。

| 资产 | 在哪个仓 | 说明 |
|---|---|---|
| `docker-compose.yml` / `docker-compose.e2e.yml` | `tellurion` | 三个服务：data / analysis / ai（**没有** web，也**没有** strategy）。e2e 那份只覆盖限流额度，不定义服务 |
| `docker-compose.nt.yaml` | `tellurion` | NT 侧车的容器形态；**Windows 下不可用**（`network_mode: host` 进的是 Linux VM 命名空间，见 [nt-sidecar-operations.md](nt-sidecar-operations.md) §3） |
| `Dockerfile.service` | `tellurion` | compose 的 data / analysis 共用这一个（多阶段） |
| `cmd/analysis/Dockerfile` · `cmd/data/Dockerfile` | `tellurion` | `Makefile` 的镜像目标用这两个 |
| `config/{analysis,data,ai}-service.yaml` | `tellurion` | **三份都在 core**，包括 ai 的 —— 理由见 §1.1 |
| `deploy/k8s/*.yaml`（含 `web-deployment.yaml` / `ingress.yaml`） | `tellurion` | 编排清单全在 core，**包括 web 的** |
| `deploy/wait-for-deps.sh` | `tellurion` | 容器启动的有界等待（替换被移除的 `depends_on`） |
| `tools/{local-stack,local-infra}.sh` · `tools/check_deploy_consistency.py` | `tellurion` | 起栈入口与静态护栏 |
| `Dockerfile`（nginx + SPA） | `tellurion-ui` | 前端镜像的**构建真相**，端口 8080 |
| `deploy/nginx-spa.conf` | `tellurion-ui` | `/api` 反代 + SSE 关缓冲 + history 回退 |
| `Dockerfile`（ai-service） | `tellurion-agent` | 需要 core 作为**命名构建上下文** `core` |
| 六个服务仓的部署资产 | — | 今天都没有（占位仓，不起进程） |

### 1.1 三处跨仓耦合（改之前先知道）

1. **ai-service 的镜像构建要两个仓**：core compose 写
   `build.context: ../tellurion-agent` + `additional_contexts: [core=.]`；
   `tellurion-agent:Dockerfile` 用 `COPY --from=core …` 取 core 的 `go.mod` 目标、
   `deploy/wait-for-deps.sh`、`config/ai-service.yaml`。
   ⇒ **agent 必须与 core 同级 checkout**，否则镜像构建直接失败。
2. **ai 的配置真相留在 core**：`config/ai-service.yaml` 与 `analysis-service.yaml`
   **逐值一致**（同一个实验不得在两个进程跑出不同结果），所以它不复制进 agent 仓，
   由该仓 Dockerfile 从 `core` 上下文 `COPY` 进去。
3. **web 的镜像在 ui、编排在 core**：`deploy/k8s/web-deployment.yaml` 用的
   `image: tellurion/web:latest` 是在 **ui 仓**里 `docker build` 出来的；
   core 的 compose 里**没有** web 服务（2026-10-09 拆仓时移除）。
   ⇒ 改 web 的端口要**同时动两个仓**（§4）。

---

## 2. 护栏的覆盖面：只到 core

`python tools/check_deploy_consistency.py`（在 core 仓）是「配置漂移」那道护栏，
但**它只看见 core 的 compose 与 core 的 `deploy/k8s/`**。分仓之后必须明确它**不**管什么：

| 看不清的 | 为什么 | 谁兜 |
|---|---|---|
| `tellurion-ui:deploy/nginx-spa.conf` 的 `listen` | 不在 core 的 compose / k8s 里 | 无护栏（§4 的手工清单） |
| `tellurion-agent:Dockerfile` 的 `EXPOSE` / 构建上下文 | 同上 | 无护栏 |
| ingress 的 backend 端口 | 脚本只比 compose ↔ k8s Service 的端口 | **无护栏**（§4 已标） |
| `RUN` 里的 `go build` 目标目录 | 护栏只查 `COPY` 的源路径（AUD-48） | **无护栏** —— 今天就漏了一次（§6） |

> 这四条不是「以后补」的空话，而是**当前断言边界**。写在这里，是为了让下一个改部署的人
> 知道哪一步没有机器校验兜着。

---

## 3. 地址口径：三处不同，且都对

同一批数据库/缓存，在三个地方写的地址**必然会不一样**，这不是漂移：

| 位置 | `DATABASE_HOST` | 为什么 |
|---|---|---|
| `config/*.yaml`（core） | `localhost` | 在**宿主机上直接跑**时的视角 |
| `docker-compose.yml`（core） | `host.docker.internal` | 容器内指**宿主机**；容器里的 `localhost` 是容器自己 |
| `deploy/k8s/configmap.yaml`（core） | `postgres` | k8s 里的 Service 名 |

**服务之间的地址是另一回事**：`http://data-service:8081` 这类保持 compose 服务名 /
k8s Service 名不变 —— 服务全在容器里，这一跳没有变。不要跟着数据库一起改成 `localhost`
（宿主机的 8081 上没有 data-service）。

---

## 4. 改一个端口，要动这些地方

### 4.1 core 的服务（以 data 从 8081 改成 8082 为例）

| # | 仓 | 文件 | 改什么 |
|---|---|---|---|
| 1 | `tellurion` | `config/data-service.yaml` | `server.port: 8082`（**代码实际读的是这个**） |
| 2 | `tellurion` | `docker-compose.yml` | 端口映射 `"127.0.0.1:8082:8082"`（回环前缀不能丢，见 §5）+ healthcheck 里的端口 |
| 3 | `tellurion` | `deploy/k8s/data-deployment.yaml` | `containerPort`（Deployment）与 `port`（Service） |
| 4 | `tellurion` | 任何 `DATA_SERVICE_URL` | compose 的 environment + `deploy/k8s/configmap.yaml` |

第 4 步最容易漏：它由护栏兜住。

### 4.2 web 的端口（**跨两个仓**，且后两步没有护栏）

web 是 nginx 不是 Go 服务，端口不来自 `config/*.yaml`，而来
`tellurion-ui:deploy/nginx-spa.conf` 的 `listen`：

| # | 仓 | 文件 | 改什么 |
|---|---|---|---|
| 1 | `tellurion-ui` | `deploy/nginx-spa.conf` | `listen 8080` |
| 2 | `tellurion-ui` | `Dockerfile` | `EXPOSE 8080` |
| 3 | `tellurion` | `deploy/k8s/web-deployment.yaml` | `containerPort` 与 Service `port` |
| 4 | `tellurion` | `deploy/k8s/ingress.yaml` | backend 的 `number: 8080` |

> **第 3、4 步没有护栏兜**：`check_deploy_consistency.py` 只比对 compose ↔ k8s Service
> 的端口，不管 ingress 的 backend；而 core 的 compose 里根本没有 web 服务可比。
> **这条漏改不会报错，只会让 k8s 路径下前端打不开。**
>
> 注意 ui 仓的 `Dockerfile` 与 nginx conf 在**同一仓**，改端口时它们是一对；
> 而 k8s 清单在**另一个仓**，这一跳跨仓，最容易只改一半。

---

## 5. 端口绑定：全都只绑回环（AUD-13 的推广）

| 目标 | 由谁保证 | 怎么做 |
|---|---|---|
| 数据库/缓存只绑回环 | **原生进程的启动参数** | core `tools/local-infra.sh` 用 `-c listen_addresses=127.0.0.1` / `--bind 127.0.0.1` **显式**指定，不靠配置文件默认值 |
| 数据库/缓存只绑回环（**验证**） | `tools/local-infra.sh status` | 读 **netstat 的真实监听 socket**，出现非回环就报 `✗` |
| 应用服务只发布到回环 | core `docker-compose.yml` 的 `ports` | **全部**带 `127.0.0.1:` 前缀 |
| 应用服务只发布到回环（静态检查） | `check_deploy_consistency.py` 检查 3c | `AUTH_INSECURE` 为真 ⟹ 每条映射都必须回环 |
| 应用服务只发布到回环（**验证**） | `tools/local-stack.sh status` | 读 netstat 断言 8081/8085/8086 只绑回环 |

**为什么验证读 netstat 而不是配置文件**：配置文件可以被命令行参数覆盖 —— 这个脚本自己
就是靠 `-c` / `--bind` 覆盖的。只有 socket 是 ground truth。

**检查 3c 的四条双向规则**（open-access 的声明与发布范围**互相蕴含**）：

| # | 条件 | 要求 |
|---|---|---|
| 3c-1 | `AUTH_INSECURE` 为真 | **每一条** ports 映射都必须带 `127.0.0.1:` 前缀 |
| 3c-2 | 存在非回环映射 | 必须有非空 `JWT_SECRET`（对外发布必须配鉴权） |
| 3c-3 | `AUTH_INSECURE` 为真 | `AUTH_INSECURE_EXPOSURE` 必须是 `loopback-published` |
| 3c-4 | 同时给 `JWT_SECRET` 与 `AUTH_INSECURE=true` | 报错（密钥优先，声明会误导读者） |

> 为什么应用端口也必须回环：analysis 以 **open-access** 运行（无鉴权），而容器**必须**绑
> `0.0.0.0` 才能被发布端口转发 —— 于是「对外可达性」从绑定地址转移到了**发布层**。
> 若映射写成 `"8085:8085"`，等于把下单接口开给整个局域网。
> 决策与备选方案见 [ADR-025](../adr/adr-025-auth-exposure-publish-layer.md)。
>
> 检查 3c 认的回环写法是 `127.*` 前缀、`::1` / `[::1]`、`localhost`；**不写宿主地址**
> （裸 `"8085:8085"`）一律当成绑 `0.0.0.0`，与运行时 netstat 读到的 `0.0.0.0:8085` 一致。

验收（实测，三条一起看才完整）：

```bash
# ① 容器必须能到宿主机（这是新形态的**必需能力**，不是漏洞）
docker run --rm alpine:3.20 nc -z host.docker.internal 5432   # 应通
# ② 原生进程自身只监听回环（局域网其他机器连不上）
netstat -ano | grep LISTENING | grep 5432                      # 应只见 127.0.0.1
# ③ 容器服务的宿主侧映射也只绑回环（一条命令顶上面整张表）
cd tellurion && tools/local-stack.sh status                    # 三个端口都应 ✓
```

> ⚠️ **别用 `host.docker.internal` 去判断「绑定是否收紧」** —— 它是 Docker Desktop 的
> **宿主侧代理**，转发到 loopback，会**绕过网卡绑定**、必然「通」。拿它对绑定下结论是
> 无效的。那个问题由两个 `status` 子命令读 netstat 回答。

---

## 6. 服务清单差异（有意的，不是漂移）

| 服务 | compose（core） | k8s（core） | 说明 |
|---|---|---|---|
| postgres | ❌ **宿主机原生** | `postgres-statefulset.yaml` | 2026-09-25 移出 compose。k8s 侧不变 |
| redis | ❌ **宿主机原生** | `redis-deployment.yaml` | 同上 |
| data-service | ✅ | ✅ | |
| analysis-service | ✅ | ✅ | |
| **ai-service** | ✅ | ❌ | `ALLOWED_MISSING_IN_K8S` 里登记：拆仓阶段 1，k8s 清单待补 |
| **web** | ❌ | ✅ | 镜像在 `tellurion-ui`，编排在 core（§1.1-③） |

差异清单写在 core `tools/check_deploy_consistency.py` 的 `ALLOWED_MISSING_IN_K8S` 里。
**新增差异必须同步加进去并写明原因** —— 否则护栏会报漂移。

> `postgres` / `redis` 两条已从该清单删除：它们不再是 compose 服务，留在清单里就是死条目
> —— 「不许回到 compose」改由检查 3a 正向断言。

### ⚠️ 已知阻断：core 的容器镜像今天构建不出来

`tellurion:Dockerfile.service` 第 26 行仍在 `go build -o /app/strategy-service ./cmd/strategy`，
而该目录 REV-16（2026-10-17，ADR-012 关闭）已删。**实测**
（`docker run --rm -v "$PWD:/app" -w /app golang:1.25-alpine go build ./cmd/strategy`
→ `stat /app/cmd/strategy: directory not found`）⇒ 同一条 `RUN` 里的 data / analysis
两个二进制也一起出不来，`docker-compose up` 在构建阶段红。

这与 AUD-48 那类「删目录忘了删 `COPY`」同型，但**护栏查不到**：它只检查 `COPY` 的源路径，
不解析 `RUN` 里的 `go build` 目标。修复属 core 仓（删该行与对应的 `COPY`），不属于本仓。

---

## 7. 两个反直觉的点

**端口不来自环境变量。** 代码读的是 viper 的 `server.port`（core `cmd/analysis/setup.go`），
来自 `config/*.yaml`。所以 `ANALYSIS_PORT` / `DATA_PORT` 这类环境变量**从未被读取** ——
它们曾在 configmap 里躺了很久，2026-09-18 作为死配置清掉。想用环境变量覆盖要用 viper 的
键名：`SERVER_PORT`。

**`DATA_SERVICE_URL` 是被读的，别以为有默认值就不用配。** 它对应 viper 的
`data_service.url`（`AutomaticEnv` + `.`→`_` 替换），core `cmd/analysis/handlers_proxy.go`
里读。代码有默认值 `http://data-service:8081`，所以 k8s 里长期缺这一项也"能用" ——
但那只是因为 k8s 的 Service 名恰好也叫 `data-service`、端口恰好也是 8081。
Service 一改名就静默失效。现在显式配了。

---

## 8. 前端 web 服务（镜像在 ui 仓）

```
浏览器 ──:8080──▶ nginx（tellurion-ui 的镜像）
                    ├─ /api/*  ──反代──▶ analysis-service:8085
                    └─ 其余    ────────▶ dist/index.html（SPA history 回退）
```

### 三个「为什么这么接」

**① 由 nginx 反代 `/api`，而不是让前端直连 `:8085`。**
前端 API 基址默认是空字符串（`tellurion-ui:web/src/api/client.ts`，
`import.meta.env.VITE_API_BASE || ''`），所有请求走相对路径 `/api/...`。反代之后浏览器
看到的仍是同源的 `/api/...`，**前端一行都不用改，CORS 也不用动** ——
`SERVER_CORS_ALLOWED_ORIGINS` 现在是留空的（= 不回显任何 ACAO，最安全），同源请求根本
不触发 CORS。

**② nginx 里用 `resolver` + 变量写反代目标，不写死域名。**
`proxy_pass http://analysis-service:8085;` 这种写法，nginx 只在**启动时**解析一次并缓存到
进程退出 —— 后端晚起来会让 nginx 直接启动失败，后端重启换 IP 后 nginx 仍在打旧地址。
变量 + `resolver` 让它每次请求时解析（见 `tellurion-ui:deploy/nginx-spa.conf` 的注释）。
resolver 写了两个地址：Docker 的 `127.0.0.11` 与 k8s CoreDNS 默认的 `10.96.0.10` ——
**k8s 集群若改过 service CIDR，这个地址要跟着改**。

**③ SSE 必须显式关掉缓冲。**
同步进度用 `EventSource`。nginx 默认缓冲上游响应，SSE 事件会攒在缓冲区里不往下发 ——
前端表现是「进度条一动不动，等任务跑完才一次性跳到 100%」。要三件事一起做：
`proxy_buffering off` + 放大 `proxy_read_timeout` + 给外层中间层发 `X-Accel-Buffering: no`
（k8s 里 ingress-nginx 在本机 nginx 之前，只关自己这层不够）。

### 未实证的部分

compose 侧已实证（构建 + 跑容器 + curl 验证）。**k8s 侧只做了配置对齐，没有集群可跑** ——
`web-deployment.yaml` 与 `ingress.yaml` 属于「按同一套约定推出来的」，首次真跑 k8s 时请
重点看：`tellurion/web:latest` 镜像是否已由 ui 仓构建并推送、CoreDNS 地址是否为
`10.96.0.10`、ingress 去掉 `rewrite-target` 后 `/api/*` 是否完整透传。