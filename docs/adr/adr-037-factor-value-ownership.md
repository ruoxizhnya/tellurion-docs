# ADR-037 · 因子值的归属与生产方：消费点按需求值，`factor_cache` 退为可选物化

- **Status**: Accepted
- **Date**: 2026-11-11
- **Deciders**: 主任（授权本轮按限界上下文 / DDD 判定）
- **Related**: ADR-027（模块分解）、ADR-028 §6 与 §11（表达式分层扩展）、ADR-036（服务化目标拓扑）、裁-14（data 不提供因子读面）、`tellurion:docs/TASKS.md` 的 `CORE-FACTOR-CACHE-WRITER`

---

## 1. 背景与问题

`public.factor_cache` 有表、有 DDL、有两个生产读点，但**没有写者**：`multi_factor` 因此在本栈里读不到任何横截面因子，回测只能以「响亮失败」收场（`CORE-FACTOR-GUARD`）。

需要裁决的不是「谁来补一个定时任务」，而是：**因子值是哪个限界上下文的产物，写者该不该存在**。三个候选：

- (a) core 恢复因子预热作业；
- (b) 归 data 提供；
- (c) 消费点按需实时计算。

---

## 2. 取证（全部来自源码与既有裁决）

### 2.1 定义面

- `tellurion:pkg/domain/factor_def_seed.go:29-151`：12 条冻结定义。`momentum = close / ts_delay(close,20) - 1`（`KernelFormula`）、`value = 1 / pe`（`KernelFormula`）、`quality = roe`（`KernelLeaf`）；其余 5 条财报因子是 `KernelCode`，其 `CodeRef` 实现**已随 `pkg/data` 删除**——`tellurion:pkg/mining/registry.go:5` 原文：「code 型因子绑定的 FactorComputer 随 pkg/data 删除」。
- `tellurion:pkg/storage/factor_definition.go`：定义、公式、版本哈希由 core 持久化。
- `tellurion:pkg/expression` 是**唯一的 DSL 语义载体**（字段来源、算子签名、`cs_*` 横截面算子都在这里）；`tellurion:pkg/mining` 只在只读快照上对候选公式求原始值做校验，不做 z-score，也不落库。

### 2.2 值面

- `tellurion:docs/migrations/006_add_factor_cache_table.sql:2-19`：主键 `(symbol, trade_date, factor_name)`，存 `raw_value / z_score / percentile / citation`。
- `tellurion:pkg/storage/cache.go:17-70`：`SaveFactorCacheBatch` 是唯一写入口。全仓 grep 只命中定义自身——**零调用方**，「有表无写者」成立。
- 生产读点只有两处：
  - `tellurion:pkg/backtest/cache/factor_cache.go:245-297` 的 `Warm`（`GetFactorCacheRange` 在 `:261`），按 `(factor, start..warmEnd)` 取全区间装入 run 级 L1；调用点是 `tellurion:pkg/backtest/run_context.go:150-158`。
  - `tellurion:internal/analysisartifact/publisher.go:198-236` 的 `zscoresFor`，按 run 窗口取因子暴露。
- 两个读点的语义都是**某日全市场横截面 z-score**（`map[factor]map[date]map[symbol]z`），不是单标的时序。

### 2.3 外部读面已经断了，且不是本 ADR 造成的

- `tellurion:cmd/analysis/handlers_proxy.go:158-180` 把 `GET /api/factors/:name` 转发到 data 的 `/factors/:name`；data 已在裁-14 撤掉该路由，`tellurion-data/internal/httpapi/server.go:183-186` 原文「不要重新引入」。
- AI 的 `factor.compute` 工具打 core 的 `/api/factor/*`；core 只注册了 `/api/factor/registrations`（`tellurion:cmd/analysis/handlers_factor_registration.go:65`），没有 compute 路由。

### 2.4 既有裁决与文档冲突

- **ADR-028 §6**（`adr-028-tiered-extension-of-strategy-expression-capability.md:418-440`）已经定过目标形态：
  - 因子**定义**住策略服务（与策略定义同级资产）；
  - 因子**求值**在回测引擎 in-process（date-loop 已持全市场当日数据）；
  - 因子**缓存**是纯性能优化，不是架构必需；
  - 「明确不做因子服务——那会把 in-process 的横截面求值变成跨服务调用」。
- **§11 表**（同文件 `:555`）把「因子服务」列入明确不做；重评触发条件是「出现多消费者需要同一份重计算因子且缓存命中率低的**实测证据**」。
- **裁-14 / data 侧 invariant 7**：data 不提供因子读面，`server.go:183-186` 明确要求不要重新引入。
- **冲突**：`tellurion-data/docs/db-schema.md` 的 SPEC-R-02 声称「factor 域 owner = data，core 写入属过渡」。这与裁-14、dataflow invariant 7、以及实际代码（data 无表达式引擎、无因子算法）直接冲突。本 ADR 裁决 `factor_cache` 与内置因子值；`factor_returns` / `ic_analysis` / `factor_hypothesis` 不在本条范围。

