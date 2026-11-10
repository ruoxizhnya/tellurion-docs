---
status: active
last-verified: 2026-10-26
verified-by: DOC-10 + DOC-11 + DOC-12 结案（2026-10-26：按第四轮审计订正现状 + ADR-036 服务化定位落档）。此前：DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
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

> 除上文外，本仓无其它未做 / 挂起 / 外部依赖项。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 底座与六服务的施工任务 | `tellurion:docs/TASKS.md` |
| 契约形状与版本纪律 | `tellurion-contracts:docs/TASKS.md` |
| 工具层（鉴权/日志等） | `tellurion-kit:docs/TASKS.md` |
