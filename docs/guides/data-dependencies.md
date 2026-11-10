---
status: evergreen
last-verified: 2026-11-11
verified-by: 代码-文档对齐审计（2026-11-11）全量订正 —— ① 仓归属按实仓重判：取数/归一化/同步/ingest 已整体在
  `tellurion-data`（`cmd/dataservice` + `internal/{ingest,normalize,sync,schema,transport}`），core 已无
  `cmd/data` / `pkg/data`，只保留 `pkg/marketdata`（只读客户端）与一条 `market.index_daily` DDL；
  ② adapter 注册点改为 `tellurion-data:internal/ingest/connectors.go` 的 `Connectors()` / `RegisterConnectors`，
  12 个 connector 逐条复核；③ `DATA_DISABLE_<NAME>` kill switch 随 core `registry_init.go` 一起删除，
  现行开关是「transport 为 nil ⇒ disabled」+ 两个凭据 env（`TUSHARE_TOKEN` / `ALPHA_VANTAGE_KEY`）；
  ④ `hkex` 在 12 仓中已无 Go 实现（仅存于历史仓 `quant-trading`），不再是「代码完整、零调用方」；
  ⑤ 凭据读取点迁至 `tellurion-data:cmd/dataservice/main.go`；core 的 `config/data-service.yaml` 已无 Go 读取点。
  下文 §7 的 Tushare 实测数字沿用 2026-09-23 / 09-24 / 10-12 三次真库取证的读数（未重跑）。
---

# 数据面外部依赖与凭据清单（12 仓）

> 回答两个问题：**数据面要接哪些外部源、各要什么凭据**，以及**这些东西今天在哪个仓**。
> 部署侧的环境变量口径见 [deploy-config.md](deploy-config.md)；本地起栈见
> [local-dev.md](local-dev.md)；数据面各表的真相源是 `tellurion-data:docs/db-schema.md`。

---

## 0. 仓归属：今天在哪、目标在哪

这份清单最容易过时的地方不是「用什么 key」，而是**这些代码属于谁**。分仓之后：

| 数据面能力 | 今天在 | 目标（触发后） | 依据 |
|---|---|---|---|
| connector / 归一化 / 同步 / aggregator | `tellurion-data`：`cmd/dataservice` + `internal/{ingest,normalize,sync,transport}`（生产 `:8081` 的唯一提供者） | 已达成（2026-11-08 core `cmd/data` 删除） | ADR-034、core `repo-inventory.md` |
| `market` / `ingest` 两个 schema 的 DDL owner | `tellurion-data:internal/schema`（23 张 `market.*` / `ingest.*`）；core 只剩一条 `market.index_daily`（`tellurion:pkg/storage/postgres.go` 的 Migration 057，供只读面自建） | `tellurion-data` | 双 owner 只剩 `market.index_daily`（第四轮审计 P0-2 的裁决对象） |
| 因子**定义** / `SeriesSpec` | core（`pkg/domain/factor_def*`、`pkg/mining/registry.go` —— 原 `pkg/data/factor_registry.go` 已随 `SVC-CORE-DATA-RETIRE` 迁走） | `tellurion-strategy`（定义）/ `tellurion-data`（值） | core `repo-inventory.md` §1.2 的 **R3** 行：定义归 strategy、值归 data、求值在消费点（ADR-035 §三 是那轮对账的升格摘要，**细则仍在 core 源文**） |
| AI 供应商凭据的**读取点** | `tellurion-agent:pkg/ai/client.go` | 同左 | 2026-10-09 AI 拆仓 |
| `quant.*`（结果 / 订单 / 持仓） | core | core（订单归属是待裁项 U2，**先立 ADR 才能拆**） | `repo-inventory.md` §3.1 |

> ⚠️ **数据面已整体迁到 `tellurion-data`（2026-11-11 复核）**：生产 `:8081` 由
> `tellurion-data:cmd/dataservice` 提供，core 的 `cmd/data` / `pkg/data` 已删除；core 只剩
> `pkg/marketdata` 的只读客户端与 `market.index_daily` 一条 DDL。本清单凡写 `tellurion-data`
> 的路径都已按实仓核对；其余仓的「今天」仍指其自身仓（策略运行时在 core、`quant.*` 在 core）。
> 六个服务仓各有 `cmd/*service` 与自有 schema，但**不要把「已实装」读成「G3 已全量切读」** ——
> 各仓闸门状态见 [`../SERVICE-INDEX.md`](../SERVICE-INDEX.md)。

---

## 1. 一句话结论

