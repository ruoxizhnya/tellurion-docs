---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 自上而下五角审查索引；只读审查，未修改业务代码与既有文档；审查阶段未提交，本目录由后续施工会话原样入库（仅把 `file://` 绝对链接规范为相对路径 / 仓 URL）
---

# tellurion 全项目审查 · 2026-11-13

> 范围：12 仓（`tellurion` / `tellurion-data` / `tellurion-broker` / `tellurion-agent` / `tellurion-analytics` /
> `tellurion-orchestration` / `tellurion-risk` / `tellurion-strategy` / `tellurion-ui` / `tellurion-contracts` /
> `tellurion-kit` / `tellurion-docs`）。
>
> 性质：**只读**。审查阶段未修改任何业务代码与既有文档，未提交，未启动破坏性动作；本目录为独立审查产物，不并入既有文档结构，2026-11-13 由施工会话原样入库。
>
> 方法：以代码与 `go.mod` / `openapi.yaml` / 路由注册表为基准，逐项对照文档与台账；每个结论给 `file:line`
> 或命令输出；「实测/查证」与「推断」分列。**未运行** `go test` / `go build` / compose / 浏览器用例
> （工作区被标记为 untrusted，禁止执行其中脚本），因此"真跑证据"只引用仓内已有日志与测试产物。

## 一、五角总分

| 角度 | 分数 | 一句话结论 |
|---|---:|---|
| [1. 产品设计](../../reviews/2026-11-13/01-product-design.md) | **7.0 / 10** | 定位与边界清晰、契约纪律强；但 S1 出口无整链证据，已实现能力（产业链）无 UI 入口，存在死面与"做了没人用" |
| [2. 实现](../../reviews/2026-11-13/02-implementation.md) | **8.0 / 10** | 六条主链真实闭合、零跨服务 import、fail-loud 到位；扣分在死包/死面、地址双默认、超大文件与探针名不统一 |
| [3. 测试](../../reviews/2026-11-13/03-testing.md) | **6.5 / 10** | 单测量大、core 有 DB + `-race` + 覆盖率门；但存在 e2e 409 假绿、7 个服务仓 CI 无 DB、43 处恒跳过、`integration` tag 从未执行 |
| [4. 文档与代码一致性](../../reviews/2026-11-13/04-doc-code-consistency.md) | **7.3 / 10** | 逐仓结构统一、契约指向基本正确；REPO-MAP 6 处漂移、TEST.md 三处反向陈述、analytics 探针名与代码不符 |
| [5. 文档架构与卫生](../../reviews/2026-11-13/05-doc-hygiene.md) | **6.2 / 10** | 单一入口 + R1–R5 + ADR/ODR 双台账设计完整；但入口页 5 处失效、常青文档引用已删除资产、归档索引停在 4 月 |
| **综合（等权平均）** | **7.0 / 10** | **工程实现强于测试，测试强于文档口径；产品承诺落后于已落地能力。** |

> 分数是"相对本项目自身目标"的成熟度判断，不是行业绝对分。等权平均便于横向比较，未按风险加权。

## 二、结论摘要

**这个项目的技术骨架比它的台账更可信。** 六个服务仓与两个库仓的依赖方向、契约 pin、fail-loud 策略、
数据库单写者边界都经得起逐文件核对；回测、数据、策略资产、风控快照、编排、broker 六条主链在代码层
是真实闭合的，不是文档画出来的。实现角度 8.0 分是本次最高的分数，且证据密度最高。

**测试是"数量达标、门禁不达标"。** 单测行数与用例数可观，core 也配了 Postgres service、`-race` 和覆盖率门；
但真正决定交付信号的几处是坏的：e2e 在 409 时只 `t.Logf` 不失败（当日日志显示 409 仍 `PASS`）、
7 个服务仓 CI 没有数据库、43 处 `t.Skip` 在没有 DSN 时恒跳过、`integration` build tag 从未在任何 CI 里执行。
覆盖率门本身也从基线 72.5/82.5 下调到 52/65，说明门是"照着现状画的"，不是"拦住退化的"。

**产品承诺与能力之间有一条稳定的时间差。** 最典型的是产业链：后端 `/api/industry/*`、供应链表、
行业活力与 ETF 成分都已实现并装配（core `handlers_industry.go` + `main.go` + openapi tag "P2-2"），
但 UI 侧零入口、REPO-MAP 未登记、ROADMAP 仍写"待开始"。反过来，`pkg/trading/stockstate`（455 行 + 556 行测试）
与 6 条未注册路由、12 个白名单死包、UI 的因子研究空壳页，是"做了但没人用"的另一半。

