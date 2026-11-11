# ODR-072: 第五轮全系统审查 · 安全 / 可靠性 / 依赖（W5）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-017（observability·request-id 重开条件）/ adr-027（横切迁 kit·request-id 断言）/ adr-029（request-id 断言）；broker adr-0003（X6c 真钱挂起）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md)；本轮 W5 = S 安全 + R 可靠性 + V 依赖 + I-5 备份容灾）

---

## Context

- **本 ODR 范围**: W5 安全/可靠性/依赖波（S-1~S-7 安全 / R-1~R-5 可靠性 / V-1~V-3 依赖 / I-5 备份容灾）。
- **取证纪律**: 同 ODR-068。本波 E1 真跑 = **govulncheck**（`go run golang.org/x/vuln/cmd/govulncheck@latest ./...`，工具链自动切 go1.26.11）+ **npm audit**；起服务实测（S-2 curl / R-2 SIGTERM 演练）挂 A4（主任已授权），施工前取证。
- **核心结论**: 鉴权 fail-closed 启动闸全服务存在（S-1 ✅）、注入面干净（S-4 ✅）、无硬编码凭证（S-5 ✅）；**两个 High = 依赖漏洞（S-6，10/12 仓符号可达）+ 宿主 PG 无备份（I-5）**；可靠性缺口 = 四服务无优雅停机（R-2）+ correlation-id 半接线（R-4）。

## Decision

### 主任授权与决策采纳

- **D1（V-1 pgx 修复档位）= b 一步收敛 v5.11.0**。govulncheck 坐实 GO-2026-5004（pgx SQLi via dollar-quoted 占位符混淆）符号命中 **7 仓**（core/agent/data/strategy/risk/orchestration/broker），fixed v5.9.2；analytics 已在 **v5.11.0 安全档**（≥v5.9.2，符号不调用）。三档分叉（v5.7.3 / v5.7.5 / v5.11.0）里最高档恰是安全档。**代价** = risk 走 database/sql stdlib 驱动、其余走 pgxpool，v5.7→v5.11 行为差异需各仓测试腿背书；AGENTS 明言「统一到一档要单独立单」——本 finding 就是那个理由。收益 = 安全驱动 + 消除三档分叉。落点 KIT-DEP-SECURITY-BUMP → X-DEP-BUMP-CONSUMERS + BROKER-DEP-BUMP。
- **D11（W5-F7 compose 默认 token）= b 保留 dev-only 并书面登记例外 + runbook 补轮换**。docker-compose.yml:122 `BROKER_SERVICE_TOKEN` 默认 `dev-only-mock-token`——broker 本体 fail-closed（未设即关写面），compose 默认值把这道闸短路了（dev 便利，已注释标明）。**代价** = 保留默认值（a 改必填会砸本地起步体验），须书面登记为 dev-only 例外 + runbook 补 token 轮换步骤；收益 = 单用户回环部署起步体验不变。落点 BROKER-AUTH-ADR 登记例外 + runbook 轮换（随 ODR-069 BROKER-AUTH-ADR）。

