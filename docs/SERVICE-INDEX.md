---
status: evergreen
last-verified: 2026-11-07
verified-by: 10 仓功能边界契约（db / api / dataflow）落地后建立索引；每行与对应仓实际文件核对。2026-11-07 DOC-13：新增「六服务 × ADR-036 就绪门 → 工单对照」，30 格逐格 grep 实仓 `###` 标题取证
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

## 六服务 × ADR-036 就绪门 → 工单对照（DOC-13）

> **只索引不复制**：格子里是该仓台账真实存在的 `###` 标题 ID 与行号，正文一律回原仓读。状态符号与标题一致，**🔶/⛔ 不表示已完成**。
> 行号取证日 **2026-11-07**；行号会随台账编辑漂移，判据是 ID 能在 `grep -n '^### <ID>'` 命中，不是行号恒等。

| 仓 | X 阶梯（`SYSTEM-DESIGN.md:123`） | G0 | G1 | G2 | G3 | G4 |
|---|---|---|---|---|---|---|
| `tellurion-data` | X1 · `QT-40`（52） | `SVC-DATA-G0`（29）✅ | `SVC-DATA-G1`（282）✅ | `SVC-DATA-G2`（347）✅ | `SVC-DATA-G3`（43）⬜ | `SVC-DATA-G4`（373）✅ |
| `tellurion-strategy` | X2 · `QT-41`（53） | `SVC-STRAT-G0`（22）✅ | `SVC-STRAT-G1`（308）✅ | `SVC-STRAT-G2`（370）✅ | `SVC-STRAT-G3`（38）⛔ | `SVC-STRAT-G4`（410）🔶 |
| `tellurion-risk` | X3 · `QT-42`（82） | `SVC-RISK-G0`（24）✅ | `SVC-RISK-G1`（664）🔶 | `SVC-RISK-G2`（685）✅ | `SVC-RISK-G3`（73）⬜ | `SVC-RISK-G4`（734）🔶 |
| `tellurion-analytics` | X4 · `QT-43`（55） | `SVC-AN-G0`（22）✅ | `SVC-AN-G1`（374）✅ | `SVC-AN-G2`（396）✅ | `SVC-AN-G3`（40）⛔ | `SVC-AN-G4`（418）✅ |
| `tellurion-orchestration` | X5 · `QT-44`（65） | `SVC-ORCH-G0`（24）✅ | `SVC-ORCH-G1`（39）⛔ | `SVC-ORCH-G2`（215）✅ | `SVC-ORCH-G3`（52）⛔ | `SVC-ORCH-G4`（236）✅ |
| `tellurion-broker` | X6 · `QT-45`（80） | `SVC-BROKER-G0`（22）✅ | `SVC-BROKER-G1`（37）✅ | `SVC-BROKER-G2`（159）✅ | `SVC-BROKER-G3`（65）⛔ | `SVC-BROKER-G4`（200）✅ |

**取证（2026-11-07，逐格实跑，不是抄 ADR 正文）**：`6 仓 × 5 门 = 30` 格**全部**命中各仓台账里真实存在的 `###` 标题，**无缺口格**（DOC-13 立单时“G2 / G4 共 0 条目”的前提已被 2026-10-26 那批立单与后续施工推翻）。实跑命令（PowerShell，等价 `grep -n '^### SVC-' <repo>/docs/TASKS.md`）：

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
foreach ($r in @('tellurion-data','tellurion-strategy','tellurion-risk','tellurion-analytics','tellurion-orchestration','tellurion-broker')) {
  Select-String -Path "c:\Users\ruoxi\Workspace\$r\docs\TASKS.md" -Pattern '^### SVC-'
}
```

命中行号已逐格写进上表；每仓 5 个 ID（G0~G4）齐全，状态的 ✅/⬜/🔶/⛔ 与标题逐字一致（例如 `SVC-RISK-G1` 标题写「代码与文档已落；真实 PG 已补跑，compose 腿未跑」⇒ 记 🔶，不记 ✅）。

**脚注 1 · 同号不同义：「派发块 G4」≠「就绪门 G4」**。表内 G4 列只指 ADR-036 的**可运维就绪门**（失败语义 / 超时重试 / runbook）。六仓台账里另有一套「**派发块 G4**」编号（wave-2 派工块，ADR-0006「服务间角色 `service` 落策略表」），现行出处实测为 `tellurion-risk:docs/TASKS.md:274` 与 `:433`。DOC-13 立单时引的 `tellurion-data:docs/TASKS.md:56-58` 与 `tellurion-strategy:docs/TASKS.md:53` 今天已无「派发块」字样（2026-11-07 在六个服务仓全量检索该词：仅 risk 两处命中），以本脚注两处为现行出处；**施工记录里的「派发块 G4」不得当成就绪验收引用**。

**脚注 2 · `X1~X6` 与 REPO-MAP 状态列的反查**。`SYSTEM-DESIGN.md:123` 的 `X1~X6` 阶梯逐仓对应本表「X 阶梯」列：X1=data / X2=strategy / X3=risk / X4=analytics / X5=orchestration / X6=broker（实测标题 `### QT-40`…`### QT-45` 分别写 X1…X6）。`REPO-MAP.md` §1 六服务行「状态」列里的「G0 已补 / 已实装」等表述，按仓名反查本表该行的 G0~G4 列即可判到门级，**不需要再读服务仓正文**；两边若不一致，以服务仓台账标题为准并回改 REPO-MAP。
