---
status: decision-material
last-verified: 2026-11-13
verified-by: 2026-11-13 逐条实测复核（代码 / CI / 路由 / 文档），九条挂起项决策材料；未改任何代码与台账
scope: CORE-STOCKSTATE-DISPOSITION、CORE-BACKTEST-ENGINE-SPLIT、CORE-DEAD-PACKAGE-DISPOSITION、CORE-TEST-EVIDENCE-VERSIONED、BROKER-LIVE-LOOPBACK-GUARD、UI-INDUSTRY-ENTRY、UI-THEME-TOGGLE、X-CI-WINDOWS、AGENT-S2-HYPOTHESIS-SOURCE
---

# 九条挂起任务的决策材料（2026-11-13）

> **本文性质**：只做决策材料，不替主任拍板，不改任何代码与台账。每条的「推荐」是执行侧依据项目已确立的边界给出的建议，最终选择权在主任。
> **证据纪律**：本文所有事实均在 2026-11-13 重新实测（命令与落点见 §11），**不照抄台账旧描述**；本轮共发现 5 处台账描述已被现状推翻，集中在 §10。
> **口径约定**：「工作量」以**改动面**计（文件数 / 步骤数 / 是否新增契约），不给日历天数。

---

## 0. 决策速览

| # | 任务 | 实际归属仓 | 推荐 | 次选 | 一句话理由 |
|---|---|---|---|---|---|
| 1 | `CORE-STOCKSTATE-DISPOSITION` | tellurion（core） | **B 退役** | C 冻结保留 | 项目明确不做实盘（ROADMAP:105），停牌/退市/强平只在真实柜台下成立 |
| 2 | `CORE-BACKTEST-ENGINE-SPLIT` | tellurion（core） | **C 不做（维持登记）** | B 局部切分 | 撮合复杂度是领域复杂度不是行长；触发条件已写清 |
| 3 | `CORE-DEAD-PACKAGE-DISPOSITION` | tellurion（core） | **B 工具 9 包保留 + 交易三包退役** | A 全部保留并登记 | 三包无数据源、无 broker 面、不在任何阶段；保留会让白名单变永久豁免 |
| 4 | `CORE-TEST-EVIDENCE-VERSIONED` | tellurion（core） | **B CI artifact + 仓内摘要** | C 维持现状 | 摘要已入库，原始日志 33 个是 `*.log`，不该进仓 |
| 5 | `BROKER-LIVE-LOOPBACK-GUARD` | **tellurion（core），不是 broker 仓** | **A 维持 Warn + 成文** | B fail-closed | 真钱未开；`/version` 对拍已拦实质风险；单机自托管下同机网关合法 |
| 6 | `UI-INDUSTRY-ENTRY` | tellurion-ui | **B 当期仅 API，S2 出口后升级建页** | A 现在建只读页 | UI 是观察窗；产业链图的价值在因果工作流里，当前无消费场景 |
| 7 | `UI-THEME-TOGGLE` | tellurion-ui | **A 移除控件** | B 完整实现 | 深色是设计基线；半成品开关比没有更伤体验 |
| 8 | `X-CI-WINDOWS` | tellurion（core） | **C 交叉编译门（不加 runner）** | B 不做 | 生产代码 0 处 `runtime.GOOS`，风险只在编译期 |
| 9 | `AGENT-S2-HYPOTHESIS-SOURCE` | tellurion-agent | **C 维持挂起（等 S1 出口）** | B 先冻结形状 | S2 的定义就是它；但加列已解锁、可随时启动 |

---

## 1. `CORE-STOCKSTATE-DISPOSITION` · stockstate 能力去留

### 1.1 现状与证据（2026-11-13 实测）

| 事实 | 证据 |
|---|---|
| 包本体存在，455 行 + 测试 556 行 | `tellurion:pkg/trading/stockstate/stock_state.go`（455 行）、`stock_state_test.go`（556 行） |
| handler 定义 **6 条**路由 | `tellurion:cmd/analysis/handlers_stock_state.go:50-59`：`GET /list`、`GET/POST /scan`、`GET /:symbol`、`POST /:symbol/set`、`DELETE /:symbol`（共 6 条，注册在 `/api/stock-state` 组） |
| **全仓非测试代码零调用** | grep `NewStockStateRegistry` / `NewForcedLiquidator` 只命中定义处（`stock_state.go:159`、`:346`）与 handler 的字段/构造签名；`cmd/analysis/main.go` 无 `NewStockStateHandler` 调用 |
| 唯一"登记"是 repoguard 白名单 | `tellurion:internal/repoguard/handler_wiring_test.go:47` 的 `NewStockStateHandler` allowlist 条目，理由写明"等 `CORE-STOCKSTATE-DISPOSITION` 裁决" |
| 该能力属于**实盘交易域** | `stock_state.go:339-366` 的 `ForcedLiquidator` 绑定 `trading.LiveTrader`，语义是"退市整理期末期强制卖出持仓" |
| 项目明确不做实盘 | `tellurion-docs:docs/ROADMAP.md:105`："**明确不做 · 实盘交易** —— 真钱通道未开……唯一通道是 `tellurion-broker` 的 Mock 网关"；`tellurion-broker:docs/adr/0003-真钱通道暂不实施与重开条件.md` 已裁决真钱通道本阶段不实施 |

### 1.2 为什么挂住，前提还成立吗

- 当初挂住的前提是："交易安全是否属于当前阶段"——台账据此**建议 A 接线**，理由是"stockstate 位于下单前校验（风险域），价值高于 12 个白名单包"。
- **该前提已被推翻**：`ROADMAP.md:105` 把实盘交易列入"明确不做"，`broker ADR-0003` 把真钱通道定为"Mock + fail-closed 为当前终态"。停牌/退市/强平三类校验**只在真实柜台 + 真实持仓下才有执行路径**；在 Mock 通道下它们连输入都不存在（Mock 网关没有证券状态，数据服务也没有证券状态接口）。
- 因此今天的问题不是"要不要投入交易安全增强"，而是"**要不要保留一段永远不会被执行的实盘风控代码**"。

### 1.3 可选方案

**A · 接线（台账原建议）**
- 要改什么：`main.go` 装配 `StockStateRegistry` + `ForcedLiquidator`、注册 6 条路由、补 `openapi.yaml`、补调用点（下单前校验）与集成测试；还需回答"证券状态从哪来"（当前无数据源）。
- 工作量：中——core 1 仓 5~6 步，新增 openapi 条目、新增装配依赖，且要先补一条数据供给（要么接数据服务新端点，要么手工维护），**会引出新契约**。
- 风险：为一条不存在的路建收费站。装配后会让人以为"系统已在做停牌校验"，而实际状态源是空表；内存 registry 重启即失，运维侧会看到"状态突然全空"。
- 可逆性：中——路由/装配可撤，但一旦 openapi 与前端/文档引用了这 6 条，撤要连带改三处。
- 长期维护：一个无持久化、无数据源的状态表，每次评审都要重新解释它为什么在。

**B · 退役（删除 handler + 包 + 测试，加负向护栏）**
- 要改什么：删 `cmd/analysis/handlers_stock_state.go`、删 `pkg/trading/stockstate/`、把 `NewStockStateHandler` 从 handler 白名单移除、在 `package_wiring_test.go` 的 `retiredPackages` 加 `tellurion/pkg/trading/stockstate`（目录复活即红）、在台账/ADR 写重开条件（P1~P5 满足 + 立 X6c 时重建）。
- 工作量：小——core 1 仓 4 步，约 3 个文件改动 + 1 条护栏，无新契约。
- 风险：删掉 455 行含交易所状态机语义（listed/suspended/delisting/delisted 与合法迁移）的实现；但全部在 git 历史里，重开时可取回。
- 可逆性：高——单笔 revert 即可恢复；负向护栏随 revert 一并消失。
- 长期维护：零。

