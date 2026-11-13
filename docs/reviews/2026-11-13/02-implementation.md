---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 只读深度审查（角度 2 实现）；证据 = 代码 file:line + 只读目录/哈希/git 观测
---

# 角度 2 · 实现（8.0 / 10）

> 审查范围：架构是否按设计落地、关键链路正确性、明显缺陷与遗留缺口、12 仓真实耦合。
> 方法：全静态只读。未执行 `go build/test`、未启动服务、未改任何文件。规模统计来自目录扫描（非编译产物）。
> 相关基线：[SYSTEM-DESIGN.md](../../SYSTEM-DESIGN.md) · [REPO-MAP.md](../../REPO-MAP.md) · 各仓 `ARCHITECTURE.md`

---

## 1. 评分

| 子维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| 架构按设计落地 | 25% | 9.0 | 模块化单体 + kernel BootOrder + composition root 真实存在；服务间零 Go 编译依赖、零 `replace`、零 `go.work`；装配期 fail-closed |
| 关键链路正确性 | 30% | 8.5 | 回测 / 异步作业 / worker 领取 / 风控快照 / 券商幂等 / 数据取数六条主链均能在代码中闭合，且每环有对应守卫 |
| 明显缺陷 | 20% | 7.0 | stockstate 约 1000 行完全未接线；探针命名分叉（`/health` vs `/healthz`）；数据服务地址默认值两套；`/api/v1` 索引过期 |
| 遗留缺口 | 15% | 7.5 | 12 个白名单死包、analytics 零消费者、options/margin 等能力无入口；均有登记或裁决，不是隐藏债 |
| 跨仓真实耦合 | 10% | 8.5 | 耦合只有 HTTP + `contracts`/`kit` 两个版本化底座；版本已统一到 contracts v0.10.0 / kit v0.5.0 |
| **加权总分** | 100% | **8.0** | 工程执行力明显高于产品完成度；扣分主要在“死代码/分叉配置/文档过期”而非主链错误 |

---

## 2. 关键链路核验（逐条给出闭合点）

| 链路 | 证据 | 结论 |
|---|---|---|
| UI → core 回测 | `cmd/analysis/handlers_backtest.go:86`（同步）、`:134`（异步 submit） | 闭合；同步 10 分钟超时，agent 侧客户端 30 分钟（`tellurion-agent/pkg/ai/client/backtest_client.go:125`），上游先超时 |
| agent 探索 → core 回测 → 回写裁决 | `tellurion-agent/cmd/ai/handlers_explore.go:54-62`（verdictSink）、`:401`（`RecordVerdict`）；`pkg/ai/client/backtest_client.go` | 闭合；每轮 attempt 真打 `POST /api/backtest` |
| core 异步 → orchestration → worker | `handlers_backtest.go:107-115`（无编排即 503，无本地回退）；`cmd/worker/main.go:4-5`、`:170-171`；orchestration `SERVICE.md:67`（`FOR UPDATE SKIP LOCKED`） | 闭合；单一路径，无第二真相 |
| core → risk 快照 | `pkg/bootstrap/engine.go:37-52`；risk `docs/db-schema.md:225`（`resolve_enabled` 出厂 true，取不到即启动失败） | 闭合；fail-closed，无默认限额静默兜底 |
| core → broker 下单 | `pkg/bootstrap/engine.go:54-61`（`BROKER_URL` 缺失即装配错误）；`pkg/brokerhttp/trader.go:60-90`（`BROKER_CHANNEL` + `BROKER_ALLOW_MOCK` 双键）；broker `docs/api-schema.md:212-214`（`(account_id, client_order_id)` 持久幂等） | 闭合；真钱路径有明确“未发送/状态未知”语义 |
| core → data 取数 | `pkg/marketdata/http_provider.go:36`（30s + 3 次重试）、`:76`（`/ohlcv/{symbol}`）、`:105`（`/stocks`）；data `internal/httpapi/server.go:142-156`（7 条兼容只读面） | 闭合；4xx 由 kit 客户端转结构化错误，不会把 401 当空数据 |
| core → data 同步作业 + SSE | `cmd/analysis/handlers_proxy.go:54-65`（ReverseProxy + `FlushInterval=-1` + 清写截止） | 闭合；SSE 不会被网关写超时截断 |

