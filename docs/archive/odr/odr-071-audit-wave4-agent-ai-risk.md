# ODR-071: 第五轮全系统审查 · agent AI 风险（W4）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-023（三角色实验室·可监督性）/ adr-024（表达式执行载体·LLM 代码只是 artifact）/ adr-041（AI 因子工具面不新造端点）/ adr-001（人工插件路径）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md)；本轮 W4 = A AI 风险面，实验员层）

---

## Context

- **本 ODR 范围**: W4 agent AI 风险波（A-1 LLM 产物不执行 / A-2 WASM 沙箱 / A-3 promote 闸门 / A-4 验证器信息隔离 / A-5 预算控制 / A-6 提示注入 / A-7 实验生命周期）。DDD 判据「试什么/怎么试/试完怎么判 = agent」。
- **取证纪律**: 同 ODR-068。本波 E1 真跑 = `w4-wasm.log`（core sandbox 三包 **121 PASS / 0 FAIL / 0 假绿**）+ `w4-agent.log`（agent 五包 **319 PASS / 0 FAIL / 1 诚实 DSN skip** = TestRun_RealPipelineAndRealDB），均 2026-11-11 EXIT=0。
- **核心结论**: AI 可监督性的四道硬闸（不执行 / 沙箱 / promote / 信息隔离）**全部 E1 成立**；缺口在预算硬上限（A-5）与实验生命周期收尸（A-7），均属「机制存在但平台侧承载不全」，非闸门失效。

## Decision

### 主任授权与决策采纳

- **D4（W4-F1 LLM 预算）= a 平台侧日累计 USD 硬闸 + 持久化**。`ResearchBudget` 全 agent 仓 Go 代码零命中，只在 `docs/hermes/config/hermes.yaml:57,72`（max_cost_per_session: 5.0）与 skill 文档——执行者是外部 LLM agent 运行时，**不是本平台代码**，Hermes 被换掉/配错就没有任何闸。`cost.go:136` 注释「Persisted to ai_costs table every minute」描述不存在的能力（ai_costs 全仓零写者）。代码侧实际边界只有 egress 令牌桶 10 req/min + 单轮 MaxTries 20，**无 USD 硬上限、无日累计闸**（10/min 全天=14,400 次调用）。**代价** = 加日累计阈值拒绝 + 持久化到 ai.*（metrics 已有累计基础）；收益 = 平台自己的闸不依赖外部运行时。落点 AGENT-LLM-BUDGET-GATE [P1]。
- **D10（W4-F2 explore run 态）= b 起步（启动收尸必须有），a 随计数读面一起做**。run 注册表=进程内 map（handlers_explore.go:262-272），崩溃后 Status 404 不可恢复；`ai.experiments` 的 running 行**无收尸者**（全仓 grep stale/reap/recover/orphan 零命中）⇒ 崩溃后永远 running。**代价** = b 只补启动收尸（run 态仍易失、以 experiments 行为准），a（run 级持久化）随 W1-F8 计数读面一起做；收益 = 收尸立即消孤儿，持久化分阶段。落点 AGENT-EXPLORE-STATE-REAP [P1]。

### A-1~A-7 判定表

| 项 | 判定 | 证据 |
|---|---|---|
| A-1 LLM 产物不执行 | ✅ E1+E3 | agent 执行面只有 go build/gofmt（pipeline.go:656、code_validator.go:134,157）；copilot.go:662 注释记录已删 plugin.Open 死链；**staticcheck 拒危险代码三测试 PASS**（RejectsDangerousCode/ExecCommand/Panic）；core plugin.Open（loader.go:145、registry.go:289）= ADR-001 人工插件路径，loader.go:87 路径校验；ai_boundary repoguard 72 PASS |
| A-2 WASM 沙箱 | ✅ E1 | w4-wasm.log 121 PASS：WithMemoryLimitPages + WithCloseOnContextDone（wazero_runtime.go:55-56，:35-37 注释点明无它超时杀不死 guest）；字节码层冻结 env 白名单（abi_check.go:77）；双预算 PerCall+RunDeadline=10min（on_bar_session.go:36-63）；TestWhileTrueTerminatesWithinBudget 等 8 条终止/监督测试 PASS。**无 fuel=时间基终止的设计取舍**，有测试钉住非缺口 |
| A-3 promote 闸门 | ✅ E1 | **TestQT32A_PromoteGateBlocksEvenAfterSuccessfulBuild PASS**（编译过也拦）；**TestQT32A_TraceWriteFailure_AbortsBeforeLLM PASS**；QT32B_RegistrationFailureIsNotGateBlock / BuildFailureIsNotReportedAsGateBlock 语义精确；copilot.go:650-685 gate+fail-closed；agent 全仓零 promote 调用方。**explore 跑表达式载体（ADR-024 sanctioned）不属闸门对象非旁路**。★H 闸门人类可用性归 W6（ODR-073 W6-F2） |
| A-4 验证器信息隔离 | ✅ E1 | **物理剜除** validation/causal.go:127-128 blind.Result=nil 再递模型；**TestValidateCausal_NarratorNeverSeesResult PASS**；narrator.go:85-114 prompt 只含 Name/IntentType/Hypothesis/Params/UniverseSize/Periods；Hypothesis 全是模板（proposer.go:30,74,80）不含结果与预期结论；system prompt 铁律 1「你看不到回测结果」。唯一自由文本=主任 Description（合法方向通道）。**Hypothesis 直通弱信号缺口归 W1-F9（ODR-068）** |
| A-5 预算控制 | ✗ | **W4-F1**（D4=a） |
| A-6 提示注入 | ✅ E3 结构隔离 | vault 文本以**结构化工具输出**返回（research_tool.go:147-148 stale 判定 + :217 消费者必须降级标注），不拼进 Go 侧指令 prompt（prompts.go 零 research/vault 引用）；残余「工具结果携带指令」风险由 A-1（不执行）+A-3（闸门）兜底 |
| A-7 实验生命周期 | 🔶 | **W4-F2**（D10=b） |

