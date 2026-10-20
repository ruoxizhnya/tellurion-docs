---
status: evergreen
last-verified: 2026-10-20
verified-by: 10 仓功能边界契约（db / api / dataflow）落地后建立索引；每行与对应仓实际文件核对
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
