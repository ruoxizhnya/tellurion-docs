---
status: active
last-verified: 2026-11-11
verified-by: 12 仓领域驱动设计（DDD）限界上下文审查；证据以当日代码/文档实测为准，`[代码]` 与 `[文档]` 分开标注；"我查到"与"我判断"分开写
---

# 12 仓限界上下文与职责边界审查（2026-11-11）

> 这是**设计审查**，不是代码审查。问题只有一个：**这个仓该负责什么、不该负责什么**。
> 本轮不动任何代码；只出结论、处置建议，以及已确认的口径类文档订正（见 §8）。

## §0 方法与证据口径

- 证据标签：`[代码]` = 直接读源码/DDL/配置；`[文档]` = 只在 markdown/yaml 注释中声称，未必与代码对拍；`[冲突]` = 两处证据互相矛盾。
- 每个结论先写「查到」，再写「判断」。判断可以被推翻，查到的行号不能。
- 已有裁决直接引用，不重新讨论：**ADR-036**（服务拓扑）、**ADR-037**（因子值归属：`factor_cache` owner=core、消费点按需求值、不新增 DB 写者）、**ADR-028 §6/§11**（因子求值在消费点 in-process）、**裁-14 + dataflow 不变量 7**（data 不提供因子读面）、**ADR-0005（analytics）**（独立只读参考实现，core 指标不迁移）。
- 12 仓：`tellurion`(core)、`-agent`、`-analytics`、`-broker`、`-contracts`、`-data`、`-docs`、`-kit`、`-orchestration`、`-risk`、`-strategy`、`-ui`。

---

## §1 逐仓结论（七问）

### 1.1 `tellurion`（core）——核心域，但有三处分析/派生渗出

**一句话**：运行时真相的唯一承载者（核心域）；边界问题不在"少了什么"，而在"多了两三个属于分析/派生上下文的东西"。

1. **核心/支撑/通用域**：核心域。`cmd/` 实际只有 `analysis`、`worker`、`dualrun`、`recon`（`[代码]` `cmd/*/main.go` 实测四个入口）；热路径包 `pkg/backtest`、`pkg/strategy`、`pkg/execution`、`pkg/portfolio`、`pkg/settlement`、`pkg/risk` 全在进程内（`[代码]` `AGENTS.md:226-237`）。
2. **限界上下文边界**：至少三块概念共存——① 交易/回测运行时；② 因子研究（`pkg/mining` + `factor_*` 表）；③ 分析产物生产（`internal/analysisartifact`）。`[代码]` `internal/analysisartifact/builder.go:75,205` 从 `factor_returns` 读数据并组装分析产物；`[代码]` `internal/repoguard/analytics_impl_freeze_test.go:33-37` 承认 metrics/reporting 是运行时承重实现。**判断**：① 是核心域，②③ 是分析/派生上下文的渗出，不是"两个仓塞一起"，而是"一个仓里住了三个上下文"。
3. **聚合与强不变量**：订单/成交/持仓/组合快照的真相在 `quant`（`[代码]` `AGENTS.md:230`、`docs/SPEC.md` 数据归属）；DDL 唯一真相是 `pkg/storage/postgres.go` 的 `migrationStatements()`（`[代码]` `AGENTS.md:237`）；同步风控裁决 `RiskPolicy.CheckOrder` 永驻进程内（`[代码]` `AGENTS.md:230`）。
4. **上下游**：core 是六个服务的**上游调用方**（`[代码]` `docker-compose.yml:225,235,240,264,276,371`）；同时对 agent 有纯反代（`:235`）。**依赖方向**：编译期 core→contracts/kit；运行期 core→data/strategy/risk/agent/broker/orchestration。
5. **共享内核与重复**：`pkg/backtest/metrics` 与 `pkg/backtest/reporting` 和 analytics 的指标实现是同一概念的两份实现；core 侧被冻结为 3 个生产 import（`[代码]` `analytics_impl_freeze_test.go:33-37`）。**判断**：core 是运行时真相，analytics 是参考实现——两份公式必然漂移，需要明确"谁是权威"（§5 C4）。
6. **数据所有权**：仍拥有 `public` 下的因子治理与派生表：`factor_definitions`、`factor_registrations`、`factor_registration_audit`、`factor_mining_records`（`[代码]` `pkg/storage/postgres.go:431-518`、`pkg/storage/factor_definition.go:29`、`factor_registration.go:45,105`、`mining.go:33`）；`factor_cache` / `factor_returns` / `ic_analysis`（`[代码]` `pkg/storage/postgres.go:207-227`、`pkg/storage/cache.go:17-70,121-236`）。**异常**：`factor_cache` 零写者（ADR-037 已裁）；`factor_returns` 有写方法零调用、有一处读者；`ic_analysis` 写方法与读方法都零调用（§5 C3）。
7. **边界泄漏**：`internal/analysisartifact` 在生产分析产物（本应属 analytics 的读模型/产物）；`pkg/mining` 在做因子研究；`market.index_daily` 一条 DDL 在 core（跨 schema 的所有权例外，`[代码]` `REPO-MAP.md` 已登记）。**判断**：前两处是设计上的上下文渗出，是否迁移需裁决（§6 D3/D4）。

### 1.2 `tellurion-data`——支撑域，包级上下文清楚，文档对因子域的主张与代码相反

**一句话**：供给上下文做得干净（`ingest → normalize → serving` 单向、唯一写 `market`/`ingest`）；问题全在文档——它把不属于自己的因子域写成了自己的。

