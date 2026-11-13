---
status: evergreen
last-verified: 2026-11-13
verified-by: DOC-28（2026-11-13）：六处漂移订正——data 对外面删已撤的 `/factors/{name}@{hash}` 并改 28 条路由 / 25 张表（原 23）；strategy 改 13 业务端点（5 公开读 + 8 受保护写，原「写 7 + 读 2」）；orchestration 改 16 条 `/api/*`（任务 7 + 父作业 2 + worker 5 + artifacts 1 + provenance 1，原「任务 4 + 批量 4 + 算力 2」）；risk「零 import contracts」已于 2026-11-11 收口（实测 5 文件 import、go.mod v0.10.0），偏差只剩 analytics；表头加核对日期与口径。DOC-21（2026-11-13）：§版本 pin 改为机器可读表（`<!-- pins:begin -->`），逐行退化为「pin 见 §版本 pin 表」，由 tools/check_doc_counts.py --workspace 比对 12 仓 go.mod（实测 contracts 全 pin v0.10.0、kit 全 pin v0.5.0，analytics 未引入 contracts、broker 未引入 kit）。此前：DOC-P3-MATRIX-TABLE-GRAIN（2026-11-12）：core / orchestration 两行显式标 `run.backtest_results` 表粒度例外（owner=core，证据 core `pkg/storage/backtest_results.go` + core 审计矩阵 `:41`），并注明 core 矩阵 `:43` 因子派生表 owner 待 core 订正（本仓台账 `CORE-MATRIX-FACTOR-OWNER-FIX`）。此前：代码-文档对齐审计（2026-11-11）：按 12 仓 `go.mod` 实测重写版本列，按各仓 `AGENTS.md` / `docs/TASKS.md` 订正状态列与「core 侧零调用方」类断言；删去 `strategy_state` 归属、`backtest_jobs` 双 owner、core `cmd/data` 提供生产 :8081 三处过期陈述。此前：DOC-11 + DOC-12（2026-10-26）按第四轮审计订正状态列与依赖边；按 ADR-036 增加「定位」块。实测依据 = 12 仓 `go.mod` / 各仓 `cmd/*service` / 各仓 `Dockerfile` / `deploy/compose.yaml`。
---

# 仓地图（REPO MAP）

