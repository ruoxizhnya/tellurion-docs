# ODR-068: 第五轮全系统审查 · 产品与治理（W1）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-023（三角色实验室）/ adr-024（表达式执行载体）/ adr-041（AI 因子工具面不新造端点）/ adr-037（factor_cache 归属）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md) 全栈静态审查与第四轮目的对齐审计 2026-10-26 之后的第五轮；本轮为 12 仓拆仓后的全维度复检）

---

## Context

- **触发**: 主任要求对 12 仓项目出一份尽量完备的审查计划，从产品设计到技术实现，技术实现以 **DDD 遵循度**与**代码整洁度**为重点，并按当前软件开发最佳实践补齐其余维度。计划经批准（14 工作流 / 86 审查项 / 风险分层 T0~T3 / 波次 W0~W7），主任授权落仓立案（A5）。
- **本 ODR 范围**: W1 产品/治理波（P 产品设计 + G 文档治理 + X 流程治理）。其余波次见 ODR-069（core 架构）/ 070（回测正确性）/ 071（agent AI）/ 072（安全/可靠性/依赖）/ 073（服务仓/前端巡检）。
- **取证纪律**: 每项判定带证据坐标（`file:line` 或 命令+真退出码）；证据分级 E1 本地真跑 > E2 CI 产物 > E3 静态读码 > E4 文档推断；环境降级标注。本轮 86 项全判定，静态/取证面收口；真跑/破坏腿见各波 ODR 的待授权腿。
- **去重**: 先对开放任务 + 已裁例外 + 历史审计闭项去重（命中只补证据不新建）；本轮去重表与逐波发现为审查工作件（不落仓），立案时证据坐标抄入各仓 `docs/TASKS.md` 对应任务的 Context 字段。

## Decision

### 主任授权与决策采纳

主任 2026-11-11 批复「所有需要授权的都同意」（A1 真库腿 / A3 破坏腿 / A4 起服务 / A5 落仓立案）。技术岔路按既往约定由审查方实测后直接定并写明代价，本波两条决策采纳如下：

- **D8（W1-F1 `Refs:` trailer）= b 修订规范承认散文引用**。实测 6 仓最近 120 commit `Refs:` trailer = 0/120，但任务号靠 subject/body 散文引用（QT-xx / CORE-xxx / ADR-xxx）120/120 可追溯。**代价**：失去机械可 grep 的 trailer，追溯靠散文；收益低（单人维护、散文已可追溯），不值得为机械形式恢复纪律。落点：core AGENTS.md §8.5 规范 3 的 commit 格式段修订为「任务号须在 subject 或 body 可追溯（散文引用即可，`Refs:` trailer 可选）」。
- **D13（W1-F7 观察窗）= 子台账过期项订正 + 主台账关系写明，随 W1-F6 一起做**。观察窗功能缺口已在 ui 设计子台账 B-01/B-02/B-06 + G1~G4 登记 ⇒ 按去重规则 1 **不新立功能单**，只补逐行证据；新发现部分（子台账 B-05 因子端点过期 / G9 镜像构建失败已被证伪 / 主台账「无开放项」与子台账开放项关系未写明）并入 UI-LEDGER-SELF-CONSISTENCY。