1. **核心/支撑/通用域**：支撑域（数据供给）。`[文档]` `AGENTS.md:5-9`、`ARCHITECTURE.md:104-109` 明确"不做策略或因子计算"。
2. **限界上下文边界**：`ARCHITECTURE.md:27-45` 自己列了 6 个上下文包，并明确 `internal/store`/`internal/schema` **不是**上下文、`internal/assembly` 是采集与存储之间的接缝。`[代码]` 目录实际存在 `internal/ingest`、`internal/normalize`、`internal/serving`、`internal/sync`。**判断**：这是 12 仓里边界写得最清楚的一个；`internal/sync`（作业/调度）与 `serving`（读面）确实是两个概念，但通过显式 port 相接，不算"塞两个上下文"。
3. **聚合与强不变量**：`market`/`ingest` 唯一写者（`[文档]` `ADR-0006`）；`visible_at` 必填的第二道防线；同内容幂等、异内容 409（`[文档]` `db-schema.md`、`dataflow.md`）。执法点在 `internal/ingest` 的 `GatePoints`/`ValidatePoints`/`Writer`（`[代码]` 包内符号）。
4. **上下游**：core/analytics/strategy/agent → data（`[文档]` `ARCHITECTURE.md:76-84`）；data 只供数、不反向调用。**判断**：单向，健康。
5. **共享内核与重复**：协议形状用 `tellurion-contracts`（`[代码]` `go.mod` require）；未发现第二套 DTO。鉴权用 kit 的 `auth/httpadapter`（`[文档]` `ARCHITECTURE.md:86-91`）。
6. **数据所有权**：`[代码]` `internal/schema/schema.go:32-60` `TableNames()` 实测 **22 张表**，全部是 `ingest.*` / `market.*`；**不含任何 `factor_*`**。但 `[文档]` `docs/db-schema.md:41-57` 仍把 `factor_definitions`/`factor_cache`/`factor_returns`/`ic_analysis`/`factor_registrations` 列为"真实表"，并写 SPEC-R-02 "唯一 owner = data" —— **与同一份仓的代码、ADR-037、裁-14 三处相反**（§5 C2）。
7. **边界泄漏**：未发现业务计算。`internal/aggregator`/`serving` 只做 PIT、聚合、票池、hash、缓存（`[文档]` `ARCHITECTURE.md:66`）。**判断**：代码边界合格；唯一"越界"是文档主张。

### 1.3 `tellurion-analytics`——支撑域，只读参考实现，与 core 指标双实现

**一句话**：唯一写 `analysis`、只读上游，边界纪律有机器判据；与 core 的指标公式是"两份实现"，且它自己的 db-schema 把因子值 owner 写错。

1. **核心/支撑/通用域**：支撑域（分析能力）。
2. **限界上下文边界**：仓内是"纯函数计算"与"报告持久化/导出"两段；`[文档]` `ARCHITECTURE.md:17-27` 把它们画成 输入→计算→`analysis.*`；`[代码]` `internal/analysis/pgstore.go:14-18` 只写 `analysis.*`。**判断**：是同一个上下文内的"计算 + 结果记录"，不是两个上下文；边界成立。
3. **聚合与强不变量**：只写 `analysis.*`；`completed` 不可变双层（应用层 + PG 触发器）；seed 必填（`[文档]` `db-schema.md:28,65`）。机器判据：`[代码]` `internal/analysis/g2_schema_write_guard_test.go:18-28` 静态扫 SQL，写别的 schema 即红。
4. **上下游**：analytics → core（报告/artifact）、data（基准行情）、orchestration（父作业）（`[代码]` `docker-compose.yml:485-490`）；**core → analytics 零调用**（ADR-0005 有意为之，`SVC-AN-G3` 关闭）。**判断**：运行期单向（analytics 是下游），但"服务定位"上它是 core 的平行实现，不是 core 的调用方。
5. **共享内核与重复**：指标/归因与 core `pkg/backtest/metrics` 双实现；`[文档]` `docs/db-schema.md:66` 声称"不重算上游已算的指标"，`ADR-0005:3-11` 声称"core 指标保留冻结、不迁移"。**判断**：两份实现会漂移；当前口径是"core 是运行时权威，analytics 是参考实现"，但这句话没有写进任何 ADR 的正式条款（§5 C4）。
6. **数据所有权**：5 张 `analysis.*` 表，唯一写者 `internal/analysis.PG`（`[代码]` `internal/analysis/ddl.go`；`[文档]` `db-schema.md:18-24,34`）。**异常**：`analysis.benchmarks` 生产写者为零（K7 挂起，`db-schema.md:21,39,46`）。
7. **边界泄漏**：未发现写上游。**但** `[文档]` `db-schema.md:57` 把"因子值"的 owner 写成 `tellurion-data` —— 与 ADR-037（owner=core、按需求值）相反（§5 C2 同族）。

### 1.4 `tellurion-agent`——支撑域（AI 实验员），因子工具面是坏的

**一句话**：`ai` schema 自持、`factor_hypothesis` 已归位；但 `factor.compute`/`factor.evaluate` 两个工具打向 core **不存在的端点**。

