# ADR-036 · 服务化目标拓扑：仓定位、服务就绪门与并行 MVP

- **Status**: Accepted
- **Date**: 2026-10-26
- **Deciders**: 主任
- **Supersedes / amends**:
  - 取代 `repo-inventory.md` §1.2 的「六仓 ≠ 六进程」与「未触发不建仓」；
  - 取代 `ADR-035` §M5 对 risk / analytics / orchestration / broker 的「进程不升」结论；
  - 修订 `ADR-034` §S4「每个服务仓升容器各需一条 ADR」为「本 ADR 作总纲；单服务切读/停写用本仓任务单记录，拓扑再变仍须新 ADR」；
  - 修订 `ADR-027` §2.1「risk 与 engine 同进程」为「**risk 控制面独立服务 + 同步裁决仍留 core 进程内**」；
  - 取代 `tellurion-broker:docs/TASKS.md` 的 **X6d（独立进程）暂缓**裁决：broker 按服务定位，先落 Mock 服务；真实 XTP 仍受 X6c 阻塞；
  - 修订 `docs/design/qt-decoupling/README.md` D1 的「不拆进程」：core 热路径不拆；六个能力服务按其定位拆为进程；K8s 不是必需项。
- **Related**: [第四轮目的对齐审计](purpose-alignment-audit-2026-10-26.md)、[ADR-025](adr-025-auth-exposure-publish-layer.md)、[ADR-032](adr-032-module-topology-and-coarse-grained-edge.md)、[ADR-035](adr-035-repo-inventory-and-naming.md)

---

## 1. 背景

前四轮把「先端口、后进程」作为纪律，结果六个能力仓全部写成了 **服务形状的代码**：有 `cmd/*service`、有自有 schema，但没有 Dockerfile / deploy，core 仍保有全部原实现，只有 data 一条读链真被消费。第四轮审计把这种状态称为「半服务」——既不是合格的服务，也不是 lib。

主任在 2026-10-26 明确目标：

1. **定位为服务，就按 microservice 做**：内部自治、接口明确、自有 deploy、内聚；
2. **定位为 lib，就把工具类与数据类分清**；
3. **平台优先，并行推进**，先把六个服务的 MVP 仓与本地部署补齐，再统一考虑测试与收口；
4. **重复代码必须避免**：先核对既有删除/迁移任务，保证任务与设计一致。

本 ADR 把这三条落成可执行的目标拓扑与验收门。

---

## 2. 决策一：12 仓定位

| 仓 | 定位 | 判定 |
|---|---|---|
| `tellurion` | **仪器单体（monolith）**，不是微服务 | 回测/撮合/结算/策略运行时/热路径留进程内；对外 HTTP 是 API 面，不按微服务拆 |
| `tellurion-agent` | **AI 应用/服务** | 有 `cmd/ai` 与 Dockerfile；需补自有 `config/` 与 `deploy/` |
| `tellurion-ui` | **前端应用** | 有 Dockerfile + `deploy/`（nginx） |
| `tellurion-contracts` | **lib：数据/契约** | 跨进程 DTO、领域值对象、端口接口、错误码、纯规范化函数；**禁止** DB/config/HTTP/工作流 |
| `tellurion-kit` | **lib：工具** | 日志/错误/Decimal/DB/HTTP/鉴权/Clock/ID/可观测性；**禁止**业务概念与表结构 |
| `tellurion-data` | **服务：数据面** | 数据摄取、归一化、PIT、`market.*`/`ingest.*` schema 的唯一 owner |
| `tellurion-strategy` | **服务：策略资产 + 编译** | 资产注册/版本/构建/解析/promote；编译器独立进程 |
| `tellurion-risk` | **服务：风控控制面 + core 进程内裁决** | 服务拥有规则/快照/审计/监控；`RiskPolicy` 的同步裁决**仍在 core 进程内** |
| `tellurion-analytics` | **服务：读侧计算** | 指标/归因/报告/敏感性；只读上游结果，写自己的报告 |
| `tellurion-orchestration` | **服务：运行编排控制面** | 任务队列/租约/worker 注册/artifact 指针；结果面留 core |
| `tellurion-broker` | **服务：交易网关**（MVP = Mock；真钱 = X6c 阻塞） | 订单/撤单/查单/持仓/对账/紧急清仓；HTTP 面待 G1；真实 XTP 仍受 SDK 阻塞 |
| `tellurion-docs` | 文档 | 非代码 |