### 发现摘要（W4-F1~F3）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W4-F1 | Medium | LLM 预算无代码硬上限，「预算控制器」只存在于文档；ai_costs 过期注释描述不存在能力 | ResearchBudget 零代码（hermes.yaml:57,72 + skill:257）；cost.go:136 ai_costs 零写者；metrics.go:35 dailyCosts 进程内 map 崩溃即失；ratelimit.go:29 10/min + handlers_explore.go:212-214 MaxTries 20 无 USD 闸 | D4=a → AGENT-LLM-BUDGET-GATE [P1] |
| W4-F2 | Medium | explore run 状态内存-only，崩溃留孤儿 running 行 | handlers_explore.go:262-272 内存 map 无 run 级持久化；全仓零收尸；pipeline.go:759-764 实验日志尽力而为（刻意取舍，NumTrials 用内存 seq+1 不受丢行影响，验证数学不脏脏的是审计完整性） | D10=b → AGENT-EXPLORE-STATE-REAP [P1] |
| W4-F3 | Low | causal 包零测试文件，parseTheory 宽松 JSON 提取无直接单测 | narrator.go:121-143 提取逻辑（裹 markdown/客气话/空理论拒收）；ValidateCausal 测试都在 validation 侧用假叙述者 | AGENT-CAUSAL-PARSE-TESTS [P3] |

### 待授权破坏腿（A3 已授权，收口前真做）

1. ai_boundary repoguard 破坏腿（改坏→变红→还原→复绿）。
2. QT-32 闸门三处绕过面破坏腿（API 直调 / 状态机跳跃 / worker 旁路）。
3. 沙箱逃逸面破坏腿（白名单外 import / 超内存 / 超时 kill 各一条真破坏）。

> 破坏腿纪律：绝对数值断言 + 「调大阈值」腿（不只删守卫）；改坏动作先拿授权（A3 已授）；全程 _test 面或纯代码面，写腿与还原腿同一个行限定。

## Consequences

**Positive**:
- AI 可监督性四道硬闸（不执行/沙箱/promote/信息隔离）全部 E1 坐实，ADR-023「可监督性一等需求」在代码面成立；
- 预算硬闸（D4=a）让平台成本边界不依赖外部 Hermes 运行时；启动收尸（D10=b）立即消孤儿 running。

**Negative**:
- 预算闸落地前，LLM 成本只有 10/min 速率闸无 USD 累计闸，Hermes 配错即无上限（14,400 次/天）；
- explore run 态在 a（持久化）落地前仍易失，跨崩溃续跑无承载（与 W1-F8 计数不可测叠加，S1 出口受阻）；
- A-1/A-2/A-3 的破坏正证据在 A3 施工前只有「护栏在且绿」的静态判定。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-071 行）
- 立单：`tellurion-agent:docs/TASKS.md` — AGENT-LLM-BUDGET-GATE [P1] / AGENT-EXPLORE-STATE-REAP [P1] / AGENT-CAUSAL-PARSE-TESTS [P3]
- 关联 ODR-068 的 AGENT-EXPERIMENT-COUNT-SURFACE / AGENT-INTERVENTION-ADOPTION-LEDGER / AGENT-HYPOTHESIS-FILTER（W1-F8/F9，同 agent 仓）
- dedup 命中只补证据：AGENT-COPILOT-WORKING-DIR ⛔（W4 A-2 沙箱证据，容器沙箱方案退出条件相关）
- 破坏腿（A3）：三组正证据施工前真做，证据抄入对应单

## Metrics

- W4 发现 **3 项**（Medium 2〔F1/F2〕/ Low 1〔F3〕）
- A-1~A-7 判定：✅ 5（A-1/A-2/A-3/A-4/A-6）/ ✗ 1（A-5）/ 🔶 1（A-7）
- E1 真跑：core sandbox 121 PASS + agent 319 PASS / 0 FAIL / 1 诚实 DSN skip

## Lessons Learned

1. **机制存在 ≠ 平台承载**：预算控制器在文档里、ai_costs 注释描述不存在的能力——「文档说有」必须用「代码 grep 零命中」证伪。过期注释（K-6 同族）要删，不能留着误导。
2. **闸门 fail-closed 正确 ≠ 人类可用**：A-3 promote 闸门代码面完美（编译过也拦），但人类侧操作面缺失（W6-F2）让 Copilot 对主任呈现为「永远失败」。可监督性要同时核「闸得住」与「人看得见、操作得了」。
3. **物理剜除优于约定隔离**：A-4 验证器信息隔离靠 blind.Result=nil 物理剜除（注释「靠约定不管用」）+ 测试钉住，而非 prompt 约定——这是可监督性的正确实现姿势。
4. **尽力而为日志的取舍要登记**：实验日志写失败继续跑是刻意取舍（验证数学不脏），但审计完整性脏——取舍本身可接受，须成文登记而非静默。