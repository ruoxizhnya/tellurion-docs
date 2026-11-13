---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 只读深度审查（角度 4 文档-代码一致性）；逐仓对照 go.mod / 路由注册 / openapi / 各仓 docs
---

# 角度 4 · 文档与代码一致性（7.3 / 10）

> 审查范围：12 仓逐仓对照，找“文档写了代码没有”与“代码做了文档没写”。
> 方法：只读。以**代码为基准**核对文档陈述；对每个仓抽查“入口面、版本 pin、路由/端点、探针、页面”。
> 相关基线：[REPO-MAP.md](../../REPO-MAP.md) · [SYSTEM-DESIGN.md](../../SYSTEM-DESIGN.md) · [TEST.md](../../TEST.md) · 各仓 `docs/api-schema.md` / `docs/db-schema.md` / `SERVICE.md`

---

## 1. 评分

| 子维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| core 文档 ↔ 代码 | 25% | 8.0 | 绝大多数陈述可逐条对上；openapi 索引漏登 3 条测量端点；`/api/v1` 只覆盖 legacy 别名 |
| 服务仓文档 ↔ 代码 | 30% | 7.5 | strategy / risk / orchestration / broker / agent / data 的仓内文档总体新鲜且精确；analytics 探针名写错，data 路由计数差 1 |
| contracts / kit | 10% | 9.0 | API surface 文件由 CI 强制（`api-surface.txt` 检查），版本与 tag 对得上 |
| docs 仓中心视图 | 20% | 5.0 | `REPO-MAP` 至少 6 处与当前 go.mod/路由不符；`SYSTEM-DESIGN` 重复写 pin 数字；`TEST.md` 测试读数停在 9 月 |
| 代码→文档覆盖 | 15% | 8.0 | 新能力（industry/macro、evidence、adoption）大多已回写；stock-state 乱码面未登记但本身是死代码 |
| **加权总分** | 100% | **7.3** | “仓内文档”质量高，“跨仓中心视图”明显滞后——两类资产的可信度差了一档 |

---

## 2. 逐仓对照

| 仓 | 文档 → 代码（文档写了但代码没有/不符） | 代码 → 文档（代码有但文档没写/写错） | 结论 |
|---|---|---|---|
| `tellurion` | `openapi.yaml:1519` 声明 AI 四组“唯一完整定义在 agent”，正确；但索引段只列 10 条反代路径，缺 `adoption` / `calibration` / `experiments/count`（`handlers_pipeline.go:166-168`） | `/api/stock-state/*`（`handlers_stock_state.go:50`）无任何文档、且未注册；`GET /api/v1` 索引只列 legacy 别名（`main.go:326-337`） | 基本一致，索引不完整 |
| `tellurion-data` | `api-schema.md:4` 写“路由总数 29→28”、`:123` 写“逐条点名 28 条”；`server.go:125-177` 字面注册 **29** 条（含 `/healthz`、`/readyz`）。差异 1 条，疑为探针是否计入的口径未说明 | 无重大漏写；因子读面已明确退役（`:111`） | 小口径差 1 |
| `tellurion-strategy` | 仓内文档准确（写侧 8 + 公开读侧 5 = 13，`docs/api-schema.md`）；**但** `REPO-MAP.md:21` 仍写“写侧 7 + 读侧 2” | 无 | 仓内对、中心图错 |
| `tellurion-risk` | 仓内 `docs/api-schema.md` 列 13 条（4+3+1+1+1+3）；`REPO-MAP.md:22` 仍写“规则 5 + 运行 4 + 监控 3 = 12” | 无 | 仓内对、中心图错 |
| `tellurion-analytics` | `SERVICE.md:80`、`:100` 写 `GET /health`；代码注册 `/healthz`（`cmd/analyticsservice/main.go`），同仓 `docs/api-schema.md` §4 也写 `/healthz` ⇒ **仓内自相矛盾** | 8 端点与文档一致 | 一处探针名错误 |
| `tellurion-orchestration` | 仓内 `docs/api-schema.md:4` 明确 16 条路由且逐条列出；`REPO-MAP.md:24` 仍写“任务 4 + 批量 4 + 算力 2 + provenance” | 无 | 仓内对、中心图错 |
| `tellurion-broker` | 仓内 `docs/api-schema.md` 与代码一致：8 条业务路由（订单 3 / 账户 4 / 紧急平仓 1）+ `/healthz` + `/version`；`REPO-MAP` 只写“BrokerGateway port + HTTP 面”，未给数，不算错 | 无 | 一致 |
| `tellurion-agent` | `docs/api-schema.md:11` 声明四组契约权威、`:131` 说明 pending 口径；与代码一致 | `README.md:9-11`“单向依赖 core”与 `:31`“零编译依赖”同段出现，读者需读完才知是运行期 HTTP 依赖 | 一致（措辞小瑕） |
| `tellurion-ui` | `docs/ARCHITECTURE.md §3.1` 只登记新增页（compliance / system-admin / walkforward / paper-trading 等 5 行），未声称是全集；README 不写页数 | 20 个页面中多数未在 §3.1 出现，但该节自述“新增页登记于此”，不算漏写 | 一致（增量式登记） |
| `tellurion-contracts` | `api-surface.txt` 由 CI 比对；`CHANGELOG` 与 tag 对齐 | 无 | 一致 |
| `tellurion-kit` | 同上；`go.mod` 不依赖 contracts，`REPO-MAP.md:42` 的“互不依赖”成立 | 无 | 一致 |
| `tellurion-docs` | `REPO-MAP.md:26` 自定规则“不复制服务仓 db/api/dataflow；**不放过期现状数字**”，但本文件 6 处违反；`SYSTEM-DESIGN.md:124/134` 重复写 kit pin 数字，与同文 `:46`“版本 pin 只写在 REPO-MAP”自相矛盾；`TEST.md:438/478/567/585` 与当前 CI/UI 实测不符 | — | 中心视图滞后 |

