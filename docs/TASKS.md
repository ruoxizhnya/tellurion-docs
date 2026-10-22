---
status: active
last-verified: 2026-10-22
verified-by: DOC-08 结案（三份 guide 改 12 仓口径 + 新护栏 `check_guide_refs.py` 21 条夹具腿 + CI 接仓名腿）
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
| DOC-06 | `PRODUCT.md` / `VISION.md` 按新定位重写 | ⬜ | 导航里已标"待重写"；需先有产品口径（分仓后单一产品变成"底座 + 实验员 + 前端 + 六服务"） |
| DOC-07 | 12 仓文档一致性巡检脚本 | ✅（2026-10-22） | 现在靠人眼：每仓应有 `AGENTS.md` + `db-schema` / `api-schema` / `dataflow` + `TASKS` + `adr/` + `odr/`。**豁免注记（2026-10-21 裁决，spec 审查 H1/L3）**：core 与本仓豁免三件薄规格与 `adr/0001-*`（API/DB/流程真相由 `tellurion:docs/openapi.yaml` / `tellurion:pkg/storage/postgres.go` / `tellurion:docs/SPEC.md` 直接承载），巡检脚本须实现该豁免分支，不得对两仓报缺件。可写成 `tools/check_repo_docs.py`（与 core 的 `check_repo_autonomy.py` 互补：那边查仓自治，这边查文档齐套）。**落地（2026-10-22）**：`tools/check_repo_docs.py`（只查存在性与形状，不读正文）+ `tools/test_check_repo_docs.py`（17 条夹具腿，stdlib unittest）。按 ticket 实现 core / 本仓的豁免分支，并**按实仓取证追加两条具名豁免**（见下行「偏差」）：core 的 `adr/` 与 `odr/` 也已随文档拆分迁走（ADR 住 `tellurion-docs/docs/adr`、ODR 住 `tellurion-docs/docs/archive/odr`，core AGENTS.md §10 记录）；本仓 ODR 家是 `docs/archive/odr` 而非 `docs/odr`（AGENTS.md §3.6），故判据接受两个 ODR 家。真跑：`python tools/check_repo_docs.py --explain` → 退出码 **0**，12/12 齐套、缺件 0、豁免 2 仓。破坏验证（临时夹具，不动真仓）：完整夹具 0 → 删 `tellurion-ui/docs/dataflow.md` → **1** 并点名该文件 → 还原 → **0**；另有「缺 AGENTS / TASKS / 单件规格 / adr 目录 / 0001 / ODR 家」「仓目录不存在」「未登记仓名」各一条红腿。**不进 CI**：CI 只 checkout 本仓，看不到另外 11 个仓（详见 AGENTS.md §1）。 |
| DOC-08 | `docs/guides/` 按 12 仓更新 | ✅（2026-10-22） | 三份全部改 12 仓口径：**`local-dev.md`** 新增「按目标选最小 checkout 集」+ 同级硬约束（agent 的 `replace tellurion => ../tellurion`、compose 的 `context: ../tellurion-agent`）+ `go.work` 的真实定位（**今天可选**：core 尚未 `require` 两库仓；一旦切依赖才必需）+ 每仓 CI 同款命令 + 端口一览；**`deploy-config.md`** 新增「部署资产分在三个仓」（ui 的 `Dockerfile`/`nginx-spa.conf`、agent 的 `Dockerfile` 要 core 作命名上下文、`deploy/k8s/` 含 web 清单仍在 core）+ 护栏覆盖面边界表（nginx conf / agent Dockerfile / ingress backend / `RUN` 里的 `go build` 四处**无护栏**）+ web 改端口跨两仓清单；**`data-dependencies.md`** 新增 §0 仓归属表（取数/同步今天仍在 core，`tellurion-data` 仍占位）+ adapter 表 9 → **12**（补 `tushare_macro` / `tushare_daily_basic` / `tushare_moneyflow`）+ 凭据表加「**谁读它（哪个仓）**」列。**订正七处已失效/错误的陈述**：① `docker-compose.yml` 的服务是 data/analysis/**ai**（原文写 strategy/web，两者都不在）；② `cmd/ai` 未删除 —— 它在 `tellurion-agent:cmd/ai`；③ 前端 `web/` 已迁 ui 仓（旧文把它按 core 目录写，还钉着 vitest 208 条 / 18 文件；今天 ui 是 38 个测试文件）；④ 连接串库名 `tellurion`（原文 `quant_trading`）；⑤ `AI_API_KEY` 读取点已迁 `tellurion-agent:pkg/ai/client.go`（core 全仓无读取者，compose 给 analysis 的注入是死注入）；⑥ 原文「`make build` 会失败，因为 `Makefile` 仍 build 已删目录」**已不成立** —— `Makefile` 现在只 build `cmd/analysis` 与 `cmd/data`（实测 `git grep '^build'`），真障碍是本机没装 `make`；⑦ 原文「`cp .env.example .env` 然后 `go run`」**跑不起来** —— Go 侧无 dotenv 加载器（`grep godotenv` 零命中），`.env` 只服务 compose，原生跑法须 `export DATABASE_PASSWORD`，否则 `pkg/storage.BuildDSN` 以 `ErrEmptyDBPassword` 退出。**三处实测新增的坑（原文没有）**：① core `Dockerfile.service` 仍 `go build ./cmd/strategy`（目录 REV-16 已删）⇒ **容器那半今天构建不出来**，`docker run golang:1.25-alpine … go build ./cmd/strategy` 实测 `directory not found`；② agent 仓没有 `config/` 目录而 `LoadConfig` 缺文件即 Fatal ⇒ 原生跑 `cmd/ai` 必须 `CONFIG_PATH=../tellurion/config/ai-service.yaml`；③ 上条 ⑦ 的 `DATABASE_PASSWORD`。**新增护栏** `tools/check_guide_refs.py`（`repo:path` 纯文本跨仓引用；仓名腿进 CI，`--workspace` 腿工作区级不进）+ `tools/test_check_guide_refs.py`（**21 条**夹具腿，含 4 条实测踩到的截断/误判回归腿：`localhost:5432/...` 被当仓名、`...` 省略号被当路径、中文 ADR 文件名被截断、否定词按行窗口）。验收实测：`check_doc_links.py` 活跃层 **210 条 / 0 断**（历史层 166 断只统计）；`check_guide_refs.py --workspace ..` 退出 **0**；破坏验证（往 guide 塞 `tellurion:pkg/ai/pipeline` + `telliurion:docs/TASKS.md`）→ **2 处红、退出 1** → 还原逐字节 → 退出 0；`test_check_guide_refs.py` **21/21 OK**（含一条钉住仓清单必须是 12 条的腿）。 |
| DOC-09 | ADR-D24/D25/D29/D30 升格为正式 ADR | ✅（2026-10-22） | 升格为四张：**ADR-032**（D24 模块拓扑与跨进程边界）· **ADR-033**（D25 执行载体落地顺序）· **ADR-034**（D29 分仓拓扑与 S0~S3 阶梯）· **ADR-035**（D30 仓清单与命名，**含本轮待裁决 A/D/E/F/G/H 附录**）。四处失效假设就地标注不得照抄：D24 第 1 条已被 M1/D29 §5 替代（domain 并入 contracts）、R 系列是 R1~R6（源文仍写五条）、host 函数 12 个（原写 13）、D29 的 S1 形态已被 ADR-D31 替代。**两处工单描述订正**：① 本行原称「D24（`ai.*` schema 自持）」——那条内容实为 **D10**（`ai.*` 的 DDL/migrate 归 agent，源文 core `target-module-topology.md` 的 ADR-D10 节），本批按源文实际内容升格，**D10 未列入本轮四张**（要升格请另立单）；② 原称「D29（待裁决表压缩/连带 L1)」，现行 D29 的承重内容是拓扑与 R/C/S 阶梯，待裁决表在 core `README.md` 而非 D29 正文。D31 未并入（它替代的是 D29 的 S1 形态，本身仍是设计集条目，升格与否待单独裁决）。索引表 + `ADR.md` 尾注 + 四份文件头三处一致 |

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