### 发现摘要（W5-F1~F7）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W5-F1 | **High** | S-6 依赖漏洞：10/12 仓可行动漏洞，contracts 唯一全绿 | govulncheck E1：GO-2026-5004 pgx SQLi 符号命中 7 仓（fixed v5.9.2）；x/net HTTP/2 ×4（GO-2026-6617/6612/6611/6603，fixed v0.60.0）命中 8 仓；x/text ×2（GO-2026-6629 fixed v0.41.0 / GO-2026-5970 fixed v0.39.0）命中 9 仓（broker v0.21.0 全组最旧）；ui npm 5 high（@vue/server-renderer XSS / nanoid / postcss / source-map-js） | D1=b → KIT-DEP-SECURITY-BUMP [P0] → X-DEP-BUMP-CONSUMERS [P0] + BROKER-DEP-BUMP [P0] + UI-NPM-AUDIT-FIX [P0] |
| W5-F2 | Medium | R-2 四服务无优雅停机；data 同步作业永久孤儿 running | data main.go:86 / risk main.go:91 / analytics main.go:146 / strategy main.go:186 裸 ListenAndServe 无 signal.Notify；data ClaimJob（pg_store.go:107-127）只领 pending 无 lease/心跳/stale 回收；core analysis/worker/agent/broker/orch ✅ 有信号处理 | DATA/RISK/AN/STRAT-GRACEFUL-SHUTDOWN [P1]（A4 演练先行） |
| W5-F3 | Medium | R-4 correlation-id 半接线，ADR「已跨服务传播」断言被证伪 | core RequestIDMiddleware（observability/middleware.go:58）全仓零安装点；kit gin 版有但 6 服务仓全 stdlib mux 装不上；agent 装 HTTPTransport 出站但未装 RequestIDMiddleware 入站恒空；6 服务仓 X-Request-ID 零命中；adr-027:1314-1316 / adr-029:126-127/:448 / adr-017:151 断言被证伪 | KIT-REQUESTID-STDLIB [P1] + 六仓安装 + DOC-ADR-REQUESTID-CORRECTION [P2] |
| W5-F4 | **High** | I-5 宿主 PG 无备份/恢复/演练 | 唯一活库 quant_trading（22 market 表 + quant/ai/strategy/risk/broker/run/analysis.*）；k8s README:88-90 pg_dumpall 只覆盖非活跃面；TASKS-2026-10-16:888「另议」从未捡起；全工作区无备份脚本/cron/恢复演练；ai.experiments/promotions/risk 规则不可重建 | CORE-PG-BACKUP-DR [P0] |
| W5-F5 | Low~Med | R-5 九个代码仓 CI 全部不构建镜像 | 9 仓 .github grep docker/buildx/build-push 零命中；core 缺口已登记（purpose-alignment-audit:135 + check_deploy_consistency.py:672/:727 + AUD-48 静态 COPY 替代）；其余 8 仓有 Dockerfile 但 CI 不构建也无书面豁免 | CORE-CI-IMAGE-GATE [P2]（领头，8 仓跟随或豁免） |
| W5-F6 | Low | R-1 弱探针两处 | analytics compose healthcheck=nc -z 127.0.0.1 8090（docker-compose.yml:480-481，TCP 活≠就绪）；ui Dockerfile 无 HEALTHCHECK；broker 无 /readyz=G4 已裁不算 | AN-READYZ-PROBE [P3] + UI-HEALTHCHECK [P3] |
| W5-F7 | Low | S-3 凭证默认值与轮换 | docker-compose.yml:122 BROKER_SERVICE_TOKEN 默认 dev-only-mock-token 短路 fail-closed；AUTH_INSECURE 默认 true（:213/:313，S-1 闸保证仅回环可接受）；无 token 轮换机制 | D11=b → BROKER-AUTH-ADR 登记例外 + runbook 轮换 |

### 逐仓依赖漏洞矩阵（govulncheck E1，符号可达 = Symbol Results 命中）

| 仓 | 漏洞/模块 | EXIT | pgx GO-2026-5004 | x/net HTTP/2 ×4 | x/text ×2 |
|---|---|---|---|---|---|
| core | 7/3 | 1 | ✓ v5.7.3（auth.go:519 ListAudit） | ✓ v0.55.0 | ✓ v0.38.0 |
| agent | 7/3 | 1 | ✓ v5.7.3（gene_pool/factor_pool.go:238） | ✓ | ✓ |
| kit | 6/2 | 1 | go.mod 有 v5.7.3 **符号未命中** | ✓ | ✓ |
| data | 7/3 | 1 | ✓ v5.7.3（sync/pg_store.go:338） | ✓ | ✓ |
| strategy | 7/3 | 1 | ✓ v5.7.3（asset/pgstore.go:357） | ✓ | ✓ |
| risk | 7/3 | 1 | ✓ **v5.7.5**（pgstore/monitor.go:64） | ✓ | ✓ |
| analytics | 6/2 | 1 | **✗ v5.11.0 已安全** | ✓ | ✓ |
| orchestration | 7/3 | 1 | ✓ v5.7.3（pgstore/queue.go:477） | ✓ | ✓ |
| broker | **3/2** | 1 | ✓ v5.7.3（ackstore/pg.go:68 Reserve） | **✗ 无 http2 调用路径** | ✓ **v0.21.0 最旧** |
| contracts | **0** | **0** | 无 pgx | 无 | 无 |
| ui | npm **5 high** | 1 | — | — | — |