**文档的问题不是缺，而是"入口页失真 + 归档层失修"。** 12 仓文档结构统一、服务卡全部落地、
ADR 41 条 / ODR 73 条都有状态列；但唯一入口 [README.md](../../README.md)
仍写 ADR"31 条 / 至 ADR-036"、服务卡"12 仓未落地"、归档 `archive/2026-Q2/*`、CI 缺失"见 TASKS.md P0"，
而 TASKS 里已没有 P0 项。常青文档 SYSTEM-DESIGN 仍让读者去用一份 2026-11-11 已删除的 compose 文件。
归档 `README.md` 的目录树停在 2026-04-11，只覆盖 2/6 子目录，还指向已不存在的 `docs/odr/`。

**如果只修三件事**：① 把 e2e 的"409 仍 PASS"改成失败，并给 7 个服务仓 CI 加 DB 腿；② 把入口页的
五个数字/路径改成脚本生成；③ 给产业链能力补 UI 入口或明确写"仅 API 可用"。这三件事分别对应
"假绿"、"口径失真"、"承诺缺口"，是本次审查中风险最高的三类。

## 三、跨角度最重的十条发现

| # | 角度 | 发现 | 关键证据 |
|---|---|---|---|
| 1 | 测试 | e2e 在 HTTP 409 时只记日志不失败，当日日志仍 `PASS` | `tellurion/e2e/tests/integration_test.go:200-217`；`w3-core-e2e.log` |
| 2 | 产品 | 产业链后端已实现并装配，UI 零入口、台账未登记 | `cmd/analysis/handlers_industry.go:74-77`、`main.go:487/493`、`pkg/storage/supply_chain.go`；UI 检索零命中 |
| 3 | 测试 | 7 个服务仓 CI 无 Postgres，43 处 `t.Skip` 恒跳过；`integration` tag 从未执行 | 各仓 `.github/workflows/*.yml`；`pkg/backtest/router_wiring_integration_test.go:1` |
| 4 | 实现/产品 | `stockstate` 455 行 + 556 行测试不可达：6 条路由未注册 | `handlers_stock_state.go:50`；`pkg/trading/stockstate` |
| 5 | 文档一致性 | REPO-MAP 6 处漂移（kit/agent pin、data 对外面、strategy 端点数、risk 依赖、orchestration 端点数） | `docs/REPO-MAP.md:17/18/20/21/22/24` |
| 6 | 文档卫生 | 常青文档引用已删除的 `docker-compose.services.yml` | `docs/SYSTEM-DESIGN.md:133`；core 仅 `docker-compose.yml` |
| 7 | 文档卫生 | 入口页 5 处失效（ADR 条数、服务卡落地、`archive/2026-Q2`、TASKS P0、ODR 范围） | `docs/README.md:45/50/86/97/101` |
| 8 | 测试 | Playwright 实测 211 通过 / 7 失败 / 2 跳过，与 UI 台账"无未做单"冲突 | `w5-playwright-final.log`；`tellurion-ui/docs/TASKS.md:15` |
| 9 | 产品/实现 | analytics 服务零调用（ADR-0005 有意），但 8 个端点与完整测试仍在维护 | `REPO-MAP.md:23`；ADR-0005 |
| 10 | 文档一致性 | analytics `SERVICE.md` 写 `/health`，代码实际 `/healthz` | `tellurion-analytics/SERVICE.md:80/100` |

## 四、证据可靠性声明

- **实测/查证**：文件内容、行号、`go.mod` pin、路由注册、openapi 路径、目录清单、`grep` 命中数。本次审查的所有
  评分都建立在这一类证据上。
- **推断**：作者意图、某个死面"是否曾经可用"、台账数字为何未同步、读者是否仍在使用归档。报告中均显式标注。
- **未做**：未运行任何构建/测试/服务；"真跑证据"只引用 `tellurion/reports/test-2026-11-13/` 与相关日志的
  既有快照（20:52–21:37 UTC），不代表本次复核时的运行结果。
- **只读边界**：本目录 5 份报告均为新增文件；审查阶段未改动任何业务代码、既有文档或部署配置，未执行 `git commit`（入库动作由后续施工会话完成）。

## 五、本目录文件

| 文件 | 内容 |
|---|---|
| [01-product-design.md](../../reviews/2026-11-13/01-product-design.md) | 产品设计 7.0：定位边界、用例闭环、承诺 vs 能力、设计未落地、落地无人用 |
| [02-implementation.md](../../reviews/2026-11-13/02-implementation.md) | 实现 8.0：六条主链闭合、架构落地、缺陷与耦合 |
| [03-testing.md](../../reviews/2026-11-13/03-testing.md) | 测试 6.5：覆盖、假绿、CI 门禁、证据可靠性 |
| [04-doc-code-consistency.md](../../reviews/2026-11-13/04-doc-code-consistency.md) | 文档与代码一致性 7.3：12 仓逐仓对照 |
| [05-doc-hygiene.md](../../reviews/2026-11-13/05-doc-hygiene.md) | 文档架构与卫生 6.2：导航、过期/重复/矛盾、归档、台账口径 |
