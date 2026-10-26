---
status: evergreen
last-verified: 2026-10-26
verified-by: DOC-10 + DOC-11 + DOC-12（2026-10-26）：按第四轮目的对齐审计与 ADR-036 订正 §3 依赖边、§5「今天实际」、§7 阶梯/过渡态（六仓=服务、G0 并行、risk 控制面+进程内裁决、broker 服务）；实测依据 = 12 仓 `go.mod` / `git log` / 各仓 `cmd/*service` 默认监听 / core `deploy/k8s/` / core 配置开关。此前：分仓后的总体设计重写（12 仓已建、ADR-D29/D30/D31 已裁决）；逐条对照 core 的 repo-topology / repo-inventory 与六份服务设计文档
---

# 总体设计（SYSTEM DESIGN）

> **本文是"整个系统怎么设计"的现行版本。** 只写跨仓的结构与边界判断；每个仓的表、接口、链路细节在**该仓的 `docs/`** 里，本文只给指针。
> 与 [`ARCHITECTURE.md`](ARCHITECTURE.md) 的分工：那份是**拆仓前的历史 Reference**（含端口/表数等已失效数字），本文是**现任**。两者冲突时以本文 + 各仓 `docs/` 为准。

---

## 1. 一段话

自托管的 A 股量化研究平台。**AI 是操作回测底座的实验员，人是实验室主任。** 系统由一个**高内聚的内核**（回测 / 策略运行时 / 撮合 / 结算 / 仪器域存储）加若干**可独立部署的能力服务**（数据 / 策略资产 / 风控 / 分析 / 编排 / 交易通道）组成，全部通过**版本化的契约仓**交换形状，通过**每个服务一个 PG schema** 划分数据归属。

---

## 2. 五条设计原则（每条都有代价，不是口号）

| # | 原则 | 为什么 | 代价 / 边界 |
|---|---|---|---|
| P1 | **热路径不出进程** | 逐 bar、逐笔、风控裁决要求零网络：多一跳网络 = 实盘不可接受，回测慢一个量级 | 内核永远是单体二进制，不能"为了统一"把引擎拆成服务 |
| P2 | **形状只有一处**（`tellurion-contracts`） | 两边各自定义 DTO，第一次改字段就会错位 | 契约仓零实现；不合格的东西进不去（C4：被 ≥2 仓使用且无实现） |
| P3 | **DDL 只有一个 owner** | 两个写者 = 两种真相；拆库时无法"按 schema 搬走" | 跨 schema 只能走只读视图或 API；出现 `join` 别人的表就是边界腐化的第一信号 |
| P4 | **仓 = 模块 / 服务** | 一个 agent 拿到一个仓就能独立开工（R1~R6） | 拆仓有固定成本：契约要版本化、CI 要能单仓跑；**未触发不建仓** |
| P5 | **稳定优先于先进** | 回测可信 > 架构漂亮；结果必须能逐位复现 | 不追新框架；容器/迁移/编排都用最笨但可验证的做法 |

---

## 3. 分层与依赖方向

```
┌──────────────────────────────────────────────────────────────┐
│  接入层     tellurion-ui（浏览器）        tellurion-agent（AI 实验员）│
│             只消费 HTTP                   运行期只走 HTTP 调 core     │
└───────────────┬──────────────────────────────┬───────────────┘
                │ HTTP                          │ HTTP
┌───────────────▼──────────────────────────────▼───────────────┐
│  运行域（core，tellurion）                                      │
│  引擎 · 策略运行时 · 撮合 · 组合结算 · 仪器域存储 · 内核装配      │
│  ★ 逐 bar / 逐笔 / 风控裁决 永驻此进程                          │
└───────┬──────────────────────────────────────────────┬────────┘
        │ 版本化契约（require，非 HTTP）                 │ HTTP（run 前 / 异步）
┌───────▼───────────────┐                    ┌──────────▼──────────────┐
│  契约底座               │                    │  能力服务（触发式，按需拆） │
│  tellurion-contracts   │◄───────────────────┤  data / strategy / risk │
│  tellurion-kit         │   只依赖形状         │  analytics / orchestration│
└───────────────────────┘                    │  / broker               │
                                             └──────────┬──────────────┘
                                                        │ 每服务一个 schema
                                             ┌──────────▼──────────────┐
                                             │  PostgreSQL（同实例多 schema）│
                                             └─────────────────────────┘
```