**可利用性如实评估（不夸大）**：pgx SQLi 触发需查询含 dollar-quoted 字面量与 $N 占位符混淆，各仓运行时 SQL 均静态参数化，**实际暴露面低**；HTTP/2 四项服务端 DoS/崩溃类，本部署全回环单用户明文 HTTP/1.1 为主暴露有限。**定 High 的理由 = SQLi 类公告 ×7 仓符号可达 + 修复 trivial + 已知不修**，而非「正在被打」。按供应链卫生处置，不因「难利用」搁置。

### 已通过项（正证据，不立案）

- **S-1 鉴权 fail-closed 启动闸 ✅**：全部服务有 kit DecideStartup 闸；开放访问仅限回环/显式 loopback-published。「无 JWT_SECRET=全开放」部分证伪。
- **S-4 注入面 ✅**：参数化查询 + quoteIdent（recon/pg_reader.go）；9 仓 SQL 拼接 sweep 干净。
- **S-5 秘密泄漏 ✅**：无硬编码凭证；.env* 未跟踪；env-only 签发。
- **S-7 promote 审计 ✅**：X-Actor fail-closed + 审计写失败响亮（strategy api.go:240-309）。
- **R-3 出站超时/重试 🔶**：kit 重试语义健全；risk 远程回落恒死 = dedup CORE-RISK-REMOTE-FALLBACK-DEAD；AI 反代无 Timeout（SSE 刻意，观察项）。

### 前提订正（W5 累计 6 条）

1. **R-2**：AGENTS「停库→恢复自愈演练」= PG 可用性自愈（503→200 同进程），**≠ 进程优雅停机**；4 服务真缺信号处理（计划原以为演练已覆盖）。
2. **S-1**：「无 JWT_SECRET=全开放」部分证伪——DecideStartup fail-closed 闸全服务存在。
3. **V-2**：kit lag = **6 仓**（agent/data/strategy/risk/analytics/orchestration 仍 v0.2.0，core 已 v0.3.0；broker 不用 kit），非计划写的 7。
4. **S-6/V-1**：analytics pgx v5.11.0 **已安全**——三档分叉里最高档恰是安全档，收敛方向明确。
5. **R-4**：ADR-027/029「request-id 已跨服务传播」在安装层面被证伪（机制有、入站零安装）。
6. **broker 漏洞比预期轻**：3/2 而非 7/3（无 x/net/http2 调用路径）；但 x/text v0.21.0 全组最旧。

### 待授权腿（A4 已授权，施工前取证）

- **S-2 live curl**：起服务实测未鉴权端点可达性矩阵（含 strategy 10 条公开读路由、broker 写面关断验证）。
- **R-2 SIGTERM 演练**：四服务 kill，验证 data running 孤儿 + strategy 编译子进程 orphan 假设（破坏腿，假设待实测确认不作已证事实）。

## Consequences

**Positive**:
- 依赖供应链修复链（kit 先行发版 → 7 消费仓 bump + broker 直 bump + ui npm fix）一次性消 10 仓漏洞 + 收敛 pgx 三档分叉；
- 宿主 PG 备份/恢复演练（I-5）补齐后，不可重建的实验资产（ai.experiments/promotions/risk 规则）有异盘副本兜底；
- correlation-id 真接线（stdlib 版 + 六仓安装）后 ADR-027/029 断言成立，跨服务排查有 trace 坐标。

**Negative**:
- pgx v5.7→v5.11 行为差异需各仓测试腿背书，risk stdlib 驱动与其余 pgxpool 不同路径，收敛有回归风险（须 _test 库腿）；
- 备份演练只恢复到 _test 库（不碰生产），真灾难恢复路径在演练成文前未验证；
- request-id 的 span/trace 树仍按 ADR-017:146-149 重开条件挂起，本波只做 correlation-id 不做完整 tracing。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-072 行）
- 立单（六字段）：
  - `tellurion-kit:docs/TASKS.md` — KIT-DEP-SECURITY-BUMP [P0] / KIT-REQUESTID-STDLIB [P1]
  - `tellurion:docs/TASKS.md` — CORE-PG-BACKUP-DR [P0] / CORE-CI-IMAGE-GATE [P2]
  - `tellurion-data/risk/analytics/strategy:docs/TASKS.md` — *-GRACEFUL-SHUTDOWN [P1]
  - `tellurion-broker:docs/TASKS.md` — BROKER-DEP-BUMP [P0]
  - `tellurion-ui:docs/TASKS.md` — UI-NPM-AUDIT-FIX [P0] / UI-HEALTHCHECK [P3]
  - `tellurion-analytics:docs/TASKS.md` — AN-READYZ-PROBE [P3]
  - `tellurion-docs:docs/TASKS.md` — DOC-ADR-REQUESTID-CORRECTION [P2]（adr-027/029 加更正注记，不改写原文）
  - 跨仓批 X-DEP-BUMP-CONSUMERS [P0]（7 消费仓 bump kit pin + govulncheck 复核 + AGENTS §4 同步）