---

## 3. 决策

**D1 · `factor_cache` 是分析/研究上下文的读模型（materialized view），不是数据面的资产。**

它的读方（回测 run 预热、分析产物发布）都在 core 这个「仪器单体」内（ADR-036 §2）；定义、公式、语义也都在 core。把「同一概念的定义」和「值」拆到两个上下文各持一半，会让 z-score/validity 口径无法单点维护。

**D2 · 目标生产形态是 (c) 消费点按需实时计算，落在回测 run setup，不新增数据库写者。**

- 用 `pkg/expression` 求值（唯一定义载体），按日做横截面标准化，物化到 **run 级内存**；
- 失败语义保持 `CORE-FACTOR-GUARD` 的响亮失败：必需因子一个有效值都算不出来时，回测拒跑并点名因子与原因；
- 不新增 core 的定时职责，不把 core 从「读多写少的 API 主体」改成批处理系统。

**D3 · `factor_cache` 已退役为遗留表：不得写入，覆盖度门禁不读它（2026-11-12 修订）。**

D2 落地后（见 §8），`public.factor_cache` **没有任何数据库写者，也不再是任何门禁的前置**：

- **不得写入**：`SaveFactorCacheBatch` 全仓零调用方，本 ADR 禁止新增写者；
- **门禁不读它**：覆盖度门禁只读 run 级内存里的按需求值结果（`runContext.factorCoverage`）；
- **空表是预期状态**，不是故障；表中残留行不构成可用因子值；
- 表本身的删除与读面清理（`GetFactorCacheRange` / `Warm` / `Load` 触库腿）另立单 `CORE-FACTOR-CACHE-RETIRE`，见 §8.4。

**D4 · 定义归属按 ADR-028 §6：目标在 strategy，当前在 core 属过渡。**

在定义搬迁完成前，「求值跟定义同仓」——因此按需求值的实现暂时留在 core 的消费点，不构成新的跨仓契约。

**D5 · 不因本 ADR 修改 `multi_factor` 的加权逻辑。**

它按可用因子加权是既有语义；本 ADR 只解决「因子值从哪来」。

---

## 4. 否决的候选

### 4.1 否决 (a) core 恢复因子预热作业

- **领域代价**：把一个**可选的性能物化**升级成 core 的常驻运行职责（调度、幂等、失败重试、PIT 可见性、全市场物化成本）。ADR-028 §6 明确「缓存不是架构必需」，恢复作业等于把可选件变成必需件。
- **事实代价**：5 条 `KernelCode` 因子的实现已随 `pkg/data` 删除（`pkg/mining/registry.go:5`）。恢复作业必须先重写这些 kernel，而本任务的前提是「不改因子数学定义」——重写无法证明与原实现等价。
- **失败语义**：作业没跑会被读成「因子值缺失」，最终仍要靠覆盖度闸兜底；多了一层「看起来有生产方，实际可能没跑」的假象。

### 4.2 否决 (b) 归 data 提供

- **没有算法载体**：data 没有表达式引擎，也没有因子算法；`contracts` 是 DTO/值对象，不是算法（ADR-036 §2）；`kit` 禁止业务概念。
- **只剩两条路，都不可接受**：
  1. 把 `pkg/expression` 抽到 contracts/kit → 跨仓发布耦合，破坏 ADR-036 的 lib 边界；
  2. 在 data 重写 DSL 语义 → **双实现、双真相**，z-score/validity/横截面口径必然漂移。
- **既有裁决不允许**：裁-14 与 dataflow invariant 7 明确 data 不提供因子读面；data 的 `policy.go:86-87` 虽留着 `POST /sync/factors/*` 的策略行，但路由从未注册——这恰好证明 data 从未具备该能力，不是「搬过去就行」。
- **契约撕裂**：定义在 core、值在 data，会让「因子」这个概念跨两个上下文各持一半；ADR-028 §6 已经把定义与求值绑在同一侧。

---

## 5. 后果

1. `multi_factor` 在 2026-11-12 之前「没有预计算缓存」时拒跑；这是**已知且正确**的中间态，不是回归。按需求值已于 2026-11-12 落地（§8），该中间态结束。
2. `GET /api/factors/:name` 是死链（转发到 data 已撤掉的路由）。本 ADR 记录为已知后果；修复（改指向 core 的按需求值或直接退役）不在本条范围。
3. 实现 (c) 有四个必须先设计的卡点，已写入 `CORE-FACTOR-CACHE-WRITER`：
   - `pkg/expression` 的横截面算子只对**最新时点**生效（`evaluator.go:210-257`），`cs_zscore` 不能直接产出时序，必须逐日重算或先算原始序列再逐日标准化；
   - `value/quality` 依赖 `pe/roe`，而引擎只对 `strategy.FundamentalAware` 预热财报（`pkg/backtest/engine.go:1061`），`multi_factor` 不是；需按因子定义的 `InputFields` 触发预热；
   - 单标的横截面 n=1，z-score 无定义——验收必须是多标的、≥60 个交易日；
   - 需对齐 `CaliberZScore`、`Validity` 表达式与 ADR-022 §5 的五元组引用坐标。