**外部数据源的凭据真正只有一个：`TUSHARE_TOKEN`。** 它不填，A 股行情 / 财务 / 宏观三类都验不了。
其余要么**已有槽位待填**（`ALPHA_VANTAGE_KEY`）、要么**免费无需 key**（yahoo / eastmoney /
xueqiu / juchao）、要么缺的是**代码依赖而不是 key**（mootdx 缺 Go SDK）。
另有一个**可选**的第三方凭据组：`AI_API_KEY` + `AI_API_URL` + `AI_MODEL`（读在 agent 仓）。

而且**「跨境」那一半其实已经做完了** —— 见下表。

---

## 2. registry 里已接线 12 个 adapter

注册点在 `tellurion-data:internal/ingest/connectors.go` 的 `Connectors(Transports)`，由
`RegisterConnectors` 在启动期一次性装配 12 个 connector；**禁用 = 对应 transport 为 nil**
（`Transports` 结构体零值），不读任何 `DATA_DISABLE_*` —— 所以「没配 key」不会让服务起不来，
只会让 Fetch 时那条链走空。

| adapter | 数据类型 | 凭据 | 现状 |
|---|---|---|---|
| `tushare` | `ohlcv_daily` / `fundamentals` | **`TUSHARE_TOKEN`** | 已接线；token 空 → disabled |
| `eastmoney` | `capital_flow` | 无 | 默认启用 |
| `eastmoney_sectors` | `sectors` / `stock_sector` | 无 | 默认启用 |
| `eastmoney_toplist` | `top_list` / `limit_up_pool` | 无 | 默认启用 |
| `juchao` | `announcements` | 无 | 默认启用 |
| `xueqiu` | `news` / `hot_search` | 无 | 默认启用 |
| `yahoo_finance` | `global_ohlcv` | 无 | 默认启用 —— **跨境 primary** |
| `alpha_vantage` | `global_ohlcv` | `ALPHA_VANTAGE_KEY` | 已接线；无 key → disabled —— **跨境 secondary** |
| `mootdx` | `realtime_quote` / `ohlcv_minute` | 无 key，**缺 SDK** | 恒 disabled（`go.mod` 里没有 `go-mootdx`） |
| `tushare_macro` | `macro`（P2-1） | 复用 `TUSHARE_TOKEN` | 已接线；token 空 → disabled |
| `tushare_daily_basic` | `market_activity`（D5） | 复用 `TUSHARE_TOKEN` | 已接线；token 空 → disabled |
| `tushare_moneyflow` | `capital_flow`（DBT-09） | 复用 `TUSHARE_TOKEN` | 已接线；token 空 → disabled |

后三个是 2026-10 新增的，**复用同一个 token、0 个新 key**；它们与其余源一样，禁用条件是
transport 为 nil，没有按源的环境变量开关。

**未接线**：`hkex`（港股源）在 12 仓中**已无 Go 实现** —— 它随历史仓 `quant-trading` 退役，
`tellurion` / `tellurion-data` 全仓 grep `hkex` 零命中（只剩 `tellurion-data:docs/dataflow.md`
的历史叙述）。原先的登记依据（`unwiredPackages` 白名单）已随 `pkg/data` 删除，
`tellurion:internal/repoguard/package_wiring_test.go` 的 `unwiredPackages` 里已没有 `hkex`。
要港股行情属于**新建 adapter**，不是「先接现成代码」，且不需要新 key。

**没有按源的环境变量 kill switch**：`tellurion-data` 全仓 grep `DATA_DISABLE` / `envDisabled`
零命中。现行开关是装配期传入的 transport：**为 nil 即 disabled**（启动不失败、Fetch 跳过）。
要单独关一个源，得改装配代码或撤掉对应凭据（`TUSHARE_TOKEN` / `ALPHA_VANTAGE_KEY`）。

> **链 ≠ 已生效**：除 `capital_flow` 外，其余链今天仍没有生产路径走 `Fetch`
> （日线同步直连 `TushareClient`）。`tellurion-data` **没有** `/api/datasource/registry/*` 端点
> （23 条路由里不存在 datasource registry），所以链配置不再承担「展示意图」的职能；
> 12 个 connector 的声明面由 `tellurion-data:internal/ingest/declaration_test.go` 钉住。

---

## 3. 凭据清单（各进程的环境变量；模板 `tellurion:.env.example`）