- adr-027:1314-1316 / adr-029:126-127/:448 加更正注记「机制已有、接线未落」（ODR 只增不删，不改写已 Accepted 决策）
- dedup 命中只补证据：CORE-RISK-REMOTE-FALLBACK-DEAD ⏸（legacy :8083 vs 今 :8089，三回落 rm==nil 恒不可达）

## Metrics

- W5 发现 **7 项**（**High 2**〔F1 依赖/F4 备份〕/ Medium 2〔F2 停机/F3 request-id〕/ Low~Med 1〔F5 镜像〕/ Low 2〔F6 探针/F7 凭证〕）
- 判定表覆盖 S-1~S-7 / R-1~R-5 / V-1~V-3 / I-5 共 16 项；✅ 5（S-1/S-4/S-5/S-7 + R-3 健全）/ ✗ 4（S-6/R-2/R-4/I-5）/ 🔶 余
- govulncheck E1：10/12 仓 EXIT=1，contracts 唯一 EXIT=0；ui npm 5 high
- 前提订正 6 条

## Lessons Learned

1. **「难利用」不是「不修」的理由**：pgx SQLi 实际暴露面低（静态参数化），但修复 trivial（依赖 bump）+ 已知不修 = 供应链卫生债。定 High 按「符号可达 × 修复成本 × 已知不修」，不按「正在被打」。
2. **机制存在 ≠ 已接线（R-4 同型）**：request-id 中间件定义齐全、出站管道有，但入站零安装 ⇒ 跨服务传播今天不成立。ADR 断言「已传播」被安装层面证伪——文档断言要用 grep 安装点核验。
3. **可用性自愈 ≠ 优雅停机**：AGENTS 的「停库→恢复演练」是 PG 可用性（503→200），不是进程 SIGTERM drain。两个可靠性维度不互相覆盖，计划前提须订正。
4. **不可重建数据无备份 = 单点抹掉全部劳动产物**：market.* 可重拉（但配额昂贵），ai.experiments/promotions/risk 规则是人力/AI 劳动产物外部源不可重建。单副本+无备份是 High，不是 Low。

## 订正注记（2026-11-11，W7 台账立单时实测发现）

> ODR 只增不删：本节为追加注记，**不改写**上文已 Accepted 的 W5-F6 判定行；原行保留作历史，归属以本注记为准。

- **W5-F6 探针归属订正（analytics → strategy）**：上文 W5-F6 行与 Artifacts 把 `nc -z 127.0.0.1 8090` 弱探针记为 **analytics**，并据此派 `AN-READYZ-PROBE`。W7 立单时逐行核 core 统一 `docker-compose.yml` 实测：`:463-486` 是 **strategy** 服务（`command -addr 0.0.0.0:8090`、端口 `8090`），其 healthcheck `:480-481` 才是 `nc -z 8090`；**analytics** 服务在 `:488-519`，healthcheck `:515-516` 已是 `curl -fsS http://127.0.0.1:8087/healthz`（HTTP，非 TCP）。弱探针的真实落点是 strategy 自证资产：`tellurion-strategy:Dockerfile:40-41`（`HEALTHCHECK ... nc -z 8090`）+ `deploy/compose.yaml:28-29`，core 统一 compose 镜像了同一行。
- **处置**：撤销 `AN-READYZ-PROBE`（前提被源码证伪，analytics 无需改）；改立 `STRAT-READYZ-PROBE [P3]`（`tellurion-strategy:docs/TASKS.md`），core 统一 compose `:480-481` 的同步行归 core。W5-F6 的另一半 `UI-HEALTHCHECK [P3]`（ui Dockerfile 无 HEALTHCHECK）不受影响，仍成立。W5 发现总数与严重度不变（仍 7 项 / Low 2），仅 F6 的仓归属订正。
- **教训补**：判定表里的 `文件:行号` 在派工前必须按**服务边界**复核——compose 里相邻服务的 healthcheck 行号极易串位（8090=strategy / 8087=analytics），端口号是比行号更可靠的归属锚。