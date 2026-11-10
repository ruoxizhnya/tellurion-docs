---
status: evergreen
last-verified: 2026-11-11
verified-by: 10 仓功能边界契约（db / api / dataflow）落地后建立索引；每行与对应仓实际文件核对。2026-11-07 DOC-13：新增「六服务 × ADR-036 就绪门 → 工单对照」。2026-11-11 代码-文档对齐审计：六服务台账已瘦身（结案条目移入各仓 `docs/archive/`），原「`###` 标题 + 行号」取证方式失效；改为按各仓 `TASKS.md` frontmatter 与 `AGENTS.md` 的收口日期重判每门状态（data G3 2026-11-10、strategy G3/G4 2026-11-10、risk G1/G3/G4 2026-11-10、orchestration G1/G3 2026-11-09、broker G3 ⬜）。
---

# 服务仓功能边界索引（SERVICE INDEX）

> **本页只做索引，不复制内容。** 判断"这个功能该放哪"时：先读本页的「边界一句话」，再点开该仓的 `db-schema`（谁拥有数据）与 `api-schema`（对外承诺什么）；两处都不该收的，就是不该放。
> 链接全部指向各仓 `main` 分支的绝对路径 —— 拆仓后相对路径必断，这是硬约束。

## 底座（两个库）

| 仓 | db（拥有什么表） | api（对外形状） | dataflow | 架构 | 台账 | ADR |
|---|---|---|---|---|---|---|
| `tellurion-contracts` | [db-schema](https://github.com/ruoxizhnya/tellurion-contracts/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-contracts/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-contracts/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-contracts/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-contracts/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-contracts/tree/main/docs/adr) |
| `tellurion-kit` | [db-schema](https://github.com/ruoxizhnya/tellurion-kit/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-kit/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-kit/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-kit/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-kit/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-kit/tree/main/docs/adr) |

- **contracts 边界一句话**：`被 ≥2 个仓使用`且`不含实现`的东西才进；只有一仓用的类型留在那个仓（否则这里会变成公共代码堆放处）。
- **kit 边界一句话**：**业务词零命中**。出现 `backtest` / `strategy` / `order` / `factor` / `market` 就是错，不管多方便。

## 能力服务（六个，触发式）

| 仓 | db（拥有什么表） | api（对外承诺什么） | dataflow | 架构 | 台账 | ADR |
|---|---|---|---|---|---|---|
| `tellurion-data` | [db-schema](https://github.com/ruoxizhnya/tellurion-data/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-data/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-data/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-data/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-data/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-data/tree/main/docs/adr) |
| `tellurion-strategy` | [db-schema](https://github.com/ruoxizhnya/tellurion-strategy/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-strategy/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-strategy/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-strategy/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-strategy/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-strategy/tree/main/docs/adr) |
| `tellurion-risk` | [db-schema](https://github.com/ruoxizhnya/tellurion-risk/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-risk/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-risk/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-risk/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-risk/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-risk/tree/main/docs/adr) |
| `tellurion-analytics` | [db-schema](https://github.com/ruoxizhnya/tellurion-analytics/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-analytics/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-analytics/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-analytics/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-analytics/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-analytics/tree/main/docs/adr) |
| `tellurion-orchestration` | [db-schema](https://github.com/ruoxizhnya/tellurion-orchestration/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-orchestration/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-orchestration/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-orchestration/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-orchestration/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-orchestration/tree/main/docs/adr) |
| `tellurion-broker` | [db-schema](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-broker/tree/main/docs/adr) |

| 仓 | 边界一句话 | **不该放这里的东西** |
|---|---|---|
| `tellurion-data` | 数据面的唯一入口：connector → 归一化 → 存储 → aggregator；`visible_at` 缺失即拒收 | 逐 bar / 逐笔取数；因子**计算**；回测结果存储 |
| `tellurion-strategy` | 策略**资产**（定义 / 版本 / artifact），**资产 ≠ 运行时** | 信号计算；回测执行；参数优化 |
| `tellurion-risk` | 规则真相源 + 聚合监控 + 熔断下发 | 逐笔同步裁决；下单；资金操作 |
| `tellurion-analytics` | 纯函数只读：指标 / 归因 / 敏感性 / 蒙特卡洛（`seed` 必填） | 生产数据；改回测结果；无 `seed` 的随机 |
| `tellurion-orchestration` | 只派活不裁决：job 队列 / batch / walkforward / worker 注册 | 结果解释；指标重算；风控裁决 |
| `tellurion-broker` | 通道适配：`BrokerGateway` 的五个方法 | 风控判断；改订单内容；明文密钥 |

## 应用与文档

| 仓 | db（拥有什么表） | api（对外承诺什么） | dataflow | 架构 | 台账 | ADR |
|---|---|---|---|---|---|---|
| `tellurion`（core） | —（core 自持 `quant`；表与字段见 [SPEC](https://github.com/ruoxizhnya/tellurion/blob/main/docs/SPEC.md)） | [openapi.yaml](https://github.com/ruoxizhnya/tellurion/blob/main/docs/openapi.yaml) | — | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) | [ADR-D 索引](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/README.md)（core 无独立 `docs/adr/`） |
| `tellurion-agent` | [db-schema](https://github.com/ruoxizhnya/tellurion-agent/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-agent/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-agent/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-agent/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-agent/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-agent/tree/main/docs/adr) |
| `tellurion-ui` | [db-schema](https://github.com/ruoxizhnya/tellurion-ui/blob/main/docs/db-schema.md) | [api-schema](https://github.com/ruoxizhnya/tellurion-ui/blob/main/docs/api-schema.md) | [dataflow](https://github.com/ruoxizhnya/tellurion-ui/blob/main/docs/dataflow.md) | [ARCHITECTURE](https://github.com/ruoxizhnya/tellurion-ui/blob/main/docs/ARCHITECTURE.md) | [TASKS](https://github.com/ruoxizhnya/tellurion-ui/blob/main/docs/TASKS.md) | [adr](https://github.com/ruoxizhnya/tellurion-ui/tree/main/docs/adr) |

---

## 三份契约怎么用（判断"放哪"的操作顺序）

1. **它有表吗** → 打开候选仓的 `db-schema.md` §1：表在这一仓，数据就归它写；两个仓都想写 = 边界没画完。
2. **它对外承诺什么** → `api-schema.md` §1 与 §5（"不提供什么"）。§5 往往比 §1 更有用：被明确排除的，就是别处该收的。
3. **它要不要在热路径上** → `dataflow.md` 的 fail-closed 点。凡是逐 bar / 逐笔 / 裁决，回 core。
4. **四处都对不上** → 要么是**新边界**（先立 ADR，再改这三份文件，再写代码），要么是**该留在 core**。不要先写代码再补文档。

---

## 六服务 × ADR-036 就绪门 → 工单对照（DOC-13，2026-11-11 重判）

> **取证方式已变**：2026-11-11 起六个服务仓的 `docs/TASKS.md` 已瘦身为「只装未做的事」，
> 已收口的 `### SVC-*` 标题连同施工记录整体移入各仓 `docs/archive/`（归档顶部有
> 「ID / 标题 / 收口日期 / commit / 证据」检索索引）。因此**不能再靠
> `grep -n '^### <ID>' docs/TASKS.md` 判状态**；状态改由各仓 `TASKS.md` frontmatter 的
> 收口摘要 + `AGENTS.md` 的状态段判定，证据回 `docs/archive/` 按 ID 查。

| 仓 | X 阶梯（`SYSTEM-DESIGN.md` §7） | G0 | G1 | G2 | G3 | G4 |
|---|---|---|---|---|---|---|
| `tellurion-data` | X1 · `QT-40` | ✅ | ✅ | ✅ | ✅ 2026-11-10 | ✅ |
| `tellurion-strategy` | X2 · `QT-41` | ✅ | ✅ | ✅ | ✅ 2026-11-10 | ✅ 2026-11-10（真 PG + 停服演练） |
| `tellurion-risk` | X3 · `QT-42` | ✅ | ✅ 2026-11-10 | ✅ | ✅ 2026-11-10 | ✅ 2026-11-10 |
| `tellurion-analytics` | X4 · `QT-43` | ✅ | ✅ | ✅ | **关闭**（ADR-0005，2026-11-10；`K7` 挂起 — 非未完成） | ✅ |
| `tellurion-orchestration` | X5 · `QT-44` | ✅ | ✅ 2026-11-09 | ✅ | ✅ 2026-11-09 | ✅ |
| `tellurion-broker` | X6 · `QT-45` | ✅ | ✅ | ✅ | ⬜（开放；不影响 Mock 通道） | ✅ |

**读法**：
- ✅ = 该门已收口且有真库/端到端证据（日期为收口日）；⬜ = 仍未做；「关闭」= 经裁决不再实施，不是没做。
- `tellurion-broker` 的 `X6c`（真实 XTP）仍 ⏸，重开条件 P1~P5 写在 broker `docs/TASKS.md`；**`G3 ⬜` 与 `X6c ⏸` 是两件事**，前者是 HTTP 面/部署腿的剩余项，后者是真钱通道。
- 六仓的「G3」都不是「切读完成度」的统一口径：data 的 G3 是 core `cmd/data` 停写并删除，risk 的 G3 是 core 走 `resolve` 快照（`SVC-CORE-RISK-RETIRE`），orchestration 的 G3 是 core 裸表 `backtest_jobs` 退役。**判据看各仓归档里的验收输出，不看门号**。

**脚注 1 · 同号不同义：「派发块 G4」≠「就绪门 G4」**。表内 G4 列只指 ADR-036 的**可运维就绪门**（失败语义 / 超时重试 / runbook）。六仓台账里另有一套「**派发块 G4**」编号（wave-2 派工块，ADR-0006「服务间角色 `service` 落策略表」），现行出处为 `tellurion-risk` 台账 / 归档里的派工块条目。**施工记录里的「派发块 G4」不得当成就绪验收引用**。

**脚注 2 · `X1~X6` 与 REPO-MAP 状态列的反查**。`SYSTEM-DESIGN.md` §7 的 `X1~X6` 阶梯逐仓对应本表「X 阶梯」列：X1=data / X2=strategy / X3=risk / X4=analytics / X5=orchestration / X6=broker（`QT-40`…`QT-45`）。`REPO-MAP.md` §1 六服务行「状态」列按仓名反查本表该行即可判到门级；两边若不一致，以服务仓台账/归档为准并回改 REPO-MAP。
