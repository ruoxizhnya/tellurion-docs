# ODR-073: 第五轮全系统审查 · 服务仓 / 前端逐仓巡检（W6）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-023（三角色实验室·人是闸门）/ adr-036（六仓服务定性·G0~G4 就绪门）；strategy adr-0004（promote/core 消费边界）；QT-32（promote 人工闸门）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md)；本轮 W6 = 6 服务仓 + ui 逐仓 D 战术 / K / T / C-4 / C-6 巡检 + 跨仓矩阵收口 + I-4 保留期）

---

## Context

- **本 ODR 范围**: W6 服务仓/前端逐仓巡检（data/strategy/risk/analytics/orchestration/broker 六服务 + ui）+ 跨仓矩阵（T-1 CI 门禁 / C-6 REST 一致）+ I-4 数据保留期（W7 收敛期补判定）。其余波次见 ODR-068/069/070/071/072。
- **取证纪律**: 同 ODR-068（E1>E2>E3>E4，真退出码，环境降级标注）。W6 主证据 = 7 仓本地真跑基线（6 Go 仓 gofmt/build/vet/test EXIT=0；ui build/lint/typecheck/test EXIT=0，**38 文件 / 540 条全 PASS**，与归档 2026-11-07 同数无退化）+ 逐仓静态抽验。破坏腿/起服务腿挂 A3/A4（主任已授权）。
- **核心结论**: 六服务仓的 DDD 战术纪律（事务边界 / SQL 隔离 / 静默回落 / 测试质量 / 错误语义）**6/6 全绿**；两个真缺口 = **W6-F2 ★H promote 闸门无人类操作面 + UI 把闸门拦下误报成「沙箱未启用」**（让 Copilot 对主任呈现为「永远失败」）+ **W6-F1 risk 集成测试双 DSN 名静默 skip**（假绿形状）；跨仓矩阵缺口 = T-1 CI（6 服务仓 + agent + contracts 无 -race/staticcheck，ui 无 build 步）+ C-6 探针命名分裂（data `/health` vs 5 仓 `/healthz`）。

## Decision

### 主任授权与决策采纳

主任 2026-11-11 批复「所有需要授权的都同意」。本波两条技术岔路按既往约定由审查方实测后直接定并写明代价：

- **D3（W6-F2 promote 人类操作面）= b 先行 + a 立案**。**b**：先给主任一条成文的人工 promote 路径（runbook + 服务 token 代调 strategy `POST .../versions/{hash}/promote`），闸门今天就能用；**a**：UI 按钮经 core 反代到 strategy（需裁角色策略——人的 promote 走什么身份，strategy 策略表今天只认 `service` + `X-Actor`，主任以管理员身份调也不通）。同时修 Copilot.vue 误报（**不依赖角色裁决**，可先行）。**代价** = b 阶段主任要拿服务 token curl（非产品面，可审计但不好用），a 须先裁「人 promote 的身份」（admin 代调还是给主任签发 service token）；收益 = 闸门可用性立即恢复 + UI 文案不再撒谎，产品面随后补。落点 UI-COPILOT-GATE-SURFACE [P1]（含 runbook b 腿 + UI a 腿）。
- **D12（C-6 探针命名分裂）= a data `/health` → `/healthz`**。data 探针名 `/health`（server_test.go:233）vs 其余 5 服务仓 `/healthz`，命名分裂。**代价** = 改名须同步消费方（core 反代 / compose healthcheck / k8s 若留——grep 可数，D7=a 退役 k8s 后消费方更少）；收益 = 全组探针命名一致，低成本。b 成文豁免也可接受但 a 改名成本更低。落点 X-PROBE-NAMING [P3]。