**依赖边只有这些**（反向依赖一律编译失败）：

| 从 | 到 | 方式 |
|---|---|---|
| `contracts` | `kit` | 编译期（只用 decimal / errors 这类纯工具） |
| `core` / `agent` / 六个服务 | `contracts`（+ `kit`） | `require` **版本号**，禁 `replace`、禁 `go.work` 入库 |
| `agent` / `ui` | `core` | **HTTP**（agent 已于 2026-10-25 S3 删 `replace`、零 import core；ui 无 Go 依赖） |
| 六个服务 | 互相 | **不 import**：要靠 contracts 的形状 + HTTP；服务之间不该有编译期耦合 |

> **core 的 module path 是单段短名 `tellurion`**，Go 会拒绝任何仓 `require` 它 —— 这是"agent 不许编译期依赖 core"的机械保证，不靠纪律（依据：ADR-D30 §0.1 的 Go 1.25 实测）。

---

## 4. 四条主链路（今天在哪跑 / 目标在哪跑）

| 链路 | 今天（2026-10-20） | 目标态 | 关键约束 |
|---|---|---|---|
| **回测** | ui → core `cmd/analysis` 的 HTTP → `pkg/backtest` 引擎（进程内）→ 读行情（同进程直连 PG）→ 结果落库 | 引擎仍在 core；**取数走 `tellurion-data` 的 aggregator（run 前 1 次）** | 同一 `dataset_snapshot_hash` 的两次拉取必须逐位一致；前视由 `visible_at` 拦两道 |
| **AI 实验** | agent（`cmd/ai`）→ 生成策略 → 调 core 回测 → 实验日志落 core 的 `quant` / `research` | agent 自持 `ai.*`；与 core 只走 HTTP 粗粒度 | 实验必须能回答"用哪份策略 / 数据 / 规则"（三 hash） |
| **实盘** | core 进程内 `RiskPolicy.CheckOrder` → `pkg/live` 的 `MockTrader`（仅 paper） | 裁决仍进程内；通道走 `tellurion-broker`（对账 + 幂等 + 熔断之后） | **同步裁决永不出仓**；无对账/幂等/熔断不接真钱 |
| **批量 / 分析** | core 内 `pkg/backtest/batch` + `walkforward` + `cmd/analysis` 的指标/归因 | 排队与 worker 归 `tellurion-orchestration`；指标与归因归 `tellurion-analytics` | 编排**只派活不裁决**；分析**纯函数**（不读时钟、不读随机，蒙特卡洛必须带 `seed`） |

---

## 5. 数据归属矩阵（谁拥有哪个 schema）

