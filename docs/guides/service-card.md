---
status: evergreen
last-verified: 2026-11-11
verified-by: 首版规范设计 —— 实读 core / data / broker / contracts 四仓的 README、AGENTS、ARCHITECTURE、api-schema、runbook、go.mod 与 compose/config；卡片只保留稳定字段，端口与端点一律指向单一真相
---

# 服务卡（Service Card）规范

> **一句话**：服务卡是给"路过的人"的 5 分钟入口——知道这个仓**是什么、不做什么、和谁相连、坏了先看哪**。
> 它不是 README 的替身，也不是 API / DB / 架构文档的摘要；它只做**索引的索引**。

---

## 1. 问题与边界

### 1.1 它解决什么

今天要回答"这个服务是什么、和谁连、依赖什么、坏了找谁"，得在四五个文件之间跳：

- `README.md`：定位与快速开始，但常被大段状态说明淹没；
- `AGENTS.md`：边界很清楚，但写法每仓不同，且面向"要改代码的 agent"；
- `docs/ARCHITECTURE.md`：有依赖方向，但藏在长文里；
- `docs/api-schema.md` / `db-schema.md` / `dataflow.md`：精确，但读者得先知道该看哪一份；
- `config/` / `deploy/compose.yaml`：端口、探针、镜像的真相，但不像给人读的入口。

服务卡把**稳定的那几件事**压到一屏：职责、边界、入边/出边、影响面、owner、真相源入口。

### 1.2 它不解决什么

| 不做 | 去哪看 |
|---|---|
| 不列端点、错误码、幂等语义 | 该仓 `docs/api-schema.md` |
| 不列表、字段、DDL | 该仓 `docs/db-schema.md` |
| 不画内部模块图、不解释实现 | 该仓 `docs/ARCHITECTURE.md` |
| 不写当前任务与进度 | 该仓 `docs/TASKS.md` |
| 不写启动命令、环境变量清单 | 该仓 `README.md` / `config/` / compose |
| 不做服务目录平台、不替代 Backstage | 本项目是 12 仓的单人实验室，不需要 |

> **判断标准**：卡片里的一条信息，如果删掉后读者只是"多点一次链接"，那它就不该在卡片里。

---

## 2. 现状盘点（2026-11-11）

实读了四个有代表性的仓：core、data、broker、contracts。结论如下。

### 2.1 已经有的，且够用

| 信息 | 今天在哪 | 评价 |
|---|---|---|
| 一句话定位 | 各仓 `README.md` 首段 | 有，但常被"状态：X1c/X6c/..."的长段落盖住 |
| 允许/禁止边界 | 各仓 `AGENTS.md` §3 | 质量高，是卡片 §2 的最佳来源 |
| 依赖方向 | core `docs/REPO-MAP.md` 全局图；各仓 `docs/ARCHITECTURE.md` §5 | 全局有，单仓视角要翻 |
| 对外接口 | `docs/api-schema.md`（contracts 用 `docs/API.md`） | 单一真相，卡片不应复制 |
| 数据归属 | `docs/db-schema.md` | 单一真相，卡片不应复制 |
| 数据流与 fail-closed | `docs/dataflow.md` | 单一真相 |
| 起停与排障 | 六个服务仓都有 `docs/runbook.md`；core/agent/ui 没有 | 覆盖不齐：应用仓缺；卡片需要统一入口 |
| 版本 pin | `go.mod` + `AGENTS.md` §4 + `REPO-MAP.md` 版本矩阵 | 三处都在变，卡片不应再抄第四份 |

### 2.2 今天缺的，或太散的

1. **一屏式"是什么 + 不做什么"**：README 的定位句和 AGENTS 的边界段不在同一页，且中间隔着大量状态说明。
2. **单仓视角的入边/出边表**：全局图告诉你有边，但不告诉你"这条边用来干什么、对方挂了会怎样"。
3. **影响面（impact）**：没有统一字段说明"这个仓挂了，是主链路断、局部降级，还是只影响编译"。
4. **owner 与升级路径**：12 仓没有 `CODEOWNERS` / `OWNERS`；跨仓争议的入口在 core `docs/TASKS.md`，但单仓文档里没有一句话指过去。
5. **探针语义**：data 的 `/health` 与 `/readyz` 语义写得很清楚，但散在 api-schema §1.1；broker 的就绪口径在 runbook §1；core 的在 README 快速开始。六个服务仓虽然都有 runbook，但卡片没有统一入口把它们串起来；core/agent/ui 则完全没有 runbook。
6. **真相源地图**：每个仓都有 5~7 份文档，但没有一张"我想知道 X，去读 Y"的小表。
7. **易变数字被反复手写**：端点数、表数、导出符号数、端口、pin 版本，在 README / AGENTS / REPO-MAP 里各有一份，任何一次发版都可能让其中一份过期。