### 发现摘要（W6-F1/F2 + 跨仓矩阵 + I-4）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W6-F1 | Low~Med | risk 集成测试双 DSN 环境变量名，只设其一另一套静默 skip 且 EXIT=0（假绿） | `RISK_TEST_DSN`（actor_pg_test.go:23 / migrate_test.go:27 / monitor_test.go:21）vs `TELLURION_RISK_TEST_DSN`（approve_pg_test.go:32）；AGENTS §2 与 runbook 均未登记任一名字 | RISK-TEST-DSN-UNIFY [P2] |
| W6-F2 | Medium·★H | promote 闸门无人类操作面，UI 把闸门拦下误报成「沙箱未启用」+ 承诺不存在的回测跳 | agent copilot.go:666-669 / stopAtGate:708-709 终态 `sandbox_rejected`；api-schema.md:92/:168-172 诚实成文四成因；ui Copilot.vue:89-92 对一切 sandbox_rejected 追加「沙箱未启用」假话、:71「→ 回测」假进度、:78-84 仍处理 backtest_complete；全 ui 仓 grep promote 零命中；strategy /promote 只认 service+X-Actor | D3=b+a → UI-COPILOT-GATE-SURFACE [P1] |
| T-1 矩阵 | Low~Med | 6 服务仓 + agent + contracts CI 无 -race/staticcheck；ui CI 无 build 步、e2e job 仅安装烟雾 | 6 服务仓 ci.yml 逐字相同最小门禁（gofmt+build+vet+test）；**core+kit 已有 -race**（core AUD-12 / kit KT-12，前提订正）；ui ci.yml 无 `npm run build`、e2e job 只 checkout+setup-node+npm ci（23 spec 真跑需手工起栈） | X-CI-RACE-STATICCHECK [P2，范围已订正] |
| C-6 矩阵 | Low | 探针命名分裂：data `/health` vs 其余 5 仓 `/healthz` | data server_test.go:233 `/health`；429+Retry-After="1" 全组一致 ✅；/readyz 三态模式一致 ✅（broker 无 /readyz=G4 已裁不算缺口） | D12=a → X-PROBE-NAMING [P3] |
| I-4 | Low | run.backtest_results / quant.run_provenance 无保留期（研究数据是否刻意长留待裁） | 全仓 grep DELETE/vacuum/retention 零命中这两表；对照 broker order_acks 已有 90 天保留（W6 ✅）+ data evidence 归档面有保留期清理（evidence.go:22） | CORE-RESULT-RETENTION [P3，待语义确认] |
| W2-F7/F12 残余 | Low 簇 | 跨仓低优先清理（承 ODR-069） | strategy Dockerfile 退役名；contracts fees 死示例注释；agent /api/health 豁免表注册；分页 offset 不一致登记；ui openapi 不复制守卫（低成本 grep） | X-LOW-CLEANUP [P3] |

### W6-F2 事实链（★H，全部 E1/E3 取证）

1. **后端闸门行为正确**：编译通过 + 资产坐标登记后链停在 `BlockedPromoteGate`，job 终态 = `sandbox_rejected`，`build_error` = 「编译通过并已登记资产坐标…未过 promote 人工闸门，不进回测（QT-32）」（agent copilot.go:666-669）。api-schema.md:92/:168-172 **诚实成文**：`sandbox_rejected` 今天有四种成因（闸门拦下 / 资产登记失败 / 链写不进 / chain sink 未装配），`generated`/`backtest_complete`/`backtest_failed` 是预留态今天不产生，UI 白名单消费它们是契约刻意保留（「不删」）。**后端与契约侧无缺口**。
2. **UI 误报**：Copilot.vue:89-92 对**一切** `sandbox_rejected` 追加「（沙箱未启用：需在后端配置 copilot.working_dir 后，AI 生成的代码才会真正编译验证）」——对今天占主导的**闸门拦下**路径这是假话：沙箱开了、编译过了、是人的闸门拦的。主任看到的 = 「生成未成功」+ 两句互相矛盾的解释。
3. **UI 承诺不存在的回测跳**：Copilot.vue:71「生成中（LLM → 沙箱编译 → **回测**）」；:78-84 仍处理 `backtest_complete`。agent 今天**不跑回测**（copilot.go:660 明写），这一跳是未来 core 执行侧的事。白名单留着是契约要求，但**进度文案**在撒谎。
4. **promote 无人类操作面**：全 ui 仓 grep `promote|promote_gate|blocked_reason` **零命中**。唯一 promote 端点 = strategy `POST .../versions/{hash}/promote`，策略表**只认 service 角色** + 要求 `X-Actor`（SVC-STRAT-G1）——主任以管理员身份调也不通，只能拿服务 token curl。agent 全仓零 promote 调用方（W4 A-3 已证）。⇒ **ADR-023 的「人是闸门」在产品面没有落地路径**：Copilot 主循环（生成 → 人审 → promote → 回测）在「人审」这一步死胡同。
5. **判定**：闸门本身 fail-closed 正确（W4 A-3 ✅ 不变）；缺的是**人类侧可用性**——按严重度标尺属漂移/产品缺口 = Medium，但它让 Copilot 功能对主任呈现为「永远失败」，W7 立案优先排期。

### 逐仓矩阵结论（6 服务仓 + ui）