### 发现摘要（W1-F1~F9）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W1-F1 | Low | `Refs:` footer 全组缺失（流程漂移，非代码缺陷） | 6 仓 120 commit `grep -c '^Refs:'`=0；core AGENTS.md §8.5 规范 3 | D8=b → CORE-REFS-TRAILER-RULE [P3] |
| W1-F2 | Medium | agent Hermes 工具契约/提示词/挖掘 skill 未随 adr-041 因子能力退役同步，指示 AI 走死路 | `tellurion-agent:docs/hermes/tools-quant-backtest.yaml:62-107,122-137` / `prompts/quant-research.md:21,26-27,109,192` / `skills/autonomous_factor_mining.md:89,284`；代码侧 `8ace9b9` 已改三工具返回 ErrFactorCapabilityUnavailable | AGENT-HERMES-DOCS-ADR041 [P1] |
| W1-F3 | Medium | 产品入口文档对接线现状整体停在 2026-10-25（退役波后新漂移，10 处） | `tellurion-docs:docs/PRODUCT.md:61` / `ROADMAP.md:10,18,20,99` / `REPO-MAP.md:16,22,25,71`；基准 SYSTEM-DESIGN.md（2026-11-11 已对齐） | DOC-PRODUCT-DRIFT-FIX [P1] |
| W1-F4 | Medium | 七仓 AGENTS.md 依赖表与 go.mod 漂移 + risk contracts indirect | 六仓 AGENTS §4 写 contracts v0.9.0 vs go.mod v0.10.0；core AGENTS:20 kit v0.1.4 vs go.mod:16 v0.3.0；risk go.mod:35 indirect 但 internal/rule/model.go:9 直接 import；core AGENTS:152/:862 :8081 归属句过期 | X-AGENTS-DEPENDENCY-TABLE [P2] + RISK-GOMOD-DIRECT [P3] |
| W1-F5 | Low~Med | frontmatter 卫生 + ADR 索引未同步 | docs TEST.md(09-25)/PRODUCT.md(10-25)/VISION.md(10-25) 等 5 份 last-verified 过期；ARCHITECTURE.md status 应 archived；3 份缺 frontmatter；ADR.md:43 adr-024 未标部分取代 | DOC-FRONTMATTER-HYGIENE [P3] |
| W1-F6 | Low | 台账自相矛盾（2026-11-11 重整引入） | ui `docs/TASKS.md:15`「无开放项」vs 两条 ⬜（:17/:28）；ui AGENTS §5 同句；broker frontmatter 仍描述已归档的 SVC-BROKER-G3 | UI-LEDGER-SELF-CONSISTENCY [P3]（含 broker frontmatter 订正） |
| W1-F7 | High·产品 | 观察窗产品要求大面积缺失（已有子台账跟踪） | ui Explore.vue:112,245-266（无 5 分钟摘要/top3）/:215-240（无路径缩略图）/:66-76（无高原×因果排序）；四干预仅叫停存在；子台账 B-05:695/G9:725 过期 | dedup ui 子台账 B/G（补证据）+ UI-LEDGER-SELF-CONSISTENCY |
| W1-F8 | High | 实验计数与校准不可测，S1 出口「无人干预 100 次」无计数来源 | agent builtin/backtest.go:126-154 + walkforward_tool.go:199 工具直调零实验行；loop.go:235 NumTrials=内存 seq+1（多重检验试验数低估）；db-schema.md:21 只写不读；无 actor/intervention 列、无采纳表、无 holdout、无对账 job | AGENT-EXPERIMENT-COUNT-SURFACE [P1] + AGENT-INTERVENTION-ADOPTION-LEDGER [P1] |
| W1-F9 | Medium·潜在 | 验证器信息隔离部分成立：Hypothesis 直通因果 prompt | agent causal.go:34-48 直通（今天 TPE/MCTS 写机械文本无实泄露，但泄露「当前最优」弱信号，换 LLM proposer 即破防）；成立面 causal.go:127-129 blind.Result=nil | AGENT-HYPOTHESIS-FILTER [P2] |

### 已通过项（正证据，不立案）

- **P-6 能力层拦截 ✅**：research_tool C2 vault 回落已授权（W0-3 核实，契约本体 `tellurion-docs:docs/archive/RESEARCH-equitydeep-legacy.md` §3.3/§3.5 + agent db-schema.md:73 登记），不构成违规。
- **P-7 设计再挑战 ✅**：第四轮「core 未减负」论断已被退役波证伪——core LOC 182,153 vs 2026-10-26 的 202,198（**净减 ~20,045 / -9.9%**，E1 全量计数）；六服务仓 72,066 vs 51,276；七条 SVC-CORE-*-RETIRE 全 ✅；SVC-DEPLOY-01 ✅ 7/7 healthy。表面积成本仍在但接线已真。
- **G-2/G-3 ✅**：W0 检查器全绿（doc_links 66 文件 / guide_refs 双腿 / repo_autonomy 12 仓，1 登记缺口 QT-08 + 2 R6 豁免）。
- **X-3 直推 main 门禁 ✅**：W0 干净 checkout 四件套 12 仓全绿 = 门禁自当闸正证据；新红登记机制存在（ui AUD-61 教训已写入 core AGENTS §8.5）。
- **P-4 promote 闸门 ✅**：copilot 链 fail-closed 无绕过（copilot.go:420-429,666-669）；signal_expr 覆盖 nuance 转 W2/W4 核。

## Consequences

**Positive**:
- 产品入口文档漂移获得集中订正单（DOC-PRODUCT-DRIFT-FIX），以 SYSTEM-DESIGN.md 为基准一次性对齐 PRODUCT/ROADMAP/REPO-MAP；
- S1 出口「无人干预 100 次」与校准可测性首次被显式定性为 High 并拆出可施工任务（计数读面 / 干预标记 / 采纳记录 / holdout / 对账）；
- 观察窗缺口归口到既有子台账，避免重复立单。

