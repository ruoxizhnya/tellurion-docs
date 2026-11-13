# ODR-074: 九条挂起任务裁决（退役 / 不做 / 保留 / 维持挂起）

> **Status**: Accepted
> **Date**: 2026-11-13
> **Category**: Process
> **Related ADRs**: adr-023（三角色实验室·人是闸门）/ adr-034（分仓拓扑与 S0~S3 阶梯）/ adr-041（AI 因子工具面不新造端点）；[broker adr-0003](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/adr/0003-真钱通道暂不实施与重开条件.md)（真钱通道暂不实施与重开条件）；agent adr-0002（`ai.*` schema 漂移护栏，部分前提已失效，见 §前提订正）
> **Supersedes**: n/a（承 ODR-068~073 第五轮审查与 2026-11-13 五角审查；本记录只裁决，不含施工）

---

## Context

- **范围**：2026-11-13 五角审查（文档架构与卫生 → 产品设计 → 实现 → 测试 → 文档与代码一致性）把 9 条「方案不唯一、需主任拍板」的任务标为 `⏸ 待主任裁决`。主任要求先出决策材料，再逐条拍板。
- **材料**：决策材料收录于 [`docs/reviews/2026-11-13/decision-materials-suspended-9-2026-11-13.md`](../../reviews/2026-11-13/decision-materials-suspended-9-2026-11-13.md)（每条 3~4 个方案 + 代价 + 动作清单 + 可复现实测方法）。**本 ODR 是这 9 条的唯一裁决真相源**，材料只作取证与推演底稿。
- **纪律**：9 条全部是「能力去留 / 文档口径」类判断，不涉及回测语义、撮合口径或契约形状变更；裁决一律贴项目已声明的边界（`PRODUCT.md` §边界、`ROADMAP.md` §明确不做、`SYSTEM-DESIGN.md` §4），不按「最佳实践」选型。
- **施工分工**：core 与 ui 的**代码改动与各自台账落账**由对应施工会话完成（验收后标 ✅ / 按裁决收口）；本记录 + 本仓文档口径由文档侧落。broker / agent 台账的订正与收敛随本记录同步完成。

## Decision

### 裁决速览

| # | 任务 | 归属仓 | 裁决 | 一句话理由 | 施工落点 |
|---|---|---|---|---|---|
| D1 | `CORE-STOCKSTATE-DISPOSITION` | core | **B 退役** | 项目明确不做实盘；stockstate 全部语义绑 `LiveTrader`，接线 = 在「不做」的领域新增运行路径 | core 删 `pkg/trading/stockstate/` + `cmd/analysis/handlers_stock_state.go` + repoguard 负断言 |
| D2 | `CORE-BACKTEST-ENGINE-SPLIT` | core | **不做（台账标作废，保留原文与理由）** | 撮合复杂度是领域复杂度，不是行长；触发条件已可判定，现在切分是「为切分而切分」 | 无代码；core 台账留原文 + 作废标记 |
| D3 | `CORE-DEAD-PACKAGE-DISPOSITION` | core | **工具 9 包保留，交易三包退役** | 工具包各有未来路径；auction / options / margin 无数据源、无 broker 面、不在任何阶段 | core 删三包；repoguard 白名单 12 → 9 + 3 条负断言 |
| D4 | `CORE-TEST-EVIDENCE-VERSIONED` | core | **CI artifact + 仓内摘要** | 结论摘要已入库；原始日志是一次性证据，不该进仓（`*.log` 已被 `.gitignore:20` 忽略） | core `ci.yml` 增 artifact 上传 + 摘要补「证据位置」节 |
| D5 | `BROKER-LIVE-LOOPBACK-GUARD` | **core（非 broker）** | **A 维持 Warn + 成文** | 真钱未开；实质风险已由 `/version.channel` 对拍拦下；单机自托管下同机网关合法 | core 成文；broker 台账只留「实现不在本仓」指针 |
| D6 | `UI-INDUSTRY-ENTRY` | ui | **B 当期仅 API，不做界面** | UI 是观察窗；产业链图的价值在「图谱→因子→回测」链路，S2 出口前该链路不存在 | ui 台账按 B 收口；建页触发 = S2 出口 |
| D7 | `UI-THEME-TOGGLE` | ui | **A 移除死控件** | 深色是唯一被设计验收过的基线；半成品开关比没有更伤体验 | ui 删按钮 / `toggleTheme` / `MoonOutline` |
| D8 | `X-CI-WINDOWS` | core | **C 交叉编译门，不引入 Windows runner** | 生产代码 `runtime.GOOS` 零处（9 处全在 `_test.go`），风险只在编译期 | core `ci.yml` 加 `GOOS=windows GOARCH=amd64 go build ./...` |
| D9 | `AGENT-S2-HYPOTHESIS-SOURCE` | agent | **C 维持挂起（等 S1 出口）** | S2 的定义就是因果来源，不能砍；但字段形状应由真实探索数据决定，不先冻结 | agent 台账补「加列已解锁」实测；重开条件不变 |

