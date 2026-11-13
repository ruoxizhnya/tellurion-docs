---
status: active
last-verified: 2026-11-13
verified-by: 2026-11-13 五角审查立单（只立单不施工）——按 `docs/reviews/2026-11-13/` 分档新立 DOC-17~DOC-24（档 1 · 文档架构与卫生）、DOC-25~DOC-27（档 2 · 产品设计）与 DOC-28~DOC-29（档 5 · 文档与代码一致性），只写台账不改既有文档；DOC-14 维持 ⏸。此前：2026-11-12 挂起任务处置批次（主任指令）——`CORE-MATRIX-FACTOR-OWNER-FIX` ✅ 完成（docs 侧）：核清 core 矩阵 `:43` 在 core HEAD `9858dd6` 仍写 `owner = tellurion-data`（该文件最后触及 `6f2cc24` 只改 fundamentals，未被任何提交修掉）；按 ADR-037 D3 修订 + §8 订正本仓 `SYSTEM-DESIGN.md` §5 `public` 行与 `ARCHITECTURE.md` 两处因子缓存/写入口径（`factor_cache` 退役遗留表、禁止新增写者、门禁不读、按需求值已落地）；core 侧残留行属 core 仓写权，本仓不代改。此前： 2026-11-12 挂起任务处置批次（主任指令）——`DOC-14` 复核维持 ⏸：上游最新 v2.0.0rc9（实测 ls-remote），仍无正式版；本地 clone 过期（2026-10-08）。此前： 2026-11-12 W7 文档维护批次：4 条全部结案（`DOC-FRONTMATTER-HYGIENE` / `DOC-ADR-REQUESTID-CORRECTION` / `DOC-PRODUCT-DRIFT-FIX` / `DOC-P3-MATRIX-TABLE-GRAIN`）——活跃层 frontmatter 校准、ARCHITECTURE 转 archived、ADR-001/024 索引标注、adr-017/027/029 追加更正注记、PRODUCT/ROADMAP 对齐 SYSTEM-DESIGN §4/§5 并清死链、REPO-MAP 与 SYSTEM-DESIGN §5 显式标 `run.backtest_results` 表粒度例外；本批施工中新立 1 条跨仓待派指针 `CORE-MATRIX-FACTOR-OWNER-FIX`。此前：2026-11-11 全面审查 W7 台账立单（A5 授权）——新立 4 条知识库维护单（`DOC-PRODUCT-DRIFT-FIX` P1 / `DOC-P3-MATRIX-TABLE-GRAIN` P2 / `DOC-ADR-REQUESTID-CORRECTION` P2 / `DOC-FRONTMATTER-HYGIENE` P3），证据坐标引 ODR-068/069/072（本仓 `docs/archive/odr/`）；本轮只立单不修复。**立单复核三处订正**：① W1-F3 的 REPO-MAP 漂移已被主任 `ad80a3d` 修复 ⇒ DOC-PRODUCT-DRIFT-FIX 收窄到 PRODUCT/ROADMAP；② W2-F11 的 DATA-FUNDAMENTALS-READ-PUBLIC 已被主任归属裁决（data `a454726` 删读面 + core `c85abff`）取代 ⇒ 该 data 单标 ✅ 作废；③ W2-F10 矩阵残留收窄到 REPO-MAP `run.*` 粒度 + core 矩阵 `:43` 行（SYSTEM-DESIGN §5 已对齐）。此前：DOC-10 + DOC-11 + DOC-12 结案（2026-10-26：按第四轮审计订正现状 + ADR-036 服务化定位落档）。此前：DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
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

### 2026-11-13 五角审查立单（只立单，不施工）

> 来源：`docs/reviews/2026-11-13/`（`index.md` + 五个角度）。本轮按审查推进顺序分档落单，**只写台账，不改既有文档**；沿用六字段与既有状态图例。每条标题下的「档 / 来源 / 顺序 / 依赖」行为施工顺序与跨仓指向。完成后按惯例移入归档。

#### 档 1 · 文档架构与卫生

### DOC-17 · 入口页五项失效目标一次性校准 [P1] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H1 · 顺序 1-1 · 依赖：无

