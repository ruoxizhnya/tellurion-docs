# ADR-041 · AI 因子工具面：不新造端点，能力未提供就显式「未提供」

- **Status**: Accepted
- **Date**: 2026-11-11
- **Deciders**: 主任（授权本轮按限界上下文 / DDD 判定）
- **Related**: ADR-037（因子值归属）、ADR-028 §6/§11（求值在消费点、不做因子服务）、ADR-032（agent↔core 只走粗粒度动作）、`tellurion-docs:docs/design/ddd-boundary-review-2026-11-11.md` C1/C9/D2

---

## 1. 背景

`tellurion-agent` 的两个工具打向 core 不存在的端点：

- `pkg/ai/client/factor_client.go:51` → `POST /api/factor/compute`（「公式 × 符号」求时序因子值）
- `pkg/ai/client/factor_client.go:93` → `POST /api/factor/evaluate`（同一入参，产出 IC/IR）

`pkg/ai/client/endpoint_contract_test.go:16-19` 自己把这两条登记为「core 无对应端点」的 allowlist，注释写「core 只有 `/api/factor/compute-returns`」。本轮实测：**core 连 `compute-returns` 也没有**。

## 2. 取证（2026-11-11 实测）

| 事实 | 证据 |
|---|---|
| core 只注册两条 factor 路由 | `cmd/analysis/handlers_factor_registration.go:65`（`POST /api/factor/registrations`，治理面）；`cmd/analysis/handlers_proxy.go:167`（`GET /api/factors/:factor_name`，反代 data，已是死链） |
| openapi 只有两条 | `tellurion:docs/openapi.yaml:1126`、`:3185` |
| `compute-returns`/`compute-ic` 只在文档里 | `tellurion:docs/SPEC.md:3197-3210` 列了 5 条 `POST/GET /api/factor/*`，代码与 openapi 均无注册 ⇒ **SPEC 该节是陈旧契约** |
| 语义对不上 | 文档里的 `compute-returns` 是「因子类型 × 交易日」的因子收益/IC 面板；agent 的 `factor.compute` 是「公式 × 符号」的因子值时序。前者既不存在，也不能承载后者 |
| agent 的 allowlist 只防「静默腐烂」 | `endpoint_contract_test.go:64-72` 断言「core 补登记后本行必须删」；它不阻止工具在运行期必失败 |

## 3. 决策

**D1 · 不新造端点。** core 不因为 agent 的工具需要就补 `/api/factor/compute|evaluate`；也不补空壳 `compute-returns` 来让测试变绿。理由：

- 因子求值的目标形态是**消费点 in-process**（ADR-028 §6；ADR-037 D2 对因子值同理），补一个「公式 × 符号」的远程求值面会把 date-loop 内的横截面求值拆成跨服务调用；
- 「公式」是 DSL 表达式，不是已登记因子名；把它开放成 HTTP 面等于把表达式执行器暴露为公网能力，超出 agent↔core 的粗粒度动作边界（ADR-032）；
- 空壳端点会让 agent 的工具「看起来能调」，实际返回错误或空集——这比显式不可用更糟。

**D2 · 语义比对结论：现有能力对不上。** 因此两个工具的状态改为**「该能力当前未提供」**：

- 工具调用返回**结构化、可判定**的错误（稳定错误码 + 文案指向「core 当前无因子求值/IC 求值端点」），不发起 HTTP 请求、不返回空 map、不伪造成功；
- 工具注册表里把这两个工具标注为 `unavailable`（描述里写明原因与替代路径），而不是「可用但总失败」；
- `endpoint_contract_test.go` 的 allowlist 改为**断言显式不可用**：若将来 core 真的提供端点，测试红，逼着重新接线；若有人偷偷把工具改回发请求，测试也红。

**D3 · 保留能对上的那一条。** `compute_factor_ic` 只在语义确实由 core 现有端点承载时才保留；本轮实测后若它同样打向不存在的端点，按 D2 同法处理，不另开例外。

**D4 · 注释与文档同批订正。** `docker-compose.yml` 与 `tellurion-agent:cmd/ai/main.go:100-101` 里「`/api/factor/*` 只在 core 注册」的表述是错误事实的传播源，必须随本 ADR 一起改成「core 只注册 `/api/factor/registrations` 与反代 `/api/factors/:name`；求值面未提供」。`tellurion:docs/SPEC.md` §Factor Analysis 的 5 条陈旧端点同批标注为「历史契约 / 当前未实现」。

## 4. 否决的候选

- **core 补两个粗粒度端点（QT-50 ③-② 的旧方向）**：与 ADR-028 §6「求值在消费点」张力最大，且需要先定义表达式 HTTP 面的鉴权/限额/超时；为一个当前无消费者的实验工具补运行时能力，代价与风险都不成立。否决。
- **路由到 data**：直接违反裁-14 与 dataflow 不变量 7（data 不提供因子读面）。否决。
- **保留工具但静默降级（返回空值）**：这正是 `multi_factor` 那次 409 之前的老毛病——空结果被当作有效结果。否决。
- **删工具**：Copilot 的因子研究链路会少一个入口；显式「未提供」比删除更能保住产品语义与用户预期。否决（作为 D2 的替代保留）。

## 4.1 实施记录（2026-11-11）

- **agent**：`pkg/ai/client/factor_client.go` 的 `ComputeFactor` / `EvaluateFactor` 不再发 HTTP，返回 `ErrFactorCapabilityUnavailable`（含 ADR-041 文案）；两个工具与 `compute_factor_ic` 的 Description 标 `[unavailable]`。`endpoint_contract_test.go` 删除 `clientEndpointGaps` 白名单，改为 `phantomFactorEndpoints` 扫描 + `TestFactorClient_UnavailableWithoutHTTP`（假 server 计数为 0）。
- **core**：`GET /api/factors/:factor_name` 退役为 410 + `factor_http_surface_retired`，不再反代（C8 / `CORE-FACTOR-DEAD-PROXY`）；`docs/SPEC.md` 只保留 `POST /api/factor/registrations` 为现役，5 条陈旧路由标为历史契约。
- **破坏验证**：agent 侧「恢复发 HTTP」⇒ 3 条用例红；core 侧「恢复反代」⇒ 2 条退役用例红；均真做真还原。
- **仍未落地（如实）**：因子求值能力本身**不提供**——这是裁决结果，不是欠账。若真实需求出现，按 §6 重开。

## 5. 后果

1. AI 的因子求值/IC 求值在该栈上**显式不可用**；这是已知且正确的状态，不是回归。
2. 已登记但必失败的工具不再发无谓请求（省时、省日志噪声，错误可归因）。
3. `tellurion:docs/SPEC.md` 的因子端点节已标注「未实现 / 已退役」（2026-11-11，见 §4.1），下一位读者不会再把它当现行契约。

## 6. 重开条件

任一满足才重新接线（且必须新立 ADR 或在本 ADR 追加裁决）：

1. core 真正实现「公式 × 符号」的因子求值面（需同时给出：鉴权、限流、超时、多标的验收；且证明不违背 ADR-028 §6 的分层）；
2. ADR-028 §6 的「因子定义与求值迁往 strategy」落地，strategy 提供稳定的求值 HTTP 面；
3. 出现真实产品需求：Copilot 必须在线做因子求值，且离线替代（提交回测 + 读结果）无法满足。

## 7. 不在本 ADR 范围

- 因子值的生产形态（ADR-037）；
- `factor_returns` / `ic_analysis` 归属（ADR-038）；
- `GET /api/factors/:factor_name` 死链的修复/退役（`tellurion:CORE-FACTOR-DEAD-PROXY`）。
