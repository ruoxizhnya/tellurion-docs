---
status: active
last-verified: 2026-11-13
verified-by: 2026-11-13 五角审查批次收口（DOC-17~DOC-29 全部施工完成并移入归档；档 1 文档架构 8 条 / 档 2 产品设计 3 条 / 档 5 文档-代码一致性 2 条；新增 tools/check_doc_counts.py + check_archive_index.py 并接入 CI）。此前：2026-11-13 五角审查立单（只立单不施工）——按 `docs/reviews/2026-11-13/` 分档新立 DOC-17~DOC-24（档 1 · 文档架构与卫生）、DOC-25~DOC-27（档 2 · 产品设计）与 DOC-28~DOC-29（档 5 · 文档与代码一致性），只写台账不改既有文档；DOC-14 维持 ⏸。此前：2026-11-12 挂起任务处置批次（主任指令）——`CORE-MATRIX-FACTOR-OWNER-FIX` ✅ 完成（docs 侧）：核清 core 矩阵 `:43` 在 core HEAD `9858dd6` 仍写 `owner = tellurion-data`（该文件最后触及 `6f2cc24` 只改 fundamentals，未被任何提交修掉）；按 ADR-037 D3 修订 + §8 订正本仓 `SYSTEM-DESIGN.md` §5 `public` 行与 `ARCHITECTURE.md` 两处因子缓存/写入口径（`factor_cache` 退役遗留表、禁止新增写者、门禁不读、按需求值已落地）；core 侧残留行属 core 仓写权，本仓不代改。此前： 2026-11-12 挂起任务处置批次（主任指令）——`DOC-14` 复核维持 ⏸：上游最新 v2.0.0rc9（实测 ls-remote），仍无正式版；本地 clone 过期（2026-10-08）。此前： 2026-11-12 W7 文档维护批次：4 条全部结案（`DOC-FRONTMATTER-HYGIENE` / `DOC-ADR-REQUESTID-CORRECTION` / `DOC-PRODUCT-DRIFT-FIX` / `DOC-P3-MATRIX-TABLE-GRAIN`）——活跃层 frontmatter 校准、ARCHITECTURE 转 archived、ADR-001/024 索引标注、adr-017/027/029 追加更正注记、PRODUCT/ROADMAP 对齐 SYSTEM-DESIGN §4/§5 并清死链、REPO-MAP 与 SYSTEM-DESIGN §5 显式标 `run.backtest_results` 表粒度例外；本批施工中新立 1 条跨仓待派指针 `CORE-MATRIX-FACTOR-OWNER-FIX`。此前：2026-11-11 全面审查 W7 台账立单（A5 授权）——新立 4 条知识库维护单（`DOC-PRODUCT-DRIFT-FIX` P1 / `DOC-P3-MATRIX-TABLE-GRAIN` P2 / `DOC-ADR-REQUESTID-CORRECTION` P2 / `DOC-FRONTMATTER-HYGIENE` P3），证据坐标引 ODR-068/069/072（本仓 `docs/archive/odr/`）；本轮只立单不修复。**立单复核三处订正**：① W1-F3 的 REPO-MAP 漂移已被主任 `ad80a3d` 修复 ⇒ DOC-PRODUCT-DRIFT-FIX 收窄到 PRODUCT/ROADMAP；② W2-F11 的 DATA-FUNDAMENTALS-READ-PUBLIC 已被主任归属裁决（data `a454726` 删读面 + core `c85abff`）取代 ⇒ 该 data 单标 ✅ 作废；③ W2-F10 矩阵残留收窄到 REPO-MAP `run.*` 粒度 + core 矩阵 `:43` 行（SYSTEM-DESIGN §5 已对齐）。此前：DOC-10 + DOC-11 + DOC-12 结案（2026-10-26：按第四轮审计订正现状 + ADR-036 服务化定位落档）。此前：DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
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
- **复核（2026-11-12，挂起任务处置批次，维持 ⏸）**：上游 `git ls-remote --tags origin` 实测最新为 `v2.0.0rc9`（rc7/rc8/rc9 相继发布），**仍无 v2.0.0 正式版**；本地 clone 停在 2026-10-08（tags 至 rc6），是过期镜像不是上游现状，施工时先 fetch。重开条件不变。

### 2026-11-13 五角审查批次（DOC-17~DOC-29）✅ 已收口

> 13 条（档 1 × 8 / 档 2 × 3 / 档 5 × 2）已于 2026-11-13 全部施工完成、逐条 atomic commit；原文与施工记录（含 commit 哈希与证据）移入 [`docs/archive/tasks-archive-2026-11.md`](archive/tasks-archive-2026-11.md) 的「2026-11-13 五角审查批次」节，检索索引同文件 §检索索引。

> 除上文外，本仓无其它未做 / 挂起 / 外部依赖项（截至 2026-11-13：W7 立单 4 条已结案归档；2026-11-13 五角审查批次 DOC-17~DOC-29 已全部结案归档，仅 DOC-14 维持 ⏸）。跨仓施工任务不在本仓——见 §三指针。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 底座与六服务的施工任务 | `tellurion:docs/TASKS.md` |
| 契约形状与版本纪律 | `tellurion-contracts:docs/TASKS.md` |
| 工具层（鉴权/日志等） | `tellurion-kit:docs/TASKS.md` |
