# AGENTS.md — tellurion-docs

> **本仓是总体设计知识库，不是代码仓。** 任何 agent 进来先读这三行：
> 1. 这里只放**跨仓的**设计与决策；单仓细节在各自仓，**不复制**。
> 2. 跨仓引用必须写**完整 GitHub URL**，相对路径在独立 checkout 时必断。
> 3. 改任何文档后跑 `python tools/check_doc_links.py`，活跃层必须 0 断链。

---

## 1. 构建 / 检查

本仓无代码，可执行物是两个巡检脚本：

```bash
python tools/check_doc_links.py          # 活跃层 0 断链才通过（退出码 0/1，CI 同款）
python tools/check_doc_links.py --all    # 连历史层明细一起看

python tools/check_repo_docs.py          # 12 仓文档齐套（默认 workspace = 本仓父目录）
python tools/check_repo_docs.py --explain   # 另打印每仓的豁免理由
python tools/test_check_repo_docs.py     # 巡检脚本自身的夹具测试（17 条）
```

- Python 3.9+，仅标准库，无依赖、无虚拟环境。
- 没有 `make` 目标：一条命令就是全部。
- `check_repo_docs.py` **不进 CI**：CI 只 checkout 本仓，看不到另外 11 个仓；它是工作区级的本地巡检（`--workspace` 指向 12 仓同级目录）。

## 2. 目录职责（写东西前先确认落在哪）

| 路径 | 放什么 | 不放什么 |
|---|---|---|
| `README.md` | 知识库入口：三种读法 + 12 仓地图 + 单一真相源表 | 具体设计内容 |
| `docs/SYSTEM-DESIGN.md` | **现行总体设计**：分层 / 四条主链路 / 数据归属 / 边界原则 / 演进阶梯 | 单仓的表与端点 |
| `docs/REPO-MAP.md` | 12 仓：管什么 / 不管什么 / 拥有 schema / 依赖 | 实现细节 |
| `docs/SERVICE-INDEX.md` | 各仓 db / api / dataflow 的**索引** | 复制过来的契约正文 |
| `docs/ARCHITECTURE.md` | ⚠️ 拆仓前历史 Reference（不再更新） | 新的现状描述 |
| `docs/adr/` | 跨领域架构决策（编号 `adr-NNN`） | 单仓决策（放该仓 `docs/adr/`） |
| `docs/design/` | 跨领域功能规格（如 EquityDeep） | 服务实现设计 |
| `docs/guides/` | 本地起步 / 部署 / 数据依赖 / 运维 | 一次性排查记录（进 `archive/`） |
| `docs/archive/` | 历史档案（只读） | 任何"以后要看"的活文档 |

## 3. 写作规则（硬约束）

1. **不复制，只索引**：服务仓的 `db-schema` / `api-schema` / `dataflow` 内容不搬进来；要引用就写一句话边界 + 绝对 URL。
   > 理由：复制的那一份一定会漂移，而漂移的契约比没有契约更危险。
2. **跨仓引用 = 完整 URL**：`https://github.com/ruoxizhnya/<repo>/blob/main/<path>`。
   **禁** `../../tellurion/...`：本机能解析（兄弟仓在旁边），GitHub 上 404。
3. **frontmatter 必填**：`status`（`evergreen` / `active` / `archived`）+ `last-verified` + `verified-by`。没有 `last-verified` 的文档视为已腐烂：可读、不可信。
4. **状态必须写明"今天 vs 目标"**：本仓吃过一次亏——`ARCHITECTURE.md` 曾以现状口吻写目标态，拆仓后整篇失效。凡写未来态，加粗标 **目标**。
5. **ADR 只增不删**：被取代的 ADR 移入 `docs/archive/superseded-adr/`，在原编号处留一行指针；不要原地改写已 Accepted 的决策。
6. **ADR 与 ODR 分工**：判断标准是"这条决定会不会让某段代码搬到别处" —— 会 → ADR；不会（流程 / 工具 / 习惯）→ ODR（`docs/odr/` 见各仓；本仓历史 ODR 在 `docs/archive/odr/`）。

## 4. 边界与禁止

- **禁止**把服务仓的契约正文复制进本仓（哪怕是"临时参考"）。
- **禁止**在本仓写"某服务当前的表结构"——那不是本仓的真相源，指向该仓 `db-schema.md`。
- **禁止**新增跨仓相对链接（见 §3.2）。
- **禁止**为了让检查器通过而给 `docs/adr/`、`docs/archive/` 加豁免——豁免是给历史档案的，不是给新写的内容。
- **禁止**在本仓放活跃施工台账：施工单在 core 的 `docs/TASKS.md`，本仓 `docs/TASKS.md` 只放"知识库维护"类任务。

## 5. 依赖的契约与外部真相源

| 依赖 | 版本/位置 | 说明 |
|---|---|---|
| 仓名与 module path | [core `repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md) | 唯一名字源 |
| 拓扑 / R1~R6 / C1~C5 / S0~S3 | [core `repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md) | 唯一拓扑源 |
| 施工顺序 | [core `docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) | 唯一台账 |
| 各仓表 / 接口 / 链路 | 各仓 `docs/{db-schema,api-schema,dataflow}.md`（core 与本仓豁免，真相直接承载，见 REPO-MAP） | 本仓只索引 |

## 6. 台账入口

本仓的活只在 [docs/TASKS.md](docs/TASKS.md)：目前只有"知识库维护"类事项（导航、坏链、过时声明）。
跨仓的施工任务一律去 core 的台账，**不要在本仓建单**（会造成两份真相）。