| schema | owner | 消费方怎么读 | 今天实际 |
|---|---|---|---|
| `market` / `ingest` | `tellurion-data` | 只读 API（`/datasets/*`） | 表在 core 库；data 仓已有 23 张 `market.*`/`ingest.*` DDL 与 `POST /ingest/points`；**生产写入仍以 core `cmd/data` 为主**（X1 未完） |
| `strategy` | `tellurion-strategy` | 写侧 HTTP / 读侧 resolve | 定义仍住 core 的 `quant.strategies` + 本地注册表；strategy 仓已有 5 张 `strategy.*` 表与 12 端点，**core 侧零调用方**（X2 未切读） |
| `risk` | `tellurion-risk` | run 前拉快照（内容寻址）；事件异步回传 | 规则快照已住 `risk.*`（core 提交时 resolve 取 `risk_rules_hash`）；**`bundle→RiskPolicy` 未接**，进程内限额仍来自 core 配置；事件回传开关默认关（X3 部分） |
| `analysis` | `tellurion-analytics` | 只读上游结果，写自己的报告 | core `cmd/analysis` 仍直接算；analytics 仓已有 8 端点与 `analysis.*` 5 表，**core 侧零调用方**（X4 未切读） |
| `run` | `tellurion-orchestration` | 任务状态 / artifact 指针 / **`strategy_state` 检查点**（**不含**订单、成交、持仓——那是 `quant`） | orchestration 已有 `run.*` 6 表与 worker 面；core 仍以裸表 `backtest_jobs` 为状态/结果权威，**两表并存**（X5 部分） |
| `ai` | `tellurion-agent` | 自持自读 | agent 已自持 `ai.*`（QT-17，`experiments` 已停写）；core 仍留 `experiments` / `factor_hypothesis` 裸表与写方法（后者生产零调用方） |
| `quant` | `tellurion`（core） | 只有 core 写 | 运行态真相：订单/成交/持仓/组合快照/对账/`risk_events`（`strategy_state` 已裁**留 core**，U3 作废） |
| `audit` | `tellurion`（core，`pkg/eventstore` + `pkg/msgbus`） | 只追加；用于消息重放 | 与 `risk.audit_logs`（人操作审计）**不是一回事** |
| 无表 | `contracts` / `kit` / `broker` / `ui` | — | 见各仓 `db-schema.md` 的"为什么没有表" |

> 迁移纪律：**按 schema 搬，不按表搬**；每次搬都是"先建第二写者 → 对拍 → 切读 → 停写"，不允许一步切换（QT-17 的四步样板）。

---

## 6. 边界原则：什么永远不拆

1. **引擎与策略运行时**：回测可信的前提是"回测与实盘跑同一个实现"，拆出去就是第二份实现。
2. **同步裁决**（`RiskPolicy.CheckOrder`）：逐笔零网络；规则**真相源**才出仓。
3. **撮合与结算**：需要 bar 级一致性与事务性。
4. **仪器域存储**（trading calendar / 上市窗口）：被引擎热路径读，且是"偏差维"的口径来源。
5. **契约实现**：`contracts` 里永远只有形状；一旦出现函数体里的业务判断，边界就没了。
6. **事件存储与消息总线**（`pkg/eventstore` / `pkg/msgbus`）：拆出去等于把热路径变成远程调用；`audit.message_log` 会被卷进网络抖动。
7. **订单/成交/持仓的真相**：`quant` 是"钱和仓位发生了什么"，`run` 是"某个任务跑到哪了"。两者事务边界与审计要求不同，**混在一起就再也拆不开**。

**"该不该建一个新仓"的判据**：需要独立伸缩 / 独立部署，**且**只走高频之外路径。逐 bar、逐笔、裁决三条一律不满足 → 不建。

---

## 7. 演进阶梯与当前位置

| 阶段 | 内容 | 状态 |
|---|---|---|
| **S-1** | 12 仓改名 + 建仓 + 推送 | ✅ 完成（QT-60，2026-10-20） |
| **W0** | 契约形状冻结（abi v2 / 四契约 / 错误三分 / 重放） | ✅ 完成（2026-10-25；QT-01~04） |
| **S1** | 契约与工具**直接落两个新仓**，core / agent 用 `require` 伪版本（**无 replace**） | ✅ 完成（ADR-D31 形态；contracts / kit 代码已落） |
| **S2** | 两仓打 `v0.1.0`，下游换 tag；两仓自治补齐 | ✅ 完成（结案时 contracts `v0.6.0` / kit `v0.1.3`；kit 现最新 `v0.1.4`，见 §7 下「服务间凭证」；下游按 tag pin） |
| **S3** | agent 删 `replace ../tellurion`，只依赖 tag + HTTP | ✅ 完成（2026-10-25；agent 零 import core） |
| **X1~X6** | 六个能力服务按 ADR-036 服务化 | 🔶 **G0/G1/G2 并行、G3 切读串行**：ADR-036 已裁「六仓 = 六服务」；G0（Dockerfile + deploy + config + 唯一端口 + 健康检查）已在各仓补齐；data 读链已真接线，risk 有客户端但开关默认关，其余四条待 G3。**不再要求「升格 ADR」——ADR-036 是总纲；单服务切读/停写用本仓任务单记录** |