> 服务卡的价值不是"再加一份文档"，而是**把第 1~6 项补成一屏，并明确第 7 项不进来**。

---

## 3. 业界参考与取舍

| 实践 | 借什么 | 不借什么 | 理由 |
|---|---|---|---|
| **Backstage `catalog-info.yaml`** | 实体身份（`kind` / `lifecycle` / `owner`）、`dependsOn` / `providesApis` / `consumesApis` 的边模型 | 完整 catalog schema、`system` / `domain` / `tag` / `annotation`、API 实体、插件生态 | 本项目没有 catalog server；抄全量 schema 会变成第二份真相源 |
| **C4 model Context Diagram** | "系统在中间，人/外部系统在四周"的上下文视角；关系要写"用来做什么" | 强制画图、Container/Component 层 | 图会过期；文字边表更便宜，且能被脚本核对 |
| **SRE runbook card** | 影响面、前三条排查、升级路径、runbook 指针 | SLO、告警面板、值班表、错误预算 | 本项目没有 Prometheus/告警体系（data 明确"不接 Prometheus"），写了就是空头承诺 |
| **Team Topologies ownership** | 一个服务一个明确 owner；跨边界交互要有约定 | 团队认知负荷、交互模式（X-as-a-Service 等） | 单人项目，团队字段是形式主义 |
| **ADR / README 的 pointer 文化** | 能指向单一真相就绝不复制 | — | 这是本仓 `AGENTS.md` §3 的硬约束，也是卡片不腐烂的前提 |

---

## 4. 两个候选模板对比

### 候选 A：薄 frontmatter + 固定 7 段正文（**采用**）

- 顶部 15~20 行 YAML：只放机器可读的**稳定身份**（repo / kind / lifecycle / owner / impact / 边 / 真相源路径）。
- 正文固定 7 段：这是什么 → 不做什么 → 与谁相连 → 运行时身份 → 数据与契约归属 → 坏了怎么办 → 5 分钟后去哪。
- 正文里不出现端口、URL、版本、端点/表数量。

### 候选 B：纯 Markdown 单表

- 一张 10~15 行的表：服务名 / 类型 / 职责 / 端口 / 依赖 / 端点 / owner / runbook。
- 优点：最好写、最好扫。
- 缺点：**必然复制端口、端点、版本**；没有机器契约；三个月后一定有过期数字。它把"5 分钟读完"建立在"数字刚好还对"上。

### 候选 C：完整 `catalog-info.yaml`（否决）

- 按 Backstage 实体模型写全量 YAML，再配一段说明。
- 优点：业界标准，未来可接目录平台。
- 缺点：12 仓、单人维护、没有 catalog server；`spec.dependsOn` 会与 `go.mod` / compose 形成第三份真相；写作成本高，读者仍然要另读 README 才知道"它到底干什么"。

### 对比结论

| 维度 | A | B | C |
|---|---|---|---|
| 5 分钟可读 | 高 | 高 | 低（YAML 不是给人读的） |
| 机器可校验 | 高（薄 schema） | 低（要解析表格） | 高 |
| 腐烂风险 | 低（不写易变数字） | **高** | 中（边和版本会漂移） |
| 与现有文档重复 | 低（只放指针） | 中（复制端口/端点） | 高（复制依赖与 API 实体） |
| 写作成本 | 中 | 低 | 高 |
| 适合本项目 | **是** | 否 | 否 |

**采用 A**。B 的可读性目标通过"固定 7 段 + 一屏长度"保留；C 的机器可读性通过薄 frontmatter 保留，但**不引入完整 catalog schema**。

> **选型状态**：本文按候选 A 成稿，供评审确认；B/C 的对比保留在本节，若改选只需替换 §5 的字段表与模板文件，不影响 §5.4「稳定/易变分界」的结论。

---

## 5. 最终规范

### 5.1 文件位置与命名