| 维度 | 结论 |
|---|---|
| W0 基线 | 7 仓全绿（6 Go 仓 gofmt/build/vet/test EXIT=0；ui build/lint/typecheck/test EXIT=0，540 条 PASS） |
| D-T2 事务边界 | 6/6 ✅（真事务 / FOR UPDATE / advisory lock / 单语句原子占位，各有绝对断言或语义套件） |
| D-T3 SQL/驱动泄漏 | 6/6 ✅（pgx 隔离在 store 单文件/单包，领域层零驱动；data 四域包 SQL 零命中） |
| K-4 静默回落 | 6/6 ✅（time.Now 命中全为时间戳/可注入 clock/限流/当日快照语义；DBT-13 严格解析已随迁 data） |
| K-7 测试质量 | 6/6 ✅ + ui 🔶（零占位断言；全部 Sleep 核实合法：helper-process / 轮询间隔 / 竞争提示+channel 同步；ui 945 warnings 为已登记刻意债，0 errors） |
| C-4 错误语义 | 6/6 ✅（哨兵→HTTP 映射表 + 绝对断言；207/409/429/503 各归其位；三态 code 一致） |
| C-6 REST 一致 | 🔶 探针命名分裂（data `/health` vs 5 仓 `/healthz`，D12=a）；429+Retry-After="1" 全组一致；/readyz 三态一致 |
| T-1 CI 门禁 | 🔶 全组矩阵缺口（6 服务仓 + agent + contracts 无 -race/staticcheck；ui 无 build 步、e2e 仅安装烟雾；**core+kit 已有 -race**） |
| T-3 skip 诚实 | 5/6 ✅ + risk ⚠️（W6-F1 双 DSN）；ui e2e 23 spec 零 fixme ✅（5 处 test.skip 全为带理由条件 skip） |
| T-4 契约测试 | broker wire 逐字节 ✅；data/strategy/risk/analytics/orchestration 各有映射表/语义套件 |

### 已通过项（正证据，不立案）

- **A-2 编译子进程硬上界 ✅（E1，strategy）**：DefaultProcessTimeout=20m / MaxProcessTimeout=1h（compilerclient.go:48/:51）；配置越界 fail-loud（:117-119，测试 :99-104 断言负值与 >1h 被拒）；exec.CommandContext 强制（:324）；真起不退出子进程到点被杀（:403-419）。
- **broker I-3 幂等原子性 ✅**：Reserve = 单条原子 `INSERT … ON CONFLICT (account_id, client_order_id) DO NOTHING RETURNING reserved_at`（ackstore/pg.go:66-78），跨实例占位正确，无需事务包装。
- **broker R10 ✅**：幂等映射读失败**不**报 channel_down（mock_test.go:334/:347）；存储 vs 通道失败区分演练（g4_drill_test.go:18）。
- **ui C-5 openapi 不复制 ✅**：全仓 glob `*openapi*.{yaml,yml,json}` 零文件；e2e 只在注释引 core:docs/openapi.yaml；ADR-0001 在位（无静态守卫防未来复制 = X-LOW-CLEANUP 观察）。
- **ui K-7 lint 945 warnings = 已登记刻意债**：eslint 三规则降 warn（no-explicit-any / no-unused-vars / no-empty-object-type），CI 明写「只守 error」；归档 :254/:416/:499 逐次记数 939→943→945，各提交均「0 新增 error、规则未放宽」——有文档、无开放单，属刻意取舍，不立案。
- **broker 无 /readyz = G4 已裁口径**（/healthz 唯一探针，就绪=装配闸通过），**不是缺口**。
- **X6c 真钱通道 ⏸ = ADR-0003 已裁**：只核 P1~P5 重开条件未满足，不重开。

### 前提订正（W6/W7 累计）

1. **T-1 矩阵「仅 kit 有 -race」错**：core 也有（AUD-12，ci.yml Test 步 `-count=1 -race -coverprofile`）。正确口径 = **core + kit 有；agent / contracts / 6 服务仓无**。X-CI-RACE-STATICCHECK 范围从「6 服务仓」扩为「6 服务仓 + agent + contracts」（contracts 是否补由立案裁——纯值对象+测试，竞态面小）。
2. **ui e2e job 不是「真跑」**：只有 checkout+setup-node+npm ci（注释已诚实订正 2026-10-26），等于「依赖装得起来」烟雾，23 spec 真跑需手工起栈。

### 待授权腿（A3/A4 已授权，施工前取证）

- W6 本身无破坏腿需求（全静态+只读门禁）；承接 W3 真跑（A1）/ W4 破坏腿三组（A3）/ W5 S-2 真 curl + R-2 SIGTERM 演练（A4）。