1. **核心/支撑/通用域**：支撑域（AI 实验能力），不是核心域。
2. **限界上下文边界**：实验循环（`pkg/ai/loop`）、能力层（validation/tools/causal）、Copilot/pipeline 工具宿主；`[文档]` `AGENTS.md:5-11` 明确"不在进程内跑引擎、不直连 core 业务表"。
3. **聚合与强不变量**：`ai` schema 唯一写者；`[代码]` `pkg/aistore/schema.go:46,171` 建 `ai.factor_hypothesis`；`[代码]` `pkg/aistore/schema_core_drift_test.go:33` 把 `factor_hypothesis → ai.factor_hypothesis` 钉成漂移基线。
4. **上下游**：agent → core（回测/walk-forward/表达式/因子）、agent → data（`[代码]` `docker-compose.yml:323,326`）；core → agent 纯反代（`:235`）。**判断**：运行期存在 **core ↔ agent 双向 HTTP**（§5 C7）。
5. **共享内核与重复**：用 contracts 的 `domain.FactorHypothesis`/`domain.FactorType`（`[代码]` `pkg/aistore/factor_hypothesis.go:13`），没有另造 DTO。
6. **数据所有权**：`ai.*`（`schema.go:46,171`）；core 的 `public.factor_hypothesis` 已退役。**判断**：原先的"归属未裁"在代码层已经闭合为 agent；只剩 data 文档的过期陈述。
7. **边界泄漏**：`[代码]` `pkg/ai/client/factor_client.go:51,93` 调 `POST /api/factor/compute` 与 `/api/factor/evaluate`；`[代码]` `pkg/ai/client/endpoint_contract_test.go:17-18,96` **自己承认 core 没有这两个端点**（core 只有 `/api/factor/compute-returns`），并标注等 QT-50 ③-② 补。**判断**：这是本轮最硬的边界冲突——不是"归属模糊"，是"跨仓契约指向不存在的实现"（§5 C1）。

### 1.5 `tellurion-strategy`——支撑域（策略资产），边界清晰

**一句话**：只存定义/版本/artifact/resolve，不执行、不回测；没有发现越界。

1. **核心/支撑/通用域**：支撑域（资产）。
2. **限界上下文边界**：定义、版本、编译/构建、promotion、resolve 同属"策略资产"一个上下文；没有第二套模型迹象。
3. **聚合与强不变量**：`version_hash` 内容寻址；artifact 字节码与定义绑定；promotion 是状态迁移。
4. **上下游**：core → strategy `resolve`（`[代码]` `docker-compose.yml:240`）；agent/操作者 → strategy `/promote`（`[文档]` `REPO-MAP.md`）。**判断**：单向。
5. **共享内核与重复**：用 contracts；未发现第二套 DTO。
6. **数据所有权**：`strategy` schema，本仓唯一写者（`[文档]` `docs/db-schema.md`）。
7. **边界泄漏**：无。内置策略仍在 core 本地 registry，这是已文档化的现状，不是泄漏。

### 1.6 `tellurion-risk`——支撑域（规则真相），与 contracts/risk 存在形状双实现

**一句话**：规则真相源 + 聚合监控；同步裁决仍在 core 进程内（有意为之）。唯一问题是 `Snapshot` 形状自持一份。

1. **核心/支撑/通用域**：支撑域（风控规则）。
2. **限界上下文边界**：规则定义/版本/审批/审计 与 监控/熔断 是两块，但都以 `risk` schema 与同一 `Snapshot` 语言连接；**判断**：一个上下文的两条能力，不是两个上下文。
3. **聚合与强不变量**：`SnapshotHash` 内容寻址 + 读时校验（`[代码]` `internal/rule/snapshot.go:57,108`）；`ParseBundle` fail-closed（`internal/rule/snapshot.go:139-144`）；进程内规则包无网络边界（`snapshot.go:120`）。
4. **上下游**：core → risk `resolve`（`[代码]` `docker-compose.yml:264`）；risk 不反向调用 core。**判断**：单向。
5. **共享内核与重复**：`[代码]` `contracts/risk/snapshot.go` 已存在，但 risk 仓 `go.mod` 零 import contracts，自己在 `internal/rule/snapshot.go:24,37,144` 定义 `SnapshotRule`/`Snapshot`/`ParseBundle`。**判断**：同一形状两份定义，属于共享内核重复（§5 C5）。
6. **数据所有权**：`risk` schema，本仓唯一写者；`risk.audit_logs` 与 core `audit` 不是一回事（`[文档]` `SYSTEM-DESIGN.md` §5）。
7. **边界泄漏**：未发现下单/持仓/资金；同步裁决留 core 是裁决结果，不是泄漏。

### 1.7 `tellurion-orchestration`——支撑域（任务域），零 import core

**一句话**：只派活不裁决，`run` 六表唯一 owner，形状用 contracts/run；边界干净。

1. **核心/支撑/通用域**：支撑域（编排）。
2. **限界上下文边界**：job 队列、batch、walkforward、worker 注册、artifact 指针同属任务域；`[代码]` `internal/queue/artifacts.go:11` 明确 `run.run_artifacts` 无 status，结论只从 `run.backtest_jobs` 取（单一同源）。
3. **聚合与强不变量**：`run.backtest_jobs.status` 是唯一状态词表（`[代码]` `internal/plan/plan.go:140-141`）；`run.*` 六表（`internal/testdb/testdb.go:75-76`）。
4. **上下游**：core `cmd/worker` → orchestration（`[代码]` `docker-compose.yml:371`）；analytics → orchestration（`:490`）。**判断**：单向；编排不反向调用。
5. **共享内核与重复**：`[代码]` `internal/httpapi/workers.go:106` 明确 `ClaimView` 形状归 contracts/run，本仓不复刻。
6. **数据所有权**：`run` 六表，本仓唯一写者；`strategy_state` 不属本仓（2026-10-21 裁决留 core）。
7. **边界泄漏**：无；不解释结果、不重算指标。

### 1.8 `tellurion-broker`——支撑域（通道适配），不持有订单真相

**一句话**：`BrokerGateway` 的两种实现，只做通道；唯一自持表是幂等映射 `broker.order_acks`。