**已知过渡态（写在这里，避免被当成设计）**：
- ~~`agent` 仍 `replace ../tellurion`~~ → **已于 2026-10-25 S3 消除**；今天 agent 只走 HTTP。
- 六个服务仓**已实装**（各自 `cmd/*service`；broker 按 ADR-036 追加服务入口），`api-schema.md` 描述的是**已实现的契约**，但只有 data 一条读链在生产路径上。
- **ADR-036（2026-10-26）已把六仓定性为服务**：G0/G1/G2 并行补部署、接口与数据；G3 切读/停写按依赖串行；risk 保留「控制面服务 + core 进程内裁决」；broker 先落 Mock 服务，真实 XTP 仍受 X6c 阻塞。
- 行情 / 任务 / 策略定义 / 风控事件仍由 core 主写；服务仓的 `db-schema.md` 是**双写/迁入中**的归属，不是唯一写者。**4 个簇 DDL 双 owner**（market / run / strategy / ai）+ **risk 裁决权双真相**（core `RiskPolicy` vs risk `bundle`），只有 `market.index_daily` 被单独裁决过。
- **部署路径**：core 的 `Dockerfile.service` 已于 2026-10-26 删除 `cmd/strategy` 的 build/COPY 行；六个服务仓按 ADR-036 各自持有 `Dockerfile + deploy/compose.yaml`，本地联调走 `docker-compose.services.yml`。**部署真相 = compose**；K8s 清单若与仓内 Dockerfile/镜像名不一致即视为 experimental。
- **服务间凭证已可用**（2026-10-25/26）：kit `v0.1.4` 已发版；data / risk / analytics 已 pin `v0.1.4`，`service` token 的 401 已关闭。剩余矩阵分叉：core 仍 `v0.1.1`、agent 仍 `v0.1.0`（非阻塞，登记即可）。

> 以上四条与 §5 的「今天实际」由 [核心仓第四轮目的对齐审计](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/purpose-alignment-audit-2026-10-26.md) 取证；本文不复制其正文。

---

## 8. 不变量（机械可查，不是口号）

| # | 不变量 | 判据 |
|---|---|---|
| R1 | 单仓可构建 | 只 checkout 本仓 `go build ./...` 绿；`replace` 指向仓外 = 红 |
| R2 | 单仓可自证 | `go test ./...` 绿 + 本仓有 CI |
| R3 | 有行为入口 | 仓根 `AGENTS.md`（构建/边界/依赖版本/禁止事项/台账指针） |
| R4 | 有任务台账 | 本仓 `docs/TASKS.md` 只放本仓可完成的单 |
| R5 | 契约是版本依赖 | 升级 = 改 `require` + 跑测试，不需读契约仓源码 |
| R6 | 功能边界有契约 | `docs/{db-schema,api-schema,dataflow}.md` 三份存在且非空（**core 与本仓豁免**，2026-10-21 裁决：真相由 `openapi.yaml` / `postgres.go` / `SPEC.md` 直接承载，见 REPO-MAP） |
| C1~C5 | 跨仓规则 | 只认 tag / `go.work` 不入库 / 契约变更由使用方触发 / 准入 ≥2 使用方 / breaking 保留一个版本周期 |

> 权威定义在 [core `repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md) §2 与 §9；本文只做摘要，冲突时以那份为准。

---

## 9. 本文与其它文档的关系

| 想知道 | 去哪 |
|---|---|
| 每个仓拥有什么、依赖谁 | [REPO-MAP.md](REPO-MAP.md) |
| 某功能该放哪个仓 | [SERVICE-INDEX.md](SERVICE-INDEX.md) |
| 决策为什么这么定 | [ADR.md](ADR.md) / `adr/`（跨领域）+ 各仓 `docs/adr/`（单仓） |
| 具体表 / 接口 / 链路 | 各仓 `docs/db-schema.md` · `api-schema.md` · `dataflow.md`（core 与本仓豁免，见 REPO-MAP） |
| 施工顺序 | [core `docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) |