**C · 冻结保留（不接线，白名单写归属与重开条件）**
- 要改什么：`handler_wiring_test.go` 的 allowlist 条目补"owner / 性质 / 重开条件"三行；不注册路由、不进 openapi。
- 工作量：小——1 个注释块。
- 风险：死代码继续参与编译与阅读；`go test ./pkg/trading/...` 仍要维护这 556 行测试。
- 可逆性：高。
- 长期维护：每次白名单评审都要解释一次，且它和 12 个死包混在一起，稀释"白名单=待接线的债"这个语义。

**D · 不做（维持 ⏸）**
- 工作量：零。
- 风险：台账长期挂 ⏸，读者无法判断"系统到底有没有停牌校验"。
- 可逆性：不适用。
- 长期维护：一个永久 ⏸ 项。

### 1.4 推荐：B 退役

理由贴着项目边界，不贴"最佳实践"：

1. `ROADMAP.md:105` 与 broker `ADR-0003` 已把实盘交易/真钱通道定为**当前阶段不做**，而 stockstate 的全部语义绑定 `LiveTrader`（`stock_state.go:366`）。接线等于在"明确不做"的领域里新增一条运行路径。
2. 台账原建议 A 的依据是"价值高于 12 个白名单包"，但价值判断的前提是"有执行机会"。当前没有真实柜台，价值无法兑现；保留反而制造"能力已可用"的假信号，与 `PRODUCT.md` 刚建立的能力状态口径（"后端可用 / UI 入口 ⬜"式诚实标注）冲突。
3. 重开路径已经存在且写死（broker ADR-0003 的 P1~P5 + X6c），删除不会抹掉"将来要做"的可能性；重建成本远低于长期维护一段假能力的成本。

### 1.5 选了之后的动作清单（B）

1. `tellurion`：删 `cmd/analysis/handlers_stock_state.go` 与 `pkg/trading/stockstate/`（含测试）。
2. `tellurion`：`internal/repoguard/package_wiring_test.go` 的 `retiredPackages` 加一条负断言（"实盘证券状态校验随实盘通道一并退役；重开见 broker ADR-0003"）。
3. `tellurion`：`internal/repoguard/handler_wiring_test.go` 删除 `NewStockStateHandler` 白名单条目（否则护栏会报"白名单陈旧"）。
4. `tellurion`：台账 `CORE-STOCKSTATE-DISPOSITION` 标 ✅ + 原文与施工记录移入归档；重开条件指向 broker ADR-0003。
5. 不需要新契约、不需要前端配套（UI 从未引用 `/api/stock-state`）。

### 1.6 不选的后果（维持现状一年）

core 里会长期同时存在两条"看起来能交易"的代码路径：`pkg/trading/*` 与 broker 仓；`PRODUCT`/`REPO-MAP` 无法诚实回答"是否支持停牌校验"。新成员按 handler 去写前端或接线，评审时再次争论同一件事；repoguard 白名单则从"待接线的债"退化成"永久豁免清单"。

---

## 2. `CORE-BACKTEST-ENGINE-SPLIT` · 回测引擎超大文件切分

### 2.1 现状与证据

| 事实 | 证据 |
|---|---|
| `engine.go` 2237 行 / 83 个顶层函数 | `tellurion:pkg/backtest/engine.go`（`^func ` 计数 83） |
| `engine_daily.go` 1128 行 / 20 个顶层函数 | `tellurion:pkg/backtest/engine_daily.go` |
| 测试密度很高 | `pkg/backtest` 下 **66** 个 `*_test.go` |
| 性能基准已存在 | `pkg/backtest/engine_bench_test.go:196` `BenchmarkBacktest`（5 股 1 年） |
| 无进行中的撮合语义变更 | 本轮未发现待实施的撮合/交易所口径工单；S3 才涉及新数据源与相关性检查 |

### 2.2 为什么挂住，前提还成立吗

- 台账把它登记为"**登记不实施**"，重开条件 = "下一次需要同时改 `engine.go` 与 `engine_daily.go` 的撮合/日频语义，或新增交易所口径"。
- **前提仍成立**：当前没有驱动变更。原审查的判据是"局部改动的影响面难以静态评估"，这是**可读性/评审成本**问题，不是正确性缺陷；66 个测试已把行为面钉住。

### 2.3 可选方案

**A · 全量按职责切分（纯撮合 / 日频编排 / 数据访问）**
- 要改什么：先补 characterization tests，再拆 3~5 个文件；禁止纯格式化搬迁。
- 工作量：大——core 1 仓，涉及 3300+ 行重组与全量测试回归；无新契约。
- 风险：撮合核心的 diff 噪声极大，评审很难看清"是否只是搬家"；一次搬家式改动就可能埋下仓位/滑点口径漂移。
- 可逆性：中——纯搬迁可 revert，但若顺带"顺手修"则不可干净撤回。
- 长期维护：切分后边界需要新的约定（哪个文件放什么），否则会再次长回去。

**B · 局部切分（只抽数据访问与纯函数，不碰撮合状态机）**
- 要改什么：把 store/loader/日历适配等副作用从 `engine.go` 抽出，目标减 300~500 行。
- 工作量：中——core 1 仓 2~3 步。
- 风险：仍需大量回归；收益有限（撮合主体仍在 1700+ 行文件里）。
- 可逆性：高（纯搬迁）。
- 长期维护：多一个文件边界。

**C · 不做，维持登记（推荐）**
- 要改什么：无代码改动；台账保持 ⏸ 与既有重开条件。
- 工作量：零。
- 风险：无新增风险；既有"影响面难评估"的问题继续存在。
- 可逆性：不适用。
- 长期维护：零；等触发条件出现时再做。

**D · 立即做到"每个文件 < 800 行"（配额式切分）**
- 要改什么：按行数硬切。
- 工作量：大。
- 风险：按行数切会切断内聚边界（撮合与日频编排强耦合），是典型的"为指标而切"。
- 可逆性：中。
- 长期维护：边界不自然，后续改动会在两个文件间来回跳。

### 2.4 推荐：C 不做（维持登记）

1. 本项目对回测的核心要求是**数字可信**（S0 出口"让现有回测数字可信"），不是文件行数；切分不改变任何可信度。
2. 触发条件已经写得可判定（"同时改撮合/日频语义"或"新增交易所口径"）。在没有触发条件时切分，属于"为切分而切分"，台账 `④ 约束与非目标` 已明确禁止。
3. 66 个测试 + 基准已提供回归护栏；真到需要切分时，这些测试正好是 characterization 的基础，现在做等于提前支付成本。

### 2.5 选了之后的动作清单（C）

- 无代码动作。台账保持 ⏸；建议在台账补一句"现状实测：engine.go 2237 行 / 83 函数、engine_daily.go 1128 行 / 20 函数、66 个测试文件"，让下一次评审不必重新数。

### 2.6 不选的后果（维持现状一年）

如果一年内出现了"同时改撮合与日频"的需求，改动仍落在 2237 行文件里，评审成本高——但这是**已知且有测试兜底**的成本。反之若现在切分，一年内每一次撮合改动都要跨 3~5 个文件读上下文，是确定的长期成本换取不确定的收益。

---

## 3. `CORE-DEAD-PACKAGE-DISPOSITION` · 12 个白名单死包逐包归属

### 3.1 现状与证据

`tellurion:internal/repoguard/package_wiring_test.go:74-99` 的白名单共 **12** 条：