1. **核心/支撑/通用域**：支撑域（交易通道适配），接近通用域。
2. **限界上下文边界**：通道适配 + 幂等映射；`[代码]` `internal/reconcile/reconcile.go:8` 明确对账报告不落表，消费方是 risk 的留痕。
3. **聚合与强不变量**：请求幂等（`broker.order_acks`）；写端点无 token 时 503（`[文档]` `docker-compose.yml:110-112`）；订单真相不在这里。
4. **上下游**：core → broker（`[代码]` `docker-compose.yml:276`）；broker 不调用其他仓。**判断**：单向。
5. **共享内核与重复**：`[代码]` `internal/gateway/model.go:26-34` 用 contracts 的 `Side`/`OrderType` 别名，没有另造。
6. **数据所有权**：`broker.order_acks`（`[代码]` `internal/ackstore/ddl.go:9,24`）；`quant` 的订单/成交/持仓仍归 core。**判断**：没有"两个仓写同一张表"。
7. **边界泄漏**：`[代码]` `internal/ackstore/ddl_test.go:13` 只用 `broker.` 前缀；未发现风控判断。

### 1.9 `tellurion-contracts`——通用域（共享内核），零实现

**一句话**：跨仓形状的唯一真相；本轮发现 `contracts/risk` 已存在但 risk 未采用。

1. **核心/支撑/通用域**：通用域（共享内核）。
2. **限界上下文边界**：`domain`、`broker`、`run`、`risk`、`engine`、`fees` 多组形状共处一仓，是"共享内核"而不是多个上下文；契约仓的本质就是跨上下文的最小共识。
3. **聚合与强不变量**：只增不破；零实现、零 DB、零配置类型。
4. **上下游**：core/agent/data/strategy/orchestration/broker require；risk 与 analytics 未引入（`[代码]` 各仓 `go.mod`）。
5. **共享内核与重复**：它**就是**共享内核；重复发生在消费方（risk 自持 Snapshot）。
6. **数据所有权**：无。
7. **边界泄漏**：无；`contracts/risk/snapshot.go` 的存在证明形状已收编，等待消费方迁移。

### 1.10 `tellurion-kit`——通用域（技术基础），零业务

**一句话**：鉴权、HTTP、DB、日志、观测、沙箱；没有业务概念与表结构。

1. **核心/支撑/通用域**：通用域。
2. **限界上下文边界**：单一技术库，多包并列；不是多个业务上下文。
3. **聚合与强不变量**：无业务不变量；只有工具 API 的兼容性。
4. **上下游**：所有仓（除 broker 未引入）require kit；kit 不依赖任何仓。
5. **共享内核与重复**：是技术共享内核；与 contracts 互不依赖（`[代码]` 两者 `go.mod` 实测）。
6. **数据所有权**：无。
7. **边界泄漏**：无。

### 1.11 `tellurion-ui`——接入层，无领域

**一句话**：SPA，只消费 HTTP，不直连 DB、不复制 openapi、不做业务裁决。

1-7 问：无核心域/支撑域之分（表现层）；无上下文聚合；不守护业务不变量；ui → core（HTTP）；DTO 来自 `openapi.yaml`；无数据所有权；无边界泄漏。**判断**：边界合格。

### 1.12 `tellurion-docs`——文档仓，无领域

**一句话**：跨仓架构、ADR、运维指南；不实现服务、不写库。

1-7 问：无领域实现；本仓是"跨仓结论的归档处"；不拥有数据；唯一风险是"复制现状数字导致过期"（本轮已见版本列漂移，§5 C11）。**判断**：边界合格。

---

## §2 跨仓依赖图（文字）

### 2.1 编译期（require，单向）

```
core ──► contracts, kit
agent ──► contracts, kit
data ──► contracts, kit
strategy ──► contracts, kit
orchestration ──► contracts, kit
broker ──► contracts   （未引入 kit）
analytics ──► kit       （未引入 contracts）
risk ──►（零 import contracts / kit）
contracts ◄──► kit      无依赖边
ui / docs               无 Go 依赖
```

**判断**：编译期没有任何环；`risk` 与 `analytics` 的 contracts 缺口是已登记偏差，不是新问题。

### 2.2 运行期（HTTP）

```
ui ──► core
core ──► data, strategy, risk(resolve), broker, orchestration(worker)
core ──► agent（copilot/pipeline/explore/tools 纯反代）
agent ──► core（回测 / walk-forward / 表达式 / 因子端点）
agent ──► data
analytics ──► core（结果 / artifact）, data（基准行情）, orchestration（父作业）
worker(core) ──► orchestration
```

**实际存在的环**：

- `core ↔ agent`：core 反代 agent 四族路由（`docker-compose.yml:235`），agent 又调 core 回测/因子面（`AI_SERVICE_FACTOR_API_URL` → `:8085`，`:326`）。compose 的启动依赖是"ai 等 analysis"单向（`:344-347`），但**请求级调用图是双向的**。
- 其余边均单向；`data`、`strategy`、`risk`、`broker`、`orchestration` 都不反向调用 core。

**判断**：`core ↔ agent` 这个环不是编译依赖，短期可接受；但必须在文档里写明"这是两条不同语义的边（反代入口 vs 因子/回测 API）"，否则下一次审查会把它当成架构回退。

---

## §3 数据所有权与异常

