---
status: active
last-verified: 2026-11-12
verified-by: 2026-11-12 W7 文档维护批次：`DOC-FRONTMATTER-HYGIENE`、`DOC-ADR-REQUESTID-CORRECTION`、`DOC-PRODUCT-DRIFT-FIX` 已结案（活跃层 frontmatter 校准 + ARCHITECTURE 转 archived + ADR-001/024 索引标注；adr-017/027/029 追加「机制已定、安装未完成」更正注记；PRODUCT/ROADMAP 接线现状对齐 SYSTEM-DESIGN §4/§5 并清死链）；仅剩 `DOC-P3-MATRIX-TABLE-GRAIN`。此前：2026-11-11 全面审查 W7 台账立单（A5 授权）——新立 4 条知识库维护单（`DOC-PRODUCT-DRIFT-FIX` P1 / `DOC-P3-MATRIX-TABLE-GRAIN` P2 / `DOC-ADR-REQUESTID-CORRECTION` P2 / `DOC-FRONTMATTER-HYGIENE` P3），证据坐标引 ODR-068/069/072（本仓 `docs/archive/odr/`）；本轮只立单不修复。**立单复核三处订正**：① W1-F3 的 REPO-MAP 漂移已被主任 `ad80a3d` 修复 ⇒ DOC-PRODUCT-DRIFT-FIX 收窄到 PRODUCT/ROADMAP；② W2-F11 的 DATA-FUNDAMENTALS-READ-PUBLIC 已被主任归属裁决（data `a454726` 删读面 + core `c85abff`）取代 ⇒ 该 data 单标 ✅ 作废；③ W2-F10 矩阵残留收窄到 REPO-MAP `run.*` 粒度 + core 矩阵 `:43` 行（SYSTEM-DESIGN §5 已对齐）。此前：DOC-10 + DOC-11 + DOC-12 结案（2026-10-26：按第四轮审计订正现状 + ADR-036 服务化定位落档）。此前：DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
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

### DOC-P3-MATRIX-TABLE-GRAIN · 已落归属裁决未对齐进残留矩阵行（run.backtest_results / 因子派生表）[P2] ⬜

- **① 目标**：把两条已落裁决（`run.backtest_results` owner=core；`factor_returns`/`ic_analysis` owner=core per ADR-038）对齐进残留矩阵行，消除「schema 粒度 `run.*`→orch」与「表粒度 `backtest_results`→core」的矛盾。
- **② 上下文**：全面审查 W2-F10（[ODR-069](archive/odr/odr-069-audit-wave2-core-architecture.md)）。**立单复核订正**：ADR-037/038 已落（commit `98a5909`/`448a87a`）；`SYSTEM-DESIGN.md` §5 已对齐（2026-11-11，`public` 行 owner=core）；core `CORE-FACTOR-DERIVED-GUARD` ✅（2026-11-11，因子派生表归 core 的代码 + 缺失原因已改）；fundamentals 行已订正（core 矩阵 `:49`，commit `c85abff`）。**残留实测**：① 本仓 `REPO-MAP.md:15`（core 拥有 schema 列「`quant` + `audit` + …`market.index_daily`」）与 `:24`（orch「`run` 六表」）按 schema 粒度把 `run.*` 全归 orch，**未显式标 `run.backtest_results` owner=core**（表粒度例外；证据 `tellurion:pkg/storage/backtest_results.go:40` CREATE + 矩阵 `:41` 裁决）；② `tellurion:docs/design/qt-decoupling/data-service-contract-and-ownership.md:43` 因子派生表行仍写 `owner = tellurion-data`（与 ADR-038 矛盾）——**该文件在 core，跨仓指针归 core，本仓不代改**。
- **③ 要求**：① REPO-MAP 显式标 `run.backtest_results` owner=core（表粒度例外，附 core `backtest_results.go:40` + 矩阵 `:41` 裁决），不把整张表改成表粒度重写；② 核验 SYSTEM-DESIGN §5 是否已含该例外（已含则只补 REPO-MAP，不重复）；③ core 矩阵 `:43` 行订正归 core（跨仓指针，附 ADR-038；本仓只登记指针不代改 core 文件）；④ 不重新裁决归属（ADR-037/038 已定）。
- **④ 约束与非目标**：不改 core 文件（跨仓指针）；不重新裁决因子/结果表归属；不动已对齐的 SYSTEM-DESIGN §5 正文（只核验）；不改代码。
- **⑤ 验收**：`grep -n "backtest_results" docs/REPO-MAP.md` 显式标 core owner；SYSTEM-DESIGN §5 例外核验记录成文；core 矩阵 `:43` 跨仓指针成文（归 core 施工）；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 `REPO-MAP.md`（+ SYSTEM-DESIGN §5 核验）；core 矩阵 `:43` 行归 core（跨仓指针，附 ADR-038）。
- **owner**：待定

> 除上文外，本仓无其它未做 / 挂起 / 外部依赖项（截至 2026-11-12：W7 立单 4 条中 `DOC-FRONTMATTER-HYGIENE`、`DOC-ADR-REQUESTID-CORRECTION`、`DOC-PRODUCT-DRIFT-FIX` 已结案并归档，其余见上）。跨仓施工任务不在本仓——见 §三指针。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 底座与六服务的施工任务 | `tellurion:docs/TASKS.md` |
| 契约形状与版本纪律 | `tellurion-contracts:docs/TASKS.md` |
| 工具层（鉴权/日志等） | `tellurion-kit:docs/TASKS.md` |