> **判定规则**：一个仓只能有一个定位。**服务不合格就补到合格，或者降级为 lib/core 模块；不允许长期停留在「半服务」。**

---

## 3. 决策二：服务就绪门（G0~G4）

所有服务仓必须按同一套门验收；**G0（部署）、G1（接口）、G2（数据）可并行**，**G3（切读/停写）按消费者依赖串行**，G4 各服务收口。

| 门 | 内容 | 机械判据 |
|---|---|---|
| **G0 可部署** | 仓内 `Dockerfile` + `deploy/`（compose 片段或 k8s）+ 自有 `config/` + 唯一端口 + 健康检查 | `docker compose config` 通过；单仓可单独起；端口不撞 |
| **G1 有接口** | 版本化 API（OpenAPI 或 contracts）、错误模型、鉴权/授权、幂等、分页/限流 | 契约测试通过；service token 可用；错误码闭合 |
| **G2 有数据** | 自有 schema、迁移、备份；**无跨 schema 写** | 该服务的表只有一个 writer；迁移可重复执行 |
| **G3 有消费者** | core/agent/ui 真调用；旧实现删除或停写 | 客户端代码 + 集成测试；旧路径零调用；删除任务已关 |
| **G4 可运维** | 超时/重试/熔断、失败语义、日志/指标/追踪、回滚 | 故障演练 + runbook；健康/就绪分离 |

**G0 的边界**：`Dockerfile + compose 片段 + 仓内 config` 即满足「自有 deploy」；**不要求 K8s**。K8s 清单只在明确需要时添加，且必须能由该仓自己的 Dockerfile 构建出镜像。

**G2 的边界**：同一个 PG 实例、按 schema 隔离、禁止跨 schema 写，即满足「自有数据」；**不要求每个服务一个物理库**。

---

## 4. 决策三：并行 MVP 的执行方式

1. **G0 并行**：六仓各自补 `Dockerfile` + `deploy/compose.yaml` + `config` + 唯一端口 + 健康检查；根仓提供一份聚合 compose 用于本地联调。
2. **G1/G2 并行**：每个服务在自己的仓内补接口/契约/鉴权与 schema 唯一 owner；互不等待，先把 MVP 服务做完整。
3. **G3 按依赖串行**：切读/停写按消费者价值排序 —— **data → risk → orchestration → strategy → analytics → broker**；前一个服务的旧写入点未归零，不开始下一个服务的 G3。
4. **S1 作为验收场景并行跑**：AI 实验回路只需要 data 读链 + core 引擎 + provenance + promote 闸门；不等待六个服务全部收口。
5. **不许并行制造「半服务」**：任何新能力必须先在该服务的 G1/G2/G3 任务单下开工；G0/G1/G2 可以并行，G3 必须有删除/停写验收。

---

## 5. 决策四：部署与数据归属

### 5.1 部署资产归位

- **每个服务仓自己持有**：`Dockerfile`、`deploy/`、`config/`、迁移入口、健康检查、runbook。
- **core 的 `deploy/` 只留**：analysis / worker / dualrun + 共享基础设施（PG/Redis/Ingress）。
- **本地唯一真相 = compose**；K8s 清单若存在，必须与该仓 Dockerfile 和镜像名一致，否则删除或标 `experimental`。
- 顶层聚合 compose 只做「组合」，不替服务仓定义构建上下文。

### 5.2 数据归属

- 一个 schema 只有一个 owner；服务之间只经 API，不直接写对方的表。
- 双 owner 是**迁移中的临时状态**，不是终态；每个服务 G2 的验收就是「它的表只有它写」。
- 删除/迁移旧实现的**任务必须显式立单**，不能只写「deprecated」；每个服务 G3 必须包含「旧写者归零 + 旧代码删除」。

### 5.3 契约与依赖方向

```
kit（工具，无业务）
  ↑
contracts（数据/契约，无 DB/config/HTTP）
  ↑
core / agent / ui / 六个服务
```

- 任何跨进程形状必须进 `contracts`；仅本服务内部使用的 DTO 可留本仓，但必须在 `api-schema.md` 里成文。
- 服务不得编译期依赖 core；core 不得 import 服务实现；跨服务只走 contracts + HTTP。
- 服务间鉴权统一用 `kit` 的 service token（`v0.1.4+`）。

---

## 6. 决策五：重复代码与旧实现退役