- **① 目标**：把 `docs/README.md` 主入口上 5 处指向"不存在 / 已变化"对象的表述改为实测现状。
- **② 上下文**：审查实测证据——`README.md:101` 指 `archive/2026-Q2/*`（实际为 `archive/reports-2026-Q2/` 与 `archive/research-2026-Q2/`）；`:86` 写"文档链接 CI 当前缺失，见 TASKS.md P0"（台账已无 P0）；`:50` 写服务卡"12 仓未落地"（12 份 `SERVICE.md` 全部存在）；`:45` 写 ADR"31 条；编号至 ADR-036"（实际 41 条、至 ADR-041，见 `ADR.md:195`）；`:97` 写归档 ODR"001–064"（实际 73 份，至 ODR-073），且 superseded 列表漏 ADR-022。
- **③ 要求**：逐项改为实测值：① 归档路径改两个真实子目录；② CI 句改为"链接检查已进 CI（`.github/workflows/docs-ci.yml`）"并删 P0 指引；③ 服务卡改"12 仓已落地"；④ ADR 改"41 条、至 ADR-041"；⑤ ODR 改"001–073"，superseded 补 ADR-022。
- **④ 约束与非目标**：只改入口页事实；不重排导航结构；不动归档正文与 ADR 正文。
- **⑤ 验收**：5 处逐一核对为真值；`grep -n "31 条\|001–064\|archive/2026-Q2" docs/README.md` 0 命中；文档链接检查 CI 绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/README.md`。

### DOC-18 · 入口页关键计数改为脚本校验 + 落实 R5 文档可验证 CI [P2] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H1 建议 1 + 评分表「R5 自述缺失」 · 顺序 1-2 · 依赖：DOC-17（先校准，避免校验固化错值）

- **① 目标**：ADR 条数 / ODR 范围 / 服务卡覆盖 / 归档目录清单由脚本校验（或生成），并把 R5 写回治理规则。
- **② 上下文**：H1 的根因是手写数字无校验；仓库已有 `scripts/check_doc_links.py` 的 CI 接入模式可扩展；R5"文档可验证 CI"在评分表中被记为自述缺失且台账无开放项。
- **③ 要求**：① 扩展/新增文档校验脚本：比对 `ADR.md` 条数与 `adr-0*.md` 文件数、`archive/odr/` 范围、12 仓 `SERVICE.md` 存在性、`README.md` 计数段落；② 接入 docs CI；③ `README.md` 治理节把"R5 缺失"改为"由脚本校验（命令/CI 位置）"。
- **④ 约束与非目标**：不引入新依赖；不改其他仓 CI；只读其他仓文件做存在性校验；本轮不追求自动改写。
- **⑤ 验收**：人为改错一处计数 → CI 红；逐字节还原 → 绿（破坏验证）；台账/README 不再出现"R5 缺失"。
- **⑥ 边界**：`tellurion-docs` 的 `scripts/`、`.github/workflows/docs-ci.yml`、`docs/README.md`。

### DOC-19 · SYSTEM-DESIGN 部署句改指 core `docker-compose.yml` [P1] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H2 · 顺序 1-3 · 依赖：无

- **① 目标**：删除常青文档对已删除部署资产的引用。
- **② 上下文**：`SYSTEM-DESIGN.md:133` 写"本地联调走 `docker-compose.services.yml`"；core 实测只剩 `docker-compose.yml`，core `ARCHITECTURE.md` frontmatter 记录 2026-11-11 已删 `.services.yml`/`.e2e.yml`/`.nt.yaml` 三份。
- **③ 要求**：§5 部署句改为 `tellurion:docker-compose.yml` + profile；全文扫 `.services.yml`/`.e2e.yml`/`.nt.yaml` 残留，改指或删除。
- **④ 约束与非目标**：只改部署事实，不动架构描述；不复制 compose 内容；不替 core 改仓。
- **⑤ 验收**：活跃文档 `grep -rn "docker-compose.services"` 仅归档层命中；SYSTEM-DESIGN 无死引用；链接检查 CI 绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/SYSTEM-DESIGN.md`。

### DOC-20 · 把 archived 的 ARCHITECTURE 移出活跃导航 [P1] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H3 · 顺序 1-4 · 依赖：无

