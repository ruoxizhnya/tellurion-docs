---
status: active
last-verified: 2026-11-11
verified-by: 2026-11-11 全面审查 W7 台账立单（A5 授权）——新立 4 条知识库维护单（`DOC-PRODUCT-DRIFT-FIX` P1 / `DOC-P3-MATRIX-TABLE-GRAIN` P2 / `DOC-ADR-REQUESTID-CORRECTION` P2 / `DOC-FRONTMATTER-HYGIENE` P3），证据坐标引 ODR-068/069/072（本仓 `docs/archive/odr/`）；本轮只立单不修复。**立单复核三处订正**：① W1-F3 的 REPO-MAP 漂移已被主任 `ad80a3d` 修复 ⇒ DOC-PRODUCT-DRIFT-FIX 收窄到 PRODUCT/ROADMAP；② W2-F11 的 DATA-FUNDAMENTALS-READ-PUBLIC 已被主任归属裁决（data `a454726` 删读面 + core `c85abff`）取代 ⇒ 该 data 单标 ✅ 作废；③ W2-F10 矩阵残留收窄到 REPO-MAP `run.*` 粒度 + core 矩阵 `:43` 行（SYSTEM-DESIGN §5 已对齐）。此前：DOC-10 + DOC-11 + DOC-12 结案（2026-10-26：按第四轮审计订正现状 + ADR-036 服务化定位落档）。此前：DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
---

# TASKS — tellurion-docs 未完成项

> **归档说明（2026-11-11）**：本文件已瘦身为「只装未做的事」。2026-11-10 及以前已收口（✅）的任务原文、施工记录、验收输出与破坏验证，已逐字移入 [`docs/archive/tasks-archive-2026-11.md`](archive/tasks-archive-2026-11.md)；该文件顶部有「检索索引」表（ID / 标题 / 收口日期 / commit / 证据链接）。检索：`grep -n "<任务ID或commit>" docs/archive/tasks-archive-2026-11.md`。
>
> 状态：`⬜ 待做` / `🔶 进行中` / `⛔ 阻塞（有未解除前置）` / `⏸ 挂起（外部依赖或已裁决暂不实施；**不计入开放项**，重开须另立单并满足该条「重开条件」）` / `✅ 完成（附日期，随即移入归档）`
>
> **本仓台账只放「知识库维护」**：导航、坏链、过时声明、索引补齐。跨仓施工任务不在这里——它们在 `tellurion:docs/TASKS.md`。建单前先问：这件事是不是「改文档结构」？不是就别在本仓建单。

## 一、状态图例

| 标记 | 含义 |
|---|---|
| ⬜ | 未开始 |
| 🔶 | 进行中 |
| ⏸ | 挂起（外部依赖或已裁决暂不实施；重开须满足该条「重开条件」） |
| ✅ | 已完成（保留一行结论，便于追溯） |

## 二、未做 / 挂起 / 外部依赖

### DOC-14 · NT v2.0.0 正式版升级（外部依赖）[P2] ⏸

- **① 目标**：把 `docs/guides/nt-sidecar-operations.md` 的 NT 侧车口径从当前版本升到 NautilusTrader v2.0.0 正式版，并把 `FillTiming` 的对齐要求写进升级验收门。
- **② 上下文**：这条原登记在 `tellurion:docs/TASKS.md` 的「八、跨仓任务索引」，指向本仓 guide，是全系统唯一的外部等待项（上游 NT v2.0.0 正式版尚未发布）。另有一条耦合：`QT-02` 的 `FillTiming` 一旦切换，NT 侧必须同步实现 `next_open`，否则 K15 会报 `ErrFillTimingMismatch`。
- **③ 要求**：① NT v2.0.0 正式版发布后，按 guide 复核侧车启动 / 配置 / 数据契约；② 把 `FillTiming` 对齐检查加进升级验收门；③ 更新 guide 与 `ARCHITECTURE.md` 中 NT 相关的事实性描述（仅版本与行为，不改设计）。
- **④ 约束与非目标**：不提前按 RC 版本改文档；不动 ADR 正文。
- **⑤ 验收**：guide 可照做跑通一次；`FillTiming` 不一致时 K15 报错的路径有用例或明确说明。
- **⑥ 边界**：文档侧升级；NT 适配代码归属以届时立单为准。
- **重开条件**：NautilusTrader v2.0.0 正式版发布，或 `QT-02` 的 `FillTiming` 确认切换。