### D1 · stockstate 退役

- **裁决**：删 `cmd/analysis/handlers_stock_state.go`（6 条路由，`main.go` 无 `NewStockStateHandler` 调用）与 `pkg/trading/stockstate/`（`stock_state.go` 455 行 + 测试 556 行），`internal/repoguard/package_wiring_test.go` 的 `retiredPackages` 加负断言，`handler_wiring_test.go` 删白名单条目。
- **理由**：① `ROADMAP.md` §明确不做 已写死不实盘，broker ADR-0003 把真钱通道终态定为 Mock，而 stockstate 的全部语义绑定 `LiveTrader`（`stock_state.go:366`）；② 台账原建议「接线」的前提是「有执行机会」，当前不存在，保留会制造「能力已可用」的假信号；③ 重开路径（broker ADR-0003 P1~P5 + X6c）已写死，删除不抹掉将来的可能性。
- **代价**：将来接实盘时需按 A 股停牌/退市/强平规则重建校验层；重建成本低于长期维护一段假能力。
- **不新增契约、无前端配套**（UI 从未引用 `/api/stock-state`）。

### D2 · 回测引擎切分：不做

- **裁决**：core 台账 `CORE-BACKTEST-ENGINE-SPLIT` **标作废并保留原文与理由**；无代码动作。重开条件保持原样（「下一次需同时改 `engine.go` 与 `engine_daily.go` 的撮合/日频语义，或新增交易所口径」）。
- **理由**：① 项目对回测的核心要求是数字可信，不是文件行数，切分不改变可信度；② 触发条件可判定，未触发时切分违反该单 ④「不为切分而切分」；③ 既有测试与基准是将来 characterization 的基础，现在做等于提前支付成本。
- **代价**：若触发条件出现，改动仍落在 2237 行文件里（已是已知且有测试兜底的沉没成本）。

### D3 · 12 个白名单死包：9 保留 + 3 退役

- **裁决**：保留 `api` / `systemalert` / `testutil` / `id` / `sandbox runner` / `staticcheck` / `strategy monitor` / `mining` / `sync`（各有「未来用途 + 触发点」）；退役 `pkg/backtest/auction/`、`pkg/strategy/options/`、`pkg/trading/margin/`，`package_wiring_test.go` 白名单 12 → 9，`retiredPackages` 加 3 条负断言（目录复活即红）。
- **理由**：判据是「是否在项目已声明边界内」，不是「有没有用」——实盘不做、日频为边界、无期权/两融数据源、broker 无两融面；保留三包会让白名单从「待接线的债」退化成永久豁免清单。
- **代价**：开盘价按日频建模，竞价时段不在口径内；若将来需要更真实的开盘成交，`auction` 按原单 ③ 重建（届时另立单）。
- **附带**：core `ARCHITECTURE.md`（或 repoguard 注释）补 9 包归属表（性质 / owner / 重开条件），由 core 施工会话落。

### D4 · 测试证据：CI artifact + 仓内摘要

- **裁决**：core `ci.yml` 的 test job 增加 artifact 上传（`coverage.out` + 测试输出，保留期明确），沿用 dualrun 报告既有的 artifact 模式（`ci.yml:373-379`）；`reports/test-2026-11-13/summary.md` 补「证据位置」节（artifact 名 + run 链接填法）。日志不入库。
- **理由**：与既有先例一致，不引入新机制；`summary.md` 已证明「仓内摘要」可行，且正是审查与验收要读的东西；原单 ④ 已写明「不提交大文件/二进制」。
- **代价**：artifact 过期后不可复核，靠摘要 + run 链接追溯；摘要必须诚实，不能替代原始证据。

### D5 · live + 回环地址：维持 Warn 并成文（含归属纠偏）

