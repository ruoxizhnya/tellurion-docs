---
status: evergreen
last-verified: 2026-11-12
verified-by: DOC-PRODUCT-DRIFT-FIX（2026-11-12）：QT-32 状态对齐 core 台账（2026-11-10 收口）、删除「仅 data 接线」过期断言并改指 SYSTEM-DESIGN §4/§5、实盘说明死链改指 broker ADR-0003。此前：DOC-FRONTMATTER-HYGIENE（2026-11-12）：frontmatter 校时。此前：DOC-11（2026-10-26）：修正「当前阶段」与阶段表的自相矛盾（S0 已完成、S1 进行中），补工程解耦线与产品线的分工；产品阶段判据未改。此前：产品重构讨论（2026-09-16）
supersedes: archive/ROADMAP-history.md（Phase 1-4 / Sprint 1-8）
---

# ROADMAP — 阶段规划

> 任务明细见 [TASKS.md](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) · 定位见 [PRODUCT.md](PRODUCT.md) · 架构见 [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 当前阶段

**产品主线：S1 通回路（进行中）。S0 已于 2026-09-17 完成。**

S0 的出口判据（回测数字可信）已达成，所以当前不是 S0。S1 的出口是「无人干预连续跑完 100 次实验」——**今天尚未达成**：core `docs/TASKS.md` 的 QT-32（AI 策略生成闭环）已于 2026-11-10 收口 ✅、agent 侧 `QT-32-A` 亦已完成，但 core/agent 台账均无「连续 100 次无人干预」的整链验收记录 ⇒ S1 以整链连续运行为出口，不以单点完成为证。

**另有一条工程解耦线在并行推进**（不属于本表的 S0~S4 产品阶段）：S-1 改名建仓 / S0 自治 / W0 契约冻结 / S1 契约落码 / S2 打 tag / S3 agent 去 replace 均已收口；X1~X6 六服务仓已实装，接线现状（data 取数、strategy resolve、risk resolve、broker HTTP、orchestration 队列；analytics 有意为 0）以 [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md) §4/§5 与各仓台账为准。工程线的状态以 core `docs/TASKS.md` 与第四轮审计（`tellurion:docs/design/qt-decoupling/purpose-alignment-audit-2026-10-26.md`）为准，**不要用工程线的「已落仓」替代本表的 S1 出口**。

---

## 排序原则

不是按"重要性"排，是按**依赖**排：

- 数字不可信 → 建什么都白建（S0 先行）
- 回路不通 → 数据无处可用（S1 先于 S2/S3）
- 没有可监控的策略 → 监控系统没有意义（S4 最后）

---

## 阶段总览

| 阶段 | 名称 | 目标 | 出口判据（可验证） | 状态 |
|---|---|---|---|---|
| **S0** | 止血 | 让现有回测数字可信 | P0-1~P0-6 全部通过；CI 红绿可见；新测试能被 git 跟踪 | ✅ 完成（2026-09-17） |
| **S1** | 通回路 | AI 能跑完一次完整实验循环 | 一条意图 → 配置 → 注册 → 回测 → 出结果，端到端可复现 | ⏳ 进行中 |
| **S2** | 加解释 | 让因子带因果来源 | 产业链数据底座可用；每个因子有 `hypothesis_source` | ⬜ 待开始 |
| **S3** | 加宽度 | 拓宽策略空间 | 宏观/跨境数据源接入；新增策略与已有策略相关性 < 0.5 | ⬜ 待开始 |
| **S4** | 加监控 | 让失效能被发现 | 策略健康度周报可用；regime + drift 接入主流程 | ⬜ 待开始 |

---

## S0 · 止血 ✅（2026-09-17 完成）

修前视偏差（财务读取改按 `COALESCE(ann_date, trade_date)`）· 建 CI · 放开 `*_test.go` · 鉴权收口（无密钥拒绝启动）· 打通实验链路。

最后一项的实际根因比登记时深两层，修法也因此定型为「执行载体 = 表达式」而非
「补一个 `plugin.Open`」，决策见 [ADR-024](adr/adr-024-expression-as-execution-target.md)。

**出口判据达成**：
- 能证明"9/30 查 Q3 财报返回空" —— `pkg/storage/fundamentals_pit_test.go`
- 任意 PR 有红绿 —— `.github/workflows/ci.yml`（build / vet / test / 文档链接）
- 新建一个 `_test.go` 能被正常 `git add` —— `.gitignore` 规则已移除
- P0-1 ~ P0-6 全部通过

---

## S1 · 通回路

`experiments` 表（能回放路径）· 循环控制器（先用现成的 TPE/遗传算法当"假实验员"，不等 LLM）· 三栏观察页（正在试什么 / 结果流 / 当前最优 + 干预入口）。

**出口**：无人干预连续跑完 100 次实验，并产出一份可审阅的摘要（含路径缩略图）。

> 这一阶段**不需要 LLM**。先把回路跑通，决策器后面换。

---

## S2 · 加解释

schema 收口（migrations 可执行 + 版本管理）· 产业链数据底座最小版 `query_supply_chain()` · 因子增加 `hypothesis_source` 字段 · 红队验证器链落地。

**出口**：至少 1 个"从产业链假设出发"的因子完成完整验证并带因果来源。

---

## S3 · 加宽度

宏观/跨境数据源（美股、汇率、利率、大宗）· 技术面策略 + **策略相关性检查**（防"以为分散了其实是同一个赌注"）· 幸存者偏差处理。

**出口**：新增策略与已有策略滚动相关性 < 0.5；回测 universe 含退市标的。

---

## S4 · 加监控

市场状态识别 + 策略漂移检测接入主流程（两者代码已存在但零调用）· 策略健康度周报。

**出口**：能回答"我的每个策略最近 3 个月是否偏离其历史基准"、"是否已连续失效超过历史最长失效期"。

---

## 明确不做

与 [VISION.md](VISION.md) 边界一致，此处只列容易被临时加回来的：

- **实盘交易** — 真钱通道未开（XTP 仍为桩，挂起与重开条件见 [broker ADR-0003](https://github.com/ruoxizhnya/tellurion-broker/blob/main/docs/adr/0003-真钱通道暂不实施与重开条件.md)）；core 进程内 `MockTrader` 已随 `SVC-CORE-BROKER-RETIRE` 退役，唯一通道是 `tellurion-broker` 的 Mock 网关
- **多 agent 投票 / arbitrator 仲裁** — 错误相关，放大偏差，不可解释
- **实时行情 / 盘中监控** — 日频已是高频边界
- **EquityDeep 作为独立智能流程** — 它是数据底座，不是 agent
- **SaaS / 多租户** — 单人自托管

---

## 历史

Phase 1–4 与 Sprint 1–8 的旧规划见 [archive/ROADMAP-history.md](archive/ROADMAP-history.md)（只读）。