| 类别 | 对象 | 证据 | 处置 |
|---|---|---|---|
| 双写 | 未发现两仓写同一张表 | 各仓 DDL 前缀 + broker/analytics 的写护栏 | — |
| 有表无写者 | `public.factor_cache` | ADR-037；`SaveFactorCacheBatch` 零调用 | 已裁：消费点按需求值；表待退出 |
| 有表无写者 | `public.factor_returns` | `pkg/storage/cache.go:121` 有写方法；非测试零调用 | §6 D1 |
| 有表无写者/无读者 | `public.ic_analysis` | `cache.go:194` 写、`cache.go:239` 读，均零调用 | §6 D1 |
| 有表无写者 | `analysis.benchmarks` | `db-schema.md:21,39,46`；K7 挂起 | 已声明"表已建、暂不启用" |
| 有表无写者（条件） | `broker.order_acks` | 仅配 DSN 时写（`internal/ackstore/ddl.go`） | 已文档化 |
| 跨 schema 例外 | `market.index_daily` 由 core 建/写 | `REPO-MAP.md` 已登记；`AGENTS.md:230` | 保留例外，需在矩阵中标注 |
| 派生表归属未定 | `factor_returns` / `ic_analysis` | 物理在 core `public`；data 文档主张相反 | §5 C2 + §6 D1 |

**判断**：`factor_cache` 的"有表无写者"不是孤例；`factor_returns` 与 `ic_analysis` 是同一模式，且 `factor_returns` 还有一个**静默读空**的读者（`internal/analysisartifact/builder.go:205`），风险等级高于 `factor_cache`（后者至少已在 ADR-037 里有明确处置）。

---

## §4 边界冲突清单（按严重度）

> 严重度定义：**P0** = 跨仓契约指向不存在的实现或会产出静默错误结果；**P1** = 同一概念两份真相/归属文档相反；**P2** = 文档过期或边界表述不清；**P3** = 已登记、有退出条件的已知偏差。

### P0

**C1. agent 的 `factor.compute` / `factor.evaluate` 工具调用 core 不存在的端点**
- 查到：`[代码]` `tellurion-agent/pkg/ai/client/factor_client.go:51,93` 调 `POST /api/factor/compute`、`POST /api/factor/evaluate`；`[代码]` `tellurion-agent/pkg/ai/client/endpoint_contract_test.go:17-18,96` 明写"core 无对应端点，core 只有 `/api/factor/compute-returns`"，并标注 QT-50 ③-② 待补；`[代码]` core 只注册 `/api/factor/registrations`（`cmd/analysis/handlers_factor_registration.go:65`）与 `/api/factors/:factor_name`（`handlers_proxy.go:167`）。
- 判断：这是"契约指向空气"，不是归属争议。AI 的因子研究工具链在该路径上必然失败（或在别处被静默吞掉）。
- 处置类别：**待主任裁决**（§6 D2）；文档口径（compose/agent 注释）需同批订正。

### P1

**C2. 因子域归属：data 文档 vs 代码/ADR-037/裁-14 三处相反**
- 查到：`[文档]` `tellurion-data/docs/db-schema.md:41-57` 把 `factor_definitions`/`factor_cache`/`factor_returns`/`ic_analysis`/`factor_registrations` 列为"真实表"，SPEC-R-02 写"唯一 owner = data"；`[代码]` `tellurion-data/internal/schema/schema.go:32-60` `TableNames()` 只有 22 张 `ingest.*`/`market.*`，**零 `factor_*`**；`[文档]` `tellurion-data/docs/ARCHITECTURE.md:40` 又写"派生 Derived 今天在 core，因子读面不在本仓"；ADR-037 与裁-14 判 owner=core/不提供因子读面。
- 判断：data 仓自己的三份文档互相矛盾，且两份与最新裁决相反。**这是文档口径问题，不是代码问题**。
- 处置类别：**改文档**（本轮已改，§8）；另建议在 ADR-037 追加一条"ADR-027 §2.6.2 的 Derived 上下文不再迁入 data"的口径（§6 D5）。

**C3. `factor_returns` / `ic_analysis` 是"有写方法、无写者"的孤儿表，且 `factor_returns` 有一个静默读空的分析产物读者**
- 查到：`[代码]` `pkg/storage/cache.go:121-163` `SaveFactorReturnBatch`、`cache.go:194-236` `SaveICEntryBatch`；全仓非测试零调用（grep `SaveFactorReturn|SaveICEntry`）；`[代码]` `internal/analysisartifact/builder.go:75,205` 读 `GetFactorReturns` 并组装产物；`GetICEntries`（`cache.go:239`）零调用。
- 判断：与 `factor_cache` 同一模式，但更危险——`factor_cache` 至少有 ADR-037 的"消费点按需求值"兜底；这两张表没有裁决，读者会拿到空集并继续产出"成功的"分析产物。
- 处置类别：**待主任裁决**（§6 D1）；代码不动。

**C4. analytics 与 core `metrics/reporting` 是同概念双实现，权威关系未写进 ADR 条款**
- 查到：`[代码]` `internal/repoguard/analytics_impl_freeze_test.go:33-37` 冻结 core 的 3 个生产 import（`pkg/backtest/engine.go`、`cmd/analysis/handlers_backtest.go`、`cmd/dualrun/main.go`）；`[文档]` `tellurion-analytics/docs/adr/0005-独立只读参考实现-core不迁移.md:3-11` 判"core 保留冻结、不迁移、SVC-AN-G3 关闭、K7 挂起"；`[文档]` `tellurion-analytics/docs/db-schema.md:66` 又说"不重算上游已算的指标"。
- 判断：当前事实上的关系是"core 运行时权威 + analytics 只读参考/子集"，但没有任何一处用"权威/参考"这两个词把它写死；两份公式的漂移没有检测机制。
- 处置类别：**改文档**（把关系写进 ADR-0005 或 ADR-037 的邻接条款）+ **待主任裁决**是否设迁移触发器（§6 D4）。