| 变量 | 必需性 | 用途 | **谁读它（哪个仓）** | 现状 |
|---|---|---|---|---|
| **`TUSHARE_TOKEN`** | **阻塞项** | A 股行情 / 财务 / 复权因子 / 宏观 / 资金流 | `tellurion-data:cmd/dataservice/main.go`（`os.Getenv`，直接注入 Tushare transport） | 按部署注入；空 ⇒ tushare 系 4 个 connector 全部 disabled |
| `JWT_SECRET` | 必填，否则拒绝启动 | 鉴权 | `tellurion`（`auth.jwt_secret`）、`tellurion-data`（`envFirst("JWT_SECRET","AUTH_JWT_SECRET")`）、agent 同构 | 需 `openssl rand -hex 32` |
| `DATABASE_PASSWORD` / `DATABASE_URL` | 必填 | 数据库 | `tellurion` / `tellurion-agent` 用 `DATABASE_PASSWORD`；`tellurion-data` 用完整 `DATABASE_URL`（空 ⇒ fail-closed 503） | 默认 `postgres` |
| `AI_API_KEY` + `AI_API_URL` + `AI_MODEL` | 可选 | 因果维 / AI 实验员 / Copilot / 探索观察台 | **`tellurion-agent:pkg/ai/client.go`**（直读 env） | key 已配（MiniMax CN）；URL/模型见 §4 |
| `ALPHA_VANTAGE_KEY` | 可选 | 跨境行情 fallback | `tellurion-data:cmd/dataservice/main.go`（`os.Getenv`） | 空 |

两个读取路径的坑（都已修，别踩回去）：

- `TUSHARE_TOKEN` **只从 env 读**（`os.Getenv("TUSHARE_TOKEN")`），没有配置文件入口。core 的
  `config/data-service.yaml` 仍留在仓里，但**已无 Go 读取点**（core 2026-11-11 审计 G-02 登记为死配置），
  不要再把 token 往里写。`tellurion:tools/check_deploy_consistency.py` 的检查 7 仍在守
  「`config/*.yaml` 不得出现 `${`」—— 那是历史不变量，不是当前数据面的配置入口。
- `ALPHA_VANTAGE_KEY` 同样只从 env 读；空 ⇒ `alpha_vantage` connector 的 transport 为 nil（disabled）。
  旧的「env 与 viper 双入口、viper 优先 + CR-54 warn」随 core `registry_init.go` 删除，已不存在。

---

## 4. AI 三项：读取点已经换了仓

这是 DOC-08 之前本文最容易误导人的一处 —— 它当时写「`pkg/ai/client.go` 直读 env」，
那还是单仓时代。**今天 `tellurion` 仓没有 `pkg/ai`**：

| 事实 | 证据 |
|---|---|
| 读取点在 agent | `tellurion-agent:pkg/ai/client.go` 的 `os.Getenv("AI_API_KEY")` / `"AI_API_URL"` / `resolveModel()` 读 `AI_MODEL` |
| core 侧无读取者 | `tellurion` 全仓 grep `AI_API_KEY` 只命中 `.env.example` 的注释与 `docker-compose.yml` 本身 |
| core compose 仍注入给 analysis | `docker-compose.yml` 的 `analysis-service.environment` 里有这三项 —— **拆仓遗留的死注入**（无害，但别据此以为 analysis 在读） |
| 给 ai-service 的注入是有效的 | 同一个 compose 的 `ai-service.environment`，agent 进程真的读它 |

三个变量必须**成对**改：`AI_API_URL` 填完整 chat-completions 端点（以 `/chat/completions`
结尾，不是 base URL），`AI_MODEL` 填该供应商的模型 id。协议是 OpenAI 兼容的
（`POST <URL>` + `Authorization: Bearer <KEY>` + body `{"model":...,"messages":[...]}`），
但**协议兼容 ≠ 模型名兼容** —— 只改 URL 会把默认的 `gpt-4o-mini` 发给对方，对方回
`model not found`。`AI_MODEL` 留空回落到 `tellurion-agent:pkg/ai` 的 `DefaultModel`。
改完必须**重建**容器，环境变量不热加载。

---

## 5. 缺的不是 key 而是代码依赖

- **mootdx**：需要 Go SDK `github.com/qmaru/go-mootdx` 进 `go.mod`，再加一个真实 transport
  实现（当前传 `nil`）。它是「实时/分钟行情」链上的 primary —— 不接它，`realtime_quote` 与
  `ohlcv_minute` 两条链实际只有 eastmoney 一个源在跑。
  **这是代码工作量，不是凭据问题。**

---

## 6. 待核实（不假装知道）

- `stk_factor_pro`（pro 版）的积分门槛 —— 下文数字取自 `stk_factor` 官方文档，pro 版可能不同。
- 各 Tushare 宏观接口的准确名称与积分要求 —— 只有 §7.2 表里那 9 个是**真 token 逐个探过**的，
  其余未逐条核对。

---