- 每个仓根目录：**`SERVICE.md`**。
- 该仓 `README.md` 顶部必须有一行指针：`> 5 分钟了解本服务：SERVICE.md`。
- 卡片是"入口"，所以放根目录，不放 `docs/` 深层。
- 本仓（`tellurion-docs`）只放规范、模板与**未落地示例**；示例文件名统一 `service-card-example-<repo>.md`。

### 5.2 Frontmatter（机器层）

只允许下面这些键；没有的写 `null` 或空数组，不要自创字段。

```yaml
---
service-card: 1                 # schema 版本，整数
repo: tellurion-data            # 必须是本仓目录名
kind: service                   # service | application | library | frontend | docs
lifecycle: production           # production | skeleton | suspended | retired
owner: ruoxizhnya               # GitHub handle；单人项目即决策人
impact: degrading               # blocking | degrading | compile-time | none

requires:                       # 编译期依赖的仓（来自 go.mod，只写仓名）
  - tellurion-contracts
required-by: []                 # 编译期被哪些仓依赖（库仓必填；服务仓可空）
calls: []                       # 运行期出边（HTTP/其他协议，只写仓名）
called-by:                      # 运行期入边（只写仓名）
  - tellurion
  - tellurion-agent

truth:                          # 单一真相源；没有的写 null
  readme: README.md
  agents: AGENTS.md
  architecture: docs/ARCHITECTURE.md
  api: docs/api-schema.md
  db: docs/db-schema.md
  dataflow: docs/dataflow.md
  runbook: docs/runbook.md
  tasks: docs/TASKS.md

status: evergreen               # 本仓文档治理字段
last-verified: 2026-11-11
verified-by: 2026-11-11 代码-文档对齐审计；端口/端点未复制
---
```

字段说明：

| 字段 | 取值 | 写什么 / 不写什么 |
|---|---|---|
| `service-card` | 整数 | schema 版本；当前 `1` |
| `repo` | 仓目录名 | 与目录名、`go.mod` module 名对齐；不写 GitHub URL |
| `kind` | 五选一 | `service` = 六个能力服务；`application` = core / agent；`library` = contracts / kit；`frontend` = ui；`docs` = 文档仓 |
| `lifecycle` | 四选一 | `production` = 有真实实现、在今天的系统里；`skeleton` = 有边界无实现；`suspended` = 主体挂起；`retired` = 已退役但保留仓 |
| `owner` | GitHub handle | 只写决策人，不写"团队"；单人项目即仓库 owner |
| `impact` | 四选一 | `blocking` = 缺它主链路起不来/断；`degrading` = 局部功能降级；`compile-time` = 只影响编译；`none` = 文档或无运行时 |
| `requires` | 仓名数组 | 只写 `go.mod` 的直接依赖；不写版本、不写外部库 |
| `required-by` | 仓名数组 | 只写编译期消费方；用工作区 `go.mod` 扫描核对 |
| `calls` | 仓名数组 | 只写**运行期**出边；不写端口、URL、协议细节（正文写） |
| `called-by` | 仓名数组 | 只写**运行期**入边；不写调用方版本 |
| `truth.*` | 相对路径或 `null` | 指向本仓内的真相源；路径必须存在 |
| `status` / `last-verified` / `verified-by` | 本仓治理字段 | 与 `tellurion-docs` 的 R1 一致 |

> **`impact` 是判断，不是数字**。同一个仓在不同部署开关下可能从 `blocking` 变 `degrading`；卡片写"今天的默认部署"的粗判，正文 §6 写清开关与例外。开关本身不写进卡片（它属于 config）。
>
> **仓名 ≠ compose 服务名**：`calls` / `called-by` 只写仓目录名（如 `tellurion-data`），不写 compose 服务名（如 `data-service`）。正文如必须提到部署名，写成 `compose: data-service`，并与 compose 对齐；不要把它混进 frontmatter 的边。

### 5.3 正文：固定 7 段

正文总长 **≤ 120 行**，顺序固定，标题固定。每段写什么、不写什么：