| 包 | 性质 | 生产导入者（实测） |
|---|---|---|
| `pkg/api` | 工具（API 版本化中间件） | 0 |
| `pkg/backtest/auction` | **交易能力**（集合竞价撮合） | 0 |
| `pkg/alert/systemalert` | 工具（系统级运维告警） | 0 |
| `pkg/trading/margin` | **交易能力**（两融） | 0 |
| `pkg/strategy/options` | **交易能力**（期权策略） | 0 |
| `pkg/testutil` | 工具（DB 集成测试底座） | 0 |
| `pkg/id` | 工具（ULID） | 0 |
| `pkg/sandbox/runner` | 工具（copilot 构建沙箱） | 0 |
| `pkg/sandbox/staticcheck` | 工具（LLM 代码校验） | 0 |
| `pkg/strategy/monitor` | 工具（策略健康监测） | 0 |
| `pkg/mining` | 工具（挖掘流水线） | 0（生产入口 `cmd/data` 已退役） |
| `pkg/sync` | 工具（同步作业队列） | 0（同上） |

补充实测：

- 交易三包体量：`auction` 2 文件 / 687 行；`options` 7 文件 / 1316 行；`margin` 4 文件 / 2280 行。
- **对照组 `pkg/trading/reconciliation` 不在白名单**，因为它有真实导入者：`cmd/analysis/handlers_reconciliation.go:12`、`cmd/analysis/main.go:21`、`pkg/alert/reconcile.go:21`。这说明"死包清单"与"活包"的边界是可靠的，不是笼统的"core 里有些没用的东西"。
- 文档现状：`ROADMAP.md` 仅在 S3 出口提到"回测 universe 含退市标的"（幸存者偏差，属数据/回测口径），**没有任何阶段提到期权、两融、集合竞价**；`ROADMAP.md:107` 明确"日频已是高频边界"，集合竞价是盘中语义。

### 3.2 为什么挂住，前提还成立吗

- 挂住的唯一前提：**交易三包（期权/两融/集合竞价）是否退役需主任确认**。
- 现在有了新证据：三者均不在任何阶段目标里；无期权/两融数据源（L1 数据层只有行情/财务/产业链/研究/实验日志）；broker 无融资融券 HTTP 面（归档记录已写明）；日频边界排除集合竞价撮合。**前提不仅成立，而且指向更明确**。

### 3.3 可选方案

**A · 12 包全部保留 + 产出归属表**
- 要改什么：只写表（包/性质/owner/去留/重开条件），写进 repoguard 注释或 `ARCHITECTURE.md`；强调"交易三包暂不暴露"。
- 工作量：小——0 代码改动，1 份文档。
- 风险：白名单 12 条继续混装"未来会用"与"永远不会用"；下一次评审还要重新判断。
- 可逆性：高（只改文档）。
- 长期维护：每次新增死包都要在这张表里解释。

**B · 工具 9 包保留（写理由）+ 交易三包退役（推荐）**
- 要改什么：删 `pkg/backtest/auction`（687 行）、`pkg/strategy/options`（1316 行）、`pkg/trading/margin`（2280 行）及其测试；白名单 12 → 9；`retiredPackages` 加 3 条负断言；9 包逐条写"保留理由 + 重开条件"。
- 工作量：中——core 1 仓 5 步（3 次删除 + 白名单/负断言 + 文档表），无新契约。
- 风险：删掉 4283 行含期权定价（BS/二叉树）、两融规则、集合竞价撮合的实现；这些是**领域知识**，重写成本高于从 git 取回。
- 可逆性：高——单笔 revert；负断言随 revert 消失。
- 长期维护：9 条白名单有明确理由，评审成本下降。

**C · 12 包全量退役（含 id / mining / sync / sandbox runner 等）**
- 要改什么：删 12 个包。
- 工作量：大——12 个包 + 各自测试 + 白名单重写。
- 风险：`pkg/mining` / `pkg/sync` 是数据服务重建时的候选实现（`package_wiring_test.go:94-99` 已写明"等待新执行入口接线"）；`pkg/id` 是订单域重建的候选；删掉它们等于把"将来要做"的实现也清空。与"不要写成永久不做"的既有口径冲突。
- 可逆性：中（删除量大，revert 冲突风险高）。
- 长期维护：零，但未来重建成本全部转为新增工作量。

**D · 不做（白名单注释继续充当登记）**
- 工作量：零。
- 风险：同上 A，且更弱——连表都没有。
- 可逆性：不适用。
- 长期维护：护栏的语义持续被稀释。

### 3.4 推荐：B（工具 9 包保留 + 交易三包退役）

1. 判据不是"有没有用"，而是"**是否在项目已声明的边界内**"：实盘不做、日频为边界、无期权/两融数据源、broker 无两融面。三条边界同时成立，三包在可预见阶段都没有接线路径。
2. 工具 9 包各自有明确的"未来用途 + 触发点"（api 版本化、systemalert 运维链路、testutil 集成底座、id 订单域、runner/staticcheck/monitor 随 AI 拆仓、mining/sync 待数据服务重建）。这些是**有路径的债**，与三包的"无路径"性质不同，应区别对待。
3. 保留三包会让 repoguard 白名单从"待接线的债"变成"永久豁免"，与护栏设计意图（每一条都是"we are keeping this on purpose, and here is what would wire it"）相反。
4. 争点只有一个：`auction` 的开盘价撮合精度。但当前引擎按日频建模，竞价时段不在口径内；若主任认为 S3 需要更真实的开盘成交，可单独保留 `auction`，其余两包退役。

### 3.5 选了之后的动作清单（B）

1. `tellurion`：删 `pkg/backtest/auction/`、`pkg/strategy/options/`、`pkg/trading/margin/`。
2. `tellurion`：`internal/repoguard/package_wiring_test.go` 白名单删 3 条（12 → 9）。
3. `tellurion`：`retiredPackages` 加 3 条负断言（目录复活即红），理由引用 ROADMAP 边界。
4. `tellurion`：`ARCHITECTURE.md` 或 repoguard 注释补 9 包归属表（性质/owner/重开条件）。
5. `tellurion`：台账标 ✅，原文移入归档。
6. 无新契约、无前端配套（UI 从未引用这三包）。

### 3.6 不选的后果（维持现状一年）

一年后，12 条白名单里 9 条有未来路径、3 条没有任何路径，但它们在同一个 map 里、同一种注释格式下。每次有人问"系统支持两融吗"，答案只能靠读代码；而 `margin` 的 2280 行会让答案看起来像"支持，只是没接线"。这是文档与代码一致性审查里最难修的一类漂移。

---

## 4. `CORE-TEST-EVIDENCE-VERSIONED` · 测试证据进入版本控制或 CI artifact

### 4.1 现状与证据

| 事实 | 证据 |
|---|---|
| `reports/` 共 42 个文件 | `Get-ChildItem reports -Recurse -File` 计数 42 |
| **只有 1 个被 git 跟踪** | `git ls-files reports` → `reports/test-2026-11-13/summary.md` |
| 8 个 untracked | `git status --porcelain -uall -- reports` 8 条（含 `baseline.dump` 199.8 KB、`dualrun.md` 40.1 KB） |
| 33 个 `*.log` 被忽略 | `.gitignore:20 *.log` |
| CI 已有 artifact 先例，但只传 dualrun | `tellurion:.github/workflows/ci.yml:375-377`（`actions/upload-artifact@v4`，`name: dualrun-reports`） |
| 测试/覆盖率日志未上传 | 同一 workflow 中 `upload-artifact` 仅命中 1 处（`:375`）；`:156` 的 `go test ./... -count=1 -race -coverprofile=coverage.out` 未上传 |
| 覆盖率门已落地 | `ci.yml:147` 注释：`CORE-COVERAGE-FLOOR（2026-11-13）已按新基线抬到 67/77` |