- **裁决**：不改 fail-closed。core `docs/live-trading.md`（或 runbook）补一节「live + loopback 的判定与处置」：同机真实网关合法 / Mock 网关必须用 `BROKER_CHANNEL=mock` 声明 / 声明与对端不符由 `/version.channel` 拒绝启动。启动 Warn 可补 `reason=loopback_gateway` 一类结构化字段（可选，1 行）。
- **归属纠偏（台账原描述有误）**：**实现落点在 core `pkg/brokerhttp/trader.go:78-99`**（`resolveChannel` 的 live 分支 + `isLoopbackHost`）；`tellurion-broker` 仓无等价代码，只有 `cmd/brokergateway/main.go:98-101` 一条关于 `/version.channel` 的注释。broker 仓台账已据此改为「实现不在本仓」的指针。
- **理由**：当前阶段的实质风险（误把 mock 当 live）已由 `/version.channel` 对拍覆盖；项目形态是单人自托管，真实网关落在同机是合理布局；原单 ④ 明确「不新增配置前缀体系」，fail-closed 方案的新放行键正是它要避免的扩张。
- **代价**：不拦「地址形态」这一层；误解 loopback 语义的人仍可能误配——由成文文档兜底。

### D6 · 产业链/宏观入口：当期仅 API

- **裁决**：**不做界面**。`PRODUCT.md` 口径为「后端可用、仅 API、无 UI 入口」；建页升级触发条件写死为 **S2 出口达成**（至少 1 个行业假设因子完成完整验证并带 `hypothesis_source`）。ui 台账按 B 收口（不是 ✅ 完成，而是「已裁决 B」），保留 A 的升级条件。
- **理由**：UI 页面都绑定一个用户动作；产业链图的正解是「图谱→因子→回测」链路，S2 出口前该链路不存在，页面没有消费场景。把 UI 提前到 S1 会打乱阶段顺序，也与「不为消掉问题发明需求」冲突。
- **代价**：S2 出口前用户只能通过 API 查产业链数据；届时建页需重做视觉基线、空态与错误态。

### D7 · 主题切换：移除死控件

- **裁决**：删 `AppHeader.vue:73-80` 的按钮块与 `:148` 的 `toggleTheme`，清理 `MoonOutline`；若有 Header 组件测试或视觉基线引用该按钮，同步更新。**对外口径：UI 只有深色主题**——深色是唯一经设计验收的基线，主题切换不作为功能。
- **理由**：主题不服务任何观察任务；完整实现（浅色 token + 图表配色）收益与成本不成比例；「点击后提示功能开发中」是可见的未完成承诺，比没有按钮更伤体验。
- **代价**：将来若要做浅色主题，须重做一套 token 与图表配色（成本远高于「加个开关」）。

### D8 · CI Windows：交叉编译门，不引入 runner

- **裁决**：core `ci.yml` 的 `go` job 在 build 之后、test 之前加 `GOOS=windows GOARCH=amd64 go build ./...`；其余 11 仓不动（推广另立单）。若生产代码将来出现 `runtime.GOOS` 分支，再升级为 `windows-latest` job。
- **理由**：生产代码零平台分支 ⇒ 风险只在编译期，交叉编译门恰好覆盖且零 runner 成本；运行时差异由 Windows 开发机首跑覆盖（项目本身就是 Windows 宿主开发、Linux CI 验证）。
- **代价**：交叉编译门不覆盖 Windows 运行时行为；该缺口在出现生产 `GOOS` 分支前可接受。

### D9 · `hypothesis_source`：维持挂起

- **裁决**：`AGENT-S2-HYPOTHESIS-SOURCE` 保持 `⏸`，重开条件不变（`CORE-S1-EXIT-EVIDENCE` 达成 + 主任启动 S2）。**不先冻结字段形状**：来源类型词表、证据指针、空值语义由 S1 出口后的真实探索数据决定，S2 启动时另立单并配一条 ADR 记录「来源词表 + 空值语义」。
- **台账补记（本轮实测）**：ADR-0002 语境下「drift 护栏要求列集一致 ⇒ 加不了列」的间接阻因**已失效**——core 七表 DDL 已退役，`TestSchema_ColumnsMatchCore` 已退场（`pkg/aistore/schema_core_drift_test.go:20`），`ai.*` 列形状以本仓 `Statements()` 为真值（`db-schema.md:13/38`）。**加列技术上已解锁，阶段门是唯一阻因**；S2 启动时不得再误判为阻塞。
- **理由**：S2 的语义就是因果来源，砍掉会让 S2 失去出口判据；抢跑则违反 S1 → S2 顺序，且现在定形状容易拍脑袋、将来大概率要改语义并处理脏数据。
- **代价**：S2 启动时仍要定义形状（届时手里有真实数据，会更准）；UI 审阅台展示与 core 反代届时确认（预计无需改动）。

## 前提订正（施工前必须知道）