| 段 | 标题 | 写什么 | 不写什么 |
|---|---|---|---|
| 0 | 标题 + 一句话 + 属性行 | 一句话职责（≤ 40 字）；`kind` / `lifecycle` / `impact` / `owner` 与 frontmatter 一致 | 技术栈、版本、状态长文 |
| 1 | 这是什么 | 2~3 句职责与系统位置；拥有哪块数据/契约（只写 schema / package 名） | 端点清单、表清单、模块图 |
| 2 | 它不做什么 | 3~5 条**被明确排除**的边界，来自 `api-schema §5` / `AGENTS §3` | 愿望、待办、未来计划 |
| 3 | 与谁相连 | 两张表：调用它（入边）、它调用（出边）；列 = 对方 / 协议 / 用来做什么 / 失败影响（入边写**本仓挂了会怎样**，出边写**对方挂了会怎样**） | URL、端口、版本、超时数字 |
| 4 | 运行时身份 | 常驻进程名；探针语义；部署真相指针（compose / Dockerfile / config）；"端口不在此卡" | 镜像 tag、副本数、启动命令全文、环境变量清单 |
| 5 | 数据与契约归属 | 拥有哪个 schema / 哪些契约包；不拥有什么；指向 db-schema / API.md | 表名清单、字段、导出符号数量 |
| 6 | 坏了怎么办 | 影响面；前 3 条排查（按顺序）；升级路径；runbook 指针 | 完整排障手册、告警规则、SLO |
| 7 | 5 分钟后去哪 | 一张"我想……读这个"的表，只放 5~7 行 | 复制其他文档的正文 |

### 5.4 稳定 / 易变的分界

这是本规范的核心。写卡片前先判断字段属于哪一类：

| 类别 | 例子 | 处理 |
|---|---|---|
| **稳定**（可写） | 职责、明确不做什么、owner、入边/出边、`impact` 粗判、`lifecycle`、真相源路径 | 写进卡片 |
| **半稳定**（写语义，不写值） | 探针的**含义**（存活不碰库 / 就绪要 DB）、拥有的 **schema 名**、契约 **package 名**、runbook 的**小节主题** | 可写，但必须配指针；值本身不写 |
| **易变**（不写） | 端口号、URL、DSN、镜像 tag、副本数、版本 pin、端点数量、表数量、导出符号数、配置默认值、当前任务状态、延迟/SLO 数字 | **一律不写**；只放"去哪看" |

**数字三不写**：端口、版本、数量。
**地址三不写**：URL、DSN、镜像 tag。
**状态三不写**：当前任务、当前进度、当前缺陷清单（去 `TASKS.md`）。

### 5.5 字段准入测试

任何想写进卡片的字段，先过五问；有一问答"是"，就不写或改成指针：

1. **服务边界不变时，它会不会变？** 会 → 不写（如端口、pin、端点数）。
2. **是否已有单一真相？** 有 → 只放指针（如 api-schema、db-schema、compose）。
3. **写错会让读者做错决定，还是只是多点一次？** 只是多点一次 → 指针。
4. **一次普通发版后，它是否仍然为真？** 否 → 不写。
5. **能不能被脚本从现有文件算出来？** 能 → 让脚本生成或校验，不手写（如 `requires`、`required-by`、端口）。

### 5.6 写作规则

- 一句话职责只写"替谁做什么"，不写"基于 Go/Gin/PostgreSQL"。
- 边界写**被排除的**，不写"我们也能做"。
- 边的"对方挂了会怎样"必须写**行为**：503、拒绝启动、降级、异步重试、无影响。
- 不写"目前""暂时""未来会"；今天态与目标态分开，目标态加粗 **目标**。
- 卡片过期时，**先删错的那一行**，不要为了显得完整保留一个三个月后必然过期的数字。

### 5.7 保留与砍掉的字段（一页账）