### 4.2 为什么挂住，前提还成立吗

- 台账原文：`reports/` 在 core 为 **0 tracked 文件**，全栈验收证据写在仓外与 untracked `reports/`。
- **前提已部分改变**：`summary.md` 已经入库（蒸馏结论 + 波次计数 + 阻塞原因），但**原始日志仍不在任何可追溯位置**（33 个 log 被 ignore，8 个 json/dump untracked）。所以问题从"证据完全没有版本控制"收窄为"结论有、证据没有"。

### 4.3 可选方案

**A · 全量提交 `reports/`**
- 要改什么：解除 ignore、提交 42 个文件（含 199.8 KB 二进制 dump）。
- 工作量：小——1 次提交。
- 风险：仓库体积与噪声；二进制 dump 会随历史永久留存；违反台账既有约束"不提交大文件/二进制"。
- 可逆性：低——`git rm` 只能删工作区，历史里的 blob 仍在（需 rewrite history 才能真删）。
- 长期维护：每次跑测试都可能产生新的 dump/log，需要人工筛选。

**B · CI artifact + 仓内摘要（推荐）**
- 要改什么：`ci.yml` 的 test job 增加 `upload-artifact`（`coverage.out` + `go test` 日志，retention 建议 30 天，与 dualrun 先例同款）；仓内只保留 `reports/<date>/summary.md` 与一条"证据在哪"的链接约定（run id / artifact 名）。
- 工作量：小——core 1 仓 3 步，无新契约。
- 风险：artifact 有过期时间（默认 90 天可配），不能当作永久档案；但永久档案本来就该是 summary。
- 可逆性：高（删 workflow 步骤即可）。
- 长期维护：artifact 命名与 retention 的约定；summary 的写法已有先例。

**C · 维持现状（摘要入库，原始日志靠本地）**
- 工作量：零。
- 风险：换机器/清理后无法复核"218 passed / 0 failed"是不是真跑出来的；flaky 用例的当日日志不可追溯。
- 可逆性：不适用。
- 长期维护：零，但每次审查都要重新跑一遍取证。

**D · 把 `reports/` 整体迁到独立证据仓 / 对象存储**
- 要改什么：新建仓或存储桶、写上传脚本、改文档链接。
- 工作量：大——跨仓 + 凭证管理。
- 风险：为一个单人自托管项目引入第二套存储与鉴权面。
- 可逆性：中。
- 长期维护：新仓的生命周期、权限、清理策略。

### 4.4 推荐：B（CI artifact + 仓内摘要）

1. 与既有先例一致：dualrun 报告已经用 artifact 上传（`ci.yml:373-379`），测试证据沿用同一模式，不引入新机制。
2. `summary.md` 已证明"仓内摘要"可行，且它正是审查与验收真正需要读的东西；原始日志是**一次性证据**，放进 artifact 足够。
3. 台账 `④ 约束与非目标` 已写明"不提交大文件/二进制"，A 与 D 都越过这条线。

### 4.5 选了之后的动作清单（B）

1. `tellurion`：`ci.yml` test job 增加 artifact 上传（`coverage.out` + 测试输出），设置 retention。
2. `tellurion`：`reports/test-2026-11-13/summary.md` 补一节"证据位置"，写明 artifact 名与 run 链接的填法。
3. `tellurion`：台账标 ✅，原文移入归档。
4. 不需要新契约、不需要前端配套。

### 4.6 不选的后果（维持现状一年）

半年后回看"W5 218 passed / 0 failed"，只能相信 `summary.md` 的自述；无法回答"当时 7 条失败具体是哪 7 条、怎么修的"。对新加入者，这等于要求他重新跑一遍全栈测试才能建立信任——而全栈测试的执行成本正是当初把日志写到仓外的原因。

---

## 5. `BROKER-LIVE-LOOPBACK-GUARD` · `BROKER_CHANNEL=live` + 回环地址的告警级别

### 5.1 现状与证据

| 事实 | 证据 |
|---|---|
| **实现不在 broker 仓，在 core** | `tellurion:pkg/brokerhttp/trader.go:66-91` 的 `resolveChannel`；broker 仓 grep `loopback` 只命中 `cmd/brokergateway/main.go:101` 的一条注释 |
| live + loopback 当前只 Warn | `trader.go:78-85`：`logger.Warn().Str("channel", ChannelLive)...Msg("BROKER_CHANNEL=live but BROKER_URL is loopback — verify ...")` |
| 注释明确"不拦截" | `trader.go:93`：`// isLoopbackHost 判断主机名是否回环（仅用于 live 通道的告警，不做拦截）` |
| 同函数对 mock 已 fail-closed | `trader.go:69-72`：`mock` 必须同时给 `BROKER_ALLOW_MOCK=true` |
| 构造期已有通道对拍 | `trader.go` 的 `verifyPeerChannel` 读对端 `/version.channel`，不一致/不可达/无字段一律拒绝启动；`deploy/README.md:22` 写明"`BROKER_CHANNEL=live` **且**对端 `/version` 自报 `live`，否则 analysis-service 拒绝启动" |
| 项目不做实盘 | `ROADMAP.md:105`；`tellurion-broker:docs/adr/0003` 已裁决真钱通道本阶段不实施 |
| 单机自托管是既定形态 | `ROADMAP.md:109`："SaaS / 多租户 — 单人自托管" |

### 5.2 为什么挂住，前提还成立吗

- 台账理由是"生产误配的代价 vs 本地联调便利"，并**建议 B fail-closed**。
- 新证据把天平推向 A：
  1. 真钱通道未开（ADR-0003），当前 `live` 声明本身就没有真实对端；真正的误配（把 mock 网关当 live）已被 `/version` 对拍拦下（`deploy/README.md:22` 已把它写成 fail-closed）。
  2. 剩下唯一能通过全部闸门的场景是"**同机部署、自报 live 的网关**"——在单人自托管形态下这是合法部署，B 会逼用户加一个只为绕过 guard 的键，等于把闸门变成仪式。
- 前提因此从"要不要 fail-closed"变成"**这条 Warn 是否已经足够，以及是否需要成文**"。

### 5.3 可选方案

**A · 维持 Warn + 成文 + 可观测（推荐）**
- 要改什么：`docs/live-trading.md` 或 `runbook.md` 增一节"live + loopback 的合法与非法场景"；启动日志保留 Warn 并补结构化字段（`channel` / `url` / `reason`）；台账写"有意设计"。
- 工作量：小——1 份文档 + 1 条日志字段（可选），无新契约。
- 风险：误配时只有一行 Warn，可能被日志淹没；靠文档与 runbook 兜底。
- 可逆性：高。
- 长期维护：一节文档 + 一次 runbook 更新。

**B · fail-closed + `BROKER_ALLOW_LOOPBACK_LIVE=true` 显式放行**
- 要改什么：`resolveChannel` 的 live 分支改为返回错误（无放行键时）；新增环境键；补 4 条用例（拒绝/放行/大小写/空值）；`deploy/README.md` 与 runbook 补配置说明。
- 工作量：中——core 1 仓 3 步（代码 + 用例 + 文档），新增 1 个配置键。
- 风险：单机自托管部署多一个必填键；与台账 `④` "不新增配置前缀体系"有张力；对"同机真实网关"这一合法形态产生误伤。
- 可逆性：高（改回 Warn 即恢复）。
- 长期维护：一个只为放行而存在的键，以及它与 `BROKER_ALLOW_MOCK` 的语义区别要长期解释。

**C · 维持现状，不成文（不做）**
- 工作量：零。
- 风险：同 A 的误配风险，但没有文档兜底；下次审查还会重新提。
- 可逆性：不适用。
- 长期维护：零。

