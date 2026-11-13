# TASKS 归档 — tellurion-docs（2026-11）

> **本文件是 `docs/TASKS.md` 的历史归档，进 git、不删除**。归档时间 2026-11-11（首批）；收录范围 = 截至 2026-11-10 已收口（✅）的任务原文与当时的施工记录，**逐字搬入、未改写**；2026-11-13 追加「五角审查批次 DOC-17~DOC-29」原文与施工记录（原文件 frontmatter 留在新台账；任务标题与正文原样保留）。

> **检索方式**：按任务 ID `grep -n "<ID>" docs/archive/tasks-archive-2026-11.md`；按 commit `grep -n "<sha>" docs/archive/tasks-archive-2026-11.md`；索引表在本节下方，含 ID / 标题 / 收口日期 / commit / 证据链接。

## 检索索引

| ID | 标题 | 收口日期 | commit / 正文所记哈希 | 证据链接 |
|---|---|---|---|---|
| DOC-01 | 拆仓后链接修复 | 未标注 | —（原文未记） | 见本节原文 |
| DOC-02 | 总体层三份建立 | 未标注 | —（原文未记） | 见本节原文 |
| DOC-03 | `ARCHITECTURE.md` 降级为历史 Reference | 未标注 | —（原文未记） | 见本节原文 |
| DOC-04 | 链接检查进 CI | 未标注 | —（原文未记） | 见本节原文 |
| DOC-05 | 历史层 166 条断链的处置 | 2026-10-21 | —（原文未记） | 见本节原文 |
| DOC-06 | `PRODUCT.md` / `VISION.md` 按新定位重写 | 2026-10-25 | —（原文未记） | [REPO-MAP.md](REPO-MAP.md) |
| DOC-07 | 12 仓文档一致性巡检脚本 | 2026-10-22 | —（原文未记） | 见本节原文 |
| DOC-08 | `docs/guides/` 按 12 仓更新 | 2026-10-22 | —（原文未记） | 见本节原文 |
| DOC-09 | ADR-D24/D25/D29/D30 升格为正式 ADR | 2026-10-22 | —（原文未记） | 见本节原文 |
| DOC-10 | `SYSTEM-DESIGN.md` §7 的"今天"栏已过时 | 2026-10-26 | —（原文未记） | 见本节原文 |
| DOC-11 | 长效文档现状对齐（REPO-MAP 状态列 / ROADMAP 当前阶段 / guides 三处 / README 条数） | 2026-10-26 | —（原文未记） | 见本节原文 |
| DOC-12 | ADR-036 服务化目标拓扑落档 + 12 仓定位同步 | 2026-10-26 | —（原文未记） | 见本节原文 |
| DOC-13 | ADR-036 就绪门 ↔ 工单 对照索引（防「门有人写、单没人立」） | 2026-11-07 | —（原文未记） | 见本节原文 |
| DOC-15 | `REPO-MAP` 依赖图补「core → agent 是 HTTP 反代、不是领域依赖」（DDD 审查 C7） | 2026-11-11 | `98a5909` | [原文](#DOC-CORE-AGENT-PROXY-NOTE) |
| DOC-16 | `REPO-MAP` contracts / kit 版本列按各仓 `go.mod` 实测订正（DDD 审查 C11） | 2026-11-11 | `98a5909` | [原文](#DOC-REPO-MAP-VERSION-CORRECTION) |
| DOC-FRONTMATTER-HYGIENE | frontmatter 过期 / ARCHITECTURE 状态错位 / ADR 索引取代标注 | 2026-11-12 | `f228c93` | [原文](#DOC-FRONTMATTER-HYGIENE) |
| DOC-ADR-REQUESTID-CORRECTION | adr-027/029/017「request-id 已跨服务传播」断言更正注记 | 2026-11-12 | `5b18e17` | [原文](#DOC-ADR-REQUESTID-CORRECTION) |
| DOC-PRODUCT-DRIFT-FIX | PRODUCT/ROADMAP 接线现状与阶段断言对齐 SYSTEM-DESIGN §4/§5 | 2026-11-12 | `b2a473f` | [原文](#DOC-PRODUCT-DRIFT-FIX) |
| DOC-P3-MATRIX-TABLE-GRAIN | `run.backtest_results` 表粒度例外显式化 + core 矩阵 `:43` 待派指针 | 2026-11-12 | 本次 commit | [原文](#DOC-P3-MATRIX-TABLE-GRAIN) |
| CORE-MATRIX-FACTOR-OWNER-FIX | core 矩阵 `:43` 因子派生表 owner 仍写 `tellurion-data`（docs 侧按 ADR-037 订正；core 行待派） | 2026-11-12 | 本次 commit | [施工记录](#CORE-MATRIX-FACTOR-OWNER-FIX) |
| DOC-17 | 入口页五项失效目标一次性校准 | 2026-11-13 | `81f5382` | [原文](#DOC-17) |
| DOC-18 | 入口页关键计数改为脚本校验 + 落实 R5 文档可验证 CI | 2026-11-13 | `1085cff` | [原文](#DOC-18) |
| DOC-19 | SYSTEM-DESIGN 部署句改指 core `docker-compose.yml` | 2026-11-13 | `b7b8348` | [原文](#DOC-19) |
| DOC-20 | 把 archived 的 ARCHITECTURE 移出活跃导航 | 2026-11-13 | `ad440f6` | [原文](#DOC-20) |
| DOC-21 | 版本 pin 与 ADR 状态的「单一真相」收敛 | 2026-11-13 | `5395205` | [原文](#DOC-21) |
| DOC-22 | 归档层可信索引重建 + status 语义修正 | 2026-11-13 | `848b08c` | [原文](#DOC-22) |
| DOC-23 | ADR-027 标 Superseded + 变更日志单调化 | 2026-11-13 | `777eca2` | [原文](#DOC-23) |
| DOC-24 | ROADMAP S2 改为「部分达成」 | 2026-11-13 | `04182ff` | [原文](#DOC-24) |
| DOC-25 | PRODUCT 能力状态显式化（产业链 / EquityDeep / S2） | 2026-11-13 | `73ab7fa` | [原文](#DOC-25) |
| DOC-26 | PRODUCT 对 analytics 的定位对齐 ADR-0005（参考实现） | 2026-11-13 | `a4aa43b` | [原文](#DOC-26) |
| DOC-27 | 测量口径的数据积累与回填策略落档（先证伪） | 2026-11-13 | `ea1e6e1` | [原文](#DOC-27) |
| DOC-28 | `REPO-MAP.md` 六处漂移订正（中心视图对齐 go.mod/路由） | 2026-11-13 | `95a644d` | [原文](#DOC-28) |
| DOC-29 | `TEST.md` 改为历史快照或读数链接 | 2026-11-13 | `13a031b` | [原文](#DOC-29) |

---

## 原文归档（逐字）

# TASKS — tellurion-docs

> **本仓台账只放"知识库维护"**：导航、坏链、过时声明、索引补齐。
> **跨仓施工任务不在这里**——它们在 [`tellurion:docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md)。建单前先问：这件事是不是"改文档结构"？不是就别在本仓建单。

> **第三轮裁决指针（2026-10-25）**：⑧ DOC-10 = **§7 整块订正**（阶梯表 S-1~S3 / X1~X6、三条「已知过渡态」、一行状态表）+ `docs/README.md:40` 的 QT-60 行；**§8 以后与阶梯表的设计理由不动**；W0 的 01/02/04 三腿先核再改。正文见 `tellurion:docs/design/qt-decoupling/cross-repo-decision-record-2026-10-25.md` §五。


## 二、本仓任务

> **台账终扫（2026-11-10）**：任务标题带 `⬜` / `🔶` / `⛔` 的 = **0 条**；DOC 单全部 ✅。**无开放项**。

| # | 事项 | 状态 | 说明 |
|---|---|---|---|
| DOC-01 | 拆仓后链接修复 | ✅ | 153 条跨仓相对链接改绝对 URL（含 `file:///Users/.../quant-trading/*` 本机路径）；活跃层 196 条链接 0 断 |
| DOC-02 | 总体层三份建立 | ✅ | `SYSTEM-DESIGN.md`（分层 / 四条主链路 / 数据归属 / 边界原则 / 阶梯）+ `REPO-MAP.md` + `SERVICE-INDEX.md` |
| DOC-03 | `ARCHITECTURE.md` 降级为历史 Reference | ✅ | 顶部留指针指向 `SYSTEM-DESIGN.md`；导航行改标"拆仓前历史 Reference（端口/表数已失效）" |
| DOC-04 | 链接检查进 CI | ✅ | `tools/check_doc_links.py` + `.github/workflows/ci.yml`；活跃层断链即红，历史层只统计 |
| DOC-05 | 历史层 166 条断链的处置 | ✅（2026-10-21） | **裁决：① 保持原样，不修**。档案属历史快照，事后改写链接等于篡改历史；历史层在 DOC-04 的 CI 里本就只统计不判红，零成本。落地动作仅为在 `docs/archive/` 索引加一行总说明「历史档案，链接指向已删除/已搬走的源码，不修」，不逐条改动 |
| DOC-06 | `PRODUCT.md` / `VISION.md` 按新定位重写 | ✅（2026-10-25 口径拍定并成文） | 导航里已标"待重写"；需先有产品口径（分仓后单一产品变成"底座 + 实验员 + 前端 + 六服务"）。**现状核对（2026-10-23 实读两文全文）**：两文的**产品哲学层仍然成立**（三角色/三层次/八原则/校准目标，2026-09-16 写定，与分仓无关），真正缺的是**系统构成层**——PRODUCT 只字未提 12 仓拓扑，引用的 `ARCHITECTURE.md` 已降级为历史 Reference（应改指 `SYSTEM-DESIGN.md`）。**重写提纲**：PRODUCT（≤3 页）= 一句话 / 为谁解决什么 / 三角色+一座底座 / **系统构成（新增：core=仪器、agent=实验员、ui=观察窗、六服务=按需触发的扩展舱、contracts+kit=接口与工具）** / 三节奏审阅 / 边界与指标；VISION（≤2 页）= 元定位 / 八条原则（不动）/ 候选新增「边界即仓库、契约只认版本号」是否升入 / 边界表 / 优先级。**待口径三问**：① 六服务在产品叙事里是"产品的一部分"还是"部署形态的可选项"；② 分仓工程原则（契约版本纪律）升入 VISION 还是留在 SYSTEM-DESIGN；③ 「系统构成」写到仓粒度（REPO-MAP 已有索引，防复制）还是功能粒度。**（2026-10-25 补：三问决策材料 → 本文件 §四，每问一份「实测事实 → 选项 → 建议 + 代价」）**。**同日本行的一处旧陈述被证伪**：原写「今天 data/analytics 等尚未接线」——实测 **data 已接且真在跑**（`data_service.url` → `marketdata` 的 HTTP provider，compose 里就有 `data-service` 容器），**risk 只有客户端**（`resolve_enabled` / `events_enabled` 出厂皆 `false`），**strategy / analytics / orchestration / broker 四条 core 侧连客户端都没有**；接线现实按仓列在 §四 F1~F3，不要在口径句里用"等"字含糊带过。**口径（2026-10-25 主任拍定，三问全取 §四 建议 A）→ 成文落地**：① PRODUCT 新增「系统构成：五种角色，一座底座」一节——**功能粒度**（仪器 / 实验员 / 观察窗 / 扩展舱 / 契约底座），每角色一句"由哪些仓承担"并指 `REPO-MAP.md`，**不复制那张表**；那句"一名多角色"按要求写明（core 既是仪器本体又是仪器域数据唯一写者）；六服务按**部署形态的可选项**处理（称"扩展舱"，并写清今天真被 core 消费的远程调用只有一条，且刻意注明"逐条接线数会随施工漂移，故不写进角色表、只在 §四 登记"）。② **VISION 八条原则与优先级序一字未动**，不升入第九条；改为在文件头与「边界（明确不做）」表各留一条指针，写明这条纪律已由 SYSTEM-DESIGN §8 的 R5·C1 机械执行、**没有裁决对象**。③ 两文头部那条指 `ARCHITECTURE.md`（"怎么搭"）的指针一并换指 `SYSTEM-DESIGN.md`，并把 ARCHITECTURE 的历史身份写明；`docs/README.md` 导航两行从「待重写」换成「现行」，各写明**改了什么、没动什么**。**验收**：`python tools/check_doc_links.py` 活跃层 **222 条 / 0 断**（EXIT 0，成文前 215，本单新增 7 条链接全部可达）；**破坏验证**＝把新增节里那条 `[REPO-MAP.md](REPO-MAP.md)` 改坏 → **1 条断、EXIT 1、点名 `docs\PRODUCT.md`** → 逐字节还原（`cmp` 相等）→ **0 断、EXIT 0**；另一条在 §四 的材料链接上做过同型验证。哲学层零改写：`git diff --numstat` 落在 PRODUCT 21/3、VISION 5/3、README 4/4——**全是新增节 + 三处指针 + frontmatter，无一行原则被重写**。**未做**：`SYSTEM-DESIGN.md` §7 的时间陈述过时不属本单，另立 **DOC-10** |
| DOC-07 | 12 仓文档一致性巡检脚本 | ✅（2026-10-22） | 现在靠人眼：每仓应有 `AGENTS.md` + `db-schema` / `api-schema` / `dataflow` + `TASKS` + `adr/` + `odr/`。**豁免注记（2026-10-21 裁决，spec 审查 H1/L3）**：core 与本仓豁免三件薄规格与 `adr/0001-*`（API/DB/流程真相由 `tellurion:docs/openapi.yaml` / `tellurion:pkg/storage/postgres.go` / `tellurion:docs/SPEC.md` 直接承载），巡检脚本须实现该豁免分支，不得对两仓报缺件。可写成 `tools/check_repo_docs.py`（与 core 的 `check_repo_autonomy.py` 互补：那边查仓自治，这边查文档齐套）。**落地（2026-10-22）**：`tools/check_repo_docs.py`（只查存在性与形状，不读正文）+ `tools/test_check_repo_docs.py`（17 条夹具腿，stdlib unittest）。按 ticket 实现 core / 本仓的豁免分支，并**按实仓取证追加两条具名豁免**（见下行「偏差」）：core 的 `adr/` 与 `odr/` 也已随文档拆分迁走（ADR 住 `tellurion-docs/docs/adr`、ODR 住 `tellurion-docs/docs/archive/odr`，core AGENTS.md §10 记录）；本仓 ODR 家是 `docs/archive/odr` 而非 `docs/odr`（AGENTS.md §3.6），故判据接受两个 ODR 家。真跑：`python tools/check_repo_docs.py --explain` → 退出码 **0**，12/12 齐套、缺件 0、豁免 2 仓。破坏验证（临时夹具，不动真仓）：完整夹具 0 → 删 `tellurion-ui/docs/dataflow.md` → **1** 并点名该文件 → 还原 → **0**；另有「缺 AGENTS / TASKS / 单件规格 / adr 目录 / 0001 / ODR 家」「仓目录不存在」「未登记仓名」各一条红腿。**不进 CI**：CI 只 checkout 本仓，看不到另外 11 个仓（详见 AGENTS.md §1）。 |
| DOC-08 | `docs/guides/` 按 12 仓更新 | ✅（2026-10-22） | 三份全部改 12 仓口径：**`local-dev.md`** 新增「按目标选最小 checkout 集」+ 同级硬约束（agent 的 `replace tellurion => ../tellurion`、compose 的 `context: ../tellurion-agent`）+ `go.work` 的真实定位（**今天可选**：core 尚未 `require` 两库仓；一旦切依赖才必需）+ 每仓 CI 同款命令 + 端口一览；**`deploy-config.md`** 新增「部署资产分在三个仓」（ui 的 `Dockerfile`/`nginx-spa.conf`、agent 的 `Dockerfile` 要 core 作命名上下文、`deploy/k8s/` 含 web 清单仍在 core）+ 护栏覆盖面边界表（nginx conf / agent Dockerfile / ingress backend / `RUN` 里的 `go build` 四处**无护栏**）+ web 改端口跨两仓清单；**`data-dependencies.md`** 新增 §0 仓归属表（取数/同步今天仍在 core，`tellurion-data` 仍占位）+ adapter 表 9 → **12**（补 `tushare_macro` / `tushare_daily_basic` / `tushare_moneyflow`）+ 凭据表加「**谁读它（哪个仓）**」列。**订正七处已失效/错误的陈述**：① `docker-compose.yml` 的服务是 data/analysis/**ai**（原文写 strategy/web，两者都不在）；② `cmd/ai` 未删除 —— 它在 `tellurion-agent:cmd/ai`；③ 前端 `web/` 已迁 ui 仓（旧文把它按 core 目录写，还钉着 vitest 208 条 / 18 文件；今天 ui 是 38 个测试文件）；④ 连接串库名 `tellurion`（原文 `quant_trading`）；⑤ `AI_API_KEY` 读取点已迁 `tellurion-agent:pkg/ai/client.go`（core 全仓无读取者，compose 给 analysis 的注入是死注入）；⑥ 原文「`make build` 会失败，因为 `Makefile` 仍 build 已删目录」**已不成立** —— `Makefile` 现在只 build `cmd/analysis` 与 `cmd/data`（实测 `git grep '^build'`），真障碍是本机没装 `make`；⑦ 原文「`cp .env.example .env` 然后 `go run`」**跑不起来** —— Go 侧无 dotenv 加载器（`grep godotenv` 零命中），`.env` 只服务 compose，原生跑法须 `export DATABASE_PASSWORD`，否则 `pkg/storage.BuildDSN` 以 `ErrEmptyDBPassword` 退出。**三处实测新增的坑（原文没有）**：① core `Dockerfile.service` 仍 `go build ./cmd/strategy`（目录 REV-16 已删）⇒ **容器那半今天构建不出来**，`docker run golang:1.25-alpine … go build ./cmd/strategy` 实测 `directory not found`；② agent 仓没有 `config/` 目录而 `LoadConfig` 缺文件即 Fatal ⇒ 原生跑 `cmd/ai` 必须 `CONFIG_PATH=../tellurion/config/ai-service.yaml`；③ 上条 ⑦ 的 `DATABASE_PASSWORD`。**新增护栏** `tools/check_guide_refs.py`（`repo:path` 纯文本跨仓引用；仓名腿进 CI，`--workspace` 腿工作区级不进）+ `tools/test_check_guide_refs.py`（**21 条**夹具腿，含 4 条实测踩到的截断/误判回归腿：`localhost:5432/...` 被当仓名、`...` 省略号被当路径、中文 ADR 文件名被截断、否定词按行窗口）。验收实测：`check_doc_links.py` 活跃层 **210 条 / 0 断**（历史层 166 断只统计）；`check_guide_refs.py --workspace ..` 退出 **0**；破坏验证（往 guide 塞 `tellurion:pkg/ai/pipeline` + `telliurion:docs/TASKS.md`）→ **2 处红、退出 1** → 还原逐字节 → 退出 0；`test_check_guide_refs.py` **21/21 OK**（含一条钉住仓清单必须是 12 条的腿）。 |
| DOC-09 | ADR-D24/D25/D29/D30 升格为正式 ADR | ✅（2026-10-22） | 升格为四张：**ADR-032**（D24 模块拓扑与跨进程边界）· **ADR-033**（D25 执行载体落地顺序）· **ADR-034**（D29 分仓拓扑与 S0~S3 阶梯）· **ADR-035**（D30 仓清单与命名，**含本轮待裁决 A/D/E/F/G/H 附录**）。四处失效假设就地标注不得照抄：D24 第 1 条已被 M1/D29 §5 替代（domain 并入 contracts）、R 系列是 R1~R6（源文仍写五条）、host 函数 12 个（原写 13）、D29 的 S1 形态已被 ADR-D31 替代。**两处工单描述订正**：① 本行原称「D24（`ai.*` schema 自持）」——那条内容实为 **D10**（`ai.*` 的 DDL/migrate 归 agent，源文 core `target-module-topology.md` 的 ADR-D10 节），本批按源文实际内容升格，**D10 未列入本轮四张**（要升格请另立单）；② 原称「D29（待裁决表压缩/连带 L1)」，现行 D29 的承重内容是拓扑与 R/C/S 阶梯，待裁决表在 core `README.md` 而非 D29 正文。D31 未并入（它替代的是 D29 的 S1 形态，本身仍是设计集条目，升格与否待单独裁决）。索引表 + `ADR.md` 尾注 + 四份文件头三处一致 |
| DOC-10 | `SYSTEM-DESIGN.md` §7 的"今天"栏已过时 | ✅（2026-10-26 结案） | §7 的「已知过渡态」写**六个服务仓只有占位 `doc.go`**、阶梯表写 **X1~X6 未触发**。**同批逮到第二处同类，且是本仓自我矛盾**：`docs/README.md` 的「仓清单与命名」行仍写「工单 QT-60，**未启动**」，而同仓的 SYSTEM-DESIGN §7 自己就记着 **S-1（12 仓改名 + 建仓 + 推送）✅ 完成（QT-60）**——导航与被导航的文档打架，读者无从判断该信哪份。2026-10-25 只读实仓取证：六个服务仓各有真 `cmd/*service` 监听 + 自有 schema 的 PG 装配（`data :8081` / `risk :8086` / `strategy :8085` / `analytics :8087` / `orchestration :8088`），core 侧装了 data 与 risk 两个消费者（risk 两条腿出厂默认关，见 §四 F2），其余四个 core 侧零调用方。⇒ 这几处"今天"不再是现状，会被读者当成设计。**§5「今天实际」列本单不预判对错**：core 无 analytics/orchestration 客户端这一条与它「今天在 core `cmd/analysis` 内直接算」一致，但 `analysis.*` / `run.*` / `risk.*` 已在各仓 own schema 里有 PG 装配，该列是否要改按各仓 `docs/db-schema.md` 逐格核对后再定，不跟着 §7 一起顺手改。**本单只改时间陈述，不改设计**：§2 五原则、§3 依赖边、§6 永不拆的六条都不动。收口判据：① §7 过渡态三条逐条对照各仓 `AGENTS.md` 的「状态」节改写（引用写 `repo:path` 纯文本，不复制正文）；② §5「今天实际」列逐格对着各仓 `docs/db-schema.md` 判"仍成立/需改"，改的要有实仓出处；③ 阶梯表 `X1~X6` 的触发状态与 core 台账一致；④ `docs/README.md` 的 QT-60 那行与 SYSTEM-DESIGN §7 对齐（两者必须同判，不再各写各的）；⑤ `python tools/check_doc_links.py` 活跃层 0 断。上游依赖：无（可独立做）。与 DOC-06 的关系：DOC-06 是**产品叙事层**（已结案），本单是**总体设计层的时间陈述**（不需口径，只需核对），两单不互相阻塞 |
| DOC-11 | 长效文档现状对齐（REPO-MAP 状态列 / ROADMAP 当前阶段 / guides 三处 / README 条数） | ✅（2026-10-26） | 第四轮目的对齐审计（core `purpose-alignment-audit-2026-10-26.md`）发现的同批过期陈述一次收口：**REPO-MAP** 状态列从「contracts/kit/六服务占位 + agent 仍 replace + core 内嵌前端」改为实仓读数，并登记 orchestration/broker 零 contracts 依赖的偏差；**ROADMAP** 修正「当前阶段 S0」与阶段表（S0 ✅ / S1 进行中）的自相矛盾，补产品线与工程解耦线的分工；**guides** 的 `local-dev:42`（六仓占位）、`data-dependencies:5,27`（data 仅 go.mod）、`deploy-config:46`（六仓无部署资产）按实仓订正；**README:40,45,55** 的 QT-60 状态 / ADR 18 条 / 首读顺序一并订正。验收：`python tools/check_doc_links.py` 活跃层 0 断；`check_repo_docs.py` 12/12 齐套。**不改设计**（SYSTEM-DESIGN §2 / §6 / §8 未动），只改时间陈述与状态读数 |

| DOC-12 | ADR-036 服务化目标拓扑落档 + 12 仓定位同步 | ✅（2026-10-26） | 主任 2026-10-26 裁决「服务按 microservice、lib 分清工具/数据、平台优先并行 MVP」。新增 `adr/adr-036-service-topology-and-readiness-gate.md`（12 仓定位 + G0~G4 就绪门 + G0/G1/G2 并行、G3 切读串行 + 部署资产回服务仓 + 同 PG 多 schema + risk 控制面/进程内裁决 + broker 服务化），并修订 ADR-027 §2.1 / ADR-034 §S4 / ADR-035 §M5 / repo-inventory §1.2 / broker X6d；`ADR.md` 索引与累计数同步（34→35）。**2026-10-26 复测订正**：累计应为 **36** 条（ADR-001~036 全部存在），现行 **30** 条；`ADR.md` 尾注原写「架构 30」是算术错（ADR-001~016 共 16 + ADR-022~036 共 15 = 31），已一并订正。`REPO-MAP` 增加定位块并把六服务状态更新为「G0 已补」；`SYSTEM-DESIGN` §7/过渡态同步。各服务仓 `docs/TASKS.md` 新增 `SVC-*-G0` / `SVC-*-G3`，冲突口径（「六仓≠六进程」「X6d 暂缓」「裁-15 鉴权暂不做」）就地标注被 ADR-036 取代。**未改**：产品边界（PRODUCT/VISION）、core 热路径、真实 XTP（仍 ⛔） |
| DOC-13 | ADR-036 就绪门 ↔ 工单 对照索引（防「门有人写、单没人立」） | ✅（2026-11-07 落地） | **本单存在的理由就是它要防的那件事**：2026-10-26 一次跨仓核对实测——ADR-036 §3 的五道门里，**G2 与 G4 在六个服务仓台账中 0 条目**（只有 data/strategy/risk/analytics 的 G0/G3 与 orchestration/broker 的 G0/G1/G3 存在）；`/readyz` 在全 workspace 代码里 **0 命中**、`runbook` 一词只出现在 ADR-036 自己的正文里 ⇒ G4 的机械判据**无人认领**；core 的七条 `SVC-CORE-*-RETIRE` 只有 ID 清单，而六个仓的 `SVC-*-G3` 在 ⑥ 边界里逐条指向那些不存在的条目（死引用）。**要做的事**：在 `SERVICE-INDEX.md` 增一张「六仓 × G0~G4 → 单号」对照表，每格填**该仓台账里真实存在的 `###` 标题 ID**或显式写 `⬜ 无单（缺口）`；同表登记两处口径歧义：① 六仓台账里的「**派发块 G4**」（wave-2 的派工块编号，见 `tellurion-data:docs/TASKS.md:56-58` 与 `tellurion-strategy:53`）与 ADR-036 的「**就绪门 G4**（可运维）」**同号不同义**，索引里必须分列，否则读者会把施工记录当成就绪验收；② 本仓 `SYSTEM-DESIGN.md` §7 的 `X1~X6` 阶梯行与 REPO-MAP 的「G0 已补」状态列，都要能被这张表反查。**只索引不复制**（AGENTS §3.1：不搬服务仓正文）。**验收**：① 表覆盖 6 仓 × 5 门 = 30 格，每格要么是可在对应仓 `grep -n "^### <ID>"` 命中的单号，要么明标缺口；② 标为「有单」的格子**逐格实跑 grep 命中**（贴命令与命中行号）；③ 两处同号不同义在表脚注里成文；④ `python tools/check_doc_links.py` 活跃层 **0 断**（EXIT 0）。**上游依赖**：core「六之二」节与各仓 `SVC-*-G1/G2/G4` 的立单（2026-10-26 那批），否则本表只能整列标缺口。**不改**：设计正文（§2/§6/§8）、ADR-036 本体。**落地（2026-11-07）**：`SERVICE-INDEX.md` 新增「六服务 × ADR-036 就绪门 → 工单对照」，`6 × 5 = 30` 格**全部**命中实仓 `###` 标题、**无缺口**（立单前提‘G2/G4 共 0 条目’已被 2026-10-26 那批立单推翻）；逐格行号由 `Select-String -Pattern '^### SVC-'` 对六仓台账实跑取得，命令与行号贴在表下。两处同号不同义已成文：① 「派发块 G4」（wave-2 派工块）现行出处实测只剩 `tellurion-risk:docs/TASKS.md:274` / `:433`，立单时引的 data:56-58 与 strategy:53 已无该词，脚注写明以现行两处为准且不得当就绪验收；② `X1~X6` 与 REPO-MAP「G0 已补」状态列的反查口径（X1 data / X2 strategy / X3 risk / X4 analytics / X5 orchestration / X6 broker）。验收：`python tools/check_doc_links.py` 活跃层 **0 断、EXIT 0**。**未改**：ADR-036 正文、SYSTEM-DESIGN §2/§6/§8。 |

> **DOC-10 结案（2026-10-26）**：§3 依赖边（agent 已零 import core）、§5「今天实际」七格、§7 阶梯（W0/S1/S2/S3 ✅；X1~X6 🔶 已落仓未收口）与五条过渡态已按实仓订正；`docs/README.md:40` 的 QT-60 行同步改 ✅。依据 = core 第四轮审计的实测（12 仓 `go.mod` / 各仓 `cmd/*service` 默认监听 / core `deploy/k8s/` / core 配置开关）。`check_doc_links.py` 活跃层 0 断。

> **DOC-11 后补 / L 组落账（2026-10-26）**：J 组 `SVC-AGENT-G0` 落地后 agent 自持 `config/ai-service.yaml` 与 `deploy/wait-for-deps.sh`、Dockerfile 无 `--from=core`，本仓 guides 两处旧口径同步订正——`deploy-config.md` §1.1（不再需要 core 命名上下文 / ai 配置两份逐值一致副本）与 `local-dev.md` §5.2（`CONFIG_PATH` 可用本仓副本）。**跨仓腿如实登记**：core `docker-compose.yml` 的 ai-service 仍写 `additional_contexts: core=.` 且 `entrypoint: /app/wait-for-deps.sh`（现路径为 `/app/deploy/wait-for-deps.sh`），core 侧同步前不能用 core compose 起 ai-service。→ **已解除（2026-10-26）**：core 侧已删 `additional_contexts`、`entrypoint` 改为 `/app/deploy/wait-for-deps.sh`；`docker compose build ai-service` 实测成功、镜像内 `config/ai-service.yaml` 与 `deploy/wait-for-deps.sh` 均在位。**L 验收**：`python tools/check_doc_links.py` → 活跃层 223 条 / 0 断；`python tools/check_guide_refs.py` → 跨仓引用全部有效。**破坏验证**：临时删 `docs/ADR.md` 中含 `ADR-036` 的全部行 → 命中 3 → 0（红）→ 逐字节还原 → 3（绿，SHA256 `76053CDA…4959E7` 改前改后一致）。

> **DOC-07 偏差登记（2026-10-22，回实仓取证，不照抄通用清单）**
>
> 1. **core 的 `adr/` 与 `odr/` 也已不存在**：工单只豁免了三件薄规格与 `adr/0001-*`，但实测 core `docs/` 下既无 `adr/` 也无 `odr/`（也不存在 `docs/archive/odr/`）——ADR 已全部住 `tellurion-docs/docs/adr`，ODR 住 `tellurion-docs/docs/archive/odr`，core AGENTS.md §10 自己就记着这处漂移。若按通用清单报缺件，巡检每天都会给一个**已知且有意**的"缺"报警，护栏会很快被训练成噪声。故对这两项给 core 具名豁免，理由写在 `EXEMPT` 表里、`--explain` 可查。
> 2. **本仓的 ODR 家不是 `docs/odr/`**：本仓 AGENTS.md §3.6 明写"本仓历史 ODR 在 `docs/archive/odr/`"。判据因此接受 `docs/odr/` **或** `docs/archive/odr/` 任一非空目录（其余 10 仓用的是前者）。
> 3. **不进 CI**：脚本要看见 12 个仓目录，而本仓 CI 只 checkout 自己。它是工作区级工具（本地跑），不冒充 CI 门禁。


## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 仓自治不变量 R1~R6 的机械检查 | core `tools/check_repo_autonomy.py`（QT-08 ①，**已交付**：2026-10-21 第六批落盘，已接进 core CI 的 `Repo autonomy self-check` 步——先 `--self-test` 再全量扫描，实测 `core/.github/workflows/ci.yml:322-323`。「未写」是 2026-10-21 之前的旧账） |
| 契约层落代码 / 打 tag | core `docs/TASKS.md` 的 QT-05 / QT-07 |
| 各仓功能边界正文 | 各仓 `docs/db-schema.md` / `api-schema.md` / `dataflow.md` |
| 施工顺序 | core `docs/TASKS.md` |

---


## 四、DOC-06 口径三问的决策材料（2026-10-25 取证；**三问已拍，均取本节建议 A**）

> 三问的口径归实验室主任拍。本节只做一件事：把每问**脚下踩着的事实**测出来，摆出选项、建议与代价。
> **2026-10-25 同批拍定并成文**（落地动作与验收登记在 §二 的 DOC-06 行）。本节保留原始事实与两条被否掉的选项，是给以后的读者看"这条口径是怎么定的、代价记在哪"，不是待办。
> 取证方式：只读源码与装配（core 的 compose / 配置读取点、五服务 `cmd/*service/main.go` 的 `-addr` 默认值）——**零次启动服务、零次数据库写入**；跨仓出处一律 `repo:path` 纯文本。

### 事实基线

| # | 实测项 | 读数 | 出处 |
|---|---|---|---|
| F1 | 今天的部署进程数 | **3**：`data-service` / `analysis-service` / `ai-service`（compose 的 service 块只有这三条） | `tellurion:docker-compose.yml` |
| F2 | core 侧**装了** HTTP 消费者的能力服务 | **2 / 6**，但两条不同档：**data 今天真在跑**（`data_service.url: http://data-service:8081`，compose 里就有这个容器）；**risk 只有客户端没有开关**——`resolve_enabled: false` 与 `events_enabled: false` 出厂皆为关，装配代码与门都在（`POST /api/risk/resolve` / `POST /api/risk/events`），本部署视为「未接入」 | `tellurion:config/analysis-service.yaml:95-96`、`tellurion:pkg/bootstrap/engine.go:19`（读取点）、`tellurion:config/analysis-service.yaml:122`、`tellurion:config/analysis-service.yaml:143`、`tellurion:cmd/analysis/wiring/risk_rules.go:182-204`、`tellurion:cmd/analysis/wiring/risk_events.go:503-529` |
| F3 | core 侧**连客户端都没有**的能力服务 | **4 / 6**：strategy / analytics / orchestration / broker —— core 非测试代码里 `8087`/`8088` 零命中，`/api/runs/`、`/api/analysis/`、`/api/broker` 零命中；策略资产那条更是被**显式删掉**的（`// strategy_service.url 已随 OBS-11 删除（策略信号只走本地注册表）`） | `tellurion:pkg/backtest/engine.go:289`（该行注释）+ grep 取证 |
| F4 | 六服务仓今天的实现量 | **已不是占位**：各有真监听与自有 schema 的 PG 装配（`data :8081`、`risk :8086`、`strategy :8085`、`analytics :8087`、`orchestration :8088`） | 各仓 `cmd/*service/main.go` 的 `-addr` 默认值 |
| F5 | 默认端口与 F1 的三进程栈**撞车** | risk `127.0.0.1:8086` = `ai-service`；strategy `127.0.0.1:8085` = `analysis-service`（两处都可 `-addr` 覆盖，但默认值同时起就 bind 失败） | 同 F4 + F1 |
| F6 | 易被误读的第三项 | `risk_service.url`（出厂 `"http://localhost:8085"`，早期默认 `:8083`，打 `/detect_regime` 等）**不是** risk 仓，是 ODR-021 合并进 analysis 进程的**进程内**风控端点。口径讨论里若把这条也算成"risk 已接线"，接线数会从 2/6 虚报成 3/6 | `tellurion:config/analysis-service.yaml:111-112`、`tellurion:pkg/backtest/engine.go:290-292`、`tellurion:pkg/backtest/engine.go:1516`、`tellurion:cmd/analysis/handlers_risk.go:22` |
| F7 | 文档层与 F4 的冲突 | `SYSTEM-DESIGN.md` §7 仍写「六个服务仓只有占位 `doc.go`」「X1~X6 未触发」⇒ 已另立 **DOC-10** | `tellurion-docs:docs/TASKS.md` §二 DOC-10 |

**一句话把 F1~F7 收住**：六服务里**今天真被 core 消费的只有 data 一条**；risk 有客户端、有门、有测试，但两个开关出厂皆 `false`；其余四条线 core 侧连客户端都没有。**「六服务」是一个都不该被写成既成事实的名单。**

### 问① 六服务在产品叙事里是"产品的一部分"，还是"部署形态的可选项"？

| 选项 | 怎么写 | 代价 |
|---|---|---|
| **A（建议）** | 产品正文只写三个进程（底座 / 实验员 / 观察窗）；六服务压成一句「同一边界纪律下的扩展舱」+ 指针指 [REPO-MAP.md](REPO-MAP.md)，并按 F2/F3 注明今天真在跑的远程消费只有 data 一条 | "谁已接线"是会变的数，PRODUCT 里那句每隔几轮要跟着改；且容易被读成「只有三个进程算产品」，六服务的存在性得靠总体设计层兜住 |
| **B** | 六服务各进一段产品叙事（数据面 / 资产 / 风控 / 分析 / 编排 / 通道） | PRODUCT 变成施工状态表；施工状态已有两处真相（core 台账 + 各仓 `AGENTS.md` 的「状态」节），第三份必然漂移——本仓 AGENTS §3.1 禁的正是这个 |

**建议 A。** 理由：产品的承重句是「AI 操作底座、人拍板」，服务个数不改变它；F1~F3 说明六条线里**五条今天没有真的在用**（四条无客户端、一条有客户端但开关关着），把它们写进产品正文等于用产品语言描述一个还不存在的回路。要保留"舱位已备好"的意思，放 SYSTEM-DESIGN 的分层图（已有）比放 PRODUCT 更诚实。

### 问② 分仓工程原则（契约只认版本号）升入 VISION，还是留在 SYSTEM-DESIGN？

| 选项 | 怎么写 | 代价 |
|---|---|---|
| **A（建议）** | 不升入。它已是 [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md) §2 的 P2（形状只有一处）+ P4（仓 = 模块/服务）的**推论**，且已机械可查（同文 §8 的 R5「契约是版本依赖」、C1「只认 tag」）。改法：VISION 末尾「边界（明确不做）」表加**一行指针**指 SYSTEM-DESIGN §8，不新增第九条、不动优先级序 | 只读 VISION 的人拿不到「跨仓只认版本号」这句，可能误以为边界靠自觉 |
| **B** | 升入为第九条「边界即仓库、契约只认版本号」 | VISION 自我限定「只写原则（为什么这样设计）」，且优先级行 `1 > 3 > 4 > 6 > 5 > 2 > 7 > 8` 必须重排。排不进序就得回答「契约纪律与『校准优于准确率』冲突时谁赢」——答不上来，恰说明它不属这一层 |

**建议 A。** 判据：一条能进 VISION 的原则，得能在两个同样正当的选择之间做裁决；「只认版本号」没有裁决对象，它是 R5/C1 那条**已被 CI 执行的**纪律的自然语言版。

### 问③ 「系统构成」写到仓粒度，还是功能粒度？

| 选项 | 怎么写 | 代价 |
|---|---|---|
| **A（建议）** | **功能粒度 + 一句仓名指针**：PRODUCT 写「仪器 / 实验员 / 观察窗 / 扩展舱 / 契约底座」五种角色，每角色一句"由哪些仓承担"并指 [REPO-MAP.md](REPO-MAP.md)（12 行 × 8 列的表已在那儿，2026-10-21 刚校准过） | 读者要跳一次文档；且角色↔仓不是一一对应（core 同时是"仪器"与"仪器域存储"），功能粒度那句**必须写明"一名多角色"**，否则比抄表更难对齐 |
| **B** | 仓粒度：PRODUCT 里直接列 12 仓表 | 第二份 REPO-MAP。两份同一事实各自维护，漂移是时间问题——DOC-06 的立项理由原是「PRODUCT 只字未提 12 仓拓扑」，但那不等于修法必须是把表搬过来 |

**建议 A。** 判据同本仓 AGENTS §3.1「不复制，只索引」。

### 口径拍完后仍要单独处理的一件（不属三问，别顺手带过）

PRODUCT.md 的导航行现在指 [`ARCHITECTURE.md`](ARCHITECTURE.md)（已被 DOC-03 降级为拆仓前历史 Reference）。重写时该改指 [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md)——这是**改链接**，不需口径，DOC-06 成文时一并收掉即可。

> F1~F7 是 2026-10-25 的读数。口径只冻结**判据**，不冻结数字：成文当日若与实仓不符，以当日实测为准，并回来订正本节。

---

## 2026-11-11 收口（DDD 边界审查 C7 / C11）

> 本节收 2026-11-10 之后收口、未进入上面「原文归档」的单；上面那份是 2026-11-10 及以前原文件的逐字快照，不改写。来源：`tellurion-docs:docs/design/ddd-boundary-review-2026-11-11.md` §4；裁决批 ADR-038~041（`tellurion:docs/TASKS.md` §三 有 13 条落点表）。

<a id="DOC-CORE-AGENT-PROXY-NOTE"></a>
### DOC-15 · `REPO-MAP` 依赖图补「core → agent 是 HTTP 反代、不是领域依赖」[P2] ✅（2026-11-11）

- **① 目标**：让 `REPO-MAP.md` 的依赖图脚注能回答「core ↔ agent 是不是双向领域调用」，避免读者把前端反代当成上下游客商边。
- **② 上下文**：DDD 边界审查 C7（2026-11-11）实测——`agent → core` 是业务调用（提交回测 / 读结果 / 表达式校验）；`core → agent` 只有 `cmd/analysis` 的 proxy 处理器，是**前端请求的 HTTP 反代**，无领域语义、无落库、无回调。原依赖图只画边、不区分这两类。
- **③ 要求**：① `REPO-MAP.md` 依赖图后补一条脚注，写明两条边的性质差异；② 写明「图上只画 `agent ──► core`」；③ 写明将来若出现「core 主动调 agent 做业务决策」必须先立 ADR。
- **④ 约束与非目标**：只补脚注与一句判据；不改 `SYSTEM-DESIGN.md` §2 的依赖边正文（避免两处漂移），不改任何仓的代码与路由。
- **⑤ 验收**：`REPO-MAP.md` 能一句话区分「反代」与「领域依赖」；`python tools/check_doc_links.py` 活跃层 0 断（EXIT 0）。
- **⑥ 边界**：本仓 `docs/REPO-MAP.md`；反代实现与是否保留归 `tellurion`（core 的 C8 退役单）。
- **收口（2026-11-11）**：commit `98a5909`（`docs/REPO-MAP.md` 依赖图脚注）；同批 ADR-038~041 与 `docs/design/ddd-boundary-review-2026-11-11.md` 落地。

<a id="DOC-REPO-MAP-VERSION-CORRECTION"></a>
### DOC-16 · `REPO-MAP` contracts / kit 版本列与推进顺序段按实测订正 [P2] ✅（2026-11-11）

- **① 目标**：把 `REPO-MAP.md` 里 12 仓的 contracts / kit pin 版本与「谁已 pin、谁待升」的读数改成 2026-11-11 各仓 `go.mod` 实测值。
- **② 上下文**：DDD 边界审查 C11（2026-11-11）实测——contracts 已发 `v0.10.0`，core / agent / broker / orchestration / strategy / data 均 pin `v0.10.0`，risk / analytics 未引入；原文版本列仍写 `v0.9.0`、data `v0.6.0`、strategy `v0.5.0`，与 `go.mod` 不一致。
- **③ 要求**：① 版本列表格与「现状（实测）」段按 `go.mod` 订正；② 推进顺序段与依赖偏差段同步（含把 `RISK-CONTRACTS-SNAPSHOT-MIGRATION` 与 ADR-040 写成迁移单指针）；③ 明确本单只订正文档读数。
- **④ 约束与非目标**：不动任何仓的 `go.mod`；不替代各仓的升版单；不改 kit 的真实读数（kit 最新 `v0.3.0` 一条本就正确，原样保留）。
- **⑤ 验收**：`REPO-MAP.md` 的版本列逐仓与 `go.mod` 一致；`python tools/check_doc_links.py` 活跃层 0 断（EXIT 0）。
- **⑥ 边界**：本仓 `docs/REPO-MAP.md`；各仓 pin 的推进归各自台账。
- **收口（2026-11-11）**：commit `98a5909`；同批 `SYSTEM-DESIGN.md` §4 目标态改「core 指标权威、analytics 不迁移」、§5 新增 `public` 行（ADR-039 落点）。

---

## 2026-11-12 收口（W7 文档维护）

> 本节收 2026-11-11 全面审查 W7 立单的四条知识库维护单。任务原文按 `docs/TASKS.md` 立单版逐字保留，收口记录追加在每单末尾。

<a id="DOC-FRONTMATTER-HYGIENE"></a>
### DOC-FRONTMATTER-HYGIENE · frontmatter 过期 / ARCHITECTURE 状态错位 / ADR 索引取代标注 [P3] ✅（2026-11-12）

- **① 目标**：补齐/校准本仓文档 frontmatter 卫生，让「没有 `last-verified` 的文档视为已腐烂」这条判据可执行。
- **② 上下文**：全面审查 W1-F5（[ODR-068](odr/odr-068-audit-wave1-product-governance.md)）。实测过期：`TEST.md` `last-verified` 2026-09-25、`PRODUCT.md` 2026-10-25、`VISION.md` 2026-10-25、`ROADMAP.md` 2026-10-26（均 >2 周）；`ARCHITECTURE.md` `status: evergreen` 但本仓 AGENTS §2 目录职责已定它为「拆仓前历史 Reference（不再更新）」⇒ `status` 应 `archived`。**立单复核订正**：原列「等 5 份过期」中 `SYSTEM-DESIGN.md` / `REPO-MAP.md` 已被主任 2026-11-11 刷新（不再过期）；「3 份缺 frontmatter」根层实测仅 `AGENTS_TEMPLATE.md`（模板，可豁免——施工时全仓扫描确认其余）；「ADR.md:43 adr-024 未标部分取代」须施工时以 ADR 正文核验取代关系（ADR-024 对 AI 生成代码部分取代 ADR-001 的 `plugin.Open`，索引是否需补标注以正文为准，不预设结论）。
- **③ 要求**：① TEST/PRODUCT/VISION/ROADMAP 复核内容后更新 `last-verified`（实质漂移随 DOC-PRODUCT-DRIFT-FIX 同批改，本单只校 frontmatter 与状态）；② `ARCHITECTURE.md` `status` evergreen→archived（`type: reference` 保留），确认文件头「历史 Reference」横幅；③ 全仓扫描缺 frontmatter 的活跃层 `.md`，补齐或登记豁免（`AGENTS_TEMPLATE.md` 模板豁免）；④ 核验 `ADR.md` 索引 ADR-001/024 取代关系标注，缺则补（以 ADR 正文为准）。
- **④ 约束与非目标**：不改 ADR 正文（只改 `ADR.md` 索引标注）；不动 SYSTEM-DESIGN/REPO-MAP（已刷新）；不为了过检查器给 `archive/` 加豁免；不改文档实质内容（实质漂移归 DOC-PRODUCT-DRIFT-FIX）。
- **⑤ 验收**：活跃层 `.md` 无缺 frontmatter（豁免除外）；`ARCHITECTURE.md` `status: archived`；TEST/PRODUCT/VISION/ROADMAP `last-verified`≥施工日；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 frontmatter 与 `ADR.md` 索引标注；实质内容漂移归 DOC-PRODUCT-DRIFT-FIX。
- **owner**：待定
- **收口（2026-11-12）**：① TEST / PRODUCT / VISION / ROADMAP 四份 `last-verified` 校到 2026-11-12；② `ARCHITECTURE.md` `status: evergreen`→`archived`，`type: reference` 与文首「拆仓前历史 Reference」横幅保留；③ 全仓扫描活跃层（排除 `docs/adr` / `docs/archive`）实测缺 frontmatter 的 5 份已补齐——`AGENTS.md`、`README.md`（`status: evergreen`）与 `docs/design/data-factor-unification.md`、`docs/design/equitydeep/EquityDeep_{Product,Technical}_Specification.md`（`status: archived` + `type: reference`），仅剩 `docs/AGENTS_TEMPLATE.md` 按模板豁免；④ `ADR.md` 索引按正文补两处标注：ADR-001 标「人工编写的策略插件机制保留；AI 生成代码不加载不执行，见 ADR-024 §4」，ADR-024 标「2026-10-06 部分被 ADR-029 取代：表达式唯一载体→双轨；『不做 plugin.Open』与三条理由保留」。验收：`python tools/check_doc_links.py` 活跃层 247 条 / 0 断（EXIT 0）；破坏验证＝向 `docs/README.md` 追加一条指向不存在文件的链接 → 活跃层 248 条中 1 断、EXIT 1 → 逐字节还原 → 247 条 / 0 断、EXIT 0。

<a id="DOC-ADR-REQUESTID-CORRECTION"></a>
### DOC-ADR-REQUESTID-CORRECTION · adr-027/029/017「request-id 已跨服务传播」断言被证伪，加更正注记 [P2] ✅（2026-11-12）

- **① 目标**：给 adr-027/029/017 的「request-id 已跨服务传播」断言加更正注记，承认「机制已有、入站接线未落」，不改写已 Accepted 决策。
- **② 上下文**：全面审查 W5-F3（[ODR-072](odr/odr-072-audit-wave5-security-reliability-deps.md)）。实测断言被证伪：core `RequestIDMiddleware`（`observability/middleware.go:58`）全仓零安装点；kit gin 版有但 6 服务仓全 stdlib mux 装不上；agent 装 `HTTPTransport` 出站但未装 `RequestIDMiddleware` 入站恒空；6 服务仓 `X-Request-ID` 零命中。被证伪的 ADR 断言（实测仍在原文）：`adr-027:1314-1316`「且已有 request-id 跨服务传播」、`adr-029:126-127`「request-id 已跨服务传播」+ `:448`「rid 传播 ✅ 已有」、`adr-017:151`「`request_id` 贯穿 inbound → 下游 HTTP…两件事都已在生产路径上，不是纸面设计」。修复机制归 `tellurion-kit:KIT-REQUESTID-STDLIB` [P1] + 六仓安装（ODR-072）；本单只做文档更正。
- **③ 要求**：① 在 adr-027/029/017 各加一条**更正注记**（追加节，不改写原文）：「机制（`RequestIDMiddleware`/`HTTPTransport`/`WithRequestIDHeader`）已定义，但入站零安装 ⇒ 跨服务传播今天不成立；见 ODR-072 W5-F3 与 KIT-REQUESTID-STDLIB」；② adr-017:146-149 的 OTel/span 重开条件不动（本波只做 correlation-id 不做 tracing）；③ 注记带日期 + 指向 ODR-072。
- **④ 约束与非目标**：**不改写已 Accepted 的 ADR 正文**（ODR 只增不删，更正走注记）；不动 span/trace 重开条件；不在本单做接线施工（归 KIT-REQUESTID-STDLIB + 六仓）；不引入 OpenTelemetry。
- **⑤ 验收**：adr-027/029/017 各有更正注记节（`grep "更正注记"` + `"W5-F3"` 命中）；原断言正文逐字保留（diff 只增不改）；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 adr-027/029/017 注记；接线施工归 `tellurion-kit:KIT-REQUESTID-STDLIB` + 六仓安装（ODR-072）。
- **owner**：待定
- **收口（2026-11-12）**：三份 ADR 各追加「更正注记（2026-11-12，DOC-ADR-REQUESTID-CORRECTION / ODR-072 W5-F3）」节，写明更正对象（adr-017 `:151-152`、adr-027 `:1315`、adr-029 `:126-127` + `:448`）、实测事实（kit 仅 gin 版、stdlib `net/http` 版未落地；core `grep -rn "RequestIDMiddleware("` 仅命中 `pkg/observability/middleware.go` 定义处，各服务入站零安装；出站发头与 metrics 读 context 已存在）与结论「机制已定、安装未完成」，并指向 ODR-072 W5-F3 与 `KIT-REQUESTID-STDLIB`。原断言正文逐字保留：`git diff --numstat` 三文件均为纯新增（+12/0、+10/0、+10/0）；`grep -c "更正注记"` 三文件各 1、`grep -c "W5-F3"` 各 ≥1；adr-017 的 OTel/span 触发条件未动。`python tools/check_doc_links.py` 活跃层 246 条 / 0 断（EXIT 0）；破坏验证＝向 `docs/TASKS.md` 追加一条失败链接 → 1 断 / EXIT 1 → 逐字节还原 → 0 断 / EXIT 0。

<a id="DOC-PRODUCT-DRIFT-FIX"></a>
### DOC-PRODUCT-DRIFT-FIX · 产品入口文档接线现状停在退役波前（PRODUCT/ROADMAP）[P1] ✅（2026-11-12）

- **① 目标**：把 `PRODUCT.md` / `ROADMAP.md` 的接线现状对齐到 `SYSTEM-DESIGN.md` 基准（2026-11-11 已对齐），消除退役波后「core 侧零调用方」类过期断言。
- **② 上下文**：全面审查 W1-F3（[ODR-068](odr/odr-068-audit-wave1-product-governance.md)）。**立单复核订正**：原列 `REPO-MAP.md:16,22,25,71` 漂移**已被主任 commit `ad80a3d`（代码-文档对齐审计 2026-11-11）修复**，`SYSTEM-DESIGN.md` §5 亦已对齐 ⇒ 本单不再含 REPO-MAP/SYSTEM-DESIGN。**残留实测**：① `PRODUCT.md:61`「其余四条（策略资产/分析/编排/交易通道）今天连调用方都没有」——strategy（core resolve 出厂启用）/ broker（`SVC-CORE-BROKER-RETIRE` 2026-11-10）/ orchestration（QT-44 真 run）均已接线，analytics 是「有意为 0」（ADR-0005），故该句过期；② `ROADMAP.md:20`「X1~X6 六服务仓已实装但只有 data 一条读链真接线」同过期；③ `ROADMAP.md:18`「QT-32…仍 ⬜」——core QT-32 已收口（2026-11-10 晚）；④ `ROADMAP.md:99`「MockTrader 足够；XTP 是桩（见 `live-trading.md` 标注）」——进程内 MockTrader 已删（`SVC-CORE-BROKER-RETIRE`），且 `live-trading.md` 不存在（死链，实测 `ls` 零命中）。基准 = `SYSTEM-DESIGN.md` §4/§5（2026-11-11）。
- **③ 要求**：① `PRODUCT.md:61` 改为「今天真接线 = data 读链 + strategy resolve + risk resolve（出厂 true）+ broker HTTP（唯一通道）+ orchestration worker；analytics 有意为 0（ADR-0005）」，逐条指 SYSTEM-DESIGN §4/§5、不复制接线数字进角色表；② `ROADMAP.md:20` 删「只有 data 一条读链真接线」，改指 SYSTEM-DESIGN §4 现状；③ `ROADMAP.md:18` QT-32 状态对齐 core 台账（已收口）；④ `ROADMAP.md:99` 删 `live-trading.md` 死链 + MockTrader 表述对齐 broker 退役（XTP 挂起见 `tellurion-broker:docs/adr/0003`）；⑤ 两文件 `last-verified` 更新到施工日。
- **④ 约束与非目标**：不改 REPO-MAP/SYSTEM-DESIGN（已对齐）；不重新裁决产品边界（PRODUCT 哲学层与八条原则不动）；不复制接线数字进角色表（`PRODUCT.md:51` 刻意不复制）；不改代码。
- **⑤ 验收**：`grep -n "连调用方都没有\|只有 data 一条读链" docs/PRODUCT.md docs/ROADMAP.md` 零命中；`grep -n "live-trading.md" docs/ROADMAP.md` 零命中；`python tools/check_doc_links.py` 活跃层 0 断链；PRODUCT/ROADMAP `last-verified`=施工日。
- **⑥ 边界**：本仓 `PRODUCT.md` / `ROADMAP.md`；REPO-MAP/SYSTEM-DESIGN 已对齐不动；接线事实以 SYSTEM-DESIGN §4/§5 + 各仓台账为准。
- **owner**：待定
- **收口（2026-11-12）**：① `PRODUCT.md:61` 重写为「截至 2026-11-11 core 真正消费的远程能力」清单（data 取数 / strategy `strategy_ref` resolve / risk 限额 `resolve`（events 仍出厂 false）/ broker 唯一下单通道 / orchestration 任务队列；analytics 有意为 0 per ADR-0005），并改指 `SYSTEM-DESIGN.md` §4/§5；② `ROADMAP.md:20` 删「仅 data 接线」断言，改列五条接线现状并指 §4/§5；③ `ROADMAP.md:18` 订正为 QT-32 ✅（2026-11-10 core 台账归档）与 `QT-32-A` 已完成，S1 出口仍以「连续 100 次无人干预」整链验收为准（core/agent 台账均未见该记录）；④ `ROADMAP.md:99` 删 `live-trading.md` 死链，改指 `tellurion-broker:docs/adr/0003`，并写明进程内 `MockTrader` 已随 `SVC-CORE-BROKER-RETIRE` 退役；⑤ 两文件 `last-verified`=2026-11-12。验收：三条过期断言与死链 grep 零命中（正文与 frontmatter 均无残留）；`python tools/check_doc_links.py` 活跃层 0 断（EXIT 0）；破坏验证＝向 `docs/PRODUCT.md` 追加失败链接 → 1 断 / EXIT 1 → 逐字节还原 → 0 断 / EXIT 0。

<a id="DOC-P3-MATRIX-TABLE-GRAIN"></a>
### DOC-P3-MATRIX-TABLE-GRAIN · 已落归属裁决未对齐进残留矩阵行（run.backtest_results / 因子派生表）[P2] ✅（2026-11-12）

- **① 目标**：把两条已落裁决（`run.backtest_results` owner=core；`factor_returns`/`ic_analysis` owner=core per ADR-038）对齐进残留矩阵行，消除「schema 粒度 `run.*`→orch」与「表粒度 `backtest_results`→core」的矛盾。
- **② 上下文**：全面审查 W2-F10（[ODR-069](odr/odr-069-audit-wave2-core-architecture.md)）。**立单复核订正**：ADR-037/038 已落（commit `98a5909`/`448a87a`）；`SYSTEM-DESIGN.md` §5 已对齐（2026-11-11，`public` 行 owner=core）；core `CORE-FACTOR-DERIVED-GUARD` ✅（2026-11-11，因子派生表归 core 的代码 + 缺失原因已改）；fundamentals 行已订正（core 矩阵 `:49`，commit `c85abff`）。**残留实测**：① 本仓 `REPO-MAP.md:15`（core 拥有 schema 列「`quant` + `audit` + …`market.index_daily`」）与 `:24`（orch「`run` 六表」）按 schema 粒度把 `run.*` 全归 orch，**未显式标 `run.backtest_results` owner=core**（表粒度例外；证据 `tellurion:pkg/storage/backtest_results.go:40` CREATE + 矩阵 `:41` 裁决）；② `tellurion:docs/design/qt-decoupling/data-service-contract-and-ownership.md:43` 因子派生表行仍写 `owner = tellurion-data`（与 ADR-038 矛盾）——**该文件在 core，跨仓指针归 core，本仓不代改**。
- **③ 要求**：① REPO-MAP 显式标 `run.backtest_results` owner=core（表粒度例外，附 core `backtest_results.go:40` + 矩阵 `:41` 裁决），不把整张表改成表粒度重写；② 核验 SYSTEM-DESIGN §5 是否已含该例外（已含则只补 REPO-MAP，不重复）；③ core 矩阵 `:43` 行订正归 core（跨仓指针，附 ADR-038；本仓只登记指针不代改 core 文件）；④ 不重新裁决归属（ADR-037/038 已定）。
- **④ 约束与非目标**：不改 core 文件（跨仓指针）；不重新裁决因子/结果表归属；不动已对齐的 SYSTEM-DESIGN §5 正文（只核验）；不改代码。
- **⑤ 验收**：`grep -n "backtest_results" docs/REPO-MAP.md` 显式标 core owner；SYSTEM-DESIGN §5 例外核验记录成文；core 矩阵 `:43` 跨仓指针成文（归 core 施工）；`python tools/check_doc_links.py` 绿。
- **⑥ 边界**：本仓 `REPO-MAP.md`（+ SYSTEM-DESIGN §5 核验）；core 矩阵 `:43` 行归 core（跨仓指针，附 ADR-038）。
- **owner**：待定
- **收口（2026-11-12）**：① `REPO-MAP.md` core 行 schema 列补「表粒度例外 `run.backtest_results`」，orch 行补同注，并在 §一表后新增一条例外注（证据 = core `pkg/storage/backtest_results.go` 的 `CREATE TABLE run.backtest_results` + core 审计矩阵 `:41`）；② 核验 `SYSTEM-DESIGN.md` §5：原文 `run` 行**未含**该例外（按 schema 粒度把 `run.*` 全归 orchestration），与 core 矩阵 `:41` 不一致 ⇒ 按「以现码事实为准」在 owner 列补「表粒度例外：`run.backtest_results` 归 core，结果面单一写者；编排只经 API 读」，并把「`run.*` 是唯一状态权威」限定为「任务状态权威」；`public` 行与因子派生表归属未动；③ core 矩阵 `:43`（`factor_hypothesis` / `factor_returns` / `ic_analysis` 仍写 owner=`tellurion-data`）在 core 仓、本仓不代改，已在本仓台账新立跨仓待派指针 `CORE-MATRIX-FACTOR-OWNER-FIX`（六字段）。验收：`grep -n "backtest_results" docs/REPO-MAP.md` 命中 core owner 与 orch 例外；`grep -n "backtest_results" docs/SYSTEM-DESIGN.md` 命中 §5 例外；`python tools/check_doc_links.py` 活跃层 0 断（EXIT 0）；破坏验证＝向 `docs/REPO-MAP.md` 追加失败链接 → 1 断 / EXIT 1 → 逐字节还原 → 0 断 / EXIT 0。

---

<a id="CORE-MATRIX-FACTOR-OWNER-FIX"></a>
### CORE-MATRIX-FACTOR-OWNER-FIX · core 审计矩阵 `:43` 因子派生表 owner 仍写 `tellurion-data`（与 ADR-038 矛盾）[P2] ✅（2026-11-12，docs 侧）

> 以下六字段为收口前的台账原文，逐字保留：

- **① 目标**：把 core `docs/design/qt-decoupling/data-service-contract-and-ownership.md:43` 的 `factor_hypothesis` / `factor_returns` / `ic_analysis` 行 owner 由 `tellurion-data（SPEC-R-02）` 订正为 `tellurion`（core），与 ADR-037/038、本仓 `SYSTEM-DESIGN.md` §5 `public` 行一致。
- **② 上下文**：本仓 `DOC-P3-MATRIX-TABLE-GRAIN` 施工实测（2026-11-12）。ADR-038 已裁「因子定义与派生值同源归 core」；core 已落 `CORE-FACTOR-DERIVED-GUARD`（2026-11-11）；本仓 `SYSTEM-DESIGN.md` §5 `public` 行 owner=core（2026-11-11）；但 core 矩阵 `:43` 仍写 `owner = tellurion-data`，并称写者为 `pkg/storage/factor_hypothesis.go` 与 `cache.go`。该文件在 core 仓，本仓不代改。
- **③ 要求**：在 core 仓订正该行 owner 与说明，附 ADR-038 依据；不改 DDL / 代码（代码侧已由 `CORE-FACTOR-DERIVED-GUARD` 收口）。
- **④ 约束与非目标**：本仓不代改 core 文件；不重新裁决归属（ADR-037/038 已定）；不在本仓复制 core 矩阵正文。
- **⑤ 验收**（归 core）：该行 owner=core 且与 `SYSTEM-DESIGN.md` §5 一致；纯文档改动，`go build ./...` 不受影响。
- **⑥ 边界**：`tellurion:docs/design/qt-decoupling/data-service-contract-and-ownership.md:43`；派单、施工、验收均在 core 仓台账。
- **owner**：待定（跨仓派单）

> **施工记录（2026-11-12，docs 侧，`docs(docs): CORE-MATRIX-FACTOR-OWNER-FIX 按 ADR-037 D3 订正因子归属口径`）**：
> - **核清结论（core 侧未被任何提交修掉）**：只读核对 core HEAD `9858dd6` 的 `docs/design/qt-decoupling/data-service-contract-and-ownership.md:43`，
>   原文仍为 `owner = tellurion-data（SPEC-R-02）`，写者列 `pkg/storage/factor_hypothesis.go` 与 `cache.go`；
>   该文件最后一次改动 `6f2cc24` 只订正 fundamentals 行，与因子行无关；`git log --all` 无其它分支修复。
> - **与 ADR-037 的一致性核对**：ADR-037 §3 D2/§8（2026-11-12 落实）= 消费点按需求值、run 级内存、**不新增数据库写者**；
>   D3（2026-11-12 修订）= `public.factor_cache` **退役遗留表**：不得写入、覆盖度门禁不读它、空表是预期状态；
>   §7 = `factor_returns` / `ic_analysis` 归 core（ADR-038），`factor_hypothesis` 归 agent（core 裸表 2026-11-10 已退役）。
>   结论：core 矩阵 `:43` 与上述三处均不一致（owner、写者、`factor_hypothesis` 归属）。
> - **docs 侧订正（本仓写权内）**：
>   ① `SYSTEM-DESIGN.md` §5 `public` 行：把「`factor_cache` 零写者、按需求值为目标形态」改为
>   「按需求值已于 2026-11-12 落地（run setup → run 级内存）；`factor_cache` 已退役为遗留表：禁止新增写者、门禁不读、空表预期」；
>   ② `ARCHITECTURE.md`：Phase 3 的「因子缓存预热 Engine 从 factor_cache 加载 z-score」追加退役注记（ADR-037 D2/D3）；
>   L2 副作用示例「回测写 `backtest_jobs`、因子写 `factor_cache`」改为「回测写 `run.backtest_results`、因子按需求值落 run 级内存、不写 `public.factor_cache`」。
> - **未覆盖（跨仓边界，如实登记）**：core 矩阵 `:43` 本行未改——core 仓本轮归其它会话写权，本仓不代改；
>   待 core 仓台账派单后按本条目 ①②⑤ 施工（owner 分三行：`factor_returns`/`ic_analysis`→core，`factor_hypothesis`→agent/`ai.*`）。
> - **验收**：`grep -n "factor_cache" docs/SYSTEM-DESIGN.md docs/ARCHITECTURE.md`——§5 旧口径「按需求值为目标形态」已消失；
>   ARCHITECTURE 的历史更新清单保留原句（不改写历史），但紧邻下一行是「已退役（ADR-037 D2/D3）」注记，L2 副作用句已改为不写 `public.factor_cache`；
>   `python tools/check_doc_links.py` 活跃层 246 条链接 0 断、EXIT=0（历史层 174 断仅统计不判红）；纯文档改动，不涉代码门禁。

---

## 2026-11-13 五角审查批次（DOC-17~DOC-29）

### 立单原文（2026-11-13，随施工记录一并归档）

> 来源：`docs/reviews/2026-11-13/`（`index.md` + 五个角度）。本轮按审查推进顺序分档落单，**只写台账，不改既有文档**；沿用六字段与既有状态图例。每条标题下的「档 / 来源 / 顺序 / 依赖」行为施工顺序与跨仓指向。完成后按惯例移入归档。

#### 档 1 · 文档架构与卫生

### DOC-17 · 入口页五项失效目标一次性校准 [P1] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H1 · 顺序 1-1 · 依赖：无

- **① 目标**：把 `docs/README.md` 主入口上 5 处指向"不存在 / 已变化"对象的表述改为实测现状。
- **② 上下文**：审查实测证据——`README.md:101` 指 `archive/2026-Q2/*`（实际为 `archive/reports-2026-Q2/` 与 `archive/research-2026-Q2/`）；`:86` 写"文档链接 CI 当前缺失，见 TASKS.md P0"（台账已无 P0）；`:50` 写服务卡"12 仓未落地"（12 份 `SERVICE.md` 全部存在）；`:45` 写 ADR"31 条；编号至 ADR-036"（实际 41 条、至 ADR-041，见 `ADR.md:195`）；`:97` 写归档 ODR"001–064"（实际 73 份，至 ODR-073），且 superseded 列表漏 ADR-022。
- **③ 要求**：逐项改为实测值：① 归档路径改两个真实子目录；② CI 句改为"链接检查已进 CI（`.github/workflows/docs-ci.yml`）"并删 P0 指引；③ 服务卡改"12 仓已落地"；④ ADR 改"41 条、至 ADR-041"；⑤ ODR 改"001–073"，superseded 补 ADR-022。
- **④ 约束与非目标**：只改入口页事实；不重排导航结构；不动归档正文与 ADR 正文。
- **⑤ 验收**：5 处逐一核对为真值；`grep -n "31 条\|001–064\|archive/2026-Q2" docs/README.md` 0 命中；文档链接检查 CI 绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/README.md`。
- **施工记录（2026-11-13）**：`81f5382`：README 五处改为实测值（归档路径 / CI / 服务卡 / ADR 41 条 / ODR 001–073 + ADR-022）；`tools/check_doc_counts.py` 同批上线。

### DOC-18 · 入口页关键计数改为脚本校验 + 落实 R5 文档可验证 CI [P2] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H1 建议 1 + 评分表「R5 自述缺失」 · 顺序 1-2 · 依赖：DOC-17（先校准，避免校验固化错值）

- **① 目标**：ADR 条数 / ODR 范围 / 服务卡覆盖 / 归档目录清单由脚本校验（或生成），并把 R5 写回治理规则。
- **② 上下文**：H1 的根因是手写数字无校验；仓库已有 `scripts/check_doc_links.py` 的 CI 接入模式可扩展；R5"文档可验证 CI"在评分表中被记为自述缺失且台账无开放项。
- **③ 要求**：① 扩展/新增文档校验脚本：比对 `ADR.md` 条数与 `adr-0*.md` 文件数、`archive/odr/` 范围、12 仓 `SERVICE.md` 存在性、`README.md` 计数段落；② 接入 docs CI；③ `README.md` 治理节把"R5 缺失"改为"由脚本校验（命令/CI 位置）"。
- **④ 约束与非目标**：不引入新依赖；不改其他仓 CI；只读其他仓文件做存在性校验；本轮不追求自动改写。
- **⑤ 验收**：人为改错一处计数 → CI 红；逐字节还原 → 绿（破坏验证）；台账/README 不再出现"R5 缺失"。
- **⑥ 边界**：`tellurion-docs` 的 `scripts/`、`.github/workflows/docs-ci.yml`、`docs/README.md`。
- **施工记录（2026-11-13）**：`1085cff`：新增 `tools/check_doc_counts.py`（ADR/ODR/服务卡/计数/pin 四条腿）并接入 `.github/workflows/ci.yml`；破坏验证：改错 ADR 计数 → 红，还原 → 绿；README 治理节改写 R5。

### DOC-19 · SYSTEM-DESIGN 部署句改指 core `docker-compose.yml` [P1] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H2 · 顺序 1-3 · 依赖：无

- **① 目标**：删除常青文档对已删除部署资产的引用。
- **② 上下文**：`SYSTEM-DESIGN.md:133` 写"本地联调走 `docker-compose.services.yml`"；core 实测只剩 `docker-compose.yml`，core `ARCHITECTURE.md` frontmatter 记录 2026-11-11 已删 `.services.yml`/`.e2e.yml`/`.nt.yaml` 三份。
- **③ 要求**：§5 部署句改为 `tellurion:docker-compose.yml` + profile；全文扫 `.services.yml`/`.e2e.yml`/`.nt.yaml` 残留，改指或删除。
- **④ 约束与非目标**：只改部署事实，不动架构描述；不复制 compose 内容；不替 core 改仓。
- **⑤ 验收**：活跃文档 `grep -rn "docker-compose.services"` 仅归档层命中；SYSTEM-DESIGN 无死引用；链接检查 CI 绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/SYSTEM-DESIGN.md`。
- **施工记录（2026-11-13）**：`b7b8348`：SYSTEM-DESIGN §7 部署句改 `docker-compose.yml` + `--profile`；guides/local-dev、deploy-config、TEST.md 同批标注三份细分 compose 已于 2026-11-11 删除。

### DOC-20 · 把 archived 的 ARCHITECTURE 移出活跃导航 [P1] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H3 · 顺序 1-4 · 依赖：无

- **① 目标**：终止"归档文档仍被当作推荐读物"的 R2 自违反。
- **② 上下文**：`docs/ARCHITECTURE.md` frontmatter 为 `status: archived`，却出现在 `README.md:37` 主表与 `:56` 推荐顺序；该文件自述"端口/表数已失效"，体积 65.9KB。
- **③ 要求**：① 从 README 主表与推荐顺序移除；② 在归档层（或其归档位置）保留一条"历史架构参考"入口；③ 若该文件仍留在 `docs/` 根，按 R2 评估移入 `archive/` 或降级为脚注。
- **④ 约束与非目标**：不删除文件、不改其正文；不再放回导航。
- **⑤ 验收**：README 导航与推荐顺序 0 处指向 ARCHITECTURE；R2 自检通过；链接检查绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/README.md`（及可能的文件位置调整）。
- **施工记录（2026-11-13）**：`ad440f6`：ARCHITECTURE 移出 README 主表与推荐顺序；`git mv` 至 `archive/ARCHITECTURE-pre-split.md`，仅改顶部指针。

### DOC-21 · 版本 pin 与 ADR 状态的「单一真相」收敛 [P2] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H4 · 顺序 1-5 · 依赖：无（数字对错由 DOC-28 承接）

- **① 目标**：消除"同一事实两处写、两处错"。
- **② 上下文**：`REPO-MAP.md:46` 自称 pin 规则"唯一处"；但 `SYSTEM-DESIGN.md:124/134` 仍复制 contracts/kit 版本数字；`ADR.md:4` 的 verified-by 自认"索引表与尾注两处是两套真相来源"。
- **③ 要求**：① `SYSTEM-DESIGN` §2 的 pin 数字改为指针（只留 `REPO-MAP` 链接，不写版本号）；② `ADR.md` 尾注改为"索引表为唯一状态源"，不再重复维护状态；③ 在 DOC-18 的校验脚本中加 `go.mod` pin ↔ `REPO-MAP` 比对（只读其他仓）。
- **④ 约束与非目标**：不删 ADR 正文与历史记录；不取得其他仓写权；本条只做机制，具体数字订正归 DOC-28。
- **⑤ 验收**：`SYSTEM-DESIGN` 不再出现具体 pin 版本号；人为改错 pin → 校验脚本可检出（破坏验证）。
- **⑥ 边界**：`tellurion-docs` 的 `SYSTEM-DESIGN.md`、`ADR.md`、校验脚本。
- **施工记录（2026-11-13）**：`5395205`：REPO-MAP §版本 pin 改机器可读表（pins 标记）+ go.mod 比对腿；SYSTEM-DESIGN §2 去版本号只留指针；ADR.md 明确「索引表 = 唯一状态源」并删重复状态清单。

### DOC-22 · 归档层可信索引重建 + status 语义修正 [P2] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H5 · 顺序 1-6 · 依赖：无（可与 DOC-18 共用脚本）

- **① 目标**：`archive/README.md` 覆盖全部 6 个子目录 + 11 个顶层文件；归档文件 frontmatter 统一 `status: archived`。
- **② 上下文**：`archive/README.md:41` 目录树停在 2026-04-11、只列两个子目录，漏 `odr/`、`superseded-adr/`、`plans-2026-Q3/`、`reports-2026-Q3/`、`tasks-archive-2026-11.md`、`TASKS-history.md`、`VISION-full.md` 等；`:29` 指向已不存在的 `docs/odr/`；顶层 11 份 .md 中 `TASKS-2026-10-08-archived.md:2` 与 `REORG-PLAN.md:2` 仍是 `status: active`。
- **③ 要求**：① 重写 `archive/README.md` 为"子目录 + 顶层文件 + 日期 + 一句话"清单（优先由 DOC-18 脚本生成）；② `docs/odr/` 死指针改为 `archive/odr/`；③ 两份 `status: active` 改 `archived`；④ 在归档 README 写明"索引维护是归档层唯一例外"。
- **④ 约束与非目标**：不改归档正文内容；只动索引与 frontmatter status。
- **⑤ 验收**：脚本比对归档实测清单缺口为 0；活跃文档无 `docs/odr/` 指针；`^status:` 扫描归档顶层 0 个 `active`。
- **⑥ 边界**：`tellurion-docs` 的 `docs/archive/`。
- **施工记录（2026-11-13）**：`848b08c`：`archive/README.md` 重建为 17 条清单（11 顶层文件 + 6 子目录）+ `tools/check_archive_index.py` 双向覆盖；`REORG-PLAN.md` / `TASKS-2026-10-08-archived.md` 的 `status: active` → `archived`。

### DOC-23 · ADR-027 标 Superseded + 变更日志单调化 [P3] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H6 · 顺序 1-7 · 依赖：无

- **① 目标**：消除"两条服务拓扑结论并存"；决策台账时间线可顺序阅读。
- **② 上下文**：`ADR.md:46-L49` 中 ADR-027/028/029 自 2026-10-06 维持 `Proposed`、ADR-030 维持 `Draft`；ADR-027 主题"模块化拆解为独立服务（5→7）"已被 2026-10-26 的 ADR-036（12 仓拓扑，`ADR.md:190` 明写修订 027 §2.1）取代，却未标 `Superseded`；`:191` 的 `_Last updated_ 2026-10-14_` 夹在 10-26 与 11-11 条目之间，`:197` 又是 10-13，日志非单调。
- **③ 要求**：① ADR-027 索引状态改 `Superseded by ADR-036`，并在 adr-027 文件头加一行注记（不改正文）；② 变更日志按日期单调整理；③ `_Last updated_` 更新为本次。
- **④ 约束与非目标**：ADR-028/029/030 的状态不在本条擅自改判，只记录现状；不动 ADR-036。
- **⑤ 验收**：ADR 索引中 027 状态与链接正确；变更日志日期单调；链接检查绿。
- **⑥ 边界**：`tellurion-docs` 的 `docs/ADR.md` + `docs/adr/adr-027*.md` 头部注记。
- **施工记录（2026-11-13）**：`777eca2`：ADR-027 索引状态改 `Superseded by ADR-036`，文件头加注记（未搬迁，因 40+ 入链）；变更日志按日期降序单调（40 块，脚本校验 monotonic=True）。

### DOC-24 · ROADMAP S2 改为「部分达成」 [P3] ✅ 2026-11-13

> 档 1（文档架构与卫生）· 来源：05-doc-hygiene H7 · 顺序 1-8 · 依赖：与 DOC-25 口径一致

- **① 目标**：阶段台账反映"产业链底座已实现、`hypothesis_source` 未实现"的真实状态。
- **② 上下文**：`ROADMAP.md:40` 把 S2 标"⬜ 待开始"，出口判据第一条"产业链数据底座可用"；但 core 已装配 `/api/industry/*`（SW 行业树 / 供应链边 / 行业活力 / ETF 成分）与 `/api/macro/series`，core `openapi.yaml` tag 描述写明 `Industry (P2-2)`、`Macro (P2-1)`。
- **③ 要求**：S2 状态改"🔶 部分达成：产业链底座 ✅ / `hypothesis_source` ⬜"，并在出口判据逐条标注已满足项。
- **④ 约束与非目标**：不改 S2 目标本身；不因部分达成提前进入 S3。
- **⑤ 验收**：S2 状态与出口判据自洽；与 `PRODUCT.md` 的能力状态表述一致（见 DOC-25）。
- **⑥ 边界**：`tellurion-docs` 的 `docs/ROADMAP.md`。

#### 档 2 · 产品设计
- **施工记录（2026-11-13）**：`04182ff`：ROADMAP S2 改「🔶 部分达成（底座 ✅ / hypothesis_source ⬜）」，附 core openapi Industry P2-2 / Macro P2-1 证据。

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

### DOC-29 · `TEST.md` 改为历史快照或读数链接 [P1] ✅ 2026-11-13

> 档 5（文档与代码一致性）· 来源：04-doc-consistency P1-2 · 顺序 5-2 · 依赖：无

- **① 目标**：消除 `TEST.md` 正文现在时陈述与实际测试状态相反的三处。
- **② 上下文**：`:438` 写"CI 不设覆盖率阈值"（实际 core 有 `-total-min=52`）；`:478` 前端"18 个文件 / 208 条"（当日实测 52 / 643）；`:567/:585` e2e"18 spec / 163 例、127 passed / 34 failed"（实际 31 spec、211 passed / 7 failed）；frontmatter 虽标"正文未改，实质基线 2026-09-22"，但正文会被外部读者当现状。
- **③ 要求**：建议 **B 更新读数并注明日期与日志链接**（§6/§7 的计数改为"截至某日 + `reports/...` 或 CI 链接"）；其余章节保留 2026-09-22 历史快照并加顶部横幅"历史快照，勿引用数字"。也可选 **A 全篇历史快照**。
- **④ 约束与非目标**：不虚构读数；不把未复跑的测试写成通过；不改 `TEST.md` 之外的文件。
- **⑤ 验收**：全文无"现在时 + 过期数字"混用；每个计数都有日期与来源；`grep "18 个文件\|208 条\|127 passed"` 不再作为现状出现。
- **⑥ 边界**：`tellurion-docs` 的 `docs/TEST.md`。
- **施工记录（2026-11-13）**：`13a031b`：TEST.md §6 覆盖率门 `-total-min=52`、§7.1 52 文件/643 条、§7.2 31 spec/218 例，文首加快照声明；README 导航行同步。
