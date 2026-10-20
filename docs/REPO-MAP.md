---
status: evergreen
last-verified: 2026-10-20
verified-by: 与 core `repo-inventory.md`（仓名唯一源）+ 各仓 `AGENTS.md` / `docs/db-schema.md` 逐条对齐
---

# 仓地图（REPO MAP）

> **一张表回答"这个仓管什么、不管什么、拥有哪块数据"。** 仓名与 module path 的权威定义在 [core `repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md)，本文与它冲突时以那份为准。

| # | 仓 | 类型 | module path | 管什么 | **明确不管** | 拥有 schema | 对外面 | 状态 |
|---|---|---|---|---|---|---|---|---|
| 1 | `tellurion` | 应用（core） | `tellurion` | 回测引擎 / 策略运行时 / 撮合 / 组合结算 / 仪器域存储 / 内核装配 | 不提供 AI 生成能力；不做前端；**不可被任何仓 import** | `quant`（+ 今天还持 `research`、`audit`、遗留 `public.sync_*`） | HTTP + 内嵌前端静态资源 | 生产代码 |
| 2 | `tellurion-contracts` | 库 | `github.com/ruoxizhnya/tellurion-contracts` | port / DTO / 值对象 / 四契约（`RunSpec`·`SignalSpec`·`ResultSpec`·`EngineRunner`）/ 哨兵错误 / abi 常量 | **零实现、零 DB、零配置类型**（`Config`/`Options`/`Impl` 禁入） | 无 | Go package | 占位（S1 落代码） |
| 3 | `tellurion-kit` | 库 | `github.com/ruoxizhnya/tellurion-kit` | logging / errors / id / decimal / statistics / httpclient / httpserver / auth{z} / observability / clock / sandbox / db | **任何业务概念**；**任何表结构**（`db` 只给连接/DSN/迁移执行能力） | 无 | Go package | 占位（S1 落代码） |
| 4 | `tellurion-agent` | 应用 | `tellurion-agent` | AI 实验员：探索循环 / 代码生成 / pipeline / 工具注册表 / 研究域数据自持 | 不在进程内跑引擎；不直连 core 业务表；不逐 bar 远程 | `ai`（目标；今天在 core 的 `quant`+`research`） | HTTP（:8086 缺省） | 生产代码（**过渡态**：仍 `replace ../tellurion`） |
| 5 | `tellurion-ui` | 应用 | —（无 `go.mod`） | 前端：回测 / 数据同步 / 研究 / 风控 / 运维页面 | 不直连 DB；不复制 `openapi.yaml`；不在前端做业务裁决 | 无 | 浏览器 | 生产代码 |
| 6 | `tellurion-data` | 服务 | `tellurion-data` | 数据面唯一入口：connector → 归一化 → 存储 → aggregator；PIT / `visible_at` 守卫 | 不提供逐 bar / 逐笔取数；不做因子**计算**；不存回测结果 | `market` / `ingest` | `/datasets/resolve`、`/datasets/{hash}`、`/factors/{name}@{hash}` | 占位（X1） |
| 7 | `tellurion-strategy` | 服务 | `tellurion-strategy` | 策略**资产**：定义 / 版本（`version_hash`）/ artifact 字节码 / resolve | **不计算信号**；不跑回测；不做参数优化 | `strategy` | 写侧 7 端点 + 读侧 2 端点 | 占位（X2） |
| 8 | `tellurion-risk` | 服务 | `tellurion-risk` | 规则真相源（定义/版本/审批/审计）+ 聚合监控 + 熔断下发 | **同步裁决**（`CheckOrder` 留 core 进程内）；不下单；不碰资金 | `risk` | 规则 5 + 运行 4 + 监控 3 | 占位（X3） |
| 9 | `tellurion-analytics` | 服务 | `tellurion-analytics` | 指标 / 基准 / Brinson 与因子归因 / 敏感性 / 蒙特卡洛 / 报告导出 | 不生产数据；不改回测结果；**不读时钟、不读随机**（`seed` 必填） | `analysis` | 8 端点（2 个异步） | 占位（X4） |
| 10 | `tellurion-orchestration` | 服务 | `tellurion-orchestration` | job 队列 / batch / walkforward / worker 注册 / `run_artifacts` 三 hash 留痕 | **不解释结果**、不重算指标、不做风控裁决；**`run` 是任务域，不含订单/持仓** | `run`（含 `strategy_state` 检查点） | 任务 4 + 批量 4 + 算力 2 + `/provenance` | 占位（X5） |
| 11 | `tellurion-broker` | 服务 | `tellurion-broker` | 交易通道适配（`MockTrader` → `XTPTrader`）：下单/撤单/查单/持仓/成交 | 不做风控判断；不改订单内容（除柜台最小单位换算）；**无对账+幂等+熔断不接真钱**；不做本地交易真相 | 无（订单/成交/持仓在 **core `quant`**；将来建 `exec` 镜像须先立 ADR） | `BrokerGateway` port | 占位（X6） |
| 12 | `tellurion-docs` | 文档 | — | 总体设计 / 跨领域 ADR / 运维指南 / 历史档案 | 不复制服务仓的 db/api/dataflow；不放过期现状数字 | 无 | 本仓 | 现行 |

---

## 依赖方向（只有这些边）

```
kit ← contracts ← core ← (HTTP) ← agent
                     ↑
                     ├── HTTP ── data / strategy / risk / analytics / orchestration / broker
                     └── 版本依赖（require）

ui ──HTTP──► core
```

| 边 | 机制 | 违反的后果 |
|---|---|---|
| `contracts` → `kit` | 编译期 | 编译失败 |
| `core` / `agent` / 服务 → `contracts`(+`kit`) | `require` 版本号 | 出现 `replace` / `go.work` 入库 = CI 红（C1/C2） |
| `agent` / `ui` → `core` | HTTP | 今天 agent 仍编译期依赖 core（S3 消除）；ui 无 Go 依赖 |
| 服务 ↔ 服务 | **无直接边** | 要共用形状 → 进 contracts；要调用 → HTTP |

---

## 状态图例

| 状态 | 含义 |
|---|---|
| **生产代码** | 有真实实现、跑在今天的系统里 |
| **占位** | 有仓、有边界、有 `go.mod` + `doc.go` + 文档，**无实现**；台账出现本仓单号前不写代码 |
| **过渡态** | 已生产，但存在已知违反不变量的地方（必须写清是哪一条） |

---

## 归属待裁的事项

有 4 条归属**没定**（订单是否建 `exec`、`strategy_state` 迁出的 core 侧义务、`eventstore`/`msgbus`、`testenv`/`testutil`）。

> `cmd/dualrun` 已于 2026-10-20 裁决 **留 core**（同进程链接两个内核 + 引擎验收门），不再是待裁项。
它们集中登记在 [core `repo-inventory.md` §3.1](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md)，
**单仓文档里只留指针** —— 否则读者不知道该找谁拍。

---

## 每仓文档入口

每仓都有同一套结构：`AGENTS.md`（行为入口）+ `docs/README.md`（导航）+ `docs/TASKS.md`（本仓台账）+ `docs/ARCHITECTURE.md` + `docs/{db-schema,api-schema,dataflow}.md` + `docs/adr/` + `docs/odr/`。

**逐仓直达链接见 [SERVICE-INDEX.md](SERVICE-INDEX.md)。**