**C5. risk 自持 `Snapshot`/`SnapshotRule`/`ParseBundle`，与 `contracts/risk` 同形状**
- 查到：`[代码]` `tellurion-risk/internal/rule/snapshot.go:24,37,144`；`[代码]` `tellurion-contracts/risk/snapshot.go`、`scope.go`、`errors.go` 已存在；`[代码]` risk `go.mod` 零 import contracts。
- 判断：共享内核重复。风险不在"形状不同"，而在"两份定义会各自演进"。
- 处置类别：**搬代码**（只建议，§6 D3）。

### P2

**C6. core 的 `internal/analysisartifact` 在生产分析产物，analytics 才是声明的分析服务**
- 查到：`[代码]` `internal/analysisartifact/builder.go:75,205` 组装 factor returns / zscores / exposures；`[代码]` `docker-compose.yml:487-489` analytics 反向读 core 的 `/runs/{id}/{kind}` artifact。
- 判断：分析产物的**生产**在 core，**消费/报告**在 analytics；这是一个上下文被切成两半。当前可接受（artifact 与 run 结果同生命周期），但必须写明"暂时如此"与退出条件。
- 处置类别：**待主任裁决**（§6 D6）。

**C7. `core ↔ agent` 请求级双向调用，文档只写了单向启动依赖**
- 查到：`[代码]` `docker-compose.yml:235`（core→agent 反代）、`:326`（agent→core 因子面）、`:344-347`（启动依赖 ai→analysis 单向）；`[文档]` core `AGENTS.md:85` 写"依赖方向单向 agent→core（repoguard 钉住）"——这句只对编译期成立。
- 判断：不是架构回退，但口径不清会把运行期环当成违规。需要在依赖图里把"编译期/运行期"分开（本报告 §2 已做）。
- 处置类别：**改文档**（§8 未改 core AGENTS 这句，建议后续补一句"运行期另有反代边"）。

**C8. `GET /api/factors/:factor_name` 仍注册，但它代理的 data `/factors/{name}` 已不存在**
- 查到：`[代码]` `cmd/analysis/handlers_proxy.go:158-167`；`[代码]` data `internal/httpapi/server.go:117-155` 只有 `/datasets/*`、`/ingest/points`、`/api/sync/*`，无 `/factors`；ADR-037 已判"死链"。
- 判断：死路由，不影响主链路，但会误导前端与 agent。
- 处置类别：**搬代码/删路由**（只建议）。

**C9. compose 与 agent 注释声称 `/api/factor/*` "只在那里注册"**
- 查到：`[代码]` `docker-compose.yml:324-326`、`tellurion-agent/cmd/ai/main.go:100-101`；实际 core 只注册 `/api/factor/registrations`。
- 判断：与 C1 同源，是错误事实的传播源。
- 处置类别：**改文档/注释**（本轮未改，列入待办；因涉及部署配置，按"不动代码"纪律只报告）。

### P3

**C10. `analysis.benchmarks` 生产写者为零（K7）** — 已显式声明"表已建、暂不启用"（`db-schema.md:46`），有重开条件，不算缺陷。

**C11. 文档版本列整体滞后** — `[文档]` `REPO-MAP.md` 与多仓 `AGENTS.md` 写 contracts `v0.9.0`/kit `v0.3.0`，`[代码]` 各仓 `go.mod` 实测 contracts 已到 `v0.10.0`。**判断**：事实漂移，不改变边界结论；按"不代他仓改文档"纪律只报告。

**C12. `market.index_daily` 由 core 拥有/写入** — 已登记的跨 schema 例外（`REPO-MAP.md`）；建议在数据所有权矩阵里显式标注"唯一例外"，避免下次审查再发现一次。

**C13. `public.factor_cache` 表仍在但无写者** — ADR-037 已裁"消费点按需求值、不新增写者"；表本身尚未有删除迁移与退出条件，属于"裁决已下、收尾未做"。

---

## §5 三处已知待裁冲突的专项结论

### 5.1 SPEC-R-02（data 文档写 factor 域 owner=data）

- **查到**：见 C2。`TableNames()` 22 张表不含 `factor_*`；data 自己的 ARCHITECTURE §2.1 也写"因子读面不在本仓"。
- **判断**：SPEC-R-02 是**过期认领**，必须改。它不是"另一种合理意见"，而是与同仓代码、ADR-037、裁-14 同时冲突。
- **处置**：本轮已改 data `db-schema.md`（§8）。附带把 data `ARCHITECTURE.md` 的 Derived 行改成"不迁入本仓"，否则同一仓内仍有两套口径。**这不是推翻 ADR-037，而是把 ADR-027 的旧目标态收敛到 ADR-037 的现行裁决**。

### 5.2 `factor_returns` / `ic_analysis` / `factor_hypothesis` 的归属

- **`factor_hypothesis`：已闭合**。`[代码]` agent `pkg/aistore/schema.go:46,171` 建 `ai.factor_hypothesis`；`pkg/aistore/schema_core_drift_test.go:33` 把映射钉住；core 的 `public.factor_hypothesis` 已从 DDL 退役（`pkg/storage/postgres.go:346-349` 注释，文件已删）。data 文档 §1.3 的"core 过渡期写者 `pkg/storage/factor_hypothesis.go`"是**过期引用**，本轮已删。
- **`factor_returns` / `ic_analysis`：仍未裁**。物理在 core `public`，写方法在 `pkg/storage/cache.go`，但零生产调用；`factor_returns` 有一处读者（`internal/analysisartifact/builder.go:205`），`ic_analysis` 无读者。ADR-037 只裁了 `factor_cache` 与内置因子值。
- **判断**：这两张表属于"派生分析结果"，与 `factor_cache` 同族，但比它更接近 analytics 的归因/IC 领域；不能因为"物理在 core"就默认归 core，也不能因为"名字带 factor"就归 data。**列待裁决，不自己拍**（§6 D1）。

