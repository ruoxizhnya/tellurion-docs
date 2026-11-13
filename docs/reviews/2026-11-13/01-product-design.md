---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 只读深度审查（角度 1 产品设计）；证据 = 代码/文档 file:line + 只读 git/目录观测
---

# 角度 1 · 产品设计（7.0 / 10）

> 审查范围：12 仓产品定义、领域边界、用例闭环、对外承诺（文档/UI/契约）与实际能力的一致性、设计未落地与落地无人用。
> 方法：全静态只读。未执行构建、测试、服务与数据变更（工作区标注为不可信，禁止执行项目脚本）；文末“实测/推断”一节逐条标注证据强度。
> 相关基线：[PRODUCT.md](../../PRODUCT.md) · [VISION.md](../../VISION.md) · [ROADMAP.md](../../ROADMAP.md) · [REPO-MAP.md](../../REPO-MAP.md)

---

## 1. 评分

| 子维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| 定位与领域边界 | 20% | 9.0 | 一句话定位、角色表、明确不做清单、仓级边界均清晰且可执行；DDD 切分口径（仪器 / 实验员 / 观察窗 / 扩展舱 / 契约底座）自洽 |
| 用例闭环 | 30% | 7.0 | 干预四动作（叫停/指方向/追问/标记）确已端到端落地；但 S1 出口（连续 100 次无人干预）无整链证据，主线闭环仍属“能跑单轮，不能证明可长跑” |
| 对外承诺 vs 实际能力 | 25% | 6.0 | 产业链/宏观后端已实现但 UI 无入口；S1 长跑无证据、S2 因果来源未落地；产品引用的三项测量 API 不在 core 契约；验证器链×5 确已实现（正例） |
| 设计未落地 | 15% | 5.5 | 12 个白名单死包 + stockstate 约 1000 LOC / 6 端点从未注册 + 因子研究页退役为空壳 + 主题切换“开发中” |
| 落地无人用 | 10% | 6.5 | analytics 零调用为有意裁决（可接受）；stockstate、mining、sync、期权、两融等属“建了但无入口”，产品面为零 |
| **加权总分** | 100% | **7.0** | 方向正确、叙事诚实；扣分集中在“主线出口未验收”和“承诺面大于可用面” |

---

## 2. 结论摘要

产品设计层面是这套系统最强的一环：角色、边界、非目标、阶段出口都写成了可判定的句子，且大量“未完成”被主动标注（而不是藏在 backlog 里）。核心问题不是“想错了”，而是**承诺面（尤其产业链/因果）比当前可用面大一个阶段**，同时仓库里沉淀了一批没有入口的能力，使“产品能力”与“可被用户触达的能力”之间出现缺口。

---

## 3. 主要发现（按严重度）

### P1-1 · 主线出口未达成，且缺少整链验收证据

- `ROADMAP.md:18` 明确写：“S1 的出口是「无人干预连续跑完 100 次实验」——**今天尚未达成**”；core/agent 台账均无整链连续运行记录。
- `ROADMAP.md:39-42` 同时显示 S2/S3/S4 均未开始。
- 结论：产品当前处于“单轮可跑、长跑未证”的状态。这是**如实披露**，不算隐瞒；但它意味着 PRODUCT 的核心承诺（“快速、大量、可解释地验证”，`PRODUCT.md:32`）尚未被系统性证明。
- 证据强度：实测（文档原文）。

### P2-1 · 产业链/宏观能力后端已实现，但产品面没有入口