---

## 3. 主要发现（按严重度）

### P1-1 · `REPO-MAP.md` 作为“仓矩阵唯一现行视图”已与代码脱节 6 处

| 行 | 文档写的 | 代码实测 | 漂移原因（可解释） |
|---|---|---|---|
| `:17` | kit 最新 `v0.3.0`；core pin `v0.3.0`；agent/data/strategy/risk/analytics/orchestration pin `v0.2.0` | 全部 `v0.5.0`（core/agent/data/strategy/risk/analytics/orchestration `go.mod`） | kit 于 2026-11-12 连发 0.4/0.5，未回写 |
| `:18` | agent kit `v0.2.0` | `tellurion-agent/go.mod:12` = `v0.5.0` | 同上 |
| `:20` | data 对外面含 `/factors/{name}@{hash}`；23 张 schema | data `api-schema.md:111` 明确“已撤掉（裁-14）”；`db-schema.md:46` = **25 张** | 数据仓 11-12 的撤面/加表未回写 |
| `:21` | strategy 写 7 + 读 2 | 仓内文档与代码 = 8 + 5 = 13 | 新端点未回写 |
| `:22` | risk “零 import contracts” | `tellurion-risk/go.mod:7` = `contracts v0.10.0`（直接依赖） | 11-12 ADR-040 迁移未回写 |
| `:24` | orchestration “任务 4 + 批量 4 + 算力 2 + provenance” | 仓内 `docs/api-schema.md:4` = 16 条 | worker/artifact 面未回写 |
| `:48` | 重复声明“2026-11-11 实测 go.mod”的旧数字 | 同上 | 与 `:17` 同步腐烂 |

**为什么算 P1**：这不是普通文档，而是所有 agent 与人都依赖的“去哪读什么”的总图，且它自己写了“不放过期现状数字”。一行错会导致 agent 去 core 找已退役的 data 因子端点、按旧版本 pin 升级、或误判 risk 没接契约。注意：这些漂移都发生在 **2026-11-11 之后**，文档在写作时是准的，问题是**没有随 11-12 的依赖/端点变更回写**——属“维护机制缺失”，不是造假。
**证据强度**：实测（逐条 go.mod / 路由 / 文档对照）。

### P1-2 · `TEST.md` 的“测试能力基线”三处与现状相反

- `TEST.md:438`：“CI **不设覆盖率阈值**”——实际 core CI 已有 `-total-min=52 -pkg-min=...=65`（`.github/workflows/ci.yml:144-146`）。
- `TEST.md:478`：前端 `18 个文件 / 208 条`——当日实测 `52 文件 / 643 条`（`reports/test-2026-11-13/w1-ui.log`）。
- `TEST.md:567/585`：e2e `18 spec / 163 例`、`127 passed / 34 failed`——实际 31 spec、当日 `211 passed / 7 failed`。
- frontmatter（`:4`）确实标注了“正文未改，实质基线 2026-09-22”，但 `TEST.md` 是外部读者理解“这个项目怎么测”的入口，正文现在时陈述会被当现状。
- 证据强度：实测（文档 vs CI/日志）。

### P2-1 · analytics `SERVICE.md` 探针名与自家代码/契约互相矛盾

- `tellurion-analytics/SERVICE.md:80`、`:100` 写 `GET /health`；代码实际注册 `/healthz`，同仓 `docs/api-schema.md` §4 也写 `/healthz`。
- 这是唯一一个“仓内两份文档互相打架”的例子；其余仓探针口径与代码一致。
- 证据强度：实测。