4. `factor_cache` 在本轮**不改表结构、不删读点、不加写者**。

---

## 6. 退出条件

**`factor_cache` 可废弃（删表 + 删读点）的条件**（全部满足才可另立单）：

1. (c) 在真栈跑通：多标的、≥60 个交易日，`multi_factor` 返回 `completed` 且 `total_trades > 0`；
2. 按需求值的单次 run 开销有实测数字，且不劣于当前 Warm 路径的可接受阈值（由主任定阈值）；
3. 两个读点（回测 Warm、分析产物 `zscoresFor`）都已改为按需求值或 run 级内存，且破坏验证证明删表后不回退到静默零成交。

**重评「恢复物化」的条件**（ADR-028 §11 的同一触发）：

- 出现**实测证据**表明「多消费者需要同一份重计算因子且缓存命中率低」，届时再评估 (a) 或独立的物化作业；在此之前不恢复写者。

> **2026-11-12 状态**：条件 1 的真栈验收尚未完成（容器镜像尚未重建，真栈仍跑旧代码）；条件 2 无实测数字；条件 3 的两个读点已改（回测门禁 + 按需求值），分析产物 `zscoresFor` 的读点不在本轮范围。因此本轮**只把 `factor_cache` 降为退役遗留、不删表**，删除走 `CORE-FACTOR-CACHE-RETIRE`。


---

## 7. 不在本 ADR 范围

- `factor_returns` / `ic_analysis` 的归属——已由 **ADR-038** 裁决为 core（`factor_hypothesis` 归 agent，代码层已闭合）；
- 因子定义从 core 迁往 strategy 的时间表（ADR-028 §6 已定方向，迁移单另立）；
- `GET /api/factors/:name` 死链的修复；
- `multi_factor` 的加权/阈值逻辑。

---

## 8. 2026-11-12 修订：D2 已实现，D3 降为退役遗留

### 8.1 实现（core 仓，`CORE-FACTOR-CACHE-WRITER`）

- `pkg/backtest/factor_derive.go`：run setup 阶段按策略的 `RequiredFactors()` 求缺失因子；用 `pkg/expression` 逐日求原始序列，再逐日做横截面 z-score（总体标准差，`std == 0` 与 `n < 2` 不出值），物化到 **run 级内存**（`FactorCacheAccessor` 内存容器），**不写库**。
- `warmFundamentalsIfNeeded` 触发条件改为「`strategy.FundamentalAware` **或** 因子定义的 `InputFields` 命中财报字段（`pe/pb/ps/roe/roa/revenue/profit`）」，不再只依赖策略接口。
- 覆盖度门禁 `runContext.factorCoverage` 只读 run 级物化结果；`pkg/backtest/engine.go` 的拒跑文案点名「`public.factor_cache` 是退役遗留表，门禁不读它」。
- 幂等：同一 run 内第二次求值 `MissingFactors` 为空，直接返回，不重算。

### 8.2 为什么不是「写穿缓存落库」

曾有提议「算完顺手写入 `factor_cache`，下次复用」。否决理由（排序即权重）：

1. **不引入第二个写者**——D2 的核心约束是只有消费点算、只有 run 级内存持有；一旦落库就产生了跨进程共享状态，需要并发、失效、PIT 可见性一整套设计。
2. **不留过期缓存**——库里的因子值会随复权、财报更正、定义修订失效，而没有人负责回收。
3. **同一 run 内可复现**——run 级内存与 run 参数同生命周期，天然一致；落库会让「同一 run 重跑」取决于库里当时有什么。

这三条比「少算一次」重要得多：省一次计算换来的是一个新的持久化契约与不确定的过期语义。

### 8.3 门禁口径变更（破坏验证标的）

- 旧口径：读 `public.factor_cache` 判断「有没有因子」。
- 新口径：读 run 级物化结果。
- 破坏验证：把门禁改回读 DB ⇒「物化有值仍放行」的用例失败；摘掉按需求值的接线 ⇒ 多标的 `multi_factor` 回测用例以 409 失败并点名退役表。

### 8.4 遗留表处置

`public.factor_cache` 自本轮起为**退役遗留表**：无写者、门禁不读、空表是预期状态。表的**删除**与读面清理（`pkg/storage` 读写方法、`GetFactorCacheRange`、`Warm`/`Load` 触库腿、迁移语句）**不在本 ADR 内顺手做**，另立单 `CORE-FACTOR-CACHE-RETIRE`（core `docs/TASKS.md`），并要求删表前确认表为空或已备份、迁移可回滚。

### 8.5 重开条件（与 §6 并列）

若将来要求**跨 run 复用**已算好的因子值，或出现外部预计算缓存需被多个 run 消费，则须**重新裁决**因子值的 owner 与物化形态；不得以「恢复 `factor_cache` 写者」作为默认答案。