- **① 目标**：终止"归档文档仍被当作推荐读物"的 R2 自违反。
- **② 上下文**：`docs/ARCHITECTURE.md` frontmatter 为 `status: archived`，却出现在 `README.md:37` 主表与 `:56` 推荐顺序；该文件自述"端口/表数已失效"，体积 65.9KB。
- **③ 要求**：① 从 README 主表与推荐顺序移除；② 在归档层（或其归档位置）保留一条"历史架构参考"入口；③ 若该文件仍留在 `docs/` 根，按 R2 评估移入 `archive/` 或降级为脚注。
- **④ 约束与非目标**：不删除文件、不改其正文；不再放回导航。
- **⑤ 验收**：README 导航与推荐顺序 0 处指向 ARCHITECTURE；R2 自检通过；链接检查绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/README.md`（及可能的文件位置调整）。

### DOC-21 · 版本 pin 与 ADR 状态的「单一真相」收敛 [P2] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H4 · 顺序 1-5 · 依赖：无（数字对错由 DOC-28 承接）

- **① 目标**：消除"同一事实两处写、两处错"。
- **② 上下文**：`REPO-MAP.md:46` 自称 pin 规则"唯一处"；但 `SYSTEM-DESIGN.md:124/134` 仍复制 contracts/kit 版本数字；`ADR.md:4` 的 verified-by 自认"索引表与尾注两处是两套真相来源"。
- **③ 要求**：① `SYSTEM-DESIGN` §2 的 pin 数字改为指针（只留 `REPO-MAP` 链接，不写版本号）；② `ADR.md` 尾注改为"索引表为唯一状态源"，不再重复维护状态；③ 在 DOC-18 的校验脚本中加 `go.mod` pin ↔ `REPO-MAP` 比对（只读其他仓）。
- **④ 约束与非目标**：不删 ADR 正文与历史记录；不取得其他仓写权；本条只做机制，具体数字订正归 DOC-28。
- **⑤ 验收**：`SYSTEM-DESIGN` 不再出现具体 pin 版本号；人为改错 pin → 校验脚本可检出（破坏验证）。
- **⑥ 边界**：`tellurion-docs` 的 `SYSTEM-DESIGN.md`、`ADR.md`、校验脚本。

### DOC-22 · 归档层可信索引重建 + status 语义修正 [P2] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H5 · 顺序 1-6 · 依赖：无（可与 DOC-18 共用脚本）

- **① 目标**：`archive/README.md` 覆盖全部 6 个子目录 + 11 个顶层文件；归档文件 frontmatter 统一 `status: archived`。
- **② 上下文**：`archive/README.md:41` 目录树停在 2026-04-11、只列两个子目录，漏 `odr/`、`superseded-adr/`、`plans-2026-Q3/`、`reports-2026-Q3/`、`tasks-archive-2026-11.md`、`TASKS-history.md`、`VISION-full.md` 等；`:29` 指向已不存在的 `docs/odr/`；顶层 11 份 .md 中 `TASKS-2026-10-08-archived.md:2` 与 `REORG-PLAN.md:2` 仍是 `status: active`。
- **③ 要求**：① 重写 `archive/README.md` 为"子目录 + 顶层文件 + 日期 + 一句话"清单（优先由 DOC-18 脚本生成）；② `docs/odr/` 死指针改为 `archive/odr/`；③ 两份 `status: active` 改 `archived`；④ 在归档 README 写明"索引维护是归档层唯一例外"。
- **④ 约束与非目标**：不改归档正文内容；只动索引与 frontmatter status。
- **⑤ 验收**：脚本比对归档实测清单缺口为 0；活跃文档无 `docs/odr/` 指针；`^status:` 扫描归档顶层 0 个 `active`。
- **⑥ 边界**：`tellurion-docs` 的 `docs/archive/`。

### DOC-23 · ADR-027 标 Superseded + 变更日志单调化 [P3] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H6 · 顺序 1-7 · 依赖：无

- **① 目标**：消除"两条服务拓扑结论并存"；决策台账时间线可顺序阅读。
- **② 上下文**：`ADR.md:46-L49` 中 ADR-027/028/029 自 2026-10-06 维持 `Proposed`、ADR-030 维持 `Draft`；ADR-027 主题"模块化拆解为独立服务（5→7）"已被 2026-10-26 的 ADR-036（12 仓拓扑，`ADR.md:190` 明写修订 027 §2.1）取代，却未标 `Superseded`；`:191` 的 `_Last updated_ 2026-10-14_` 夹在 10-26 与 11-11 条目之间，`:197` 又是 10-13，日志非单调。
- **③ 要求**：① ADR-027 索引状态改 `Superseded by ADR-036`，并在 adr-027 文件头加一行注记（不改正文）；② 变更日志按日期单调整理；③ `_Last updated_` 更新为本次。
- **④ 约束与非目标**：ADR-028/029/030 的状态不在本条擅自改判，只记录现状；不动 ADR-036。
- **⑤ 验收**：ADR 索引中 027 状态与链接正确；变更日志日期单调；链接检查绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/ADR.md` + `docs/adr/adr-027*.md` 头部注记。

### DOC-24 · ROADMAP S2 改为「部分达成」 [P3] ⬜

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H7 · 顺序 1-8 · 依赖：与 DOC-25 口径一致