### DOC-PRODUCT-DRIFT-FIX · 产品入口文档接线现状停在退役波前（PRODUCT/ROADMAP）[P1] ⬜

- **① 目标**：把 `PRODUCT.md` / `ROADMAP.md` 的接线现状对齐到 `SYSTEM-DESIGN.md` 基准（2026-11-11 已对齐），消除退役波后「core 侧零调用方」类过期断言。
- **② 上下文**：全面审查 W1-F3（[ODR-068](archive/odr/odr-068-audit-wave1-product-governance.md)）。**立单复核订正**：原列 `REPO-MAP.md:16,22,25,71` 漂移**已被主任 commit `ad80a3d`（代码-文档对齐审计 2026-11-11）修复**，`SYSTEM-DESIGN.md` §5 亦已对齐 ⇒ 本单不再含 REPO-MAP/SYSTEM-DESIGN。**残留实测**：① `PRODUCT.md:61`「其余四条（策略资产/分析/编排/交易通道）今天连调用方都没有」——strategy（core resolve 出厂启用）/ broker（`SVC-CORE-BROKER-RETIRE` 2026-11-10）/ orchestration（QT-44 真 run）均已接线，analytics 是「有意为 0」（ADR-0005），故该句过期；② `ROADMAP.md:20`「X1~X6 六服务仓已实装但只有 data 一条读链真接线」同过期；③ `ROADMAP.md:18`「QT-32…仍 ⬜」——core QT-32 已收口（2026-11-10 晚）；④ `ROADMAP.md:99`「MockTrader 足够；XTP 是桩（见 `live-trading.md` 标注）」——进程内 MockTrader 已删（`SVC-CORE-BROKER-RETIRE`），且 `live-trading.md` 不存在（死链，实测 `ls` 零命中）。基准 = `SYSTEM-DESIGN.md` §4/§5（2026-11-11）。
- **③ 要求**：① `PRODUCT.md:61` 改为「今天真接线 = data 读链 + strategy resolve + risk resolve（出厂 true）+ broker HTTP（唯一通道）+ orchestration worker；analytics 有意为 0（ADR-0005）」，逐条指 SYSTEM-DESIGN §4/§5、不复制接线数字进角色表；② `ROADMAP.md:20` 删「只有 data 一条读链真接线」，改指 SYSTEM-DESIGN §4 现状；③ `ROADMAP.md:18` QT-32 状态对齐 core 台账（已收口）；④ `ROADMAP.md:99` 删 `live-trading.md` 死链 + MockTrader 表述对齐 broker 退役（XTP 挂起见 `tellurion-broker:docs/adr/0003`）；⑤ 两文件 `last-verified` 更新到施工日。
- **④ 约束与非目标**：不改 REPO-MAP/SYSTEM-DESIGN（已对齐）；不重新裁决产品边界（PRODUCT 哲学层与八条原则不动）；不复制接线数字进角色表（`PRODUCT.md:51` 刻意不复制）；不改代码。
- **⑤ 验收**：`grep -n "连调用方都没有\|只有 data 一条读链" docs/PRODUCT.md docs/ROADMAP.md` 零命中；`grep -n "live-trading.md" docs/ROADMAP.md` 零命中；`python tools/check_doc_links.py` 活跃层 0 断链；PRODUCT/ROADMAP `last-verified`=施工日。
- **⑥ 边界**：本仓 `PRODUCT.md` / `ROADMAP.md`；REPO-MAP/SYSTEM-DESIGN 已对齐不动；接线事实以 SYSTEM-DESIGN §4/§5 + 各仓台账为准。
- **owner**：待定

### DOC-P3-MATRIX-TABLE-GRAIN · 已落归属裁决未对齐进残留矩阵行（run.backtest_results / 因子派生表）[P2] ⬜

