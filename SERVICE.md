---
service-card: 1
repo: tellurion-docs
kind: docs
lifecycle: production
owner: ruoxizhnya
impact: none

requires: []
required-by: []
calls: []
called-by: []

truth:
  readme: README.md
  agents: AGENTS.md
  architecture: docs/SYSTEM-DESIGN.md
  api: null
  db: null
  dataflow: null
  runbook: null
  tasks: docs/TASKS.md

status: evergreen
last-verified: 2026-11-11
verified-by: 2026-11-11 实读 README / AGENTS / docs/README / SYSTEM-DESIGN / REPO-MAP / SERVICE-INDEX / tools，并跑三份巡检脚本；不复制单仓表与端点
---

# 服务卡：tellurion-docs

> **一句话**：跨仓设计知识库——总体设计、12 仓地图、服务索引、跨领域 ADR 与起步指南；只索引不复制。
>
> `docs` · `production` · `none` · `ruoxizhnya`

## 1. 这是什么

它是 12 仓共同的「为什么这样分、边界在哪」的真相源：现行总体设计、12 仓职责与依赖地图、服务索引、跨领域架构决策（ADR）、部署与本地起步指南、跨仓功能规格。它**不**承载任何单仓的表结构、接口正文或施工台账。

**它拥有**：跨领域 ADR 编号与正文（`docs/adr/`）、12 仓地图（`docs/REPO-MAP.md`）、服务索引（`docs/SERVICE-INDEX.md`）、总体设计（`docs/SYSTEM-DESIGN.md`）、起步与运维指南（`docs/guides/`）、跨仓设计规格（`docs/design/`）。
**它不拥有**：单仓 `db-schema` / `api-schema` / `dataflow` 的正文、任何施工台账、任何代码或运行时。

## 2. 它不做什么

- 不复制单仓契约正文：只写一句话边界 + 指向该仓 `main` 分支的完整 URL。
- 不写「某服务当前的表结构」：那不是本仓的真相源，指向该仓 `db-schema.md`。
- 不放活跃施工台账：施工单在 core `docs/TASKS.md`，本仓台账只装「知识库维护」类事项。
- 不改写已 Accepted 的 ADR：被取代的移入 `docs/archive/superseded-adr/`，原编号处只留指针。
- 不新增跨仓相对链接：本机能解析、GitHub 上必 404。

## 3. 与谁相连

**运行期没有边**：本仓不被任何进程加载，也不调用任何服务。

### 调用它（入边）

| 来源 | 协议 | 用来做什么 | 本仓挂了会怎样 |
|---|---|---|---|
| 12 仓的维护者 / 读者 | git / GitHub | 查边界、查 ADR、查部署与起步步骤 | 不影响任何运行时；设计与决策的单一入口消失 |
| 各仓 `AGENTS.md` / `README.md` | 链接 | 跨仓引用回指本仓的 ADR、REPO-MAP 与指南 | 断链；单仓文档仍可独立阅读 |

### 它调用（出边）

| 目标 | 协议 | 用来做什么 | 目标挂了会怎样 |
|---|---|---|---|
| 无（只有阅读链接，不是运行期调用） | — | — | — |

> 本仓对 11 个仓的引用一律是 `https://github.com/ruoxizhnya/<repo>/blob/main/<path>` 形式的阅读链接，不参与构建。

## 4. 运行时身份

- **常驻进程**：无；本仓是知识库，不是服务。
- **可执行物**：三份巡检脚本——`tools/check_doc_links.py`（活跃层断链）、`tools/check_guide_refs.py`（guides 的 `repo:path` 仓名与可选路径）、`tools/check_repo_docs.py`（12 仓文档齐套）。
- **存活/就绪语义**：无端口、无探针；「健康」= 三份巡检退出码 0。
- **端口**：不适用。

## 5. 数据与契约归属

| 维度 | 归属 | 真相源 |
|---|---|---|
| DB schema | 无表、不连库 | — |
| 跨仓 DTO / 契约 | 只索引；形状归各仓 `docs/api-schema.md`，跨仓形状归 `tellurion-contracts` | `docs/SERVICE-INDEX.md` |
| 对外 HTTP | 无 | — |

> 本仓拥有的是**跨仓边界与决策**，不是任何字段级契约；`SERVICE-INDEX.md` 只放链接。

## 6. 坏了怎么办

- **影响面**：`none`——没有任何运行时依赖本仓；坏的是「人查文档」这条路径，不是系统。
- **先确认（按顺序）**：
  1. 跑 `python tools/check_doc_links.py`，看活跃层断链清单。
  2. 跑 `python tools/check_guide_refs.py`；仓名腿进 CI，路径腿需 `--workspace ..`。
  3. 跑 `python tools/check_repo_docs.py`，看 12 仓文档齐套与豁免理由。
- **升级路径**：`owner` → 跨仓争议 → core `docs/TASKS.md`
- **runbook**：无（知识库不需要起停手册）；维护流程见 `AGENTS.md` §1~§3。

## 7. 5 分钟后去哪

| 我想…… | 读这个 |
|---|---|
| 知道总体分层、四条主链路与数据归属 | `docs/SYSTEM-DESIGN.md` |
| 知道 12 仓各管什么、依赖谁 | `docs/REPO-MAP.md` |
| 知道某仓的表 / 接口 / 链路在哪 | `docs/SERVICE-INDEX.md` |
| 知道某个跨仓决策为什么这么定 | `docs/adr/`、`docs/ADR.md` |
| 部署 / 本地起步 / 数据依赖 | `docs/guides/` |
| 本仓怎么维护、检查器怎么跑 | `AGENTS.md` |
| 当前在做什么 | `docs/TASKS.md` |
