# Archive — 归档层

> **归档 ≠ 现状。** 本目录所有内容都是历史快照：其中的端口、表数、覆盖率、条数与路径都可能已经失效。引用前必须回到活跃层（[README](../README.md) / [SYSTEM-DESIGN](../SYSTEM-DESIGN.md) / [REPO-MAP](../REPO-MAP.md) / [ADR](../ADR.md)）复核。
>
> 本目录整体语义为 `status: archived`。个别文件正文里残留的「Status: Active / Canonical」是**归档前原文**，不代表现状。
>
> ⚠️ **历史档案的链接不修（2026-10-21 DOC-05 裁决）**：本目录内的相对/绝对链接可能指向已删除或已搬走的源码与文档，属历史快照的一部分，**保持原样、不逐条修改**；CI 对历史层只统计断链数、不判红。

## 归档清单

> 清单是归档层的可信索引：**每个文件必须被下表某一行的条目覆盖**，反之每行也必须至少命中一个文件。校验：`python tools/check_archive_index.py`（CI 同款）。

<!-- archive:begin -->
| 条目 | 内容 | 归档原因 |
|---|---|---|
| `ARCHITECTURE-pre-split.md` | 拆仓前总体架构（端口 / 表数 / 包归属） | 2026-10-09 拆仓后被 SYSTEM-DESIGN 取代（2026-11-13 DOC-20 移入） |
| `IMPLEMENTATION_PLAN.md` | 2026-05-04 全面实施计划 v2.0（Proposed） | 可执行任务已迁入 TASKS.md |
| `NEXT_STEPS.md` | 2026-05-03 审查发现归档 v3.0 | 可执行任务已迁入 TASKS.md |
| `REORG-PLAN.md` | 2026-09-16 目录重组计划 | 重组已完成，仅留过程记录 |
| `RESEARCH-equitydeep-legacy.md` | EquityDeep 工作面 1（纵向深研）详案 v0.2 | 2026-11 产品定位变更（ADR-039 后 analytics 只读参考） |
| `ROADMAP-history.md` | 2026-05-03 旧路线图 v1.2 | 被 ROADMAP.md 取代 |
| `TASKS-2026-10-08-archived.md` | 2026-10-08 任务台账快照 | 被后续台账取代 |
| `tasks-archive-2026-11.md` | 2026-11-11 归档的已收口任务原文（含检索索引） | 当前台账的历史归档，进 git 不删除 |
| `TASKS-history.md` | Sprint 1–8 旧任务文档 v3.41 | 被新台账取代 |
| `tasks-phase-2.md` | Phase 4 任务追踪 v1.3 | 已完成 / 前端部分按 ODR-045 废弃 |
| `VISION-full.md` | 旧愿景全文 v2.0（ADR-022 口径） | 精简为 VISION.md |
| `odr/` | ODR 001–073：实施与取证记录 | 与 git log 重复，2026-08-31 起归档 |
| `plans-2026-Q3/` | 3 份 S7 P3 计划与索引（5–7 号） | 计划已执行完毕 |
| `reports-2026-Q2/` | 4 份 2026-Q2 清理 / 审计 / 迁移 / 终验报告 | 一次性运维记录 |
| `reports-2026-Q3/` | 2 份 2026-09-21 审查与元审查报告 | 一次性评审记录 |
| `research-2026-Q2/` | 6 份 2026-Q2 调研与阶段评审 | 结论已并入活跃文档 |
| `superseded-adr/` | ADR 009/010/012/021/022 全文 | 已被新 ADR 取代（状态见 [ADR.md](../ADR.md) 索引表） |
<!-- archive:end -->

## 怎么找归档内容

1. 先看 [ADR.md](../ADR.md) 索引表与 `adr/` —— 被取代的决策在那里有终态与替代关系；
2. 需要原始执行细节再进本目录；
3. `git log --follow -- docs/archive/<文件>` 可看归档时点与来源。

## 归档策略

- 活跃引用价值低于日常使用阈值时归档，**永不删除**；
- 归档文件可能含过期信息，**必须**与现状交叉核对；
- 归档层的相对链接不修（见顶部裁决），只保证**清单覆盖**与 `status` 语义；
- 季度复核：归档超 12 个月的文件可评估清理，需维护人批准。

---
_Last updated: 2026-11-13（DOC-22 重建清单；此前 2026-04-11）_