**D · 把 live + loopback 直接判为配置错误（不提供放行键）**
- 要改什么：同 B，但不加放行键。
- 工作量：小。
- 风险：同机真实网关部署被彻底堵死，且与"单人自托管"形态直接冲突；一旦将来真钱通道落在本机，必须再改一次。
- 可逆性：高。
- 长期维护：将来必然要重开。

### 5.4 推荐：A（维持 Warn + 成文）

1. 当前阶段的实质风险（误把 mock 当 live）已由 `/version` 对拍覆盖，B 增加的是"地址形态"这一层的重复保险。
2. 项目形态是单人自托管，真实网关落在同一台机器是合理布局；B/D 都会与这一形态冲突。
3. 台账 `④` 明确"不新增配置前缀体系"，B 的新键正是它要避免的那类扩张。
4. 保留 Warn 并在 runbook 写清"什么情况下 live+loopback 是合法的、什么情况下必须停"，比再加一道闸更符合"当前阶段不做实盘"的定位。

> **归属纠偏（重要）**：本条的实现落点在 **core** `pkg/brokerhttp/trader.go`，broker 仓没有等价代码（只有一条注释）。无论选哪个方案，台账应从 broker 仓迁到 core 仓，或在 broker 台账改成指针，避免施工时改错仓。

### 5.5 选了之后的动作清单（A）

1. `tellurion`：`docs/live-trading.md`（或 `runbook.md`）补一节"live + loopback 的判定与处置"，写明"同机真实网关合法 / mock 网关必须用 mock 声明 / 声明与对端不符由 `/version` 拒绝启动"。
2. `tellurion`：启动 Warn 补 `reason=loopback_gateway` 一类结构化字段（可选，1 行）。
3. 台账：core 立单并收口；broker 仓台账改为"实现不在本仓"的指针。
4. 无新契约、无前端配套。

### 5.6 不选的后果（维持现状一年）

若选 B，一年后每台单机部署都带一个"放行键"，新加入者会问"为什么 live 还要额外放行"；若维持现状且不成文，下一次误配时只有一行 Warn，事故复盘找不到"这是有意设计"的依据，审查报告会第二次提同一条。

---

## 6. `UI-INDUSTRY-ENTRY` · 产业链/宏观产品入口

### 6.1 现状与证据

| 事实 | 证据 |
|---|---|
| 后端 5 条端点已实现并注册 | 4 条行业：`tellurion:cmd/analysis/handlers_industry.go:71-77`（tree / edges / vitality / etf/:code/constituents），注册于 `cmd/analysis/main.go:495`；1 条宏观：`handlers_macro.go:77`（`/macro/series`），注册于 `main.go:501` |
| UI 零命中 | `tellurion-ui:web/src` 搜 `industry`、`macro`、`产业链` 无业务代码命中（仅设计稿 `docs/design/stitch_quantlab_ux_redesign/macro/code.html`） |
| UI 当前 15 条业务路由 | `web/src/router/index.ts`（`name:` 计数 17，去掉 `login` / `not-found`）：dashboard / backtest / backtest-compare / walkforward / paper-trading / screener / strategy-lab / explore / review / data-sync / alerts / compliance / system-admin / evidence / factors；`web/src/pages` 共 20 个 `.vue` |
| PRODUCT 口径**已改** | `PRODUCT.md:72`："产业链查询（后端 ✅ / UI 入口 ⬜）"；`:81`："产业链查询：后端可用，UI 无入口……性质 = 能力已具备、未暴露" |
| ROADMAP 的 S2 出口 | `ROADMAP.md:40` S2 = 加解释（底座 ✅ / `hypothesis_source` ⬜）；`:80` 出口 = "至少 1 个从产业链假设出发的因子完成完整验证并带因果来源" |
| 设计稿已标注 | `docs/design/stitch_quantlab_ux_redesign/ANNOTATIONS.md:272-281`：目标路由 `/research`，5 条数据端点全部 ✅，属 F18 P2；同文件把"HMM/GARCH 模型栈"标为虚构 |

### 6.2 为什么挂住，前提还成立吗

- 台账原前提是"`PRODUCT.md` L2 承诺产业链查询、UI 无任何入口"，即**承诺写高了**。
- **该前提已消解**：`PRODUCT.md:72/81` 已把能力状态显式标注为"后端 ✅ / UI 入口 ⬜"。现在的问题不再是"文档骗人"，而是纯粹的"**要不要建这个页面**"。
- 需要区分：这是"能力已具备但没暴露"，不是"缺功能"，也不该按"旧设计稿有 macro 页"就当成既定承诺硬补。

### 6.3 可选方案

**A · 现在建只读「产业链」页（读 5 条端点）**
- 要改什么：`ui` 新增 1 个页面 + 1 条路由 + 1 个 api 模块；行业树 / 供应链边 / 活力 / ETF 成分 / 宏观序列 5 个视图；空态/错态/断 core 态；组件测试 + 视觉基线。
- 工作量：大——ui 1 仓 6~8 步，新增页面与图表，无新契约（后端已就绪）。
- 风险：当前 S1 未出口、S2 未开始，页面没有进入任何用户工作流（审阅台/探索观察台都不消费它），大概率成为"第二个数据浏览页"；设计稿中的模型栈已被标注为虚构，照搬会引入假能力。
- 可逆性：高（删路由与页面即回退）。
- 长期维护：5 个视图的空态、错误态、视觉基线，以及"为什么有这个页面"的解释。

**B · 当期明确仅 API，写死升级条件（推荐）**
- 要改什么：`ui` 的 `ARCHITECTURE.md §3.1` 或 README 补一句"产业链/宏观暂无 UI，消费方为 API；建页触发条件见 TASKS"；`REPO-MAP.md` 已由 DOC-28 回写，无需再改；`PRODUCT.md` 已改（DOC-25），无需再改。
- 工作量：小——0 代码，1 份 ui 文档。
- 风险：能力继续"藏在 API 里"；但 PRODUCT/ROADMAP 已诚实标注。
- 可逆性：高。
- 长期维护：一句文档 + 一个触发条件。

**C · 不做（不改任何东西）**
- 工作量：零。
- 风险：`PRODUCT`/`ROADMAP` 已诚实，所以不会骗人；但"何时建页"没有判据，S2 出口时会重新争论。
- 可逆性：不适用。
- 长期维护：零。

**D · 最小页：只做行业树 + 宏观序列两图**
- 要改什么：1 页 2 图 + 1 条路由。
- 工作量：中——ui 1 仓 3~4 步。
- 风险：仍然没有工作流消费；且"最小"会留下后续 3 个视图的悬空承诺。
- 可逆性：高。
- 长期维护：同 A 的一部分。

### 6.4 推荐：B（当期仅 API，S2 出口后升级为 A）

1. 项目定位是"观察窗"：UI 的页面都绑定一个用户动作（回测、审阅、叫停、采纳）。产业链图的正解在设计稿里也是"图谱→因子→回测"的链路（`ANNOTATIONS.md:274`），而这条链路的终点是 S2 的"从产业链假设出发的因子"。当前该链路不存在，页面没有消费场景。
2. S2 出口判据（`ROADMAP.md:80`）是"至少 1 个带因果来源的因子"，不是"有产业链页面"。把 UI 提前到 S1 会打乱阶段顺序，且与"不为消掉问题发明需求"的纪律冲突。
3. 文档口径已经诚实（`PRODUCT.md:72/81`），不需要用页面去补承诺。
4. 升级条件写死：**S2 出口达成后**（至少 1 个行业假设因子完成验证并带 `hypothesis_source`），按 A 建页，届时页面有真实的因果解释工作流。