| # | 台账旧描述 | 2026-11-13 实测 | 影响 |
|---|---|---|---|
| 1 | `CORE-TEST-EVIDENCE-VERSIONED`：「`reports/` 为 0 tracked 文件」 | `git ls-files reports` = 1（`reports/test-2026-11-13/summary.md`）；42 个文件中 33 个 `*.log` 被 `.gitignore:20` 忽略、8 个 untracked | 任务范围从「完全没有版本控制」收窄为「结论有、原始证据没有」 |
| 2 | `CORE-STOCKSTATE-DISPOSITION`：建议 A 接线 | `ROADMAP.md` §明确不做 写死不实盘；broker ADR-0003 终态 = Mock；6 条路由 0 调用、registry 0 构造 | 推荐从 A 改为 B 退役（D1） |
| 3 | `BROKER-LIVE-LOOPBACK-GUARD`：挂在 broker 仓 | 实现在 core `pkg/brokerhttp/trader.go:78-99`；broker 仓只有一条 `/version.channel` 注释 | 施工会改错仓；broker 台账改指针（D5） |
| 4 | `AGENT-S2-HYPOTHESIS-SOURCE` 间接阻因：「加不了列」 | 漂移对拍已退场（`schema_core_drift_test.go:20`），列形状以本仓 `Statements()` 为真值 | 加列已解锁；阶段门是唯一阻因（D9） |
| 5 | `X-CI-WINDOWS`：「存在 Windows 专属分支」 | 生产代码 `runtime.GOOS` 0 处，9 处全在 `_test.go` | 风险从运行时降为编译期（D8） |

## 对外口径变更（本仓落地）

| 文档 | 变更 |
|---|---|
| [PRODUCT.md](../../PRODUCT.md) §三层结构 L2 | 产业链查询：`后端 ✅ / UI 入口 ⬜` → **后端 ✅ / 仅 API，无 UI 入口** |
| [PRODUCT.md](../../PRODUCT.md) §能力状态 | 产业链条补「已裁决当期仅 API + 建页触发 = S2 出口（D6）」；`hypothesis_source` 条补「维持挂起至 S1 出口（D9）」 |
| [PRODUCT.md](../../PRODUCT.md) §边界 | 新增三行：实盘证券状态校验（随实盘退役，D1）/ 期权·两融·集合竞价撮合（D3）/ 浅色主题·主题切换（深色为唯一基线，D7） |
| [ROADMAP.md](../../ROADMAP.md) §明确不做 | 实盘条补「停牌/退市/强平校验随实盘通道退役（D1）」；新增期权·两融·竞价撮合（D3）、产业链/宏观 UI 页面（D6）、浅色主题（D7） |
| [ROADMAP.md](../../ROADMAP.md) §S2 | 现状态补「`hypothesis_source` 维持挂起（D9）；S2 启动时另立单定形状」；出口判据不变 |
| [SYSTEM-DESIGN.md](../../SYSTEM-DESIGN.md) §4 实盘行 | 补「live + 回环只 Warn 为有意设计（D5，误配由 `/version.channel` 对拍拦下）；证券状态校验随实盘退役（D1）」 |
| [SYSTEM-DESIGN.md](../../SYSTEM-DESIGN.md) §7 过渡态 | 补「实盘交易域代码已退役（D1/D3）：stockstate + auction/options/margin，repoguard 负断言防复活」 |

## 台账归属

| 仓 | 条目 | 落账方式 | 何时 |
|---|---|---|---|
| core | D1 / D3 / D4 / D8 | 施工会话在代码落地并验收后标 ✅ 并归档（含 D2 的作废标记） | 本轮施工完成时 |
| ui | D6 / D7 | D7 施工后标 ✅ 归档；D6 按裁决 B 收口（不归档，保留 A 升级条件） | 本轮施工完成时 |
| broker | D5 | **已完成**：活跃层改为「实现不在本仓」指针，原文与订正移入归档 | 本记录同批 |
| agent | D9 | **已完成**：维持 `⏸`，补「加列已解锁」实测与重开条件 | 本记录同批 |

## 不在本记录范围

- core / ui 的代码改动与验证（破坏验证、全量测试）——由各自施工会话负责，本记录不替代验收证据。
- 新契约、新端点、新配置项——9 条裁决均不新增。
- 其余 11 仓的 CI 改造（D8 只落 core，推广另立单）。

## Artifacts

- 决策材料：[`docs/reviews/2026-11-13/decision-materials-suspended-9-2026-11-13.md`](../../reviews/2026-11-13/decision-materials-suspended-9-2026-11-13.md)（含 9 条方案推演、代价表与可复现实测命令）
- 审查报告：`docs/reviews/2026-11-13/`（文档架构与卫生 / 01-product-design / 02-implementation / 03-testing / 04-consistency）
- 台账：core `docs/TASKS.md`、ui `docs/TASKS.md`、broker `docs/TASKS.md`、agent `docs/TASKS.md`