### P2-2 · core openapi 是“前端索引”，但漏登了产品仍在使用的 3 条测量端点

- `openapi.yaml:1519` 与 agent `docs/api-schema.md:11` 已对齐：agent 是四组端点唯一权威，core openapi 只是索引。
- 索引实际只列 10 条（copilot 3 / pipeline 3 / explore 2 / tools 2），缺 `POST /api/pipeline/adoption`、`GET /api/pipeline/calibration`、`GET /api/pipeline/experiments/count`（`handlers_pipeline.go:166-168`），而 UI 的 `pipeline.ts` 与 `reviewDesk` 正在调用。
- 这不构成契约冲突（权威在 agent），但会让“只用 core 索引”的前端/脚本发现不了测量面。
- 证据强度：实测。

### P3-1 · 计数口径与小重复

| 项 | 证据 | 说明 |
|---|---|---|
| data 路由 28 vs 29 | `data/docs/api-schema.md:4/123` vs `internal/httpapi/server.go:125-177` | 探针是否计入未说明，差 1 |
| `SYSTEM-DESIGN.md` 重复写 pin | `:124`、`:134` 与 `:46`“只写在 REPO-MAP” | 自定单一处却自己重复 |
| 仓内 `contracts/` 目录 | core 根目录有 5 个 yaml/sql 数据契约文件（tracked） | 与 `tellurion-contracts` 仓同名，易被误读为子模块；建议文档点明“这是数据契约资产，不是 Go 契约仓” |
| UI 页面登记 | `docs/ARCHITECTURE.md §3.1` 只列新增页 | 该节自述增量登记，非缺陷；但“页面总览”仍缺一个全集入口 |

---

## 4. 正面证据

1. **仓内文档精度高**：data / strategy / risk / orchestration / broker / agent 的 `api-schema.md` 普遍带“实现状态 + 日期 + 守卫测试名 + 误差码”，且与代码逐条对得上（orchestration 16 条、risk 13 条、strategy 13 条、broker 8+2）。
2. **core 有意识拒绝抄数字**：`ARCHITECTURE.md:134` 明写“表数与表清单以源码为准，不要引用任何文档里的数字”，并解释“数字一抄就会腐烂”；这解释了为什么 core 文档比 docs 仓更耐用。
3. **契约唯一性写清楚了**：core `openapi.yaml:1519` 与 agent `api-schema.md:11` 一致指向 agent 为四组端点权威，没有出现“双真相”冲突。
4. **退役写成了可验证的负断言**：data `api-schema.md:111` 不仅写“撤掉”，还写“路由表里不存在 ⇒ ServeMux 404”，并有 `TestFactorSyncPolicyIsRetired`、`TestHealthAliasIsRemoved` 钉住。
5. **contracts/kit 的 API surface 由 CI 强制**，不依赖人肉同步。

---

## 5. 建议（仅供决策）

1. 给 `REPO-MAP` 加一条“依赖/端点变更必须同笔回写”的机械门（例如 CI 比对 `go.mod` 的 contracts/kit 版本与 REPO-MAP 表格；或在 contracts/kit 升 tag 的清单里加 REPO-MAP 一项）。
2. 把 `REPO-MAP:20` 的 data 对外面改成 `/datasets/*` + `/api/sync/*` + 兼容只读面，删除已退役的 `/factors/*`。
3. `TEST.md` 要么改成“历史快照（勿引用数字）”，要么把 §6/§7 的读数改为链接到当日日志；当前“正文未改 + 现在时口径”最容易被误读。
4. 修 analytics `SERVICE.md` 的探针名；顺手给 data 的路由计数加一句“含/不含探针”的口径。
5. 把 core openapi 索引补齐 3 条测量端点（或显式写“测量面不在本索引，见 agent api-schema”）。

---

## 6. 实测 / 推断分界

| 结论 | 强度 |
|---|---|
| REPO-MAP 6 处与 go.mod/路由不符 | 实测 |
| TEST.md §6/§7 与 CI/UI 实测不符 | 实测 |
| analytics SERVICE.md 探针名错误 | 实测 |
| core openapi 索引缺 3 条测量端点 | 实测 |
| data 路由 28 vs 29 | 实测（差 1，口径未说明） |
| “维护机制缺失导致漂移” | 推断（依据 11-12 变更时间线） |
| “REPO-MAP 错误会误导 agent” | 推断（影响面判断） |

---

## 7. 未覆盖与限制

- 未逐条核对 12 仓所有文档（每仓抽样 3–6 个高价值断言：入口面、版本 pin、端点、探针、页面）。
- 未核对中文文档中的历史叙述（“2026-10-xx 已落”这类过去时）与代码考古；只核对“现在时陈述”。
- 未核对外部链接有效性（docs CI 有 link check，本审查未复跑）。