### 6.5 选了之后的动作清单（B）

1. `tellurion-ui`：`docs/ARCHITECTURE.md`（页面登记节）或 README 补一句"产业链/宏观仅 API，建页触发条件 = S2 出口"。
2. `tellurion-ui`：`docs/TASKS.md` 的 `UI-INDUSTRY-ENTRY` 标为"已裁决 B（当期仅 API）"，并保留 A 的升级条件；不需要归档（它不是 ✅ 完成，而是按 B 收口）。
3. `tellurion-docs`：无需改动（`PRODUCT.md` / `ROADMAP.md` 已在 DOC-25 回写）。
4. 无新契约、无后端改动。

### 6.6 不选的后果（维持现状一年）

若现在选 A：一年后大概率是一个访问量接近 0 的只读页，维护成本（视觉基线、空态、错误态）持续存在；更糟的是它会让 `PRODUCT` 的"UI 入口 ⬜"变成"已建但没人用"，能力状态再次失真。若选 C（什么都不写）：S2 出口时没人记得"为什么当时没建"，讨论从零开始。

---

## 7. `UI-THEME-TOGGLE` · 主题切换死控件

### 7.1 现状与证据

| 事实 | 证据 |
|---|---|
| 按钮存在且可点击 | `tellurion-ui:web/src/components/layout/AppHeader.vue:73-80`（`n-tooltip` + `n-button @click="toggleTheme"`） |
| 点击只弹提示 | `AppHeader.vue:148`：`function toggleTheme() { message.info('主题切换功能开发中') }` |
| 全局主题是**硬编码深色** | `web/src/App.vue:3` `:theme="darkTheme"`；`:18` 从 naive-ui 导入 `darkTheme`；`:32` `themeOverrides` 只针对深色做对比度 |
| 只有一套深色 token | `web/src/styles/variables.css` 的 `--q-*` 变量为深色设计（如 `--q-border-light: #2a3449`、`--q-primary-dark: #2563eb`） |
| 图表配色也绑定深色 | `web/src/styles/palette.ts:6` 注释：Chart.js 与 naive 的 themeOverrides 都吃不了 CSS 变量，颜色在两处共用 |
| 设计文档把主题切换列为 Header 组成 | `docs/design/components.md:66/77` |

### 7.2 为什么挂住，前提还成立吗

- 挂住的是"移除 vs 实现"这一对，没有外部前提。**前提仍成立**：工程里确实没有主题系统，只有一套深色 token。

### 7.3 可选方案

**A · 移除控件（推荐）**
- 要改什么：删 `AppHeader.vue` 的 `n-button`（`:73-80`）与 `toggleTheme`（`:148`），清理不再使用的 `MoonOutline` 导入；跑视觉基线/组件测试。
- 工作量：小——ui 1 仓 2 步，2 处代码 + 1 处 import。
- 风险：少一个"看起来有"的功能入口；对深色主线的用户无实际损失。
- 可逆性：高（单笔 revert）。
- 长期维护：零。

**B · 实现完整主题切换**
- 要改什么：一套 light token（`variables.css` 双套或 CSS 变量作用域切换）、`App.vue` 动态 `theme`（`darkTheme` / `null`）+ 持久化（localStorage）、`palette.ts` 双套图表配色、对比度校验、视觉基线双跑、e2e 双主题。
- 工作量：大——ui 1 仓 8~10 步，无新契约。
- 风险：深色是设计基线（DESIGN.md / variables.css / palette 都只按深色调过对比度），补浅色等于重做一次设计验收；且 Chart.js 配色需要逐图检查。
- 可逆性：中（涉及全局 provider 与持久化，回退要连带清 localStorage 语义）。
- 长期维护：两套 token、两套图表配色、双份视觉基线。

**C · 不做（保留"开发中"提示）**
- 工作量：零。
- 风险：可见的死控件每次点击都提示"未完成"，对完成度的伤害大于缺失本身；审查已判定为产品面缺陷。
- 可逆性：不适用。
- 长期维护：零，但缺陷长期存在。

**D · 只切 naive-ui 主题、不切自定义 CSS 与图表**
- 要改什么：`App.vue` provider 动态 theme + 持久化。
- 工作量：中——ui 1 仓 3 步。
- 风险：naive 组件变浅、页面背景/自定义卡片/图表仍深色，出现"半张脸"；这是比没有更差的中间态（台账 `④` 已明确禁止"只有开关、没有主题的中间态"）。
- 可逆性：高。
- 长期维护：一个永远不完整的主题系统。

### 7.4 推荐：A（移除控件）

1. UI 的核心价值是"观察窗"，主题不服务任何观察任务；深色是唯一被设计验收过的基线。
2. 台账 `④` 已明确"不做只有开关、没有主题的中间态"，而完整实现（B）需要重做 token 与图表配色，收益与成本不成比例。
3. "点击后告诉我功能开发中"是**可见的未完成承诺**，比没有按钮更伤体验；移除是唯一零成本消除缺陷的做法。

### 7.5 选了之后的动作清单（A）

1. `tellurion-ui`：删 `AppHeader.vue:73-80` 的按钮块与 `:148` 的 `toggleTheme`，清理 `MoonOutline`。
2. `tellurion-ui`：若有 Header 组件测试或视觉基线引用该按钮，同步更新；跑一次视觉基线确认无差异。
3. 台账 `UI-THEME-TOGGLE` 标 ✅ 并归档。
4. 无新契约、无后端改动。

### 7.6 不选的后果（维持现状一年）

每个新用户都会点一次，看到"主题切换功能开发中"，对产品完成度打一次折；若某天有人真去实现，会先发现需要重做一套浅色 token 与图表配色——成本远高于当初评估的"加个开关"。

---

## 8. `X-CI-WINDOWS` · Windows runner 是否纳入 CI

### 8.1 现状与证据

| 事实 | 证据 |
|---|---|
| 12 仓 CI 全部只跑 Ubuntu | 逐仓 `.github/workflows/ci.yml` grep `runs-on`：**全部 `ubuntu-latest`**，无 `windows-*` / matrix |
| **生产代码 0 处 Windows 分支** | 全工作区 `runtime.GOOS` 命中 9 处，**全部在 `_test.go`**：core `internal/orchestrationworker/wire_e2e_test.go:297`、`internal/httpapi/sensitivity_e2e_test.go:135`；agent `pkg/sandbox/runner/runner_test.go:209/510`、`cmd/compiler/main_test.go:126`、`internal/compile/compile_test.go:30` 等 |
| 核心测试的权威覆盖在 CI | `ci.yml:156-157` 在 ubuntu 跑 `-race -coverprofile` + `coveragegate`；本机 Windows 无 gcc 时 `-race` 腿记为 BLOCKED（`reports/test-2026-11-13/summary.md:34-38`） |
| 开发机是 Windows | 同上 summary 的 B1：本机 Windows 宿主无 gcc/cc |

### 8.2 为什么挂住，前提还成立吗

- 台账前提："存在 Windows 专属分支（路径分隔符、进程管理）但无 runner 验证"。
- **该前提已被实测推翻**：生产代码没有任何 `runtime.GOOS` 分支；9 处全部是测试内的跳过逻辑（例如本地无 gcc 时跳过 `-race`、Windows 下调整路径）。开发机本身就是 Windows，运行时差异在开发机第一跑就会暴露。

### 8.3 可选方案

**A · core 加 `windows-latest` job（build + vet + 单测，不跑 DB/race）**
- 要改什么：`ci.yml` 新增 job，`runs-on: windows-latest`，`go build ./... && go vet ./... && go test ./... -short`。
- 工作量：中——core 1 仓 2 步（job + 跳过 DB/race 的条件），但需要长期消耗 runner 分钟。
- 风险：runner 分钟成本；Windows 上测试的临时目录/进程行为可能引入 flaky，需要长期 triage。
- 可逆性：高（删 job）。
- 长期维护：一个需要盯的 job 与其 flaky 历史。