| 保留 | 为什么 | 砍掉 | 为什么 |
|---|---|---|---|
| 一句话职责 | 5 分钟入口的第一句；README 里有但常被埋 | 端口 / URL / DSN | 易变；config / compose 是真相 |
| 不做什么 | 比"能做什么"更能防止功能放错地方 | 版本 pin / 镜像 tag | 每次发版都变；go.mod / compose 是真相 |
| `kind` / `lifecycle` / `impact` | 机器可读的分类；影响面是排障第一判断 | 端点清单 / 数量 | api-schema 是真相；数量必过期 |
| `owner` | 坏了找谁；12 仓没有 CODEOWNERS | 表清单 / 数量 | db-schema 是真相 |
| 入边 / 出边 + 失败语义 | 单仓视角最缺的一屏；全局图不写行为 | 导出符号数量 | API.md / api-surface 是真相 |
| 探针语义 | 排障第一步；语义稳定，路径稳定 | 配置键全量 / 默认值 | config / compose 是真相 |
| 拥有的 schema / 契约 package | 边界判断；只写"哪块"，不写明细 | 副本数 / 资源限额 | 部署真相；且单人项目没有调度平台 |
| 前三条排查 + runbook 指针 | 让读者知道从哪开始，不替代 runbook | SLO / 延迟 / 告警规则 | 没有观测体系，写了就是空头承诺 |
| 真相源地图 | 把"读哪份"变成一张表 | 当前任务 / 进度 / 缺陷清单 | TASKS.md 是真相，且每周都变 |
| `last-verified` / `verified-by` | 让"可信"可判断 | 启动命令全文 | README / runbook 是真相 |
| — | — | 内部模块图 / 实现说明 | ARCHITECTURE 是真相 |
| — | — | 历史沿革 / 变更日志 | CHANGELOG / archive 是真相 |

> 一句话：**卡片只保留"边界与关系"，把所有"值"留给单一真相源。**

---

## 6. 机器校验契约

### 6.1 硬校验（默认，改到哪张卡就查哪张）

| 校验 | 规则 | 失败含义 |
|---|---|---|
| frontmatter 存在且可解析 | YAML + `service-card: 1` | 卡片不可被脚本读取 |
| 必填字段 | `repo` / `kind` / `lifecycle` / `owner` / `impact` / `truth` / `status` / `last-verified` / `verified-by` | 身份不完整 |
| 枚举合法 | `kind` / `lifecycle` / `impact` / `status` 在枚举内 | 分类漂移 |
| `repo` 对齐 | 等于卡片所在仓目录名，且等于 `go.mod` module 末段 | 复制粘贴串仓 |
| `truth` 路径存在 | 每个非 `null` 路径在本仓存在 | 指针断链 |
| 仓名合法 | `requires` / `required-by` / `calls` / `called-by` 的值 ∈ 12 仓名单，且不含自己 | 依赖图脏 |
| 不写裸端口/URL | 正文（代码块外）不出现 `:\d{4,5}`、`http://`、`postgres://` | 复制了易变信息 |

> 最后一条是**防腐烂 lint**，不是接口校验。它不判断端口对不对，只判断"你有没有把端口抄进来"。

### 6.2 软校验（工作区级，告警不阻断）

| 校验 | 规则 | 为什么软 |
|---|---|---|
| 边互认 | A 的 `calls` 含 B ⇒ B 的 `called-by` 含 A | 跨仓并发修改时可能暂时不一致 |
| compose 名对齐 | 正文如写 `compose: <name>`，该 name 必须存在于 compose | 部署名与仓名是两套命名 |
| `requires` 对齐 | 与工作区各仓 `go.mod` 扫描结果比对 | 单仓 CI checkout 不到别的仓 |
| `required-by` 对齐 | 库仓的消费方列表与工作区 `go.mod` 扫描一致 | 新增消费方是正常演进 |
| 卡片年龄 | `last-verified` 超过 180 天 | 提醒复核，不是错误 |
| 长度 | 正文 > 120 行 | 可读性提醒 |

### 6.3 明确不校验

- **端口号是否正确**：卡片不写端口，没有可校验的副本；端口真相在 config / compose。
- **端点清单/数量是否完整**：那是 `api-schema.md` 的职责。
- **表清单/数量是否正确**：那是 `db-schema.md` 的职责。
- **版本 pin / 镜像 tag 是否最新**：那是 `go.mod` / compose / `REPO-MAP.md` 的职责。
- **正文陈述是否真实**：机器只能查结构，真实性靠 `last-verified` 与人工复核。

### 6.4 CI 策略：不要做成第二道必红门禁

- 默认只在**改动到的卡片**上跑硬校验，退出码 0/1；
- 工作区级软校验只在本地或夜间跑，**不进单仓 CI**（CI 只 checkout 本仓，看不到另外 11 个仓）；
- 不做"全仓 12 张卡必须同时存在"的强制门禁，否则新建仓/迁移仓会被卡住；
- 建议实现为 `tools/check_service_cards.py`（Python 标准库，零依赖），但**本轮不落脚本**；先让 3 张试点卡证明模板可用，再决定是否值得写检查器。

---

## 7. 模板与示例