- **① 目标**：把两条已落裁决（`run.backtest_results` owner=core；`factor_returns`/`ic_analysis` owner=core per ADR-038）对齐进残留矩阵行，消除「schema 粒度 `run.*`→orch」与「表粒度 `backtest_results`→core」的矛盾。
- **② 上下文**：全面审查 W2-F10（[ODR-069](archive/odr/odr-069-audit-wave2-core-architecture.md)）。**立单复核订正**：ADR-037/038 已落（commit `98a5909`/`448a87a`）；`SYSTEM-DESIGN.md` §5 已对齐（2026-11-11，`public` 行 owner=core）；core `CORE-FACTOR-DERIVED-GUARD` ✅（2026-11-11，因子派生表归 core 的代码 + 缺失原因已改）；fundamentals 行已订正（core 矩阵 `:49`，commit `c85abff`）。**残留实测**：① 本仓 `REPO-MAP.md:15`（core 拥有 schema 列「`quant` + `audit` + …`market.index_daily`」）与 `:24`（orch「`run` 六表」）按 schema 粒度把 `run.*` 全归 orch，**未显式标 `run.backtest_results` owner=core**（表粒度例外；证据 `tellurion:pkg/storage/backtest_results.go:40` CREATE + 矩阵 `:41` 裁决）；② `tellurion:docs/design/qt-decoupling/data-service-contract-and-ownership.md:43` 因子派生表行仍写 `owner = tellurion-data`（与 ADR-038 矛盾）——**该文件在 core，跨仓指针归 core，本仓不代改**。
- **③ 要求**：① REPO-MAP 显式标 `run.backtest_results` owner=core（表粒度例外，附 core `backtest_results.go:40` + 矩阵 `:41` 裁决），不把整张表改成表粒度重写；② 核验 SYSTEM-DESIGN §5 是否已含该例外（已含则只补 REPO-MAP，不重复）；③ core 矩阵 `:43` 行订正归 core（跨仓指针，附 ADR-038；本仓只登记指针不代改 core 文件）；④ 不重新裁决归属（ADR-037/038 已定）。
- **④ 约束与非目标**：不改 core 文件（跨仓指针）；不重新裁决因子/结果表归属；不动已对齐的 SYSTEM-DESIGN §5 正文（只核验）；不改代码。
- **⑤ 验收**：`grep -n "backtest_results" docs/REPO-MAP.md` 显式标 core owner；SYSTEM-DESIGN §5 例外核验记录成文；core 矩阵 `:43` 跨仓指针成文（归 core 施工）；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 `REPO-MAP.md`（+ SYSTEM-DESIGN §5 核验）；core 矩阵 `:43` 行归 core（跨仓指针，附 ADR-038）。
- **owner**：待定

### DOC-ADR-REQUESTID-CORRECTION · adr-027/029/017「request-id 已跨服务传播」断言被证伪，加更正注记 [P2] ⬜

- **① 目标**：给 adr-027/029/017 的「request-id 已跨服务传播」断言加更正注记，承认「机制已有、入站接线未落」，不改写已 Accepted 决策。
- **② 上下文**：全面审查 W5-F3（[ODR-072](archive/odr/odr-072-audit-wave5-security-reliability-deps.md)）。实测断言被证伪：core `RequestIDMiddleware`（`observability/middleware.go:58`）全仓零安装点；kit gin 版有但 6 服务仓全 stdlib mux 装不上；agent 装 `HTTPTransport` 出站但未装 `RequestIDMiddleware` 入站恒空；6 服务仓 `X-Request-ID` 零命中。被证伪的 ADR 断言（实测仍在原文）：`adr-027:1314-1316`「且已有 request-id 跨服务传播」、`adr-029:126-127`「request-id 已跨服务传播」+ `:448`「rid 传播 ✅ 已有」、`adr-017:151`「`request_id` 贯穿 inbound → 下游 HTTP…两件事都已在生产路径上，不是纸面设计」。修复机制归 `tellurion-kit:KIT-REQUESTID-STDLIB` [P1] + 六仓安装（ODR-072）；本单只做文档更正。
- **③ 要求**：① 在 adr-027/029/017 各加一条**更正注记**（追加节，不改写原文）：「机制（`RequestIDMiddleware`/`HTTPTransport`/`WithRequestIDHeader`）已定义，但入站零安装 ⇒ 跨服务传播今天不成立；见 ODR-072 W5-F3 与 KIT-REQUESTID-STDLIB」；② adr-017:146-149 的 OTel/span 重开条件不动（本波只做 correlation-id 不做 tracing）；③ 注记带日期 + 指向 ODR-072。
- **④ 约束与非目标**：**不改写已 Accepted 的 ADR 正文**（ODR 只增不删，更正走注记）；不动 span/trace 重开条件；不在本单做接线施工（归 KIT-REQUESTID-STDLIB + 六仓）；不引入 OpenTelemetry。
- **⑤ 验收**：adr-027/029/017 各有更正注记节（`grep "更正注记"` + `"W5-F3"` 命中）；原断言正文逐字保留（diff 只增不改）；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 adr-027/029/017 注记；接线施工归 `tellurion-kit:KIT-REQUESTID-STDLIB` + 六仓安装（ODR-072）。
- **owner**：待定