- **① 目标**：阶段台账反映"产业链底座已实现、`hypothesis_source` 未实现"的真实状态。
- **② 上下文**：`ROADMAP.md:40` 把 S2 标"⬜ 待开始"，出口判据第一条"产业链数据底座可用"；但 core 已装配 `/api/industry/*`（SW 行业树 / 供应链边 / 行业活力 / ETF 成分）与 `/api/macro/series`，core `openapi.yaml` tag 描述写明 `Industry (P2-2)`、`Macro (P2-1)`。
- **③ 要求**：S2 状态改"🔶 部分达成：产业链底座 ✅ / `hypothesis_source` ⬜"，并在出口判据逐条标注已满足项。
- **④ 约束与非目标**：不改 S2 目标本身；不因部分达成提前进入 S3。
- **⑤ 验收**：S2 状态与出口判据自洽；与 `PRODUCT.md` 的能力状态表述一致（见 DOC-25）。
- **⑥ 边界**：`tellurion-docs` 的 `docs/ROADMAP.md`。

#### 档 2 · 产品设计

### DOC-25 · PRODUCT 能力状态显式化（产业链 / EquityDeep / S2）[P2] ⬜

> 档 2（产品设计）· 来源：01-product-design P1-1/P2-1/P2-2 · 顺序 2-7 · 依赖：与 UI-INDUSTRY-ENTRY 裁决、DOC-24 保持一致

- **① 目标**：把 `PRODUCT.md` 的现在时承诺与"已实现 / 仅 API / 未实现"对齐，避免读者把设计设想读成现状。
- **② 上下文**：`PRODUCT.md:71` 把"产业链查询"列为 L2，但 UI 无入口（性质 = 能力已具备未暴露）；`:166-168` 把 adoption / calibration / experiments/count 写成"可测"当前能力，但 core `openapi.yaml` 未收录（性质 = 契约索引缺口）；S2 的 `hypothesis_source` 12 仓零命中（性质 = 确实缺功能）。
- **③ 要求**：三处加状态标——① 产业链："后端可用；UI 入口见 UI-INDUSTRY-ENTRY 裁决"（若裁 B 则写"仅 API"）；② 测量端点："已实现；core 契约索引补齐中（见档 5 `CORE-OPENAPI-MEASUREMENT-INDEX`）"；③ 因果来源："S2 未开始，依赖 S1 出口"。
- **④ 约束与非目标**：不新增需求；不把 S2 写成已开始；不动八条原则与优先级序。
- **⑤ 验收**：三处均能区分"已实现 / 仅 API / 未实现"；与 ROADMAP S2、UI 裁决单口径一致。
- **⑥ 边界**：`tellurion-docs` 的 `docs/PRODUCT.md`。

### DOC-26 · PRODUCT 对 analytics 的定位对齐 ADR-0005（参考实现）[P3] ⬜

> 档 2（产品设计）· 来源：01-product-design P2-4 · 顺序 2-8 · 依赖：无

- **① 目标**：消除"扩展舱"叙事与"core 调用方为 0"的落差。
- **② 上下文**：`PRODUCT.md:58/61` 把 analytics 列为扩展舱；`REPO-MAP.md:23` 与 ADR-0005 已裁决 core 调用方为 0、analytics 是独立只读参考实现。性质 = 透明接受的产品冗余，不是隐瞒，但叙事应降级。
- **③ 要求**：PRODUCT 中 analytics 改为"参考实现（非主流程依赖）"，并写"进入主流程"的重开条件（出现真实消费者 + 数据一致性验收 + 新 ADR）；不删仓、不新增对接需求。
- **④ 约束与非目标**：不动 VISION 八条原则；不把"参考实现"写成"将被替换"。
- **⑤ 验收**：PRODUCT / REPO-MAP / ADR-0005 三处口径一致；无"将接入主流程"式现在时承诺。
- **⑥ 边界**：`tellurion-docs` 的 `docs/PRODUCT.md`（必要时 `SERVICE-INDEX.md` 一行指针）。

### DOC-27 · 测量口径的数据积累与回填策略落档（先证伪）[P3] ⬜

> 档 2（产品设计）· 来源：01-product-design P3-1（"缺少回填策略"为**推断**）· 顺序 2-9 · 依赖：无

