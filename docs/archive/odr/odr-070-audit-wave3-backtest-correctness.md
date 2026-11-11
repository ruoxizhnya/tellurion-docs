# ODR-070: 第五轮全系统审查 · 回测正确性（W3）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-024（表达式执行载体）；contracts adr-0004（值对象纯函数）；X6c 真钱通道挂起（broker adr-0003）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md)；本轮 W3 = Q 回测正确性 + I-3 幂等，仪器域计算面）

---

## Context

- **本 ODR 范围**: W3 回测正确性波（Q-1 前视 / Q-2 PIT / Q-3 幸存者偏差 / Q-4 T+1·涨跌停·SPEC 互锁 / Q-5 费用语料 / Q-6 确定性重放 / Q-7 数值精度 / Q-8 日历时区 + I-3 幂等）。仪器域计算面，DDD 判据「怎么算 = core」。
- **取证纪律**: 同 ODR-068。本波**预取证在 W2 等待期顺手真跑（全部 E1，2026-11-11，无库无服务）**，是本轮证据最硬的一波——回测正确性的核心断言全部本地真跑绿。
- **环境**: 无库无服务腿已跑；需 _test 库的 PIT 回填腿（Q-2）/ 幂等 PG 腿（I-3）挂 A1（主任已授权）；Q-6 双跑对齐已有 E2（02d1847 align-gate SUCCESS），A2 本地 Docker 双跑建议撤销。

## Decision

### 主任授权与决策采纳

- **D9（W3-F1 float64 口径）= a 接受 float64 + 补舍入方向/累计误差断言**。资金路径全 float64（contracts `fees/ashare.go:181-185` Config 五字段，SPEC.md:334「数值字段一律 *float64」是成文政策）；kit/decimal 存在且有牙（div_rounding_test：TestDiv_Rounding / OverflowFailsClosed）但**全 12 仓零消费者**（ADR-027:674 时点即孤立包，随横切迁 kit 后仍闲置）。**代价** = 不采纳 decimal，长回测累计误差靠不变量网 + 新增断言钉住；收益 = X6c 真钱挂起期间改动面小、纸交易阶段 decimal 收益不显著。**decimal 采纳与否随 X6c 重开再裁**。落点 CORE-FEE-ROUNDING-ASSERT [P2]。

### 预取证（E1 真跑，2026-11-11，无库无服务）

| 项 | 命令/范围 | 结果 | log |
|---|---|---|---|
| Q-5 费用语料三仓 | core `python tools/check_contract_conformance.py`（= make contracts-conformance 底层） | **EXIT=0**：语料 33 条/9 kind，core+agent 通过，0 跳过；fee_defaults_via_yaml 钉 commission_rate=0.0003 / slippage_rate=0.0001（cases.json:352-355） | w3-conformance.log |
| Q-5 语料自检腿 | contracts `go test ./conformance -count=1` | EXIT=0 | 同上会话 |
| Q-4 SPEC↔Go 互锁 | core `go test ./e2e/guard/... -count=1` | EXIT=0（spec_drift 双向反射比对 + resultspec） | — |
| Q-6 确定性重放 | core pkg/backtest 8 条 | **8/8 PASS，EXIT=0**：DeterministicReplay / RNG_NotGlobal / NextID_Deterministic / SameInputProducesSameResult / TopNSelectionIsOrderIndependent / **REV18_SameRangeRerunBitIdenticalAcrossQfqResync** / DualModeSignalEquivalence / StreamingFeedOrderIsDeterministic（含 bit 级重跑断言；RNG 非全局、TopN 序无关 = map 遍历序风险已钉） | w3-replay.log |
| Q-4 T+1/涨跌停/不变量 | core pkg/backtest -run 'T1\|Limit\|Invariant' + auction 全包 | **23 PASS + auction ok，EXIT=0**（T1Violation / PriceLimitDetection_EdgeCases / ResolvePriceLimit_BoardMatrix / STDateSegmented / NewStockTakesPrecedence） | w3-t1-limit.log |
| Q-1 前视（成交时点） | core pkg/backtest -run 'TestQT02\|TestEligibleUniverse' | **16/16 PASS，EXIT=0**：OpenPrices_FillsAtOpenNotClose / MissingOrDirtyBarRejectsInsteadOfFallingBackToClose / NextOpen_FillsOnNextDayAtOpen / CaliberPair_DifferenceIsOneBar | w3-lookahead-survivor.log |
| Q-3 幸存者偏差 | 同上 EligibleUniverse 5 条 | PASS：**DelistedStockStaysInPoolBeforeDelisting** / DelistedButHeldIsKeptForLiquidation / FiltersByListingDate（退市股退市前留在宇宙，非剔除） | 同上 |
| Q-2 PIT 无库单元腿 | data `go test ./internal/normalize/... ./internal/schema/... -count=1` | EXIT=0（PIT 闸门 + visible_at 三集合 DDL 单元面；回填腿仍需 _test 库 A1） | — |
| Q-7 资金守恒 | core pkg/backtest 不变量 6 条 | **6/6 PASS，EXIT=0**：CashNeverNegative / PositionQuantityNeverNegative / **NAVEqualsCashPlusPositions** / AllTradesHavePositiveFee | w3-finding 内 |

### 发现摘要（W3-F1）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W3-F1 | Low~Med | 资金路径全 float64，decimal 能力闲置，舍入方向与长回测累计误差无专门断言 | contracts fees/ashare.go:181-185 五字段 float64；kit/decimal 零消费者；唯一舍入点 `pkg/trading/price_cage.go:288` math.Round(x*1e4)/1e4（价格笼 4 位）；settlement/portfolio 无舍入；不变量网 6/6 绿 | D9=a → CORE-FEE-ROUNDING-ASSERT [P2] |