链路层面的核心判断：**这套系统的主链不是“文档里画出来的”，而是代码里真的接上了**。这在 12 仓、14 万行的规模下不常见。

---

## 3. 主要发现（按严重度）

### P1-1 · stockstate 是一整块“编译进来但永不注册”的死面

- `cmd/analysis/handlers_stock_state.go:50` 定义了 6 条路由（停牌/退市/强制平仓相关），但全仓 `main.go` **没有** `NewStockStateHandler` 调用点（只读 grep 确认）。
- 其底层 `pkg/trading/stockstate/stock_state.go` 455 行生产代码 + `stock_state_test.go` 556 行测试一并成为不可达代码。
- 为什么严重：这是**交易安全语义**（停牌/退市股票不可交易、强平）的实现，却不在任何运行路径上；现有 `internal/repoguard/package_wiring_test.go` 只守“包无导入者”，守不到“handler 有定义、路由没注册”。
- 证据强度：实测（路由注册缺失 + 包引用链）。

### P2-1 · 探针命名分叉：`/health` 与 `/healthz` 并存

- 数据仓已按 `X-PROBE-NAMING` 统一为 `/healthz` 并删除 `/health`（`tellurion-data/internal/httpapi/server.go:121-126`）。
- core 仍只有 `GET /health`（`cmd/analysis/main.go:309`），agent 仍只有 `GET /health`（`tellurion-agent/cmd/ai/main.go:128`），二者的免鉴权白名单也写死 `/health`（agent `cmd/ai/lifecycle.go:143`）。
- `docker-compose.yml` 已按各自实际路径配置（core `:274` 用 `/health`，data `:160` 用 `/healthz`），所以**今天不会坏**；已收口的 `X-PROBE-NAMING` 只覆盖 data（core 侧只做 e2e 复验），core/agent 仍保留 `/health`，跨仓探针名因此不统一。
- 证据强度：实测（8 仓探针路径扫描）。

### P2-2 · 同一个 `data_service.url` 有两套默认值

- `pkg/bootstrap/engine.go:22-25` 缺失时回落 `http://localhost:8081`。
- `cmd/analysis/handlers_proxy.go:35-38` 缺失时回落 `http://data-service:8081`。
- 配置存在时（`config/analysis-service.yaml:114`）无影响；一旦配置缺项，回测取数与 `/api/sync/*` 反代会指向**不同主机**，表现为“回测取不到数但同步页正常”这类割裂故障。
- 证据强度：实测（两处代码）。

### P2-3 · `/api/v1` 服务索引只覆盖 legacy 别名，不覆盖主面

- `cmd/analysis/main.go:326-337` 返回的端点列表是 `GET /health`、`POST /backtest`、`GET /backtest/:id/report` 等**裸路径**。
- 这些路径确实存在：`handlers_backtest.go:511-533` 有一组 legacy 别名把 `/backtest*` 重写到 `/api/backtest*`，`main.go:309` 也真的提供 `GET /health`。所以索引**不是错的**，此前“会 404”的判断不成立。
- 真正的问题是覆盖不全：现代主面 `/api/backtest`、`/api/sync/*`、`/api/explore/*`、`/api/copilot/*` 均不在索引里；机器读到的是一个“只有兼容别名”的自描述面。
- 证据强度：实测（索引内容 + legacy 重写 + 路由注册）。

### P2-4 · `POST /api/backtest` 用“字段探测”区分两种请求体

- `handlers_backtest.go:97` 先试异步体（`strategy_id` + `universe` 同时非空），否则退回 legacy 信封（`:153` 要求 `strategy`）。
- 后果：同时携带 `strategy` 与 `strategy_id/universe` 的请求会**静默走异步分支**；异步体只写对一半（例如有 `strategy_id` 无 `universe`）则落到 legacy 分支报“strategy required”，错误信息与真实原因不符。
- 属 API 设计缺陷而非数据错误；`routes_contract_rev13_test.go` 只锁路由存在性，不锁这种 union 语义。
- 证据强度：实测（分支条件）；“调用方会踩到”为推断。

### P2-5 · 可维护性集中在少数超大文件