### 5.3 analytics 与 core `metrics/reporting` 的关系与未来迁移

- **查到**：core 保留冻结（3 个生产 import，护栏 `analytics_impl_freeze_test.go`）；analytics 是独立只读服务、core 零调用（ADR-0005）；analytics 指标面是 core 的子集（`[文档]` `ADR-0005` 与 `AGENTS.md`）。
- **判断**：现状是"**core = 运行时权威实现；analytics = 只读参考实现 + 报告/导出面**"。这不是"两个仓各持一半"，因为 analytics 不写回 core、不参与回测。真正的问题是**没有漂移检测**：core 改公式，analytics 不会红。
- **处置**：短期**不迁移**（迁移需要新端点 + DTO，且会动运行时承重路径，代价大于收益）；把"权威/参考"写进 ADR 裁决语；中期若要迁移，触发条件应是"analytics 成为报告的唯一产出方且 core 不再对外导出"，届时按 §6 D4 立项。

---

## §6 待主任裁决（不自己拍）

### D1. `factor_returns` / `ic_analysis` 的归属与去留

- 选项 A：**归 core，保留为派生读模型**，补一个写者或在消费点按需求值；代价 = core 继续背分析域，且需要新的写者/计算路径。
- 选项 B：**归 data，作为派生数据集**；代价 = data 需要因子计算逻辑，若重写就是双实现（违反单一真相）；若抽共享库，contracts 不能放算法，只能放 kit 或新库。
- 选项 C：**弃用两张表**，`factor_returns` 由 `internal/analysisartifact` 现场从行情+因子值算，`ic_analysis` 删除；代价 = 需要迁移/删表与退出条件，且 `analysisartifact` 会变重。
- **建议**：先把"零写者"事实与 `analysisartifact` 的静默读空修掉（响亮失败或明确空语义），归属再裁；不要在归属未定时补写者。

### D2. agent 因子工具面的处置

- 选项 A：**core 补粗粒度端点**（QT-50 ③-② 已登记的方向）；代价 = core 增加因子求值 HTTP 面，与 ADR-028 §6"求值在消费点 in-process"有张力。
- 选项 B：**agent 移除/降级 `factor.compute`/`factor.evaluate` 工具**，只保留已有端点能支持的 `compute_factor_ic`；代价 = Copilot 的因子研究能力缩水。
- 选项 C：**路由到 data**；代价 = 直接违反裁-14 与 dataflow 不变量 7（data 不提供因子读面），不建议。
- **建议**：A 或 B，取决于 Copilot 是否必须在线做因子求值；C 不可选。

### D3. risk 是否迁到 `contracts/risk`

- 选项 A：**迁**（risk 改用 contracts/risk 的 `Snapshot`/`Scope`）；代价 = 一次跨仓形状迁移 + risk 的 pgstore/解析路径改造。
- 选项 B：**不迁，正式声明 risk 的内部形状是私有实现**，contracts/risk 只服务其他消费方；代价 = 两份定义继续存在，但至少口径一致。
- **建议**：A 是 DDD 正解（共享内核只留一份）；若排期不允许，先做 B 的口径声明。

### D4. analytics 指标迁移

- 选项 A：**维持冻结**（现状）；代价 = 双实现长期漂移。
- 选项 B：**设迁移触发器**（analytics 成为唯一报告产出方时再迁）；代价 = 需要现在定义"触发器"与验收。
- 选项 C：**立即迁移**；代价 = 动 core 运行时承重路径 + 新端点/DTO，风险最高。
- **建议**：B。

### D5. 是否修订 ADR-027 §2.6.2 的 Derived 上下文目标

- 选项 A：**在 ADR-037 追加一条口径**，明确"Derived 不再迁入 data"；代价 = ADR-027 与 ADR-037 并存，读者需按时间序读。
- 选项 B：**修订 ADR-027**（标注 superseded 的段落）；代价 = 改动历史 ADR，需要主任签字。
- **建议**：A（最小改动、保留历史）。

### D6. `internal/analysisartifact` 的归属

- 选项 A：**暂留 core**，写明退出条件（analytics 接管 artifact 生产时迁）；代价 = core 继续持有分析产物生产。
- 选项 B：**迁 analytics**；代价 = 需要新端点 + 跨仓 DTO，且 artifact 与 run 生命周期耦合，风险高。
- **建议**：A。

---

## §7 与上一轮基线的差异（明说推翻/修正）

- **修正**：上一轮基线把 `analysis.benchmarks` 零写者当作"待核 K7"；本轮确认 ADR-0005 已把它挂起并有重开条件，不再算未知冲突。
- **新增**：`factor_returns` / `ic_analysis` 的孤儿状态是上一轮没有单列的；本轮把它提升为 P1（因为 `factor_returns` 有静默读空读者）。
- **修正**：上一轮"agent 与 core 依赖方向单向"只描述了编译期；本轮明确运行期存在 `core ↔ agent` 环（C7）。这不是推翻上一轮结论，而是把它限定到"编译期"。
- **未变**：`factor_hypothesis` 归 agent、`factor_cache` 归 core 且无 DB 写者、data 不提供因子读面——本轮全部维持。

---

## §8 本轮文档订正清单（已改，单列）

