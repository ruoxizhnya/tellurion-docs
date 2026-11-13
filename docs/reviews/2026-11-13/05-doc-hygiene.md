---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 自上而下五角审查 · 角度 5（文档架构与卫生）；只读静态审查，未运行构建/测试，未修改任何既有文档
---

# 角度 5 · 文档架构与卫生 — 6.2 / 10

> 审查对象：`tellurion-docs`（12 仓文档枢纽）及其对 11 个仓文档入口的导航承诺。
> 审查方式：**只读**。读取导航与索引文件、目录清单、frontmatter 扫描；未执行任何构建、测试或写操作。
> 证据路径均相对 `tellurion-docs/docs/`。

## 一、结论摘要

这套文档体系**治理设计是同类项目里少见的完整**：单一入口、三层结构（现有 / 设计 / 归档）、R1–R5 治理规则、
ADR/ODR 双台账、逐仓服务卡与三份契约索引都真实存在且在维护。问题不在"没有制度"，而在
**制度执行到导航层就开始失真**：入口页仍在描述已删除的文件、已落地的功能"未落地"、已增长的台账
"31 条"，而归档层几乎没有可信索引。

一句话：**骨架好、口径旧；规则写得比执行得严。**

## 二、评分表

| 维度 | 权重 | 得分 | 依据 |
|---|---|---|---|
| 结构与可导航性 | 25% | 7.5 | 单一入口 + 三层导航 + SERVICE-INDEX 逐仓直达，结构清晰；但入口页 5 处目标已失效、2 份 guide 成为导航孤儿 |
| 过期 / 重复 / 自相矛盾 | 30% | 5.5 | 常青文档引用已删除的 `docker-compose.services.yml`；README 与 ADR 台账数字冲突；"唯一处"去重承诺已漂移 |
| 归档卫生 | 15% | 5.0 | `archive/README.md` 索引停在 2026-04-11，只覆盖 2/6 子目录；归档文件 status 语义违规 |
| 台账口径可信度 | 15% | 6.5 | 活跃层 frontmatter 覆盖完整、TASKS 已瘦身；但 ADR 台账自认"两套真相来源"，4 条 ADR 长期未裁决 |
| 治理机制可执行性 | 15% | 6.5 | R1–R5 设计完整；但 R5（文档可验证 CI）自述缺失且台账无对应开放项，R2 被自身导航违反 |

加权：`7.5×0.25 + 5.5×0.30 + 5.0×0.15 + 6.5×0.15 + 6.5×0.15 = 6.225` → **6.2 / 10**

## 三、做得好的部分（查证得到）

