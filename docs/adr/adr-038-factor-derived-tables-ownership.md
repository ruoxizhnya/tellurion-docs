# ADR-038 · 因子派生表的归属：`factor_returns` / `ic_analysis` 归 core

- **Status**: Accepted
- **Date**: 2026-11-11
- **Deciders**: 主任（授权本轮按限界上下文 / DDD 判定）
- **Related**: ADR-037（因子值的归属与生产方）、ADR-028 §6/§11（因子定义与求值的分层）、ADR-036（服务拓扑）、裁-14（data 不提供因子读面）、`tellurion-docs:docs/design/ddd-boundary-review-2026-11-11.md` C3/D1

---

## 1. 背景与问题

`public.factor_returns` 与 `public.ic_analysis` 物理在 core，写方法在 `tellurion:pkg/storage/cache.go`（`SaveFactorReturnBatch:121`、`SaveICEntryBatch:194`），但**全仓非测试零调用**；`factor_returns` 有一处生产读者（`tellurion:internal/analysisartifact/builder.go:75,205`），`ic_analysis` 的读方法（`cache.go:239`）零调用。ADR-037 只裁了 `factor_cache` 与内置因子值，第 §7 条明确把这两张表列为「不在本 ADR 范围」。

本轮主任已裁决：**两张表归 core**。本 ADR 记录裁决、否决理由与落地边界。

## 2. 事实

| 事实 | 证据 |
|---|---|
| 两表 DDL 在 core | `tellurion:pkg/storage/postgres.go:207-227` |
| 写方法存在、零生产调用 | `tellurion:pkg/storage/cache.go:121-163,194-236`；grep `SaveFactorReturn\|SaveICEntry` 只命中定义自身与测试 |
| `factor_returns` 有一处读者 | `tellurion:internal/analysisartifact/builder.go:75,205` |
| `ic_analysis` 无读者 | `cache.go:239` 零调用 |
| data 仓没有这两张表 | `tellurion-data:internal/schema/schema.go:32-60` 的 `TableNames()` 只有 22 张 `ingest.*`/`market.*` |
| agent 不持分析结果 | agent 自持的只有 `ai.factor_hypothesis`（`tellurion-agent:pkg/aistore/schema.go:46,171`），它是**假设**，不是因子收益/IC |

## 3. 决策

**D1 · owner = core。** 两张表与因子值同源：都是「用 core 的因子定义 + `pkg/expression` 语义 + 行情」派生出来的计算结果。定义、公式、横截面口径都在 core，把值放到别的上下文会让同一个概念各持一半（与 ADR-037 D1 同一条理由）。

**D2 · 沿用 ADR-037 的生产形态：消费点按需求值，不新增数据库写者。**

- `factor_returns` 的真实需求方是 `internal/analysisartifact`（分析产物组装），它在 run 生命周期内已有行情与因子值，可以现场算，不需要先落一张表；
- `ic_analysis` 今天连读者都没有，**不补写者、不补读面**，先按「空语义必须显式」收尾（见 D3），删除与否另立单；
- 因此本 ADR **不引入**新的定时作业、不引入第二套计算实现。

**D3 · 零写者的表必须响亮，不许静默读空。**

`internal/analysisartifact/builder.go:205` 当前在 `GetFactorReturns` 返回空集时继续组装，产出「成功的」分析产物。这与 `CORE-FACTOR-GUARD` 是同一类缺陷：**空集必须要么是显式空语义（产物里明确标注缺失），要么拒产**。落地单见 `tellurion:CORE-FACTOR-DERIVED-GUARD`。

**D4 · 表自身不升格为跨仓契约。** 两张表是 core 的实现细节；analytics 只消费 core 的 run artifact / 报告（ADR-039），不得直连这两张表。

## 4. 否决的候选

### 4.1 否决「归 data，作为派生数据集」

- data **没有算法载体**：它没有表达式引擎，也不做因子计算（`tellurion-data:docs/ARCHITECTURE.md` §2.1、`AGENTS.md` 的「不做策略或因子计算」）；
- 落地只剩两条路：把 `pkg/expression` 抽成跨仓库（违反 ADR-036 的 lib 边界，且让 data 依赖 core 的 DSL 演进），或在 data 重写一遍（**双实现 = 双真相**，IC/收益口径必然漂移）；
- 与裁-14、dataflow 不变量 7（data 不提供因子读面）直接冲突，且 data 的 `TableNames()` 实测零 `factor_*` 表，所谓「迁过去」是从零造。

### 4.2 否决「归 agent」

- agent 是**实验编排层**：它产出假设、发起回测、聚合实验结论，不持有分析真相。`ai.factor_hypothesis` 是「待验证的假设」，`factor_returns`/`ic_analysis` 是「已验证的度量」，两者不是同一个概念；
- agent 的 `factor_returns` 需求可以通过 core 的 run 结果/artifact 读面满足，不需要自己持表；
- 若归 agent，会出现「实验层同时是度量真相源」，与 ADR-023/029 的三层模型（编排 / 能力 / 数据）相反。

### 4.3 否决「升格为 analytics 的 `analysis.*` 表」

analytics 是只读参考实现（ADR-039），它不写回上游、不参与回测；把 factor returns/IC 挪进 `analysis.*` 会让 core 的产物组装跨仓读 analytics，把单向依赖反过来。这是 ADR-0005 明确避免的方向。

## 5. 后果

1. **本轮不改代码、不补写者**。`factor_returns` / `ic_analysis` 仍是「有表无写者」，这是**已知且已裁决**的中间态。
2. 立即要做的只有一件事：把 `analysisartifact` 的静默读空改成显式语义（`CORE-FACTOR-DERIVED-GUARD`，P1）。
3. `ic_analysis` 的删除/保留在 `CORE-FACTOR-DERIVED-GUARD` 收口后另立单，需同时给出迁移（DDL 回滚）与读面退出条件。
4. data / analytics 的文档口径已在本轮订正为 owner=core（见 `docs/design/ddd-boundary-review-2026-11-11.md` §8）。

## 6. 退出条件 / 重开条件

**`factor_returns` 可从「表」退为「现场计算」的条件**（全部满足才另立单）：

1. `analysisartifact` 已改为按需求值，且有多标的 run 的产物对拍证明与表内口径一致（golden fixture）；
2. 单次 run 的额外开销有实测数字，且不劣于读表路径的可接受阈值（阈值由主任定）；
3. 删表后破坏验证证明不会回退到「静默空产物」。

**`ic_analysis` 可删除的条件**：确认无任何读者（含外部报表/手工脚本），且 DDL 回滚脚本与 `docs/SPEC.md` 的表清单同批更新。

**重评「补物化写者」的条件**：出现 ADR-028 §11 的同一实测证据——多消费者需要同一份重计算 IC/收益且按需求值的开销不可接受。

## 7. 不在本 ADR 范围

- `factor_cache` 的归属与退出（ADR-037 已裁）；
- 因子定义从 core 迁往 strategy 的时间表（ADR-028 §6 已定方向）；
- 因子求值 HTTP 面（ADR-041 已裁「不新造端点」）；
- `multi_factor` 的加权逻辑。