### DOC-FRONTMATTER-HYGIENE · frontmatter 过期 / ARCHITECTURE 状态错位 / ADR 索引取代标注 [P3] ⬜

- **① 目标**：补齐/校准本仓文档 frontmatter 卫生，让「没有 `last-verified` 的文档视为已腐烂」这条判据可执行。
- **② 上下文**：全面审查 W1-F5（[ODR-068](archive/odr/odr-068-audit-wave1-product-governance.md)）。实测过期：`TEST.md` `last-verified` 2026-09-25、`PRODUCT.md` 2026-10-25、`VISION.md` 2026-10-25、`ROADMAP.md` 2026-10-26（均 >2 周）；`ARCHITECTURE.md` `status: evergreen` 但本仓 AGENTS §2 目录职责已定它为「拆仓前历史 Reference（不再更新）」⇒ `status` 应 `archived`。**立单复核订正**：原列「等 5 份过期」中 `SYSTEM-DESIGN.md` / `REPO-MAP.md` 已被主任 2026-11-11 刷新（不再过期）；「3 份缺 frontmatter」根层实测仅 `AGENTS_TEMPLATE.md`（模板，可豁免——施工时全仓扫描确认其余）；「ADR.md:43 adr-024 未标部分取代」须施工时以 ADR 正文核验取代关系（ADR-024 对 AI 生成代码部分取代 ADR-001 的 `plugin.Open`，索引是否需补标注以正文为准，不预设结论）。
- **③ 要求**：① TEST/PRODUCT/VISION/ROADMAP 复核内容后更新 `last-verified`（实质漂移随 DOC-PRODUCT-DRIFT-FIX 同批改，本单只校 frontmatter 与状态）；② `ARCHITECTURE.md` `status` evergreen→archived（`type: reference` 保留），确认文件头「历史 Reference」横幅；③ 全仓扫描缺 frontmatter 的活跃层 `.md`，补齐或登记豁免（`AGENTS_TEMPLATE.md` 模板豁免）；④ 核验 `ADR.md` 索引 ADR-001/024 取代关系标注，缺则补（以 ADR 正文为准）。
- **④ 约束与非目标**：不改 ADR 正文（只改 `ADR.md` 索引标注）；不动 SYSTEM-DESIGN/REPO-MAP（已刷新）；不为了过检查器给 `archive/` 加豁免；不改文档实质内容（实质漂移归 DOC-PRODUCT-DRIFT-FIX）。
- **⑤ 验收**：活跃层 `.md` 无缺 frontmatter（豁免除外）；`ARCHITECTURE.md` `status: archived`；TEST/PRODUCT/VISION/ROADMAP `last-verified`≥施工日；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 frontmatter 与 `ADR.md` 索引标注；实质内容漂移归 DOC-PRODUCT-DRIFT-FIX。
- **owner**：待定

> 除上文外，本仓无其它未做 / 挂起 / 外部依赖项（截至 2026-11-11 全面审查 W7 立单：新增 4 条知识库维护单 `DOC-PRODUCT-DRIFT-FIX` / `DOC-P3-MATRIX-TABLE-GRAIN` / `DOC-ADR-REQUESTID-CORRECTION` / `DOC-FRONTMATTER-HYGIENE`，证据坐标引 ODR-068/069/072；本轮只立单不修复）。跨仓施工任务不在本仓——见 §三指针。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 底座与六服务的施工任务 | `tellurion:docs/TASKS.md` |
| 契约形状与版本纪律 | `tellurion-contracts:docs/TASKS.md` |
| 工具层（鉴权/日志等） | `tellurion-kit:docs/TASKS.md` |
