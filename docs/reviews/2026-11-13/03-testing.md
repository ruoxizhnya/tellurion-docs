---
status: review
last-verified: 2026-11-13
verified-by: 2026-11-13 只读深度审查（角度 3 测试）；证据 = CI 定义 + 测试代码 file:line + 当日真跑日志（reports/test-2026-11-13/*，只读引用）
---

# 角度 3 · 测试（6.5 / 10）

> 审查范围：覆盖面、真跑证据可靠性、假绿（跳过 / 过宽断言）、CI 门禁有效性。
> 方法：只读。**未由本审查执行任何测试**；但审查期间发现工作区存在同日另一会话的综合测试产物 `reports/test-2026-11-13/`（未提交），本报告将其作为“当日真跑证据”引用，并标注为他人执行、快照时间。
> 相关基线：[TEST.md](../../TEST.md) · 各仓 `.github/workflows/ci.yml` · `docs/COMPREHENSIVE-TEST-PLAN-2026-11-13.md`（未提交）

---

## 1. 评分

| 子维度 | 权重 | 得分 | 依据摘要 |
|---|---|---|---|
| 覆盖面 | 30% | 8.0 | 10 个 Go 仓约 2,800 个 Test 函数、测试代码 16.6 万行（生产 14.2 万）；分层 L0–L6 有明确分工；服务仓 DB 腿在 CI 恒跳过 |
| 真跑证据可靠性 | 25% | 5.5 | 当日全栈 e2e `TestBacktestAPI_EndToEnd` 在 **409** 下仍 PASS；Playwright 7 failed 尚未分类；证据文件多在仓外/未提交 |
| 假绿 | 20% | 5.0 | e2e 对 4xx/5xx/空数据普遍“记日志即通过”；7 仓 43 处 `t.Skip` 在 CI 无数据库时全部跳过；`integration` 构建标签从未被执行 |
| CI 门禁 | 25% | 7.0 | gofmt/vet/staticcheck/`-race`/govulncheck/覆盖率/路由契约/文档链接门齐全且 0 `continue-on-error`；但覆盖率下限 52% 对实测 72.5%，服务仓与 UI 无覆盖率门 |
| **加权总分** | 100% | **6.5** | 测试资产丰富且诚实标注多，但“绿”的可信度被几处结构性缺口拉低 |

---

## 2. 覆盖面盘点（实测）

| 仓 | 生产行 | 测试行 | Test 函数 | CI 有 DB | CI 覆盖率门 |
|---|---:|---:|---:|---|---|
| tellurion（core） | 75,786 | 94,335 | 1,622 | 有（service + applymigrations + DSN） | 有（total 52 / backtest 65） |
| tellurion-agent | 9,161 | 10,987 | 349 | **无** | 无 |
| tellurion-strategy | 4,931 | 3,363 | 117 | **无** | 无 |
| tellurion-data | 7,132 | 6,124 | 166 | **无** | 无 |
| tellurion-risk | 3,409 | 2,301 | 83 | **无** | 无 |
| tellurion-orchestration | 3,714 | 2,009 | 52 | **无** | 无 |
| tellurion-analytics | 4,186 | 3,035 | 92 | **无** | 无 |
| tellurion-broker | 2,847 | 1,101 | 33 | **无** | 无 |
| tellurion-contracts | 5,036 | 4,410 | 209 | 不涉及 | 无（TASKS 已自陈“75% 门槛无承接者”） |
| tellurion-kit | 5,111 | 6,829 | 87 | 不涉及 | 无 |
| tellurion-ui | – | 52 个 vitest 文件 | 643 例 | 不涉及 | 无（CI 不跑 `test:coverage`） |

测试体量本身是强项：core 测试/生产行比 1.24，kit 1.34。`lint:tests` 还会扫描 51 个前端测试文件，禁止 `toBe(expected, "message")` 误用（`reports/test-2026-11-13/w1-ui.log` 实测 “no misuse found”）。

---

## 3. 主要发现（按严重度）

### P1-1 · 核心 e2e 对失败“记日志即通过”，409 也算 PASS

- 代码：`e2e/tests/integration_test.go:200-217`。`TestBacktestAPI_EndToEnd` 只在 200 分支里做 `pollForCompletion`；非 200 只 `t.Logf("Backtest request failed with status %d", ...)`，**没有任何 `t.Fatal/assert`**。
- 当日真跑日志（`reports/test-2026-11-13/w3-core-e2e.log`）：
  
  ```
  === RUN   TestBacktestAPI_EndToEnd
      integration_test.go:216: Backtest request failed with status 409: 409 Conflict
  --- PASS: TestBacktestAPI_EndToEnd (0.00s)
  ```
- 同一模式还出现在 `TestOHLCVAPI_DataRetrieval`（400 也 PASS）、`TestFundamentalsAPI_DataRetrieval`（无数据也 PASS）。
- 后果：这套 e2e 被当作“回测端到端已验”的证据，但**它在回测被拒绝时仍然绿**。这正是用户要求的“假绿”定义。
- 证据强度：实测（代码 + 当日日志）。

### P1-2 · 当日全栈 Playwright 7 条失败，与“0 开放项”台账冲突

- 综合测试计划 W5 判据（`docs/COMPREHENSIVE-TEST-PLAN-2026-11-13.md:35`）：**218 passed / 0 failed / 2 skipped**，视觉 12/12。
- 当日实测（`reports/test-2026-11-13/w5-playwright-final.log` 末段）：**211 passed / 7 failed / 2 skipped**，耗时 9.3m。
- 7 条失败：`a08-job-console.spec.ts:296`（取消走真后端）、`api-strategy.spec.ts:28`（copilot 未配 key 的错误形状）、`backtest-engine.spec.ts:442`（responsive 布局）、`copilot.spec.ts:73`（导航）、`data-sync-error.spec.ts:16/126`（未知 job 类型、重试计数）、`data-sync.spec.ts:146`（重试失败作业）。
- 同期 `tellurion-ui/docs/TASKS.md:15` 写“**当前没有未做的单**”，`:25` 只把 V-2/V-3 两条视觉基线列为测试债；7 条红未出现在任何台账中。
- 这 7 条里至少 3 条看起来是**功能/契约**（取消状态回写、data-sync 重试计数、未知 job 失败），不是纯环境；其余含环境因素（AI_API_KEY、旧镜像）。**未分类**本身就是问题：无法判断是回归还是环境。
- 证据强度：实测（日志 + 台账原文）；“其中 3 条为真实缺陷”为推断，需按计划 §1.3 三分类复跑确认。

### P1-3 · 7 个服务仓 CI 不提供数据库，43 处 `t.Skip` 恒跳过

- 逐仓 CI 检索：`tellurion-data / broker / agent / analytics / orchestration / risk / strategy` 的 `.github/workflows/ci.yml` **均无** `services: postgres`、无 `*_TEST_DSN` 注入（core 有）。
- 同时服务仓共 43 处 `t.Skip(`（data 14 / agent 16 / analytics 3 / orchestration 4 / strategy 4 / broker 1 / risk 1），绝大多数以 DSN 为空为跳过条件。
- 被跳过的恰是**迁移、幂等、租约/领取、持久化**这类只能对真库验证的语义；CI 绿只覆盖纯内存逻辑。
- 这是“按仓各自负责”的结构性缺口，不是某一条单；`CORE-CI-DB-LEGS-SKIPPED` 只修了 core。
- 证据强度：实测（CI 文件 + skip 计数）。

### P2-1 · `integration` 构建标签的测试从未在 CI / Makefile 执行

- `pkg/backtest/router_wiring_integration_test.go:1`（`//go:build integration`）等 4 个文件带非平台标签；CI 与 `Makefile` 均未出现 `-tags=integration`（全仓检索）。
- 其中包含“intraday 路由正/负腿”这类**防静默缺 0** 的验证；默认构建下它们连编译都不参与。
- 证据强度：实测（标签文件 + CI/Makefile 无引用）。

### P2-2 · 覆盖率门禁偏松且覆盖不均

- core CI：`-total-min=52 -pkg-min=tellurion/pkg/backtest=65`（`.github/workflows/ci.yml:144-146`），注释自陈基线为 **72.5% / 82.5%**（`:124-126`）⇒ 总覆盖率下滑 **20.5 个点**仍绿。
- 服务仓、contracts、kit 全部无覆盖率下限；UI CI 只跑 `npm test`，不跑 `test:coverage`（`tellurion-ui/web/package.json` 有脚本但 CI 未调用），且 vitest 的 coverage include 排除 `src/pages/**`、`src/components/layout/**` 等页面层。
- 结论：四分之三的代码面“覆盖率不可见”，核心面“可见但门很宽”。
- 证据强度：实测（CI/配置）。

### P2-3 · 测试非 hermetic：会扫未跟踪的工作区文件

- `cmd/analysis/rate_limit_budget_test.go:147-171` 从仓库根 `WalkDir` 所有 `.yml/.yaml`（只排除 `.git/node_modules/reports/vendor`），把**未跟踪**的 `deploy/compose/isolated-test.override.yml` 也纳入。
- 当日两次真跑（`w1-core-cover.log` 20:52、`w1-core-db-tests.log` 21:37）均因该文件 FAIL：
  
  ```
  --- FAIL: TestCompose_DefaultRateLimitIs100AndOverridable
      Should be empty, but was [deploy\compose\isolated-test.override.yml]
  ```
- 该文件当前已不含匹配内容（只读复查），所以是“执行者工作区状态决定测试结果”：本地红、干净检出/CI 绿。对“破坏验证”文化是反向噪声。
- 证据强度：实测（代码 + 两次日志 + 当前文件内容）。

### P2-4 · TEST.md 的测试口径与现状脱节

- `docs/TEST.md:438`：“CI **不设覆盖率阈值**”——实际 core CI 自 REV-21 起已有阈值（`ci.yml:118-146`）。
- `docs/TEST.md:478`：前端 `18 文件 / 208 条`（2026-09-25）——实际当日 `52 文件 / 643 条`（`w1-ui.log`）。
- `docs/TEST.md:567`：e2e `18 spec / 163 例`、`:585` `127 passed / 34 failed`——实际 `31 spec`、当日 `211 passed / 7 failed`。
- frontmatter（`:4`）只声明“frontmatter 校时，正文未改”，但正文是其它文档引用测试能力的入口，读者会把它当现状。
- 证据强度：实测（文档原文 vs 当日日志/文件计数）。

### P2-5 · “真跑证据”存放在仓外，不可审计

- core `docs/TASKS.md` 的 W0 取证指向 `C:\Users\ruoxi\.qoder-cn\plans\audit-w0\<repo>.log`（仓外、非版本化）；本次综合测试的证据 `reports/` 与计划 `docs/COMPREHENSIVE-TEST-PLAN-2026-11-13.md` 均为 **git 未跟踪**（`git status` 实测 `?? docs/...`、`?? reports/`）。
- 后果：任何“已实测”的结论都无法从仓库历史复现；换机器/换会话即丢失。
- 证据强度：实测（git status + 路径）。

### P3-1 · CI 口径小漂移

| 项 | 证据 | 影响 |
|---|---|---|
| agent CI 缺 `gofmt` 步 | `tellurion-agent/.github/workflows/ci.yml` 仅 Build/Vet/Govulncheck/Test/Test-race/Staticcheck | 其他 6 个 Go 仓都卡格式，agent 不卡 |
| staticcheck 版本漂移 | data/risk/strategy 用 `@v0.8.2`；broker/agent/analytics/orchestration 用 `@latest` | 规则集随日期变化，历史绿不可复现 |
| 仅 Linux 跑测试 | core CI `runs-on: ubuntu-latest`，Windows 仅 `GOOS=windows go vet` | Windows Job Object / 路径分支无 CI 覆盖 |
| 服务仓重复跑两遍测试 | data/agent 等先 `go test` 再 `go test -race` | 时长翻倍，收益有限（可在 race 腿加 `-short`） |

---

## 4. 正面证据（为什么不给更低分）

1. **CI 无 `continue-on-error`**：12 仓扫描为 0，没有“允许失败”的软门。
2. **结构性护栏多且会咬人**：路由契约（`routes_contract_rev13_test.go`）、路由策略（`route_policy_test.go`）、包接线（`package_wiring_test.go`）、部署面限流（本次真红过）、contracts 5 条护栏。
3. **覆盖率门来自实测基线**，不是拍脑袋，且有“改阈值须同笔改 TASKS”的纪律注释（`ci.yml:127`）。
4. **诚实标注缺口**：QT-61 用 `::notice` 显式点名未覆盖面；`testdb` 会打印被跳过的条数与原因（当日日志可见“11 个 DB 用例被跳过”）。
5. **UI 单测全绿且真跑**：52 文件 / 643 例通过，另有测试写法 lint。

---

## 5. 建议（仅供决策）

1. 把 `TestBacktestAPI_EndToEnd` 改成“非 200 即 Fail”，并把 409 的幂等冲突作为**显式**期望处理；否则该用例不配叫 e2e。
2. 给 7 条 Playwright 失败按计划 §1.3 做 PASS/FAIL/BLOCKED 分类，落进 UI 台账；未分类前不得宣称“0 开放项”。
3. 服务仓 CI 增加一个 Postgres service（或统一 matrix），至少让迁移 / 幂等 / 领取三类 DB 腿在 CI 真跑。
4. 给 `integration` 标签加一条 CI 腿（可 nightly），至少覆盖路由正/负腿。
5. 把 `reports/` 与综合测试计划纳入版本控制（或改为 CI artifact），否则“真跑证据”不可审计。
6. 提高覆盖率门（按实测基线留 5pt 而非 20pt），并给 contracts/kit/服务仓补最低下限；UI CI 跑 `test:coverage`。

---

## 6. 实测 / 推断分界

| 结论 | 强度 |
|---|---|
| e2e 409 仍 PASS | 实测（代码 + 日志） |
| Playwright 211/7/2 与 W5 判据不符 | 实测（日志） |
| 服务仓 CI 无 DB、43 处 skip | 实测（CI 文件 + 计数） |
| integration 标签从未执行 | 实测（检索） |
| 覆盖率门 52/65 vs 72.5/82.5 | 实测（CI 注释 + 门禁参数） |
| 测试非 hermetic 导致本地红 | 实测（两次日志） |
| TEST.md 数字过期 | 实测（文档 vs 当日日志） |
| “7 条失败中≥3 条为功能缺陷” | 推断（未逐条复跑分类） |

---

## 7. 未覆盖与限制

- 本审查**没有执行**任何 `go test` / Playwright / compose；所有“真跑”均引用 `reports/test-2026-11-13/` 的他人产物快照（20:52–21:37 UTC），该批次可能仍在进行。
- 未审查 `pkg/backtest` 全部断言质量；只抽样了 e2e 与结构性护栏。
- 未核验 GitHub Actions 历史运行结果（无网络访问）。
