# ADR-039 · 指标权威：core 运行时权威，analytics 只读参考实现

- **Status**: Accepted
- **Date**: 2026-11-11
- **Deciders**: 主任（授权本轮按限界上下文 / DDD 判定）
- **Related**: ADR-0005（analytics 定位为独立只读分析服务，core 指标不迁移）、ADR-036 §3（G3 与 G4 就绪门）、ADR-038（因子派生表归 core）、`tellurion-docs:docs/design/ddd-boundary-review-2026-11-11.md` C4/D4

---

## 1. 背景与问题

指标/归因存在两份实现：core 的 `pkg/backtest/metrics` + `pkg/backtest/reporting`，与 `tellurion-analytics:internal/analysis`（`metrics.go`、`attribution.go`、`benchmark.go` 等）。ADR-0005 已裁「analytics 是独立只读参考实现、core 保留冻结」，但**没有一处用「权威 / 参考」把关系写死**，也没有定义「什么条件下必须收敛」。

本 ADR 补齐这两件事。不重新讨论 ADR-0005 的方向（不迁移），只把共存边界与收敛触发条件写成可判定条款。

## 2. 事实

| 事实 | 证据 |
|---|---|
| core 是运行时承重实现 | `tellurion:pkg/backtest/engine.go` 每次 run 调 `metrics.GenerateBacktestResult`；`cmd/analysis/handlers_backtest.go` 调 `reporting.RenderHTML`/`CompareReports`；`cmd/dualrun` 用它做双内核等价判定 |
| 引用面已冻结 | `tellurion:internal/repoguard/analytics_impl_freeze_test.go:33-37` 钉住恰好 3 处生产 import，新增/减少都红 |
| analytics 只写 `analysis.*` | `tellurion-analytics:internal/analysis/g2_schema_write_guard_test.go:18-28` 静态扫 SQL |
| core 对 analytics 零调用 | ADR-0005 §3；`SVC-AN-G3` 已关闭 |
| analytics 指标面是子集 | `tellurion-analytics:docs/adr/0005-*.md` §理由：只覆盖 volatility/VaR/CVaR 等；Sharpe/Sortino/Calmar/回撤/交易统计仍在 core |

## 3. 决策

**D1 · core 的 `pkg/backtest/metrics` 是**运行时权威实现**。** 回测结果里出现的任何指标数字，以 core 为准；它是 `quant.run_provenance` 与历史回测口径的一部分，不因 analytics 的实现而改变。

**D2 · analytics 是**只读参考实现 + 报告/导出面**。** 它可以在自己的 `analysis.*` 里计算同名指标，但：

- 不写回 core 的任何表；
- 不被 core 调用（core → analytics 的调用边继续为零）；
- 不宣称自己是上游口径的权威。

**D3 · 共存边界（全部成立才允许双实现继续存在）。**

| # | 边界 | 判据 |
|---|---|---|
| B1 | 写面隔离 | analytics 只写 `analysis.*`；`g2_schema_write_guard_test` 红即边界破裂 |
| B2 | 调用方向 | core 生产代码对 analytics 的 import / HTTP 调用 = 0；出现即红线 |
| B3 | 口径仲裁 | 同一指标两份结果不一致时，**以 core 为准**；修 analytics，不改 core（除非触发 T3） |
| B4 | 引用面冻结 | core 的 `metrics`/`reporting` 生产 import 恰 3 条；新增先重开归属裁决 |
| B5 | 承诺面差异 | analytics 只承诺它自己文档列出的指标子集；core 独有的指标不要求 analytics 对齐 |

**D4 · 收敛触发条件（任一满足 ⇒ 必须另立 ADR 与任务单启动收敛，不得「将来再说」）。**

- **T1 · 报告出口单点化**：`cmd/analysis` 不再注册任何报告导出/对比路由（`reporting.RenderHTML` / `CompareReports` 的生产调用点归零），且 analytics 的报告端点成为唯一产出面 ⇒ `pkg/backtest/reporting` 不再是运行时承重，可在同 ADR 里删除。
- **T2 · 口径漂移超限**：同一 golden fixture（同一 run 的净值序列 + 交易明细）在两侧产出的同名指标，**连续两个发布版本**相对差 > `1e-9`（比率类）或绝对差 > `0.01` 元（金额类）⇒ 必须先定权威再修一侧，禁止两边各改各的。
  - 该触发条件的量测前置是漂移检测单（`tellurion-analytics:ANALYTICS-METRIC-DRIFT`）；检测未落地前，T2 视为「不可判定」，不得据此宣布无漂移。
- **T3 · 冻结解冻**：任何需求要求修改 core 冻结实现的公式（即 `analytics_impl_freeze_test.go` 的快照需要变更）⇒ 必须在同一笔变更里先写「谁是权威、另一侧如何跟随」，不允许改完实现顺手更新快照。**更新快照而不写裁决 = 违反本 ADR。**

**D5 · 漂移检测是 T2 的可判定前提，不是可选项。**

检测形态：以一次真实 core run 的 artifact（净值 + 交易 + 持仓）为输入，跑 analytics 的同名指标计算，输出逐指标差值；固定 fixture 入库，阈值按 D4-T2。检测跑在 analytics 仓（它有实现与测试基建），core 侧只提供 artifact 形状。

## 4. 否决的候选

- **立即迁移（analytics 成为唯一实现）**：要改 core 运行时承重路径（`engine.go` 每次 run）、补新端点与 DTO，且 analytics 只覆盖子集，切换会让回测口径不可逆变化。代价与风险都高于收益，ADR-0005 已否决，本 ADR 维持。
- **保持「无裁决」的双实现**：两份公式各自演进，没有任何判据能在漂移发生时报警；这正是本轮 C4 的问题。否决。
- **把 analytics 改成 core 的远程指标服务**：把进程内计算变成跨服务调用，违背 ADR-028 §6/§11 的「求值在消费点」与 ADR-036 的服务定位。否决。

## 5. 后果

1. 双实现继续共存，但**权威关系与收敛条件可判定**；「谁对」不再靠口头约定。
2. `ANALYTICS-METRIC-DRIFT` 落地前，T2 不可判定——这一点必须写进 analytics 的台账，避免「没检测 = 没漂移」的误读。
3. 不改变任何运行时行为、不改公式、不动冻结护栏。

## 6. 不在本 ADR 范围

- `analysis.*` 五张表的归属（analytics 自持，ADR-036 已定）；
- `analysis.benchmarks` 零写者（K7 已挂起，维持）；
- 因子归因的因子值来源（ADR-037 已裁）；
- core 报告 UI（`tellurion-ui`）。
