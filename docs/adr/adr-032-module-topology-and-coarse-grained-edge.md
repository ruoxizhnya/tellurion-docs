# ADR-032: 模块拓扑第四/五分之争与跨进程边界 —— domain 独立成 module（已被并入 contracts 取代）· agent↔core 只走粗粒度 HTTP · 策略线先资产后运行时

> **Status**: **Accepted**（原 ADR-D24，若曦裁决 2026-10-19；2026-10-22 由 `tellurion-docs:docs/TASKS.md` DOC-09 升格归档于此）。
> **第 1 条已被替代**（2026-10-20，M1 / D29 §5 订正）：`domain` 不再是独立 module，已并入 `tellurion-contracts/domain`。第 2、3 条不变、仍然生效。
> **Date**: 2026-10-19（裁决）／2026-10-22（升格）
> **Category**: Architecture
> **Supersedes (部分)**: ADR-D9 的四 module 拓扑与「domain 留 core」
> **Superseded-by (部分)**: [ADR-034](adr-034-repo-topology-and-ladder.md)（D29，依赖方向最终形态）· `tellurion:docs/design/qt-decoupling/repo-topology-and-naming.md` §5
> **Related**: [ADR-027](adr-027-modular-decomposition-to-independent-services.md) · [ADR-033](adr-033-carrier-order-m0-market-first.md)（D25，策略线顺序的落地形态）· [ADR-035](adr-035-repo-inventory-and-naming.md)（D30，仓清单）
> **核对（last-verified 2026-10-22）**: 逐条对照现行裁决 —— 依赖方向订正 banner、三值 status 口径（[ADR-031](adr-031-kernel-pluggable-nt-ready.md) K9）、QT-50 的 wire 契约面。源文在 core 仓 [`target-module-topology.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/target-module-topology.md)（ADR-D24 节）与 [`project-engineering-file.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/project-engineering-file.md)。

## Context

拆仓之前必须先回答两件事：**module 怎么分**，以及**跨进程的缝在哪**。

- D9 时期的答案是四 module（`kit` / `contracts` / `core` / `agent`），`domain` 留在 core 里。实测挡住了这条路：`pkg/domain` 17 文件 3,983 行被 **core 306 文件、agent 48 文件**同时使用 —— 一个被两个部署单元同时 import 的类型集合不可能是某个仓的内部件。
- 另一半问题是「AI 实验员要不要直接摸数据」。如果 agent 能逐 bar 远程取数，热路径的延迟预算立刻破产；如果它只能碰粗粒度动作，能力层的存在才有意义（拦住 AI 直接读库）。

## Decision

### 第 1 条 —— `domain` 独立成第五个 module　⚠️ **已被替代，不要照抄**

原文：`domain` 独立为第 5 module，不变量 `kit ← domain ← contracts ← core`。

**现行形态**（2026-10-20 M1 订正 + D29 §5 落地）：`domain` 并入 `tellurion-contracts`，最终不变量是

```
kit ← contracts(含 domain) ← core        agent → kit + contracts（编译期）+ HTTP → core（运行期粗粒度）
```

`contracts → kit` 只允许纯工具（`decimal` / `errors`）；反向边一条都不许有。**module 数从 5 回落到 4**，但这次回落与 D9 的四 module 不是同一个形状：`domain` 进了 contracts 而不是回 core。改判理由与逐仓影响见 [ADR-034](adr-034-repo-topology-and-ladder.md) §依赖方向。

### 第 2 条 —— agent ↔ core 走 HTTP，但**只限粗粒度**（仍然生效）

允许的动作清单（六类，逐字照 D24）：**提交回测 · 批量回测 · 因子求值 · 行情查询 · 策略定义拉取 · 因子登记**。

**禁止**任何 per-bar / per-symbol / per-order 粒度的远程调用；**策略执行、风控裁决、撮合永远在 core 进程内**。

- 判据是延迟预算，不是审美：回测循环里出现一次 HTTP 就是错的。
- 风控同步裁决（`RiskPolicy.CheckOrder`）留在 core 进程内零网络 —— `tellurion-risk` 仓是**规则真相源**，不是裁决的远程调用点。
- ⚠️ **清单今天是六类，不是七类**：「交易日历 / 上市窗口只读 port」这一条第 7 类动作仍是**提案、待若曦确认**（出处：core `project-engineering-file.md` 的「D24 清单缺一类动作」条与 `tellurion-agent:docs/TASKS.md` 的开工前置）。**升格时不得把它写成已定**，`tellurion-agent:AGENTS.md` §3 那句「待 D24 补第 7 类动作」指的就是这个缺口。