## Consequences

**Positive**:
- promote 闸门人类侧可用性恢复（D3=b runbook 先行 + a UI 立案）+ Copilot.vue 误报订正，主任不再看到「永远失败」的假象，ADR-023「人是闸门」在产品面有落地路径；
- risk 双 DSN 统一后 PG 集成腿不再静默 skip，「跑的人以为全过」的假绿形状消除；
- 跨仓 CI 补强（-race/staticcheck）+ 探针命名一致后，全组门禁矩阵对齐 core+kit 既有水平。

**Negative**:
- D3=b 阶段主任要拿服务 token curl promote（可审计但非产品面），a 的角色裁决（人 promote 走什么身份）未定前 UI 按钮不能落；
- I-4 保留期须先裁「研究数据是否刻意长留」语义——不默认删研究数据，清理腿只 _test 验证；
- X-CI-RACE-STATICCHECK 的 -race 结论只认 CI（本机无 gcc 不可跑），破坏腿（注入竞态验证 CI 红）属 E2 待 CI 真跑。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-073 行）+ 尾注 + 累计计数（ODR 67→73，Audit 15→21）
- 立单（六字段，证据坐标抄入 Context）：
  - `tellurion-ui:docs/TASKS.md` — UI-COPILOT-GATE-SURFACE [P1]（D3=b runbook + a UI；含 Copilot.vue 误报订正）
  - `tellurion-risk:docs/TASKS.md` — RISK-TEST-DSN-UNIFY [P2]
  - `tellurion:docs/TASKS.md` — CORE-RESULT-RETENTION [P3]（I-4，待语义确认）
  - 跨仓批 X-CI-RACE-STATICCHECK [P2]（6 服务仓 + agent + contracts CI 补 -race/staticcheck；ui 补 build 步；core+kit 已有不动）
  - 跨仓批 X-PROBE-NAMING [P3]（D12=a，data /health→/healthz + 消费方同步）
  - 跨仓批 X-LOW-CLEANUP [P3]（承 ODR-069 W2-F7/F12 残余：strategy Dockerfile 退役名 / contracts fees 死注释 / agent /api/health 豁免注册 / 分页 offset 登记 / ui openapi 不复制守卫）
- dedup 命中只补证据：ui 子台账 B-01/B-02/B-06/G1~G4（W1-F7 观察窗，见 ODR-068）/ AGENT-COPILOT-WORKING-DIR ⛔（W4 A-2 沙箱证据，见 ODR-071）

## Metrics

- W6 发现 **2 项**（W6-F1 Low~Med / W6-F2 Medium·★H）+ 跨仓矩阵 **2 项**（T-1 Low~Med / C-6 Low）+ I-4 **1 项**（Low）+ W2-F7/F12 残余 Low 簇
- 判定表覆盖 6 服务仓 × D-T2/D-T3/K-4/K-7/C-4/C-6/T-1/T-3/T-4 + ui 共 ~60 项；战术纪律 D-T2/D-T3/K-4/K-7/C-4 **6/6 ✅**；🔶 = C-6/T-1/T-3(risk)
- 7 仓本地真跑基线全绿（E1）；ui 38 文件 / 540 PASS（与归档同数无退化）；e2e 23 spec 零 fixme
- 全计划 86 项截至 W7 全判定（本波贡献逐仓矩阵 + 跨仓收口）

## Lessons Learned

1. **fail-closed 正确 ≠ 产品可用**：promote 闸门后端 fail-closed 无缺口（W4 A-3 ✅），但「人是闸门」在产品面没有操作路径 + UI 把闸门拦下误报成「沙箱未启用」⇒ 功能对主任呈现为「永远失败」。可监督性（ADR-023 一等需求）要求闸门不仅拦得住，还要让人看得见、操作得了。
2. **静默 skip 是假绿形状（T-3）**：risk 双 DSN 名只设其一另一套静默 skip 且 EXIT=0，跑的人以为 PG 腿全过。集成测试的环境变量名必须统一 + 登记，否则「绿」不可信。
3. **矩阵前提要用 grep 核验，不沿用预取证口径**：T-1「仅 kit 有 -race」沿用了计划预取证口径，实测 core 也有（AUD-12）。跨仓矩阵结论须逐仓核 CI 文件，不靠记忆。
4. **已登记的刻意债不立案，但要有文档**：ui 945 warnings 有归档逐次记数 + 「0 新增 error、规则未放宽」声明 = 刻意取舍，不是缺陷；与「无文档的漂移」区分处置。