**原则：新服务上线的同一张单里，必须包含旧实现的删除或停写验收。** 不允许「新写一套、旧的留着」。

| 旧实现 | 新归属 | 退役任务 |
|---|---|---|
| core `pkg/data` + `cmd/data` 的行情/同步写路径 | `tellurion-data` | `SVC-CORE-DATA-RETIRE`（G3） |
| core `pkg/backtest/job` / `batch` 的任务创建 | `tellurion-orchestration` | `SVC-CORE-RUN-RETIRE` |
| core `strategies` 表 + 本地注册表 | `tellurion-strategy` | `SVC-CORE-STRAT-RETIRE`（运行时 `pkg/strategy` 保留） |
| core `pkg/risk` 本地规则配置 | `tellurion-risk` 控制面 + core `RiskPolicy` | `SVC-CORE-RISK-RETIRE`（只退役规则源，不退役裁决） |
| core `pkg/backtest/metrics` / `reporting` | `tellurion-analytics` | `SVC-CORE-AN-RETIRE` |
| core `pkg/live` / `pkg/live/broker` | `tellurion-broker` | `SVC-CORE-BROKER-RETIRE`（R4） |
| core `experiments` / `factor_hypothesis` 遗留写方法 | `tellurion-agent` `ai.*` | `SVC-CORE-AI-RETIRE` |

> 既有任务已覆盖的部分（data `X1d` / orchestration `X5b` / broker `R4`）保留原单号，只补「删除代码」的验收；未覆盖的（AI / strategy / risk / analytics / data 代码退役）新增单。

---

## 7. 后果

### 正面

- 六个仓有了明确身份，不再靠「半服务」维持；
- G0/G1/G2 并行能让本地马上跑起来，G3 切读串行防止「新写一套、旧的留着」继续扩散；
- 数据归属与删除任务绑定，能机械判定「重构完成」；
- contracts/kit 的边界更清楚：数据/契约 vs 工具。

### 负面与风险

- 多进程增加网络失败面与运维成本；对单人实验室，必须用 compose + 同 PG 多 schema 控制复杂度，**不引入 mesh/MQ**。
- risk 的同步裁决仍在 core，意味着 risk 不是纯微服务；这是为延迟与 ADR-027 的安全边界保留的**有意例外**。
- broker 服务化会增加每笔一次网络跳；MVP 只接 Mock，真实交易的进程形态须在 X6c 前另立 ADR。
- G0/G1/G2 并行会产生六个待联调的服务；必须在聚合 compose 中固定端口与依赖，否则本地体验会很差。
- G3 串行意味着六个服务的「旧代码删除」不会同时完成；这是有意的，因为切读必须等真实消费者，不能为了并行而制造双写。

### 非目标

- 不接真实 XTP / 真钱；
- 不做 service mesh、MQ、物理库拆分；
- 不把 core 的热路径（回测/撮合/结算）拆成服务；
- 不要求 K8s；
- 不重写 `contracts` / `kit` 的现有公开面。

---

## 8. 验收

1. 六仓均有 `Dockerfile` + `deploy/compose.yaml` + `config`，端口唯一，`docker compose config` 通过；
2. 根仓聚合 compose 能同时起 core（analysis/data/worker）+ agent + 六个服务，端口无冲突；
3. 每个服务至少有一个健康检查路径或 TCP 探针；
4. 六仓 `go.mod` 的 contracts/kit 版本一致（或矩阵登记）；
5. 每张服务单都包含 G0~G4 与「旧实现删除/停写」验收；
6. 文档（REPO-MAP / SYSTEM-DESIGN / 各仓 AGENTS）与定位表一致。

---

## 9. 变更记录

- 2026-10-26：新建。依据主任 2026-10-26 的四条指令与第四轮目的对齐审计；取代/修订 §1 所列条款。

---

## 10. 引用

- `tellurion-docs:docs/SYSTEM-DESIGN.md`
- `tellurion-docs:docs/REPO-MAP.md`
- `tellurion:docs/design/qt-decoupling/purpose-alignment-audit-2026-10-26.md`
- `tellurion:docs/design/qt-decoupling/repo-inventory.md`
- `tellurion:docs/design/qt-decoupling/repo-topology-and-naming.md`
- `tellurion-broker:docs/TASKS.md`（X6d）
- `tellurion-risk:docs/ARCHITECTURE.md` §F4 / §R1