**B · 不做**
- 工作量：零。
- 风险：Windows 编译期问题（例如 `syscall`/`filepath` 用法）只在开发机暴露，PR 可能先绿后坏。
- 可逆性：不适用。
- 长期维护：零。

**C · 不加 runner，在现有 Ubuntu job 加交叉编译门（推荐）**
- 要改什么：在现有 `go` job 加一步 `GOOS=windows GOARCH=amd64 go build ./...`（必要时加 `go vet`）。
- 工作量：小——core 1 仓 1 步（1 行 step）。
- 风险：只覆盖编译期，不覆盖 Windows 运行时行为；但生产代码无 GOOS 分支，运行时风险本来就由开发机（Windows）首跑覆盖。
- 可逆性：高（删 1 行）。
- 长期维护：零。

**D · 12 仓全部加 Windows job**
- 要改什么：12 个 workflow 各加 job。
- 工作量：大——12 仓 × 2 步，runner 分钟数倍增。
- 风险：同 A，且成本 ×12；多数服务仓依赖 PG service，Windows 上还要额外配。
- 可逆性：高。
- 长期维护：12 个 job 的 flaky 面。

### 8.4 推荐：C（交叉编译门，不加 runner）

1. 实测结论是"生产代码零平台分支"，所以真正的风险只剩**编译期**平台差异；交叉编译门恰好覆盖它，且零 runner 成本。
2. 运行时差异由 Windows 开发机首跑覆盖（项目本身就是 Windows 宿主开发、Linux CI 验证的形态）。
3. 若将来引入真正的 Windows 专属运行时代码（届时会出现 `runtime.GOOS` 生产分支），再按 A 升级；触发条件可写死。

### 8.5 选了之后的动作清单（C）

1. `tellurion`：`ci.yml` 的 `go` job 增加 `GOOS=windows GOARCH=amd64 go build ./...`（放在 build 之后、test 之前）。
2. `tellurion`：台账 `X-CI-WINDOWS` 标 ✅（按 C 收口）并归档；写清"若生产代码出现 GOOS 分支，升级为 windows-latest job"。
3. 其他 11 仓不动（如需推广，另立单）。
4. 无新契约、无前端配套。

### 8.6 不选的后果（维持现状一年）

若选 A/D：一年后为两个几乎不会红的 job 持续支付 runner 分钟与 flaky triage；若选 B：某次引入 Windows 不兼容的 `syscall` 或路径写法，Linux CI 全绿、开发机首跑才炸，PR 已经合并。

---

## 9. `AGENT-S2-HYPOTHESIS-SOURCE` · S2 因果来源字段

### 9.1 现状与证据