| 文件 | 用途 |
|---|---|
| [service-card-template.md](service-card-template.md) | 可直接复制的模板；每个字段带"写什么/不写什么"注释 |
| [service-card-example-data.md](service-card-example-data.md) | 业务服务示例：`tellurion-data`（有 DB、外部数据源、runbook） |
| [service-card-example-contracts.md](service-card-example-contracts.md) | 非服务仓示例：`tellurion-contracts`（纯库、无进程、编译期依赖） |

> 三个文件都是**规范资产**，不是 12 仓已落地的卡片。示例卡里的路径相对于目标仓，落到目标仓时才改成可点击链接；在本仓里用行内代码表示，避免链接检查器误判。

**为什么示例选 data + contracts，而不是 core + contracts**：data 是六个能力服务里最典型的"有 DB + 外部依赖 + runbook + fail-closed"的服务；contracts 是纯库。两者覆盖了模板的两端。core 是 `application` 变体（多进程入口、反代、进程内引擎），差异写在 §8.4，落地时按同一模板补齐即可。

---

## 8. 12 仓落地建议

### 8.1 顺序

| 阶段 | 仓 | 目的 |
|---|---|---|
| P0（本轮） | 本仓 | 规范 + 模板 + 两个示例；不改 12 仓 |
| P1 试点 | `tellurion-contracts`（库）、`tellurion-data`（服务）、`tellurion`（应用） | 三种 `kind` 各一张，验证模板没有漏字段 |
| P2 其余五服务 | `tellurion-strategy` / `risk` / `analytics` / `orchestration` / `broker` | 复用 data 样板；broker 补"Mock 可用、真钱挂起"的 lifecycle 表达 |
| P3 其余 | `tellurion-agent` / `tellurion-ui` / `tellurion-kit` / `tellurion-docs` | agent 走 application 变体；ui 走 frontend 变体；kit 走 library 变体；docs 走 docs 变体 |
| P4 收口 | 本仓 | 在 `SERVICE-INDEX.md` 加"服务卡"列；视试点结果决定是否写检查器 |

**P1 必须先做 contracts**：它的 `required-by` 是其他卡的边校验基准；先把库卡写对，后面服务卡的 `requires` 才有对照。

### 8.2 每仓需要谁提供什么

| 字段 | 谁提供 | 依据 |
|---|---|---|
| `kind` / `lifecycle` | 仓 owner | `REPO-MAP.md` 定位 + 该仓 `AGENTS.md` 状态段 |
| `owner` / `impact` | 仓 owner（人工判断） | 主链路影响；部署开关的默认值 |
| 一句话职责 / 不做什么 | 仓 owner 或本仓 agent | `README.md` 首段 + `AGENTS.md` §3 + `api-schema.md` §5 |
| 入边 / 出边 | 仓 owner + 调用方确认 | `config/` + compose 的 URL/服务名 + 调用方 `dataflow.md` |
| 探针语义 / 前三条排查 | 运维/值班（本项目 = owner） | `runbook.md`；没有 runbook 的仓先补最小节 |
| `requires` / `required-by` | 脚本生成，人工确认 | 各仓 `go.mod` |
| `truth` 路径 | 脚本生成 | 文件存在性 |
| `last-verified` / `verified-by` | 写卡人 | 实际核对记录 |

### 8.3 可脚本生成 vs 必须人写

**可生成（不要让 agent 手抄）**

- `repo`、`truth` 路径骨架、`status` / `last-verified` 模板；
- `requires`（`go.mod` 直接依赖）；
- `required-by`（工作区 `go.mod` 反向扫描）；
- 正文 7 段标题与"5 分钟后去哪"表格骨架；
- 边的**候选清单**（从 compose 环境变量、`config/*.yaml` 的 `url` / `resolve_url` 提取，人工确认后才写入）。

**必须人写**

- 一句话职责（要判断"替谁做什么"）；
- "它不做什么"（要判断边界，不能从代码自动推断）；
- `impact` 与失败影响（要判断主链路/降级）；
- 前三条排查（要判断排查顺序）；
- owner 与升级路径；
- 任何"对方挂了会怎样"的行为描述。

### 8.4 四种 `kind` 的写法差异