**Negative**:
- 校准前三项指标无自动采集路径前，S1 出口不可判定（PRODUCT.md:171 自认）；修复（AGENT-INTERVENTION-ADOPTION-LEDGER）落地前过拟合防护的试验数被低估；
- Hermes 挖掘回路文档指示走死路，浪费 AI 试错次数（运行时哨兵响亮，不静默，但文档与 adr-041 脱节）。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-068 行）+ 尾注 + 累计计数
- 立单（六字段，证据坐标抄入 Context）：
  - `tellurion-agent:docs/TASKS.md` — AGENT-HERMES-DOCS-ADR041 / AGENT-EXPERIMENT-COUNT-SURFACE / AGENT-INTERVENTION-ADOPTION-LEDGER / AGENT-HYPOTHESIS-FILTER
  - `tellurion-docs:docs/TASKS.md` — DOC-PRODUCT-DRIFT-FIX / DOC-FRONTMATTER-HYGIENE
  - `tellurion-ui:docs/TASKS.md` — UI-LEDGER-SELF-CONSISTENCY
  - `tellurion:docs/TASKS.md` — CORE-REFS-TRAILER-RULE（D8=b 规范修订）
  - 跨仓批 X-AGENTS-DEPENDENCY-TABLE（六仓 AGENTS §4）+ RISK-GOMOD-DIRECT 见 ODR-072/073 落点
- dedup 命中只补证据：ui 子台账 B-01/B-02/B-06/G1~G4（W1-F7 逐行证据）

## Metrics

- W1 发现 **9 项**（High 2〔F7 产品/F8〕/ Medium 4〔F2/F3/F4/F9〕/ Low~Med 2〔F1/F5〕/ Low 1〔F6〕）
- 判定表覆盖 P-1~P-7 / G-1~G-5 / X-1~X-3 共 15 项；通过 5（P-6/P-7/G-2/G-3/X-3）/ 漂移或缺口 10
- 全计划 86 项截至 W7 全判定（本波贡献 15 项）
- core LOC 净减 20,045（-9.9%）实证退役波真减负

## Lessons Learned

1. **退役波必然制造新文档漂移**：W1-F3 的 10 处漂移全部是 2026-11-08~11-11 退役波之后产生（DOC-10/11 已闭的是上一代漂移）。代码退役与产品入口文档同步必须同批，否则「现状口吻写历史态」反复发生（ARCHITECTURE.md 教训同型）。
2. **「有日志」不等于「可测」**：ai.experiments 有写入但工具直调漏计 + 零读面 + 无干预标记 ⇒ S1 出口不可判定。可测性是独立审查项，不能从「表存在」推断。
3. **子台账与主台账关系须写明**：ui 主台账「无开放项」与子台账开放 B/G 项并存而不矛盾的前提是关系写明，否则读者（含 agent）会误判仓状态。

## 订正注记（2026-11-11，W7 台账立单时实测发现）

> ODR 只增不删：本节为追加注记，**不改写**上文已 Accepted 的 W1-F3 判定行；原行保留作历史，施工范围以本注记为准。

- **W1-F3 REPO-MAP 漂移已被主任提交修复（ad80a3d）**：上文 W1-F3 把 `REPO-MAP.md:16,22,25,71` 列为「现状口吻写历史态」漂移点。W7 立单时逐行核 `tellurion-docs` 当前 `REPO-MAP.md` + `git log` 实测：主任提交 **ad80a3d**（`docs: 代码-文档对齐审计（2026-11-11）`，已 `merge-base --is-ancestor` 确认在 main）已按 12 仓 `go.mod` 实测重写版本列、订正状态列与「core 侧零调用方」类断言，REPO-MAP 的这四处漂移**已闭**。`SYSTEM-DESIGN.md` 同批刷新。
- **处置**：`DOC-PRODUCT-DRIFT-FIX [P1]`（`tellurion-docs:docs/TASKS.md`）**收窄**到仍漂移的两份入口文档——`PRODUCT.md:61`（「其余四条…连调用方都没有」与 risk 客户端已装配带开关测试不符）+ `ROADMAP.md:18`（QT-32 仍 ⬜ 但 core 已收口）/`:20`（「只有 data 一条读链真接线」）/`:99`（MockTrader + `live-trading.md` 死链）。REPO-MAP / SYSTEM-DESIGN 从该单**剔除**（已修，不重复施工）。W1 发现总数与严重度不变，仅 F3 的施工面收窄。
- **教训补**：退役波与文档对齐是两条并行的施工流，主任侧的对齐审计（ad80a3d）会先闭掉一部分本波登记的漂移点。派工前必须按**当前工作区 + git log** 复核每个 `文件:行号`，不能拿审查时点的快照直接立单——否则会把已修的点重新派一遍。