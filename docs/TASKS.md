---
status: active
last-verified: 2026-10-25
verified-by: DOC-06 结案（2026-10-25）：口径三问全部拍定（均取 §四 建议 A），PRODUCT 新增「系统构成」一节、VISION 只加指针不动八条原则与优先级序，docs/README 两行导航换成「现行」；同日新立 DOC-10（`SYSTEM-DESIGN.md` §7 的"六服务只有占位 doc.go"与实仓冲突）
---

# TASKS — tellurion-docs

> **本仓台账只放"知识库维护"**：导航、坏链、过时声明、索引补齐。
> **跨仓施工任务不在这里**——它们在 [`tellurion:docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md)。建单前先问：这件事是不是"改文档结构"？不是就别在本仓建。

## 一、状态图例

| 标记 | 含义 |
|---|---|
| ⬜ | 未开始 |
| 🔶 | 进行中 |
| ✅ | 已完成（保留一行结论，便于追溯） |

## 二、本仓任务

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
| DOC-10 | `SYSTEM-DESIGN.md` §7 的"今天"栏已过时 | ⬜（2026-10-25 取证立项） | §7 的「已知过渡态」写**六个服务仓只有占位 `doc.go`**、阶梯表写 **X1~X6 未触发**。**同批逮到第二处同类，且是本仓自我矛盾**：`docs/README.md` 的「仓清单与命名」行仍写「工单 QT-60，**未启动**」，而同仓的 SYSTEM-DESIGN §7 自己就记着 **S-1（12 仓改名 + 建仓 + 推送）✅ 完成（QT-60）**——导航与被导航的文档打架，读者无从判断该信哪份。2026-10-25 只读实仓取证：六个服务仓各有真 `cmd/*service` 监听 + 自有 schema 的 PG 装配（`data :8081` / `risk :8086` / `strategy :8085` / `analytics :8087` / `orchestration :8088`），core 侧装了 data 与 risk 两个消费者（risk 两条腿出厂默认关，见 §四 F2），其余四个 core 侧零调用方。⇒ 这几处"今天"不再是现状，会被读者当成设计。**§5「今天实际」列本单不预判对错**：core 无 analytics/orchestration 客户端这一条与它「今天在 core `cmd/analysis` 内直接算」一致，但 `analysis.*` / `run.*` / `risk.*` 已在各仓 own schema 里有 PG 装配，该列是否要改按各仓 `docs/db-schema.md` 逐格核对后再定，不跟着 §7 一起顺手改。**本单只改时间陈述，不改设计**：§2 五原则、§3 依赖边、§6 永不拆的六条都不动。收口判据：① §7 过渡态三条逐条对照各仓 `AGENTS.md` 的「状态」节改写（引用写 `repo:path` 纯文本，不复制正文）；② §5「今天实际」列逐格对着各仓 `docs/db-schema.md` 判"仍成立/需改"，改的要有实仓出处；③ 阶梯表 `X1~X6` 的触发状态与 core 台账一致；④ `docs/README.md` 的 QT-60 那行与 SYSTEM-DESIGN §7 对齐（两者必须同判，不再各写各的）；⑤ `python tools/check_doc_links.py` 活跃层 0 断。上游依赖：无（可独立做）。与 DOC-06 的关系：DOC-06 是**产品叙事层**（已结案），本单是**总体设计层的时间陈述**（不需口径，只需核对），两单不互相阻塞 |

> **DOC-07 偏差登记（2026-10-22，回实仓取证，不照抄通用清单）**
>
> 1. **core 的 `adr/` 与 `odr/` 也已不存在**：工单只豁免了三件薄规格与 `adr/0001-*`，但实测 core `docs/` 下既无 `adr/` 也无 `odr/`（也不存在 `docs/archive/odr/`）——ADR 已全部住 `tellurion-docs/docs/adr`，ODR 住 `tellurion-docs/docs/archive/odr`，core AGENTS.md §10 自己就记着这处漂移。若按通用清单报缺件，巡检每天都会给一个**已知且有意**的"缺"报警，护栏会很快被训练成噪声。故对这两项给 core 具名豁免，理由写在 `EXEMPT` 表里、`--explain` 可查。
> 2. **本仓的 ODR 家不是 `docs/odr/`**：本仓 AGENTS.md §3.6 明写"本仓历史 ODR 在 `docs/archive/odr/`"。判据因此接受 `docs/odr/` **或** `docs/archive/odr/` 任一非空目录（其余 10 仓用的是前者）。
> 3. **不进 CI**：脚本要看见 12 个仓目录，而本仓 CI 只 checkout 自己。它是工作区级工具（本地跑），不冒充 CI 门禁。

## 三、跨仓指针（不在本仓，勿双写）

| 事项 | 去哪 |
|---|---|
| 仓自治不变量 R1~R6 的机械检查 | core `tools/check_repo_autonomy.py`（QT-08 ①，未写） |
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