| `kind` | 特有字段/段落 | 可省略 |
|---|---|---|
| `service` | DB schema、外部依赖、runbook、fail-closed 语义 | 无 |
| `application` | 多进程入口（常驻/一次性/无监听）、反代关系、进程内能力 | DB schema 可简写（core 的表真相在 `SPEC.md`） |
| `library` | `required-by`、导出面真相（`docs/API.md` / `api-surface.txt`）、版本纪律 | 探针、端口、runbook |
| `frontend` | 消费的 HTTP 面、静态托管形态 | DB、runbook |
| `docs` | 知识库边界、导航入口 | 数据、运行时、依赖边 |

### 8.5 12 仓初判（2026-11-11 基线，落地时以实测为准）

| 仓 | `kind` | `lifecycle` | `impact` 初判 | 卡片重点 |
|---|---|---|---|---|
| `tellurion` | application | production | blocking | 前门 + 进程内引擎；调用 data / agent / broker / risk / strategy / orchestration |
| `tellurion-agent` | application | production | degrading | AI 四族反代目标；直连 data 取数/交易日历；LLM 外部依赖 |
| `tellurion-ui` | frontend | production | degrading | 只消费 core HTTP；不直连 DB |
| `tellurion-data` | service | production | degrading | 数据面唯一入口；market/ingest；外部数据源；runbook 齐全 |
| `tellurion-strategy` | service | production | degrading | 策略资产；非空 `strategy_ref` 时 core fail-closed 解析 |
| `tellurion-risk` | service | production | degrading（`resolve_enabled=true` 时等价 blocking） | 规则快照；默认 compose 关 resolve，开启后 core 启动期依赖；同步裁决仍在 core |
| `tellurion-analytics` | service | production | none（当前零调用方） | 独立只读分析；core 调用方为 0 是有意为之 |
| `tellurion-orchestration` | service | production | degrading | 只派活不裁决；core worker 调用 |
| `tellurion-broker` | service | production | blocking | 通道适配；Mock 可用、真实 XTP 挂起；core 装配期必填 |
| `tellurion-contracts` | library | production | compile-time | 跨仓形状；零实现/零 DB；版本纪律 |
| `tellurion-kit` | library | production | compile-time | 横切工具；零业务概念 |
| `tellurion-docs` | docs | production | none | 总体设计索引；不复制单仓真相 |

> 这张表是**落地起点**，不是新真相源。`impact` 尤其会随部署开关变化（例如 risk 的 `resolve_enabled`），落地时按该仓当时的默认配置重判，并在正文 §6 写清开关。

---

## 9. 维护与腐烂控制

1. **触发复核**（任一发生就改卡，不是等季度）：
   - 服务边界变化（新增/删除"不做什么"）；
   - 入边/出边变化；
   - owner / `impact` 变化；
   - runbook 新增或迁移；
   - `truth` 路径移动。
2. **不触发复核**：普通发版、依赖 pin 升级、端点增删、表结构增删、镜像 tag 变化——这些都不该让卡片 diff 出现；如果出现了，说明卡片写错了层。
3. **`last-verified` 是承诺**：没有它，卡片视为已腐烂，可读不可信（与 `tellurion-docs` R1 同规）。
4. **宁可删，不要留**：一条信息过期且不确定新值，删掉并留指针，比保留错误数字好。
5. **卡片不参与版本号**：它没有 semver；`service-card: 1` 只标识 schema 版本。

---

## 10. 落地状态（2026-11-11）

- 12 仓根目录的 `SERVICE.md` 已按本规范落地，各仓 `README.md` 顶部加了指针；每仓一个独立 commit（`docs(card): 新增 service card`）。
- core / agent / ui 三仓没有 runbook，其卡片 `truth.runbook` 写 `null`，「排查」段指向 `docs/TASKS.md` 的六字段缺口条；**没有虚构 runbook 指针**。
- 未裁归属在卡片里显式标注「待裁决」并指向 `ddd-boundary-review-2026-11-11.md` 的对应条目：`factor_returns` / `ic_analysis`（C3/D1）、core 与 analytics 指标权威口径（C4/D4）、`contracts/risk` 与 risk 自持 `Snapshot`（C5/D3）。
- `SERVICE-INDEX.md` 已加「服务卡」列。
- **没有写 `tools/check_service_cards.py`**：是否把 frontmatter / 边 / 路径做成门禁仍是**待定**，本轮不设门禁；现阶段只靠 `last-verified` 与本规范 §9 的触发复核。