1. **单一入口与三层结构成立**：[README.md](../../README.md#L7-L27) 明确"文档的唯一入口"，总体层只放
   SYSTEM-DESIGN / REPO-MAP / SERVICE-INDEX 三份索引，并声明"本页不复制其他文档的内容"。
2. **服务卡已全部落地**：`Glob */SERVICE.md` 实测 12 个仓根目录均有 `SERVICE.md`（含 core / docs），
   与 [SERVICE-INDEX.md](../../SERVICE-INDEX.md#L12) 的"12 仓根目录各有一份"一致。
3. **活跃层 frontmatter 覆盖率高**：根目录 12 份 .md 与 `guides/` 8 份、`design/` 5 份全部带
   `status` / `last-verified`（grep `^status:` 逐文件命中）。
4. **ADR/ODR 双台账真实存在且有状态列**：[ADR.md](../../ADR.md#L18-L60) 收录 ADR-001~041（41 条），
   `archive/odr/` 实测 73 份（ODR-001~073），归档 ADR 5 份（009/010/012/021/022）确实在
   `archive/superseded-adr/`，编号缺口有解释。
5. **TASKS 台账"只装未做的事"已执行**：[TASKS.md](../../TASKS.md#L9-L13) 明确瘦身规则，
   [TASKS.md:37](../../TASKS.md#L37) 只剩 1 条挂起项（DOC-14），口径干净。

## 四、扣分点（按严重度）

### H1（P1）入口页 5 处指向"不存在 / 已变化"的对象

单页即入口，因此单页失真会放大到所有读者。逐条实测：

| # | 位置 | 文档声明 | 实测事实 |
|---|---|---|---|
| 1 | [README.md:101](../../README.md#L101) | `archive/2026-Q2/*` | 该目录不存在；实际为 `archive/reports-2026-Q2/` 与 `archive/research-2026-Q2/`（Glob 实证） |
| 2 | [README.md:86](../../README.md#L86) | 文档链接 CI"当前缺失，见 TASKS.md P0" | TASKS.md 已无任何 P0 项，全文仅 DOC-14 一条 ⏸（[TASKS.md:37](../../TASKS.md#L37)）→ 指向的是已不存在的任务 |
| 3 | [README.md:50](../../README.md#L50) | 服务卡"12 仓未落地" | 12 个 `SERVICE.md` 全部存在（Glob 实证），SERVICE-INDEX 也写"各有一份" |
| 4 | [README.md:45](../../README.md#L45) | ADR"31 条；编号至 ADR-036" | ADR.md 索引到 ADR-041，尾注自述"累计 41 条"（[ADR.md:195](../../ADR.md#L195)） |
| 5 | [README.md:97](../../README.md#L97) | 归档 ODR"001–064" | `archive/odr/` 实测 73 份（至 ODR-073）；同行的 superseded 列表漏了 ADR-022（该文件在 `archive/superseded-adr/` 实测存在，ADR.md:41 也链到它） |

扣分理由：入口页是"唯一入口"制度的核心，上述 5 处说明入口页自 2026-11-11 后未随 ADR/ODR/服务卡
的增量同步，R1 的 `last-verified` 字段虽在，但没有覆盖真实变更面。

### H2（P1）常青文档引用已删除的部署资产

[SYSTEM-DESIGN.md:133](../../SYSTEM-DESIGN.md#L133)："本地联调走 `docker-compose.services.yml`"。

实测：core 仓 `docker-compose*.yml` 只剩 `docker-compose.yml` 一份（Glob 实证）；core
[ARCHITECTURE.md](https://github.com/ruoxizhnya/tellurion/blob/main/docs/ARCHITECTURE.md) 的 frontmatter 明确记录 2026-11-11 已删除
`docker-compose.services.yml` / `.e2e.yml` / `.nt.yaml` 三份文件。而 SYSTEM-DESIGN 的 frontmatter 是
`last-verified: 2026-11-12` —— **校时晚于删除，内容仍是旧口径**，说明"打时间戳"没有触发实质复核。

性质：**实测**（文件不存在 + 文档原文）。

### H3（P1）R2 规则被入口页自己违反：归档文档仍在导航表

[README.md:68-L72](../../README.md#L66-L72) 规定 `archived` = "只读、不改、**不进本页导航**"；
[README.md:108](../../README.md#L108) 再次强调"文档进入 archived 状态时，必须从导航表移除"。

但 [docs/ARCHITECTURE.md](../../ARCHITECTURE.md) 的 frontmatter 是 `status: archived`，
却被 [README.md:37](../../README.md#L37) 放进"我该读哪一份"主表，
并在 [README.md:56](../../README.md#L56) 再次作为推荐顺序提及。该文件自述
"端口/表数已失效"、体积 65.9KB（目录实测），是当前导航层里最大的一份失效文档。

这不是"保留历史"的问题——历史在 `archive/` 里；问题是**活跃导航仍然把它当推荐读物**。

### H4（P2）"唯一处"去重承诺已漂移（同一事实两处写）

[REPO-MAP.md:46](../../REPO-MAP.md#L46) 明确："本节是这条规则的**唯一处**；
`SYSTEM-DESIGN.md` §2 只放指针，避免两处漂移。"

实测两处仍在复制版本数字：SYSTEM-DESIGN
[:124](../../SYSTEM-DESIGN.md#L124)（contracts `v0.10.0` / kit `v0.3.0`）与
[:134](../../SYSTEM-DESIGN.md#L134)（kit 逐仓 pin 清单）。角度 4 已证两份文档的
pin 数字都已与 `go.mod` 实测不符（REPO-MAP 写 kit `v0.3.0`/`v0.2.0` 与实际 `v0.5.0` 冲突），说明"两处写"直接导致了"两处错"。

同类问题在 ADR 台账被自认：[ADR.md:4](../../ADR.md#L4) 的 verified-by 原文
"索引表与本尾注两处同步，**两处是两套真相来源**"。制度层面承认了重复，但没有收敛动作。

### H5（P2）归档层没有可信索引，且 status 语义违规

1. `archive/README.md` 的目录树停在 2026-04-11（[archive/README.md:41](../../archive/README.md#L41)），
   只列 `reports-2026-Q2` / `research-2026-Q2` 两个子目录；实测归档有 6 个子目录 + 11 个顶层文件，
   其中 `odr/`、`superseded-adr/`、`plans-2026-Q3/`、`reports-2026-Q3/`、`tasks-archive-2026-11.md`、
   `TASKS-history.md`、`VISION-full.md` 等全部未登记。
2. 同一文件 [archive/README.md:29](../../archive/README.md#L29) 指向 `docs/odr/`，
   该目录已不存在（ODR 实际在 `archive/odr/`）。
3. 用 `^status:` 扫描归档顶层 11 份 .md：仅 2 份带 frontmatter，且都写 `status: active`
   （[TASKS-2026-10-08-archived.md:2](../../archive/TASKS-2026-10-08-archived.md#L2)、
   [REORG-PLAN.md:2](../../archive/REORG-PLAN.md#L2)）——与 R2
   "归档 = `archived`、只读"相反，也与文件名里的 `archived` 相反。

`README.md:92` 声明"归档层只读、不维护、不进导航"，这条豁免可以解释"不修链接"，
但不能解释"归档层自己的索引只覆盖 12%"：归档层的可用性恰恰取决于索引。

### H6（P3）决策台账有序性与时效性

- [ADR.md:191](../../ADR.md#L191) 的 `_Last updated by ... 2026-10-14_` 夹在
  2026-10-26 与 2026-11-11 的条目之间；其下 [ADR.md:197](../../ADR.md#L197) 又是 2026-10-13。
  变更日志非单调排序，"最后更新"行长期未改。
- ADR-027/028/029 自 2026-10-06 起维持 `Proposed`、ADR-030 维持 `Draft`
  （[ADR.md:46-L49](../../ADR.md#L46-L49)）。其中 ADR-027 的主题是
  "模块化拆解为独立服务（服务数 5→7）"，而 2026-10-26 的 ADR-036 已给出并落地了不同的 12 仓拓扑
  （[ADR.md:190](../../ADR.md#L190) 明写"修订 ADR-027 §2.1"），
  ADR-027 却仍未标 `Superseded`，读者会读到两条并存的"服务拓扑"结论。

### H7（P3）阶段台账与实现状态不同步

[ROADMAP.md:40](../../ROADMAP.md#L40) 把 S2 标为"⬜ 待开始"，其出口判据第一条是
"产业链数据底座可用"；但 core 已实现并装配 `/api/industry/*`（SW 行业树 / 供应链边 / 行业活力 / ETF 成分）
与 `/api/macro/series`，core `openapi.yaml` 的 tag 描述明确写 "Industry ... (P2-2)"、"Macro ... (P2-1)"。
即使 S2 的另一半（`hypothesis_source`）未完成，台账也应写成"部分达成"，而不是"待开始"。

## 五、实测 / 推断 区分

| 类型 | 内容 |
|---|---|
| **实测（命令或文件原文）** | 12 份 `SERVICE.md` 存在；`docker-compose*.yml` 只剩 1 份；`archive/2026-Q2` 不存在；`archive/odr/` 73 份；归档顶层 11 份 .md 中 2 份带 `status:` 且均为 `active`；README 与 ADR.md 的计数原文冲突；SYSTEM-DESIGN:133 原文；ARCHITECTURE frontmatter `status: archived` 且被导航引用 |
| **推断（未运行验证）** | "入口页未随增量同步"是行为解释，不是日志证据；ADR 台账条目是否有人按顺序消费无法验证；`archive/README.md` 是否仍被读者使用无访问数据 |
| **未做（超出只读边界）** | 未运行链接检查脚本、未跑文档 CI、未统计全库断链数量、未修改任何文档 |

## 六、修复建议（仅建议，本次未执行）

1. 入口页五项一次性校准（H1），并把"服务卡落地 / ADR 条数 / ODR 范围"改为由脚本生成的数字，而不是手写。
2. SYSTEM-DESIGN §5 的部署句改为指向 core `docker-compose.yml` + profile，删除 `.services.yml`（H2）。
3. ARCHITECTURE 从导航表移除，保留一条"历史参考见 archive/…"或在 README 内降级为脚注（H3）。
4. 把 REPO-MAP 的 pin 段做成唯一数字源，SYSTEM-DESIGN 只留链接；ADR 台账尾注改为"索引表为唯一状态源"（H4）。
5. 重写 `archive/README.md` 为脚本生成的目录清单（子目录 + 顶层文件 + 日期 + 一句话），并把归档文件统一改 `status: archived`（H5）。
6. ADR-027 标 `Superseded by ADR-036`；变更日志按日期倒序整理（H6）。
7. ROADMAP S2 改"部分达成：产业链底座 ✅ / hypothesis_source ⬜"（H7）。