## 7. 历史取证（结论仍成立；数字是各次实测读数）

> 这一节的正文属于 core 的 P2 台账取证；代码已随 `pkg/data` 迁入 `tellurion-data`，
> 取证结论与读数保持原样（未重跑）。

### 7.1 跨境已完成、宏观已落地（P2-1）

- **跨境（美股等境外行情）**：**已做完**。链已配 `global_ohlcv: [yahoo_finance, alpha_vantage]`
  （yahoo 免 key 为主、alpha 为辅）。登记里「新建 adapter」这个说法对跨境这一半**已经过时**。
- **宏观（汇率 / 利率 / 物价 / 货币）**：**已落地**（2026-10-12）。
  `quant.macro_series` 的 DDL 在 `tellurion:pkg/storage/postgres.go`
  （`Migration 050`，文档副本 `tellurion:docs/migrations/050_add_macro_series_table.sql`，
  **不执行**，只作历史证据）；`tellurion-data:internal/transport/tushare/macro.go`（原
  `pkg/data/source` 的 `DataTypeMacro` + `TushareMacroAdapter`）；
  只读 API 仍在 core 的 `GET /api/macro/series`。跨境之外的另一半（大宗 / 境外宏观）**仍未接**。

候选源与代价（选型依据）：

| 源 | 覆盖 | 凭据 | 代价 |
|---|---|---|---|
| **Tushare 宏观接口** | 国内宏观 | **复用 `TUSHARE_TOKEN`** | 0 个新 key，但吃积分 —— **已选这条** |
| Alpha Vantage | FX / 大宗 / 美债收益率 | 复用 `ALPHA_VANTAGE_KEY` 槽位 | 0 个新 key；**免费档 25 req/day**，只够探测 |
| FRED（美联储） | 美国利率 / 宏观 | 免费注册拿 key | 1 个新 key |
| World Bank | 跨境宏观 | 无 | 0 个新 key |

### 7.2 实测接口清单（2026-10-12，真 token 逐个探测，不是文档推断）

> 用仓库 `.env` 里的真 token 逐个 POST `api.tushare.pro` 探出来的，**`code:0` 且有真数据**
> 才算通过。第三方博客给的 doc_id 映射不可信（实测 3 个错的）。

| indicator | tushare 接口 | 频 | 日期列 / 数值列 | 官方积分 | 入库行数（真库） |
|---|---|---|---|---|---|
| `CPI_YOY` | `cn_cpi` | M | `month` / `nt_yoy` | 600 | 512（1951-12 → 2026-08） |
| `PPI_YOY` | `cn_ppi` | M | `month` / `ppi_yoy` | 600 | 377（1978-12 → 2026-08） |
| `PMI` | `cn_pmi` | M | `month` / `pmi010000` | 5000（官方页） | 261（2005-01 → 2026-09） |
| `M2` | `cn_m` | M | `month` / `m2` | 600 | 407（1990-12 → 2026-08） |
| `M2_YOY` | `cn_m` | M | `month` / `m2_yoy` | 同上（共用请求） | 373（1991-12 → 2026-08） |
| `TSF_INC` | `sf_month` | M | `month` / `inc_month` | 2000 | 296（2002-01 → 2026-08） |
| `LPR_1Y` | `shibor_lpr` | D | `date` / `1y` | 120（正式权限 5000） | 1532（2013-10-25 → 2026-08-20） |
| `LPR_5Y` | `shibor_lpr` | D | `date` / `5y` | 同上（共用请求） | 见流控注记 |
| `USDCNY_CLOSE` | `fx_daily` | D | `trade_date` / `bid_close`（`ts_code=USDCNH.FXCM`） | 2000 | 2410（2019-01-02 → 2026-10-11） |

#### 三个坑（实测推翻文档，动手前先看）

1. **`cn_pmi` 响应字段是大写**（`MONTH` / `PMI010000`），与文档的小写不一致；
   `fields` 参数传小写仍有效（实测 `fields=month,pmi010000` 正常返回）。
   → normalize 必须**大小写不敏感**匹配列名。
2. **`shibor_lpr` 限 1 次/小时**：实测返回
   `40203 抱歉，您访问接口(shibor_lpr)频率超限(1次/小时)`。
   ⚠️ 官方页（doc_id=151）标称「500 次/min」，与实测**冲突**；以实测为准 —— 标称是上限，
   实测才是你真会撞到的墙。
   → `LPR_1Y` / `LPR_5Y` **必须共用一次请求**，也**不能按年分段**（分段要 14 次请求，
   必然撞限）。改回逐条拉取 = 第二个 LPR 永远拉不到。