- `pkg/backtest/engine.go` 2237 行 + `engine_daily.go` 1128 行；`pkg/backtest` 目录下测试文件 70+ 个（含 `qt04_duplicate_signal_scan_test.go` 1341 行）。
- core 生产代码 75,786 行 / 测试 94,335 行（比例 1.24），服务仓 0.68–1.20；测试密度是优点，但引擎核心单文件体量会让“局部改动的影响面”难以静态评估。
- 证据强度：实测（行数统计）。

### P2-6 · 已登记的死能力与“无入口能力”

- `internal/repoguard/package_wiring_test.go:72-100` 列出 12 个白名单死包：api / auction / systemalert / margin / options / testutil / id / sandbox runner / staticcheck / strategy monitor / mining / sync。
- 其中 `options`（期权）、`margin`（两融）、`auction`（集合竞价）是**交易能力**而非工具包；它们没有 HTTP 入口，用户不可达。
- analytics 服务 8 端点、4186 行生产代码，core 调用方为 0（`REPO-MAP.md:23`，ADR-0005 有意裁决）。
- 证据强度：实测（护栏自述 + 调用点检索）。

### P3-1 · 其它小口径不一致

| 项 | 证据 | 影响 |
|---|---|---|
| agent README 自述“单向依赖 core”与“零编译依赖”同段出现 | `tellurion-agent/README.md:9-11` 对比 `:31` | 读者需读完两段才知道是“运行期 HTTP 依赖” |
| 空目录 `cmd/tmpdrill` | 目录存在但无文件（git 不跟踪） | 无功能影响，属工作区残留 |
| core 仍保留 `GET /health` 的 rate-limit 豁免测试 | `cmd/analysis/rate_limit_exempt_test.go:45` | 与 X-PROBE-NAMING 统一动作绑定，改名时需同步 |
| broker 有 `BROKER_CHANNEL=live` + 回环地址只 Warn | `pkg/brokerhttp/trader.go:79-84` | 有意设计（真实网关可能就在本机），但生产误配只留日志 |

---

## 4. 跨仓耦合的真实形态

- **零编译耦合**：在 7 个服务仓中检索 `"tellurion-<其他服务>/`，除本模块自身 import 外零命中；`go.mod` 无 `replace`，全工作区无 `go.work`（10 个 Go 仓逐一扫描）。
- **两个版本化底座**：所有服务 pin `contracts v0.10.0`（最新 tag 即 `v0.10.0`），除 broker 外均 pib `kit v0.5.0`（最新 tag 即 `v0.5.0`）；broker 只用 contracts。
- **运行期耦合集中在 6 条 URL**：`data_service.url`(8081)、`strategy_asset.resolve_url`(8090)、`risk_service.resolve_url`(8089)、`risk_service.events_url`、`ORCHESTRATION_URL`(8088)、`BROKER_URL`(8091)（`config/analysis-service.yaml:102-214`）。全部有“缺失即拒绝启动/503”的显式语义，无静默回退。
- **数据库耦合是最大的隐式耦合**：core 与 risk 共享 `risk` schema（已裁决）、core 与 data 共享 `ingest/quant`；跨仓表结构变更只能靠 `contracts` 与文档，没有 schema 级联校验。当前靠各仓 `db-schema.md` + 迁移纪律兜底，属可接受风险，但应当知道它不是“技术上强约束”。
- 证据强度：实测（go.mod/import/配置扫描）；“隐式耦合风险”为推断。

---

## 5. 实测 / 推断分界

| 结论 | 强度 |
|---|---|
| 六条主链闭合、装配 fail-closed | 实测（代码路径） |
| stockstate 未注册、约 1000 行不可达 | 实测 |
| 探针命名分叉、双默认值、`/api/v1` 过期 | 实测 |
| 12 个白名单死包、analytics 零调用 | 实测（护栏/文档 + 检索） |
| 版本 pin 统一 | 实测（go.mod + tag） |
| “调用方会踩 union 请求体坑” | 推断 |
| 跨仓数据库隐式耦合的风险量级 | 推断 |

---

## 6. 未覆盖与限制

- 未编译、未跑测试、未启动任何服务；因此“链路闭合”是**静态可达性**结论，不是运行期观测。
- 未做性能剖析（除源码中的超时/并发参数外，无实测数据）。
- 未深读 `pkg/backtest` 全部 2237 行撮合细节；对账/滑点/涨跌停等口径以既有测试与注释为证据，属抽样核验。