### 静态核（Q-8/K-4，E3，2026-11-11）

- **DBT-13 修复随迁完好 ✅**：data `internal/ingest/juchao_adapter.go:283-306` parseEpochMillis（epoch 毫秒→FixedZone CST 取日历日→UTC 零点归一）+ :277 strict 兜底腿；`eastmoney_sectors_adapter.go:711-721` parseEastmoneyDateStrict 认不出即 ok=false（注释明写旧回落教训）。
- **全组 time.Now() 回落扫描 ✅**（8 Go 仓 pkg/internal/cmd 生产代码）：命中 10 处全部为**可注入时钟提供者**（data sync/reference.go:175-181、worker.go:166-172 带 Now/Clock 注入；strategy cache/service 默认 cfg.Now；orch timeNow；core margin/compliance 属 DBT-13 已裁墙钟）或注释/测试 ⇒ **无第二处 parseEastmoneyDate 式静默解析兜底**。
- **日历读面 ✅**：data `GET /api/v1/trading/calendar`（legacy_read.go:144，policy 四角色可读）；缺省日期参数取 UTC 当日零点（legacy_read.go:42）——查询参数墙钟默认，非数据解析，语义可接受。

### 已通过项（正证据，不立案）

- **Q-1 前视 ✅ / Q-3 幸存者偏差 ✅ / Q-4 T+1·涨跌停·SPEC 互锁 ✅ / Q-5 费用语料 ✅ / Q-6 确定性重放 ✅（含 bit 级）/ Q-8 日历时区 ✅**：全部 E1 真跑绿（见预取证表）。回测正确性核心断言无缺陷。
- **D-T4 值对象不可变性/纯函数四判据 ✅**（W7 补判定，跨编号覆盖）：float64 面归 W3-F1/D9；contracts 值对象纯函数四判据（ADR-0004：无 I/O / 依赖受限 / 无跨调用持久状态 / 不替代服务）= D-S2 check_contract_shape 真跑绿。
- **D-T1 T+1/涨跌停撮合 ✅ / D-T5 事件主题契约冻结 ✅**（W7 补判定）：msgbus/topics.go 16 冻结主题 + AST 守卫 + frozenTopicValues 钉值。

### 待真跑腿（A1 已授权，施工前取证）

- **Q-2 PIT 回填腿**：data `-tags backfill`（DATA_TEST_DSN，_test 库限定，库名必须 _test 结尾）；无库单元腿已跑绿。
- **I-3 幂等 PG 腿**：broker Reserve（ackstore/pg.go:66-78 单条原子 INSERT…ON CONFLICT DO NOTHING RETURNING）/ orch 子 run 键（parent:<id>:<index>）/ risk 去重键的 _test 库腿。静态面 W6 已核 ✅（单语句原子占位无需事务包装），PG 腿补跨实例回读正证据。
- **Q-6 双跑对齐**：已有 E2（02d1847 align-gate job SUCCESS：PG16 service + 合成 fixture + sidecar + dualrun -gate bh/quarterly）⇒ A2 本地 Docker 双跑非必需，要 E1 再授权。

## Consequences

**Positive**:
- 回测正确性核心（前视/幸存者/T+1/涨跌停/确定性重放/费用语料）全部 E1 真跑绿，仪器域计算面可信度高；
- float64 口径明确成文（D9=a），舍入方向+累计误差断言补齐后资金计算口径被钉住，decimal 采纳推迟到 X6c 重开有明确触发条件。

**Negative**:
- 长回测累计误差在补断言前无专门上界保证（不变量网只保证 NAV=现金+持仓、现金非负等守恒，不保证舍入误差累积上界）；
- PIT 回填与幂等的 PG 腿在 A1 施工前只有单元面/静态面正证据，跨实例/真库行为待补。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-070 行）
- 立单：`tellurion:docs/TASKS.md` — CORE-FEE-ROUNDING-ASSERT [P2]（D9=a，舍入方向+累计误差断言+float64 口径成文）
- 真跑腿（A1）：Q-2 PIT 回填 / I-3 幂等 PG，施工前取证，证据抄入对应单 Context

## Metrics

- W3 发现 **1 项**（W3-F1 Low~Med）；预取证 **9 组 E1 真跑全绿**（Q-1/3/4/5/6/7/8 + Q-2 单元腿）
- 判定表覆盖 Q-1~Q-8 + I-3 共 9 项；✅ 8（Q-1/3/4/5/6/8 + D-T1/D-T4/D-T5）/ 🔶 1（Q-7→W3-F1）/ I-3 静态 ✅ PG 腿待 A1
- 确定性重放含 REV18 bit 级跨 qfq resync 断言；资金守恒 6/6 PASS

## Lessons Learned

1. **「有守恒不变量」不等于「有精度保证」**：NAV=现金+持仓、现金非负是守恒断言，但费用舍入方向（四舍五入/银行家/截断）与长回测累计误差上界是另一回事，须专门断言。float64 在纸交易阶段可接受，但口径要钉住。
2. **闲置能力不是缺陷，是待裁项**：kit/decimal 有牙但零消费者，不主张现在全量换（改动面大、收益不显著），随 X6c 真钱重开再裁——把「采纳触发条件」写明比「现在就用」更诚实。
3. **预取证在等待期顺手真跑**：W3 核心断言在 W2 等待期无库无服务真跑绿，是本轮证据最硬的一波；正确性审查应优先真跑而非静态推断。