| 事实 | 证据 |
|---|---|
| 代码零命中 | 全工作区 grep `hypothesis_source`：仅文档（`PRODUCT.md:82`、`ROADMAP.md:40/73/77`、`adr-023`、`SPEC.md`、审查报告），**12 仓代码 0 命中** |
| 表结构无该列 | `tellurion-agent:pkg/aistore/schema.go:64-81`：`ai.experiments` 列为 `id/run_id/seq/parent_id/hypothesis(TEXT)/params(JSONB)/dataset_split/strategy_name/expression/status/metrics/verdict/error_message/created_at/finished_at` |
| Go 结构无该字段 | `pkg/aistore/experiment.go:43-61` 的 `Experiment` 无 source 字段 |
| **旧阻因已失效** | `adr-0002` 曾写"`ai.experiments` 是 QT-17 从 core 逐列搬来的表，drift 护栏要求列集一致，加不了列"；但 core 七表 DDL 已于 2026-11-10 退役，`TestSchema_ColumnsMatchCore` 已退场（`pkg/aistore/schema_core_drift_test.go:20` 注释），列形状现在以本仓 `Statements()` 为真值（`docs/db-schema.md:13/38`） |
| 迁移机制允许前滚 | `db-schema.md`：每条 DDL 可重入（`IF NOT EXISTS`），**只前滚**；Postgres 支持 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` |
| 阶段门未到 | `ROADMAP.md:39` S1 ⏳ 进行中；`:40` S2 部分达成（底座 ✅ / `hypothesis_source` ⬜） |

### 9.2 为什么挂住，前提还成立吗

- 挂住的前提 = "`CORE-S1-EXIT-EVIDENCE` 达成且主任启动 S2"。
- **该前提仍成立**：S1 出口（无人干预连续跑完 100 次实验并产出可审阅摘要）尚未验收；S2 未开始。
- 但要区分两件事：**能不能做**（技术上已解锁，旧 ADR 的"加不了列"已过期）与**该不该现在做**（阶段门未到）。

### 9.3 可选方案

**A · 现在开工（加列 + 写读链 + 契约 + 测试）**
- 要改什么：`schema.go` 增 `ALTER TABLE ai.experiments ADD COLUMN IF NOT EXISTS hypothesis_source JSONB`；`Experiment` 结构 + `InsertExperiment`/读面；`docs/db-schema.md` + `docs/api-schema.md`；写入点 = 探索/回测工具产生假设处；空值语义（未知 ≠ 空串）；契约测试 + 破坏验证。
- 工作量：中——agent 1 仓 5~6 步，新增列（结构变更，按 `db-schema.md` 需同步文档，可能需一条 ADR）。
- 风险：抢跑。当前没有消费方（UI 审阅台/校准都还没接），字段形状只能拍脑袋；S1 出口后真实数据流可能推翻它。
- 可逆性：高（列可保留但不再写；彻底回退需 DROP COLUMN 迁移）。
- 长期维护：一个可能被重定义的字段与两处文档。

**B · 只冻结形状（一页字段语义，不落码）**
- 要改什么：写一页决策材料：来源类型词表（产业链假设 / 文献 / 人工 / 挖掘）、证据指针（`content_hash` / 行业节点 id）、置信说明、空值语义；不建列、不改代码。
- 工作量：小——0 代码，1 份文档。
- 风险：没有真实消费方时，形状容易过度设计；但成本低、可被 S2 启动时修订。
- 可逆性：高（文档可改）。
- 长期维护：一页文档。

**C · 维持挂起，等 S1 出口后按 S2 正式单开工（推荐）**
- 要改什么：无。台账保持 ⏸，重开条件已是"`CORE-S1-EXIT-EVIDENCE` 达成 + 主任启动 S2"。
- 工作量：零。
- 风险：S2 启动时前期准备为零；但 S2 的第一件事本来就是"形状取决于真实探索轮次"。
- 可逆性：不适用。
- 长期维护：零。

**D · 从 S2 出口判据中移除 `hypothesis_source`**
- 要改什么：改 `ROADMAP.md` S2 出口、`PRODUCT.md` 能力状态、可能涉及 ADR-023。
- 工作量：小——文档 2~3 处。
- 风险：S2 的定义就是"让因子带因果来源"（`ROADMAP.md:40`）；移除它等于掏空 S2，只保留"产业链底座"，S2 失去可判定出口。
- 可逆性：高（文档可改回）。
- 长期维护：需要重新定义 S2 的"解释"是什么。

### 9.4 推荐：C（维持挂起）

1. S2 的语义就是因果来源（`ROADMAP.md:40`"让因子带因果来源"），D 会让 S2 变成没有判据的阶段，不可取。
2. A 抢跑违反 `ROADMAP` 的 S1 → S2 顺序，且字段形状应由 S1 出口后的真实探索轮次决定（"来源类型"取决于实际有哪几类假设），现在定容易拍脑袋。
3. B 是低成本的准备，但当前没有消费方，容易把"设想"写成"契约"；如果主任希望降低 S2 启动延迟，B 可接受，但应在 S2 启动时重新评审形状。
4. **本轮新增的重要事实**：ADR-0002 的"加不了列"阻因已随 core DDL 退役失效（§9.1），所以 S2 一旦启动，实现路径是通的，不会再被旧约束卡住——这一条应在台账里补记，避免 S2 启动时再误判为阻塞。

### 9.5 选了之后的动作清单（C）

1. 无代码动作；`AGENT-S2-HYPOTHESIS-SOURCE` 保持 ⏸，重开条件不变。
2. 建议（可在本轮之后另做，不属本材料范围）：在 agent 台账该条补一句"2026-11-13 实测：core 七表 DDL 已退役、`TestSchema_ColumnsMatchCore` 已退场，加列技术上已解锁；阶段门仍是 S1 出口"。
3. S2 启动时的动作（届时另立单）：`agent` 加列 + 写读链 + `db-schema.md`/`api-schema.md`；`ui` 审阅台展示（另立）；`core` 反代无需改动。
4. 需要新契约吗：不需要跨仓 Go 契约；但**结构变更**按 `db-schema.md` 规则需要同步文档，建议配一条 ADR 记录"来源词表 + 空值语义"。

### 9.6 不选的后果（维持现状一年）

维持现状不是"什么都不发生"：S1 出口后 S2 启动，第一件事仍是定义形状——只是届时手里有真实探索数据，定义会更准。若现在硬做（A），一年后大概率要再改一次字段语义，并处理已写入的脏数据；若做 D，S2 会退化成"产业链底座已就绪"的单腿阶段，`ROADMAP` 的出口判据失效。

---

## 10. 本轮推翻的台账旧描述（施工前必须知道）

| # | 台账旧描述 | 2026-11-13 实测 | 影响 |
|---|---|---|---|
| 1 | `CORE-TEST-EVIDENCE-VERSIONED`："`reports/` 在 core 为 **0 tracked 文件**" | `git ls-files reports` = **1**（`reports/test-2026-11-13/summary.md`）；42 个文件中 33 个 `*.log` 被 `.gitignore:20` 忽略、8 个 untracked | 任务范围从"完全没有版本控制"收窄为"结论有、原始证据没有" |
| 2 | `CORE-STOCKSTATE-DISPOSITION`：**建议 A 接线** | `ROADMAP.md:105` 明确不做实盘；broker `ADR-0003` 真钱通道终态 = Mock；6 条路由 0 调用、registry 0 构造 | 推荐从 A 改为 **B 退役** |
| 3 | `BROKER-LIVE-LOOPBACK-GUARD`：挂在 **broker 仓** | 实现在 `tellurion:pkg/brokerhttp/trader.go:78-99`；broker 仓仅有 `cmd/brokergateway/main.go:101` 一条注释 | 施工会改错仓；台账需迁 core 或改指针 |
| 4 | `AGENT-S2-HYPOTHESIS-SOURCE` 的间接阻因："drift 护栏要求列集一致，加不了列"（ADR-0002 语境） | `TestSchema_ColumnsMatchCore` 已退场（`schema_core_drift_test.go:20`），`ai.*` 列形状以本仓 `Statements()` 为真值（`db-schema.md:13/38`） | 加列技术上已解锁；阶段门才是唯一阻因 |
| 5 | `X-CI-WINDOWS`："存在 Windows 专属分支（路径分隔符、进程管理）" | 生产代码 `runtime.GOOS` **0 处**；9 处全部在 `_test.go` | 风险从"运行时"降为"编译期"，推荐从 windows runner 改为交叉编译门 |

---

## 11. 实测方法（可复现）

```powershell
# 1. stockstate 调用面
Select-String -Path (Get-ChildItem C:\Users\ruoxi\Workspace\tellurion -Recurse -Filter *.go -File).FullName `
  -Pattern 'NewStockStateHandler|NewStockStateRegistry|NewForcedLiquidator'

# 2. 死包导入者（对每个白名单包替换路径）
Get-ChildItem C:\Users\ruoxi\Workspace\tellurion -Recurse -Filter *.go -File |
  Select-String -Pattern 'pkg/trading/margin"'

# 3. 引擎体量
(Select-String -Path C:\Users\ruoxi\Workspace\tellurion\pkg\backtest\engine.go -Pattern '^func ').Count
(Get-ChildItem C:\Users\ruoxi\Workspace\tellurion\pkg\backtest -Filter *_test.go).Count

# 4. 测试证据
git -C C:\Users\ruoxi\Workspace\tellurion ls-files reports
git -C C:\Users\ruoxi\Workspace\tellurion status --porcelain -uall -- reports
git -C C:\Users\ruoxi\Workspace\tellurion check-ignore -v reports/test-2026-11-13/w0-build.log

# 5. broker 通道闸
Select-String -Path C:\Users\ruoxi\Workspace\tellurion\pkg\brokerhttp\trader.go -Pattern 'isLoopbackHost|ChannelLive'

# 6. UI 入口
Select-String -Path (Get-ChildItem C:\Users\ruoxi\Workspace\tellurion-ui\web\src -Recurse -File).FullName -Pattern 'industry|macro|toggleTheme'

# 7. CI runner 与 artifact
foreach ($r in 'tellurion','tellurion-agent','tellurion-analytics','tellurion-broker','tellurion-contracts','tellurion-data','tellurion-docs','tellurion-kit','tellurion-orchestration','tellurion-risk','tellurion-strategy','tellurion-ui') {
  Select-String -Path "C:\Users\ruoxi\Workspace\$r\.github\workflows\ci.yml" -Pattern 'runs-on' | ForEach-Object { "$r :: $($_.Line.Trim())" }
}

# 8. hypothesis_source
Get-ChildItem C:\Users\ruoxi\Workspace -Directory -Filter 'tellurion*' | ForEach-Object {
  Get-ChildItem $_.FullName -Recurse -Filter *.go -File | Select-String -Pattern 'hypothesis_source'
}
```

> 说明：以上命令均为只读；本轮未修改任何代码、台账或既有设计文档。

---

## 12. 需要主任拍板的 9 个勾

| # | 任务 | 请勾选 |
|---|---|---|
| 1 | `CORE-STOCKSTATE-DISPOSITION` | A 接线 / **B 退役** / C 冻结 / D 维持 ⏸ |
| 2 | `CORE-BACKTEST-ENGINE-SPLIT` | A 全量切分 / B 局部切分 / **C 不做** / D 配额切分 |
| 3 | `CORE-DEAD-PACKAGE-DISPOSITION` | A 全部保留 / **B 三包退役** / C 全量退役 / D 不做 |
| 4 | `CORE-TEST-EVIDENCE-VERSIONED` | A 全量入库 / **B artifact+摘要** / C 维持现状 / D 独立证据仓 |
| 5 | `BROKER-LIVE-LOOPBACK-GUARD` | **A Warn+成文** / B fail-closed / C 不做 / D 直接判错 |
| 6 | `UI-INDUSTRY-ENTRY` | A 现在建页 / **B 仅 API + 升级条件** / C 不做 / D 最小两图 |
| 7 | `UI-THEME-TOGGLE` | **A 移除** / B 完整实现 / C 不做 / D 半套主题 |
| 8 | `X-CI-WINDOWS` | A windows job / B 不做 / **C 交叉编译门** / D 12 仓铺开 |
| 9 | `AGENT-S2-HYPOTHESIS-SOURCE` | A 现在开工 / B 冻结形状 / **C 维持挂起** / D 移出 S2 判据 |