- 先纠正一个容易误判的点：产业链**不是**“只有表”。core 已实现并接线 4 条行业端点（`cmd/analysis/handlers_industry.go:74-77`：tree / edges / vitality / ETF 成分）与宏观序列端点（`cmd/analysis/handlers_macro.go`），装配在 `cmd/analysis/main.go:487`、`:493`；存储层在 `pkg/storage/supply_chain.go:112-284`；契约也在 `docs/openapi.yaml` 的 `/api/industry/*`、`/api/macro/series`。
- 真正的问题是**用户触达面为零**：`tellurion-ui/web/src` 内检索 `industry|macro|产业链` 只命中无关文案（`Alerts.vue:170/233` 的“行业”标签），没有任何页面或 api 模块调用这 5 条端点；`REPO-MAP.md` 也未登记它们（检索零命中）。`PRODUCT.md:71` 把“产业链查询”列为 L2 能力，用户却无处可查。
- 同时 S2 出口要求的 `hypothesis_source` 仍不存在（12 仓 grep 零命中，`ROADMAP.md:40`、`:73`），所以“因果解释”这一层确实未落地。
- 结论：产业链是“建好了、通了、没人用”；因果来源是“确实没做”。两者性质不同，PRODUCT 的现在时表述把前者与后者混在了一起。
- 证据强度：实测（路由/装配/存储/UI 检索）。

### P2-2 · 契约面缺少产品自己引用的测量端点

- `PRODUCT.md:166-168` 把 `POST /api/pipeline/adoption`、`GET /api/pipeline/calibration`、`GET /api/pipeline/experiments/count` 写成“可测”的当前能力；UI 也确实在调用（`tellurion-ui/web/src/api/pipeline.ts`）。
- agent 侧三端点已实现：`tellurion-agent/cmd/ai/handlers_pipeline.go:166-168`。
- 但 core 的 `docs/openapi.yaml` 只登记了 10 条 AI 反代路径（copilot 3 / pipeline 3 / explore 2 / tools 2），**不含 adoption / calibration / experiments/count**。
- 后果：产品承诺的三项成功指标没有出现在 core 的对外契约里；按“core openapi 是前端唯一索引”的既有约定，这是承诺—契约缺口。
- 证据强度：实测（三处代码 + openapi 路径清单）。

### P2-3 · 死能力面积大：产品面前承诺了，运行时不可达

| 项 | 证据 | 性质 |
|---|---|---|
| 12 个“无导入者”包 | `tellurion/internal/repoguard/package_wiring_test.go:72-100`（api / auction / systemalert / margin / options / testutil / id / sandbox runner / staticcheck / strategy monitor / mining / sync） | 已登记为技术债，属“主动保留” |
| stockstate（停牌/退市/强制平仓） | `tellurion/pkg/trading/stockstate/stock_state.go` 455 行 + 测试 556 行；`cmd/analysis/handlers_stock_state.go:50` 定义 6 条路由，但 `main.go` 全仓**没有** `NewStockStateHandler` 调用 | **未登记的完全死代码**（护栏未覆盖“handler 定义了但没接线”这一类） |
| 因子研究页 | `tellurion-ui/web/src/components/factor/FactorCitation.vue:4-10` 自述 410 退役；`navItems.ts:61` 仍保留“因子研究”一级入口 | 有意裁决保留入口，但用户点进去只能读到退役说明 |
| 主题切换 | `tellurion-ui/web/src/components/layout/AppHeader.vue:148` 点击仅弹 `主题切换功能开发中` | 小而真实的未实现控件 |

- 结论：产品“观察窗”承诺的是“5 分钟知道该关注什么”，但当前导航里存在一个只讲“这里曾经有什么”的入口；同时最贴近交易安全的 stockstate 能力完全没有入口。
- 证据强度：实测（代码 + 路由注册缺失）。

### P2-4 · analytics 的“扩展舱”定位与“零消费者”并存

- `PRODUCT.md:58`、`:61` 把 analytics 列为扩展舱；`REPO-MAP.md:23` 与 PRODUCT 同页都注明 core 调用方为 0、属 ADR-0005 的有意裁决。
- 评价：这是**透明地接受的产品冗余**，不算隐瞒；但从用户价值看，一套已实装 8 端点的分析服务目前不进入任何主流程，属于“做了但没人用”的代表项（另一个是 broker 真钱通道，属明确挂起）。
- 证据强度：实测（文档 + core 无调用、gRPC/HTTP 客户端检索未发现调用方）。

### P3-1 · 成功指标的“可测”仍依赖人工与时间