3. **`fx_daily` 单次限量 1000 行（文档）但实测返回 2410 行不截断**。
   → **不依赖未文档化行为**，仍按年分段（每年 ~300 行，8 段）。

> **40203 ≠ token 无效**（那是 40101）。撞 40203 只说明**该接口撞了流控**，不是没权限
> （对比 §7.3 的 `stk_factor_pro` 才是真的无权限）。

### 7.3 复权口径：`daily` + `adj_factor` 自己算（P2-8）

> ⚠️ **原文「用 `stk_factor_pro` 多请求 4 个 `*_hfq` 字段即可」的方案已被实测推翻
> （2026-09-23）** —— 那是基于接口文档推断的，**没有考虑权限**。真跑返回
> **40203「没有接口(stk_factor_pro)访问权限」**，行情一只都进不来。别再按旧方案动手。

实测权限边界（容器内 curl，同一个 token）：

| 接口 | 结果 |
|---|---|
| `daily`（不复权行情） | ✅ |
| `adj_factor`（复权因子） | ✅ |
| `stock_basic` | ✅ |
| `stk_factor` / `stk_factor_pro` | ❌ **40203 无权限** |

**现改为 `daily` + `adj_factor` 自己算复权**（`tellurion-data:internal/transport/tushare/stocks.go`），口径取自
Tushare 官方 `adj_factor` 文档示例 4：

```
前复权价 = 当日价格 × 当日复权因子 / 最新复权因子     (qfq)
后复权价 = 当日价格 × 当日复权因子                   (hfq，基准为上市日)
```

这个改法**比原方案更好**：官方自己说 `stk_factor` 的 qfq 是「从最新交易日往前复权的历史快照，
数据不更新」，而 `adj_factor` 是每日更新的因子（盘前 8:30-9:30 入库），自己算可以避开快照问题。
代价是每次取数要两次请求。

**hfq 落库仍被推迟，判据如下**（`tellurion-data:internal/transport/tushare/stocks_test.go`
真库 + 真 Tushare + 真引擎实测）：

- 把每只票的价格乘一个正数常数（收益率序列逐点不变），同一策略、同一批票、同一引擎，
  **总收益会动 21.6 个百分点**（资金放大 100 倍后 24.9pp；均匀缩放只差 1.1pp）。
  ⇒ 「只差一个每股常数，影响可能只有取整」**方向对、量级错**。
- 通道**不在** regime 判定（`tellurion:pkg/risk/regime_scale_invariance_test.go` 实测对每票
  各自缩放 14/14 窗口完全一致，数学上也对组内缩放不变），而在**下单侧**：策略无状态
  （每天对 top-N 发 `Long`、不读持仓）＋ 引擎「目标 − 已持」抵扣只在 `PendingQty > 0` 时生效
  → 每天重发全量买单、每天被 `insufficient cash` 拒一次。
- **AUD-55 已修**（抵扣改无条件、已持仓实时读 tracker），资金侧敏感度随之塌掉
  （合成 4.82pp → 0.76pp、资金阶梯转收敛、零拒单）。
- **但「修完就能落 hfq」不成立**：hfq 价 = qfq 价 × **每股各自**的常数（实测 1.7~181），
  单位已不是「元」；拿固定资金交易被放大过的价格 ⇒ 高价票连一手都买不起 ⇒ **票池成分被改写**。
  这是整手规则 × 固定资金的结果，**不是引擎缺陷**。
  ⇒ 落 hfq 前必须先回答：**资金要不要按同一基准缩放？「票池被改写」要不要接受？**
  **21.6pp 也不能读成「前视偏差值 21.6 个百分点」**，里面含着一块与「前视」无关的成分。

积分（`adj_factor` 官方原文）：**2000 积分起，5000 以上可高频调取** —— 与 `stk_factor`
（5000 起）相比门槛低一档。

### 7.4 产业链底座与验证器（P2-2 / P2-13）：新增 0 个 key

- **产业链 `query_supply_chain(name)`**：没有哪个公开 API 直接给「公司-环节归属 + 上下游映射
  + 传导指标」（给的都是行业标签），所以它是**构建**任务不是**接入**任务 —— 骨架复用已有的
  tushare 行业分类 + eastmoney 板块（两个源都已在链上），环节关系可由 AI 生成草案再人工审
  （只用到**已存在的 `AI_API_KEY`**）。**不产生任何新凭据**。
- **验证器接真实回测取证**：不需要新数据源。前置是①库里有真数据（同一个 `TUSHARE_TOKEN`）；
  ②因果维要调模型 → `AI_API_KEY`。统计/经济/稳健/偏差/冗余五维是纯计算，不需要任何凭据。