1. `tellurion-data/docs/db-schema.md`
   - §1.3 标题与表头改为"因子（不属本仓）"，并加一句"本仓 `TableNames()` 实测 22 张表，不含任何 `factor_*`"。
   - SPEC-R-02 认领段改写：owner = **core**（依据 ADR-037 + 裁-14），`factor_hypothesis` = agent；`factor_returns`/`ic_analysis` 标"归属待裁、当前零生产写者"。
   - 删除已删文件 `tellurion:pkg/storage/factor_hypothesis.go` 的引用。
2. `tellurion-data/docs/ARCHITECTURE.md`
   - §2.1 "派生 Derived"行：由"目标包 `internal/derived`、今天在 core"改为"**不迁入本仓**；owner=core，按 ADR-037 在消费点按需求值"。
3. `tellurion-analytics/docs/db-schema.md`
   - §2 只读输入表：把"因子值"的 owner 从 `tellurion-data` 拆出，改为 `core`（按需求值，ADR-037）。
4. `tellurion/AGENTS.md`
   - IDE 入口行删除 `cmd/data/main.go`；目录树删除 `cmd/data` 与 `pkg/data` 条目；`pkg/sync` 收窄为"数据管道已迁 tellurion-data"。
   - 技术栈表"数据服务 :8081"补注"源码在 `tellurion-data` 仓"。
   - "Redis `factor_cache`" → "PostgreSQL `public.factor_cache`（当前无写者，见 ADR-037）"。
   - ADR 计数 36 → 37。
   - AI 实验日志表名改为 `ai.experiments` / `ai.factor_hypothesis`（芯表已退役）。
   - 包结构链与迁移入口去掉 `pkg/data` / `cmd/data/setup.go`；测试命令删掉已不存在的 `go test ./pkg/data/...`。
   - **未改**：附录"已知风险"里仍有多条历史条目引用 `pkg/data/*`、`cmd/data/*`（如 DBT-09/DBT-13 的取证路径）。它们是当时的事实记录，逐条改写会篡改审计叙事，故保留并在本清单单列。

**未改（只报告）**：`docker-compose.yml` 与 agent 代码注释里"/api/factor/* 只在那里注册"（C9）；各仓 `AGENTS.md` 的 contracts/kit 版本列（C11）。前者涉及部署配置、后者涉及他仓文档，按本轮纪律不越权。

---

## §9 结论摘要

- **12 仓的宏观边界是成立的**：core 是运行时核心域，六个能力仓是支撑域，contracts/kit 是通用域，ui/docs 无领域；没有发现跨仓双写同一张表。
- **真正的问题集中在三处**：① agent 的因子工具指向不存在的 core 端点（P0）；② 因子域文档与 ADR-037/裁-14/自身代码相反（P1，已改文档）；③ `factor_returns`/`ic_analysis` 孤儿表（P1，待裁）。
- **两个"看起来像问题、实际是已裁决"的项**：`factor_cache` 无写者（ADR-037）、`analysis.benchmarks` 无写者（K7）。
- **一个需要写进口径的现状**：core 是运行时权威、analytics 是只读参考实现；两者不是双主，但缺漂移检测。

冲突清单共 **13 条**（P0×1、P1×4、P2×4、P3×4）。

---

## §10 主任裁决回填（2026-11-11，本报告之后）

§6 的待裁项已全部裁决，落在跨仓 ADR 与本仓/各仓台账：

| 原待裁项 | 裁决 | 落点 |
|---|---|---|
| D1 `factor_returns`/`ic_analysis` 归属 | **归 core**（与因子值同源；沿用「消费点按需求值、不设跨上下文写者」；否决 data 无引擎重写、agent 不持分析真相） | [ADR-038](../adr/adr-038-factor-derived-tables-ownership.md)；`tellurion:CORE-FACTOR-DERIVED-GUARD` |
| D2 agent 因子工具面 | **不新造端点**；core 现有能力语义对不上 ⇒ 工具显式返回「该能力当前未提供」，标 `unavailable` | [ADR-041](../adr/adr-041-ai-factor-tools-no-phantom-endpoints.md)；`tellurion-agent:AGENT-FACTOR-TOOLS-UNAVAILABLE` |
| D3 risk `Snapshot` 双定义 | **唯一真相 = `contracts/risk`**；`Bundle`/`ParseBundle` 留 risk；别名引用、零数据迁移、hash 不变 | [ADR-040](../adr/adr-040-risk-snapshot-single-source.md)；`tellurion-risk:RISK-CONTRACTS-SNAPSHOT-MIGRATION` |
| D4 analytics vs core 指标 | **core 运行时权威、analytics 只读参考**；五条共存边界 + 三条可判定收敛触发（T1 报告出口单点化 / T2 漂移超限 / T3 冻结解冻） | [ADR-039](../adr/adr-039-metric-authority-and-dual-implementation.md)；`tellurion-analytics:ANALYTICS-METRIC-DRIFT` |
| D6 `analysisartifact` 去留 | **保留在 core**，记三条保留条件与退出信号（ADR-039 T1）；本轮不改代码 | `tellurion:CORE-ANALYSISARTIFACT-RETENTION`（⏸） |

**§8 的「未改（只报告）」已在本轮补齐**：C9 的注释订正立 `tellurion:CORE-COMPOSE-FACTOR-COMMENT` + agent 同批；C11 的版本列已按 2026-11-11 实测订正到 `REPO-MAP.md`（contracts `v0.10.0`、data/strategy 已 pin）。

**13 条逐条状态**以 `tellurion:docs/TASKS.md` §三台账为准（本报告不重复维护状态，避免双写）。