> **一张表回答"这个仓管什么、不管什么、拥有哪块数据"。** 仓名与 module path 的权威定义在 [core `repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md)，本文与它冲突时以那份为准。
>
> **定位（ADR-036，2026-10-26）**：`tellurion` = 仪器单体；`agent` / `ui` = 应用；`contracts` / `kit` = 库（数据/契约 vs 工具）；六个能力仓 = **服务**，按 G0（可部署）→ G1（接口）→ G2（数据）→ G3（消费者）→ G4（可运维）过门。**G0/G1/G2 并行，G3 切读串行，G4 各服务收口**；服务仓必须自有 `Dockerfile + deploy/ + config/`，部署真相 = compose，K8s 非必需。

> **本表以各仓 `go.mod` / `docs/api-schema.md` 为准（最后核对 2026-11-13，DOC-28）。** 端点数只写"面"不复制路由表；数字对不上时先改本表附注的实测口径，再回改该仓契约。

| # | 仓 | 类型 | module path | 管什么 | **明确不管** | 拥有 schema | 对外面 | 状态 |
|---|---|---|---|---|---|---|---|---|
| 1 | `tellurion` | 应用（core） | `tellurion` | 回测引擎 / 策略运行时 / 撮合 / 组合结算 / 仪器域存储 / 内核装配 | 不提供 AI 生成能力；不做前端；**不可被任何仓 import** | `quant` + `audit`（另有未加 schema 前缀的因子/用户/审计表、一条 `market.index_daily`，以及**表粒度例外** `run.backtest_results`——见本节注） | HTTP API（前端在 `tellurion-ui` 仓） | 生产代码 |
| 2 | `tellurion-contracts` | 库 | `github.com/ruoxizhnya/tellurion-contracts` | port / DTO / 值对象 / 契约（`RunSpec`·`SignalSpec`·`ResultSpec`·`EngineRunner`·`dataprotocol`·`run`·`broker`·`risk`）/ 哨兵错误 / abi 常量 | **零实现、零 DB、零配置类型**（`Config`/`Options`/`Impl` 禁入） | 无 | Go package | 已发版；各仓 pin 见 §版本 pin 表，analytics 未引入的「待升」登记在该仓台账 |
| 3 | `tellurion-kit` | 库 | `github.com/ruoxizhnya/tellurion-kit` | logging / errors / id / decimal / statistics / httpclient / httpserver / auth{z} / observability / clock / sandbox / db | **任何业务概念**；**任何表结构**（`db` 只给连接/DSN/迁移执行能力） | 无 | Go package | 已发版；各仓 pin 见 §版本 pin 表，broker 未引入 |
| 4 | `tellurion-agent` | 应用 | `tellurion-agent` | AI 实验员：探索循环 / 代码生成 / pipeline / 工具注册表 / 研究域数据自持 | 不在进程内跑引擎；不直连 core 业务表；不逐 bar 远程 | `ai`（已自持；core 遗留 `experiments`/`factor_hypothesis` 已于 2026-11-10 退役） | HTTP（:8086 缺省） | 生产代码（**S3 已落**：删 `replace`、零 import core）；pin 见 §版本 pin 表 |
| 5 | `tellurion-ui` | 应用 | —（无 `go.mod`） | 前端：回测 / 数据同步 / 研究 / 风控 / 运维页面 | 不直连 DB；不复制 `openapi.yaml`；不在前端做业务裁决 | 无 | 浏览器 | 生产代码 |
| 6 | `tellurion-data` | 服务 | `tellurion-data` | 数据面唯一入口：connector → 归一化 → 存储 → aggregator；PIT / `visible_at` 守卫 | 不提供逐 bar / 逐笔取数；不做因子**计算**；不存回测结果 | `market` / `ingest` | 28 条路由：`/datasets/*`、`/ingest/points`、`/api/ingest/raw`、`/api/evidence*`、`/api/sync/*`、6 条 core 只读兼容面（`/factors/{name}@{hash}` 已于裁-14 撤除，路由不存在） | 已实装：`cmd/dataservice` :8081 + 25 张表（`market` 21 + `ingest` 4）；G0–G4 全绿（`SVC-DATA-G3` ✅ 2026-11-10），**生产 :8081 已由本仓提供**（core `cmd/data` 于 2026-11-08 删除）；pin 见 §版本 pin 表 |
| 7 | `tellurion-strategy` | 服务 | `tellurion-strategy` | 策略**资产**：定义 / 版本（`version_hash`）/ artifact 字节码 / resolve | **不计算信号**；不跑回测；不做参数优化 | `strategy` | 13 条业务端点：5 条公开读 + 8 条受保护写（另 2 条公开探针） | 已实装；G0–G4 全绿（G3 ✅ 2026-11-10、G4 真 PG + 停服演练 2026-11-10，:8090）；core 对非空 `strategy_ref` 走本仓 `resolve`（`strategy_asset.resolve_url`，出厂启用），`/promote` 由 agent/操作者直连本仓；pin 见 §版本 pin 表 |
| 8 | `tellurion-risk` | 服务 | `tellurion-risk` | 规则真相源（定义/版本/审批/审计）+ 聚合监控 + 熔断下发 | **同步裁决**（`CheckOrder` 留 core 进程内）；不下单；不碰资金 | `risk` | 规则 5 + 运行 4 + 监控 3 | 已实装；G0–G4 全绿（G1/G3/G4 ✅ 2026-11-10，:8089）；core 的 `risk_service.resolve_enabled` 出厂 **true**（限额走 `POST /api/risk/resolve` 快照），`events_enabled` 仍出厂 **false**（事件回传覆盖见 `RISK-EVENTS-COVERAGE` ⏸）；依赖见 §版本 pin 表 |
| 9 | `tellurion-analytics` | 服务 | `tellurion-analytics` | 指标 / 基准 / Brinson 与因子归因 / 敏感性 / 蒙特卡洛 / 报告导出 | 不生产数据；不改回测结果；**不读时钟、不读随机**（`seed` 必填） | `analysis` | 8 端点（2 个异步） | 已实装；G0–G2/G4 已跑真库腿（:8087）；ADR-0005（2026-11-10）定位为独立只读分析服务/参考实现，**core 调用方为 0 是有意为之**（`SVC-AN-G3` 关闭、K7 挂起）；pin 见 §版本 pin 表 |
| 10 | `tellurion-orchestration` | 服务 | `tellurion-orchestration` | job 队列 / batch / walkforward / worker 注册 / `run_artifacts` 三 hash 留痕 | **不解释结果**、不重算指标、不做风控裁决；**`run` 是任务域，不含订单/持仓** | `run`（六表；`strategy_state` **不属本仓** —— 2026-10-21 H5 裁决归 core `quant.strategy_state`；**表粒度例外**：`run.backtest_results` 归 core，见本节注） | 16 条 `/api/*`：任务 7 + 父作业 2 + worker 5 + artifacts 1 + provenance 1（另 2 条公开探针） | 已实装；G0–G4 全绿（G1 ✅ 2026-11-09、G3 ✅ 2026-11-09，:8088）；worker 进程在 core（本仓零 import core）；`run.backtest_jobs` 是唯一 owner（core 裸表 `backtest_jobs` 已随 Migration 065 删除）；pin 见 §版本 pin 表 |
| 11 | `tellurion-broker` | 服务 | `tellurion-broker` | 交易通道适配（`MockTrader` → `XTPTrader`）：下单/撤单/查单/持仓/成交 | 不做风控判断；不改订单内容（除柜台最小单位换算）；**无对账+幂等+熔断不接真钱**；不做本地交易真相 | 无（订单/成交/持仓在 **core `quant`**；将来建 `exec` 镜像须先立 ADR） | `BrokerGateway` port + HTTP 面（G1） | 服务（ADR-036）：Mock 网关 :8091 + `Dockerfile` / `deploy/compose.yaml`；G0–G2/G4 已收口，G1 HTTP 面已落且 **core 唯一真实通道已切到本仓 HTTP**（`SVC-CORE-BROKER-RETIRE` 2026-11-10：`pkg/bootstrap.BuildExecutionTrader` → `pkg/brokerhttp`，缺 `BROKER_URL` 即 fail-loud；`pkg/trading` 的 `MockTrader` 类型仍在但已无装配入口）；真实 XTP 挂起（X6c ⏸，重开条件 P1~P5）；pin 见 §版本 pin 表 |
| 12 | `tellurion-docs` | 文档 | — | 总体设计 / 跨领域 ADR / 运维指南 / 历史档案 | 不复制服务仓的 db/api/dataflow；不放过期现状数字 | 无 | 本仓 | 现行 |

> **`run.backtest_results` 表粒度例外（2026-11-12 补注，DOC-P3-MATRIX-TABLE-GRAIN）**：该表归 **core**（结果面单一写者），orchestration 只经 API 读结果；证据 = core `pkg/storage/backtest_results.go` 的 `CREATE TABLE run.backtest_results` + core 审计矩阵 `:41`（2026-10-21 裁决）。本仓 `SYSTEM-DESIGN.md` §5 `run` 行已同步标注同一例外。另：core 审计矩阵 `:43` 的因子派生表 owner 仍写 `tellurion-data`（与 ADR-038 矛盾），属 core 仓文件，本仓已立待派指针 `CORE-MATRIX-FACTOR-OWNER-FIX`（见 [TASKS.md](TASKS.md)），不代改。

---

## 依赖方向（只有这些边）

```
ui ──(HTTP)──► core ◄──(HTTP)── agent
                │
                ├──(HTTP，run 前 / 异步)──► data / strategy / risk / analytics / orchestration / broker
                ├──(require)──► contracts
                └──(require)──► kit
```

> **`contracts` 与 `kit` 互不依赖**（2026-11-11 实测：两者 `go.mod` 都没有对方）。库是两个正交的：契约放业务形状，kit 放工具。

### 版本 pin 的推进顺序与前置（2026-11-11）

> 本节是这条规则的**唯一处**；`SYSTEM-DESIGN.md` §2 只放指针，避免两处漂移。

**现状（机器可读，2026-11-13 实测 `go.mod`）**：下表是 pin 的**唯一真相源**，由
`python tools/check_doc_counts.py --workspace <12 仓父目录>` 逐仓比对 `go.mod`；
改 pin 先改表再改代码，或改完代码回改表 —— 表与 `go.mod` 不一致即红。`—` = 无 Go 模块。

<!-- pins:begin -->
| 仓 | contracts | kit |
|---|---|---|
| `tellurion`（core） | v0.10.0 | v0.5.0 |
| `tellurion-agent` | v0.10.0 | v0.5.0 |
| `tellurion-data` | v0.10.0 | v0.5.0 |
| `tellurion-strategy` | v0.10.0 | v0.5.0 |
| `tellurion-risk` | v0.10.0 | v0.5.0 |
| `tellurion-analytics` | 未引入 | v0.5.0 |
| `tellurion-orchestration` | v0.10.0 | v0.5.0 |
| `tellurion-broker` | v0.10.0 | 未引入 |
| `tellurion-ui` | — | — |
| `tellurion-contracts` | — | — |
| `tellurion-kit` | — | — |
| `tellurion-docs` | — | — |
<!-- pins:end -->

**库最新发版 tag**：contracts `v0.10.0`、kit `v0.5.0`（2026-11-13 实测本地 tag；发版后本行与上表同步改）。

**推进顺序（谁先升、为什么）**

1. **库先发版，消费仓后升**。contracts / kit 是叶子库且互不依赖，可并行发版；消费仓不得先把 pin 指向未 push 的 tag（无法 `go get`，等于没发版）。
2. **contracts 先于 kit**。contracts 的破坏面是跨仓形状（改签名 / 删符号会同时弄红多个仓），kit 的破坏面通常只在编译期工具 API。同一批升级先收缩契约形状、再升工具库，才能把「形状不兼容」与「工具 API 不兼容」两类红分开定位。
3. **消费仓按「消费面从窄到宽」升**：data / strategy（单点消费）→ 六个能力服务各自的窄面 → agent（AI 侧多处）→ **core 最后**（AST 复核量最大：contracts 别名类 nontest 262 / test 533）。core 最后还有一个结构性原因：它是六服务的 HTTP 上游，先升会把所有服务的联调窗口压在同一时刻。
4. **同一 PR 内做完三件事**：改 `go.mod` pin → `go build ./...` + `go vet ./...` → 更新本仓 `AGENTS.md` / `README.md` 里「已切 vX.Y.Z」的标注。只做前两件 = 下轮审计必红。
5. **不跨仓强推**（2026-11-11 裁决）：本仓只记录现状与顺序，不代其他仓改 `go.mod`、不批量提 PR。某仓长期停在旧 pin 时，登记在该仓台账的「待升」项，不在此处标成「已切」。
6. **回滚**：消费仓升级后构建红 ⇒ 该仓把自己的 `go.mod` 回退到上一个已发版本；库**不回退已发布 tag**（只前进发新版本，0.x 阶段也只加不减）。

**前置（升之前必须满足）**：① 目标版本已 push annotated tag；② 该版本的 `CHANGELOG.md` 节与兼容矩阵行已更新（库仓 `check_release_matrix` 绿）；③ 若涉及删符号，先满足对应下游迁移单（如 contracts 的 `CT-06-ALIAS-EXIT` 要求三仓迁移完成）。

> **箭头图例**：`A ──► B` = A 调用 / 依赖 B，箭头指向**被调方**（与下表「从 → 到」同向）。
> 六服务的 HTTP 边一律是 **core → 各服务的「对外面」**（run 前取数 / 异步派活），
> 六服务在此是**被调方** —— 与上表「对外面」列、各仓 `docs/ARCHITECTURE.md` §5
> 的读侧（引擎读服务端点）同向。

| 边 | 机制 | 违反的后果 |
|---|---|---|
| `contracts` ↔ `kit` | **无依赖边** | 实测两者 `go.mod` 互不 require；kit 只放工具、contracts 只放业务形状，不要互引 |
| `core` / `agent` / 服务 → `contracts`(+`kit`) | `require` 版本号 | 出现 `replace` / `go.work` 入库 = CI 红（C1/C2） |
| `agent` / `ui` → `core` | HTTP | **agent 已于 2026-10-25 S3 删 `replace`、零 import core**；ui 无 Go 依赖 |
| 服务 ↔ 服务 | **无直接边** | 要共用形状 → 进 contracts；要调用 → HTTP |

> **规则与现状的偏差（2026-11-13 实测）**：pin 现状以上表为准。仍缺的一处是 **`tellurion-analytics` 不引 contracts**（DTO owner 已裁为本仓，见其 `AGENTS.md` §4；`go.mod` 确有该 pin 缺失，不是文档滞后）。`tellurion-risk` 的「零 import contracts」已于 2026-11-11 收口——`go.mod` pin `v0.10.0`，`internal/rule/{errors,hash,model,snapshot}.go` 等 5 个文件 import `contracts/risk`（`RISK-CONTRACTS-SNAPSHOT-MIGRATION` ✅、ADR-040）。规则仍是上面那条，偏差逐仓登记在各仓台账。

> **`core ↔ agent` 那条线不是领域依赖（2026-11-11 DDD 审查 C7）**：`agent → core` 是业务调用（提交回测 / 读结果 / 表达式校验）；`core → agent` 只是**前端请求的 HTTP 反代**（`cmd/analysis` 的 proxy 处理器，无领域语义、无落库、无回调）。图上只画 `agent ──► core`，反代不构成上下游客商边；如果将来出现「core 主动调 agent 做业务决策」，必须先立 ADR。

---

## 状态图例

| 状态 | 含义 |
|---|---|
| **生产代码** | 有真实实现、跑在今天的系统里 |
| **占位** | 有仓、有边界、有 `go.mod` + `doc.go` + 文档，**无实现**；台账出现本仓单号前不写代码。**2026-10-26 起无仓处于此态**（保留该语义供将来新建仓使用） |
| **过渡态** | 已生产，但存在已知违反不变量的地方（必须写清是哪一条） |

---

## 归属待裁的事项

有 3 条归属**没定**（订单是否建 `exec`、`eventstore`/`msgbus`、`testenv`/`testutil`）。`strategy_state` 的迁移义务已于 U3 裁决作废（留 core）。

> `cmd/dualrun` 已于 2026-10-20 裁决 **留 core**（同进程链接两个内核 + 引擎验收门），不再是待裁项。
它们集中登记在 [core `repo-inventory.md` §3.1](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md)，
**单仓文档里只留指针** —— 否则读者不知道该找谁拍。

---

## 每仓文档入口

每仓都有同一套结构：`AGENTS.md`（行为入口）+ `docs/README.md`（导航）+ `docs/TASKS.md`（本仓台账）+ `docs/ARCHITECTURE.md` + `docs/adr/` + `docs/odr/`。其中 10 仓另有 `docs/{db-schema,api-schema,dataflow}.md`（四件套齐全）；**core 与本仓豁免三件薄规格（2026-10-21 裁决：豁免+声明，不补件）**——API / DB / 流程真相直接由 `tellurion:docs/openapi.yaml` / `tellurion:pkg/storage/postgres.go`（内联 DDL）/ `tellurion:docs/SPEC.md` 承载。同裁决**一并豁免 `docs/adr/0001-*` 边界裁决单**（其余 10 仓有）：core 的边界裁决在 `tellurion:docs/design/qt-decoupling/`（ADR-D 系），本仓边界即本文件与跨领域 `docs/adr/`。

**逐仓直达链接见 [SERVICE-INDEX.md](SERVICE-INDEX.md)。**