### 第 3 条 —— 策略线顺序：先资产服务，后运行时（仍然生效）

策略这条线分两半：**资产**（定义 / 版本 / artifact / resolve）可以做成服务；**运行时**（逐 bar 执行、WASM host）不做成服务、留在 core 进程内。
顺序上先落资产侧（`tellurion-strategy`），运行时不搬。落地形态与 M0 市场级先行见 [ADR-033](adr-033-carrier-order-m0-market-first.md)。

## 后续修订（升格时一并入账，不算新决策）

1. **H2 / QT-50：粗粒度的边一旦跨进程，就必须有 wire 契约**。agent↔core 那条边在拆进程之后就是真 wire，因此 endpoint + DTO 必须落 core 的 `docs/openapi.yaml`（被 `//go:embed` 嵌进二进制、`GET /api/openapi.yaml` 直出），`tellurion-contracts:dto/` 是 oapi-codegen 的**生成物、禁手改**；鉴权按 JWT + RBAC + CORS，insecure 仅限显式配置的 loopback 本地开发（默认 fail-closed）。出处：core [`protocol-and-data-boundary.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/protocol-and-data-boundary.md)。
2. **三值口径与本条的关系**：粗粒度动作的响应判据是 `completed / invalid / failed` 三值（K9 冻结，见 [ADR-031](adr-031-kernel-pluggable-nt-ready.md)）。`invalid` 是一个**结果属性**不是故障，所以它不进 `error` 字段 —— 消费侧（agent / ui）必须能读到 status，不能靠 `invalid_reasons` 反推。这条在 2026-10-22 分别落了 `tellurion-agent`（OBS-01-R2-A）与 `tellurion-ui`（API-01）。

## Consequences

**正面**

- 跨边界的类型有唯一去处（contracts），「两边各写一份理解」在编译期就能被发现。
- 「六类粗粒度动作」是一张可核对的清单：新增一类要走 ADR，不能在代码里悄悄长出来。
- 热路径的边界变成硬约束而不是性能建议：per-bar 远程调用被明文禁止，评审有抓手。

**负面 / 代价**

- 第 1 条的改判让 D24 自身变成「三条里有一条已废」的文档 —— 这正是本 ADR 要就地标注的（照抄历史句会立即写出错的依赖方向）。
- 六类动作清单**不含**日历 / 上市窗口，于是 agent 侧相关工单（QT-17 / 数据自持）在开工前置上挂着一个「等用户确认」的悬项。
- 契约层落码（QT-05）之前 contracts 仓零符号，服务仓拿不到协议类型 ——「粗粒度 HTTP」是目标形态而不是今天的现实，今天 agent 仍编译期依赖 core（过渡例外，S3 收回）。

## 不做（明确排除）

- 不做 per-bar 远程取数（第 2 条的硬否决项）。
- 不在本 ADR 里定 `ai.*` schema 的归属——那是 **D10**（`ai.*` 的 DDL / migrate 归 agent），与 D24 是两条。
  ⚠️ `tellurion-docs:docs/TASKS.md` 的 DOC-09 条目把 D24 描述成「`ai.*` schema 自持」，**那句是 D10 的内容**（源文：core `target-module-topology.md` 的 ADR-D10 节）。升格时按源文实际内容落，D10 未列入本轮四张，另见 DOC-09 尾注。
- 不引入 gRPC / 消息总线承载这条边（QT-50 的 HTTP 粗粒度 + openapi 是唯一 wire 面）。

## 出处

- core：[`docs/design/qt-decoupling/target-module-topology.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/target-module-topology.md)（ADR-D24 节，含 D10 相邻节）
- core：[`docs/design/qt-decoupling/project-engineering-file.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/project-engineering-file.md)（D24 摘要与「清单缺一类动作」条）
- core：[`docs/design/qt-decoupling/repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md) §3.1 / §5（依赖方向最终形态）
- 消费侧落码：`tellurion-agent:docs/TASKS.md` OBS-01-R2-A · `tellurion-ui:docs/TASKS.md` API-01