- `PRODUCT.md:164-169` 自评：采纳记录需人工、校准需半年数据、证据覆盖率仍为“部分（JSON Pointer 未实现）”。
- 这与“系统考核指标是校准误差”（`:146`）的目标之间存在时间差：指标管道已通，但**没有数据积累机制/回填策略**的说明。
- 证据强度：实测（文档原文）；“缺少回填策略”为推断（未在 TASKS/ADR 中找到相关条目）。

---

## 4. 正面证据（为什么不给更低分）

1. **非目标写得可执行**：`VISION.md:55-64` 与 `PRODUCT.md:152-158` 明确排除投资建议、实时行情、多 agent 投票、SaaS，并解释理由。
2. **干预闭环真的通了**：agent 的 G1–G4 路由齐全（`tellurion-agent/cmd/ai/handlers_explore.go:220-231`），UI 的 stop/steer/ask/mark 客户端齐全（`tellurion-ui/web/src/api/explore.ts:151-237`），core 只做反代。
3. **验证器链不是 PPT**：`tellurion-agent/pkg/ai/validation/` 下 statistical / economic / robustness / bias / redundancy 五片 + `causal/` 语义维均已实现，并在探索循环里写回裁决（`handlers_explore.go:54-57`、`190-191`）。
4. **产品承诺与实现一致的测量面**：adoption / calibration / experiments count 三端点确已落地（`handlers_pipeline.go:166-168`），且明确“不另立计数表”（同文件 `:17`）。
5. **退役是诚实的**：因子 HTTP 面退役后，UI 不发请求、不显示数值、给出机器码与 ADR 链接（`FactorCitation.vue:4-33`），并有测试钉住“不再撞 410”（`FactorCitation.test.ts:46-51`）。

---

## 5. 建议（仅供决策，不在本次只读范围内实施）

1. 在 `PRODUCT.md` 的 L2/EquityDeep/S2 相关句子上加显式状态标（未落地 / S2），避免“现在时叙事”被读成现状。
2. 把 `adoption` / `calibration` / `experiments/count` 补进 core `openapi.yaml` 的反代索引（或明确声明“测量面以 agent api-schema 为唯一契约”）。
3. 为“handler 定义了但未注册”增加一类 repoguard 断言（当前护栏只覆盖包级无导入者），stockstate 是现成样本。
4. 决定“因子研究”入口的去留：保留则改名为“退役说明/历史”，删除则同步清理导航与路由；现状是产品承诺与页面内容不一致。
5. 对 analytics 给出“何时进入主流程”的重开条件，否则应在产品叙事中降级为“参考实现”而非“扩展舱能力”。

---

## 6. 实测 / 推断分界

| 结论 | 强度 | 依据 |
|---|---|---|
| S1 出口未达成 | 实测 | `ROADMAP.md:18` |
| 产业链后端已实现但无 UI 入口、无 REPO-MAP 登记 | 实测 | `handlers_industry.go:74-77` + `main.go:487/493` + UI 检索零命中 |
| `hypothesis_source` 未实现（S2 未落地） | 实测 | 12 仓 grep 零命中；`ROADMAP.md:40` |
| 三项测量端点已实现但 core 契约缺失 | 实测 | `handlers_pipeline.go:166-168`；`openapi.yaml` 反代段仅 10 条 |
| stockstate 未接线 | 实测 | `handlers_stock_state.go:50`；`main.go` 无 `NewStockStateHandler` |
| 12 个包无导入者 | 实测（护栏自述） | `package_wiring_test.go:72-100` |
| analytics 零调用为有意 | 实测（文档裁决） | `REPO-MAP.md:23`、`PRODUCT.md:61` |
| “缺少回填策略” | 推断 | 文档只写“需半年数据积累”，未检索到回填机制 |
| 产品叙事会让读者误判现状 | 推断（阅读体验判断） | `PRODUCT.md:71/77/103` 使用现在时 |

---

## 7. 未覆盖与限制

- 未执行任何服务、测试、构建或数据查询；因此“实际运行行为”类结论仅来自代码路径与既有测试断言，不等同于真跑证据。
- 未做用户访谈/可用性测试；“5 分钟知道该关注什么”只能从页面结构与 API 覆盖推断，无法实测认知负荷。
- 未核对线上部署实例与 compose 实际状态（属角度 2/3 范围）。