- **① 目标**：让 GT-1~GT-6 的"可测"有数据来源、积累窗口与回填能力说明。
- **② 上下文**：`PRODUCT.md:164-169` 自评"采纳记录需人工、校准需半年数据、证据覆盖率部分（JSON Pointer 未实现）"；审查在 TASKS/ADR 未检索到回填策略，但明确标注为推断。施工第一步必须先证伪前提——查 data 同步/备份脚本、CI artifact、报表脚本、run 结果保留策略（`CORE-RESULT-RETENTION` 已定 90/365 天）。
- **③ 要求**：① 核实现有积累与回填机制并记录证据；② 若有缺口，在 PRODUCT 测量节写清"数据从哪来 / 多久可评 / 能否回填 / 责任仓"；③ 若确认无缺口，本条标 ✅ 作废并附证据。
- **④ 约束与非目标**：不新造指标；不写无法兑现的"可回填"承诺；不改 `CORE-RESULT-RETENTION` 已定保留期。
- **⑤ 验收**：每个 GT 指标都能回答上述三问；或本条带证据作废。
- **⑥ 边界**：`tellurion-docs` 的 `docs/PRODUCT.md` + 必要时 data/analytics 文档指针。

#### 档 5 · 文档与代码一致性

### DOC-28 · `REPO-MAP.md` 六处漂移订正（中心视图对齐 go.mod/路由）[P1] ⬜

> 档 5（文档与代码一致性）· 来源：04-doc-consistency P1-1 · 顺序 5-1 · 依赖：DOC-21 的机械门可后置，本条先修数

- **① 目标**：让"仓矩阵唯一现行视图"与当前 `go.mod` / 路由一致，消除 agent 按旧图找错的情况。
- **② 上下文**：实测漂移——`:17` kit 最新/pin 仍写 `v0.3.0`、`:18` agent 写 `v0.2.0`（实际 7 仓均 `v0.5.0`）；`:20` data 仍列已撤的 `/factors/{name}@{hash}`、schema 写 23（实际 25）；`:21` strategy 写"写 7 + 读 2"（实际 8 + 5 = 13）；`:22` risk 写"零 import contracts"（实际直接依赖 `contracts v0.10.0`，ADR-040 迁移后）；`:24` orchestration 写"任务 4 + 批量 4 + 算力 2 + provenance"（仓内 `api-schema.md` 为 16 条）；`:48` 重复旧数字同腐。
- **③ 要求**：逐行改为实测值；在表头写"本表以各仓 `go.mod` / `docs/api-schema.md` 为准，最后核对日期"；`:48` 与 `:17` 单一化，不保留两份数字。
- **④ 约束与非目标**：不复制服务仓细节表；不在本条改其他文档的数字；不删"不放过期数字"的自定规则。
- **⑤ 验收**：6 处逐条与 `go.mod` / 路由文档对上；表头有核对日期；改错一行能被 DOC-21 的校验脚本检出（若已落地）。
- **⑥ 边界**：`tellurion-docs` 的 `docs/REPO-MAP.md`。

### DOC-29 · `TEST.md` 改为历史快照或读数链接 [P1] ⬜

> 档 5（文档与代码一致性）· 来源：04-doc-consistency P1-2 · 顺序 5-2 · 依赖：无

- **① 目标**：消除 `TEST.md` 正文现在时陈述与实际测试状态相反的三处。
- **② 上下文**：`:438` 写"CI 不设覆盖率阈值"（实际 core 有 `-total-min=52`）；`:478` 前端"18 个文件 / 208 条"（当日实测 52 / 643）；`:567/:585` e2e"18 spec / 163 例、127 passed / 34 failed"（实际 31 spec、211 passed / 7 failed）；frontmatter 虽标"正文未改，实质基线 2026-09-22"，但正文会被外部读者当现状。
- **③ 要求**：建议 **B 更新读数并注明日期与日志链接**（§6/§7 的计数改为"截至某日 + `reports/...` 或 CI 链接"）；其余章节保留 2026-09-22 历史快照并加顶部横幅"历史快照，勿引用数字"。也可选 **A 全篇历史快照**。
- **④ 约束与非目标**：不虚构读数；不把未复跑的测试写成通过；不改 `TEST.md` 之外的文件。
- **⑤ 验收**：全文无"现在时 + 过期数字"混用；每个计数都有日期与来源；`grep "18 个文件\|208 条\|127 passed"` 不再作为现状出现。
- **⑥ 边界**：`tellurion-docs` 的 `docs/TEST.md`。

> 除上文外，本仓无其它未做 / 挂起 / 外部依赖项（截至 2026-11-13：W7 立单 4 条已结案归档；2026-11-13 五角审查档 1 新立 DOC-17~DOC-24、档 2 新立 DOC-25~DOC-27、档 5 新立 DOC-28~DOC-29）。跨仓施工任务不在本仓——见 §三指针。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 底座与六服务的施工任务 | `tellurion:docs/TASKS.md` |
| 契约形状与版本纪律 | `tellurion-contracts:docs/TASKS.md` |
| 工具层（鉴权/日志等） | `tellurion-kit:docs/TASKS.md` |
