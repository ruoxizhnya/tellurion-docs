# ODR-069: 第五轮全系统审查 · core 架构与契约（W2）

> **Status**: Accepted
> **Date**: 2026-11-11
> **Category**: Audit
> **Related ADRs**: adr-036（六仓服务定性）/ adr-037（factor_cache 归属）/ adr-038（factor_returns/ic_analysis 归 core）/ adr-040（risk 快照别名 contracts）；contracts adr-0002（Config 族边界）/ adr-0004（值对象纯函数）
> **Supersedes**: n/a（承 [ODR-065](odr-065-fullstack-static-review.md) 与第四轮目的对齐审计 2026-10-26；本轮 W2 = D 战略 + C 契约 + I 数据归属，含 W7 收敛期 core CI 基线红取证）

---

## Context

- **本 ODR 范围**: W2 core 架构波（D-S1~S6 上下文映射 / C-1~C6 契约纪律 / I-1~I-2 数据归属与迁移）+ W7 收敛期发现的 core CI 基线红（W7-F1 Doc link / W7-F2 Test 步间歇红）。其余波次见 ODR-068/070/071/072/073。
- **取证纪律**: 同 ODR-068（E1>E2>E3>E4，真退出码，环境降级标注）。W2 主证据 = repoguard 27 文件 **72 PASS / 0 FAIL**（E1，`w2-repoguard.log`）+ 逐条静态抽验（主审对研究 agent 取证逐项复核）。
- **结论反转（放最前）**: W0「基线红名单空」**只对本地工作区门禁成立**；CI 维度 core 基线即红（W7-F1/F2）。本地绿 ≠ CI 绿（QT-01 教训同型：工作区被顺手修过而未提交，CI 判提交内容）。

## Decision

### 主任授权与决策采纳

主任 2026-11-11 批复「所有需要授权的都同意」。本波三条技术岔路按既往约定由审查方实测后直接定并写明代价：

- **D5（W2-F9 risk PG-down 语义）= a 对齐 data 族 503 `dependency_unavailable`**。risk `internal/httpapi/api.go:419-420` classify default→500 internal，与同文档 `api-schema.md:372`「读不到事件→503」自相矛盾（:335 又如实写 500）。**代价**：改 classify 哨兵 + 订正文档两处；收益 = core→risk resolve 腿的重试决策能区分「库挂了（可重试/查 readyz）」与「代码 bug（不可重试）」。落点 RISK-PGDOWN-503 [P2]。
- **D6（W2-F11 stock_fundamentals 归属）= b 低成本止血 + I-1 例外登记 + a 退出任务**。core 建 `public.stock_fundamentals`（DDL owner=core），data 按 `DATA_MARKET_SCHEMA` 前缀读（`internal/store/reference.go:14-16,95`），`DATA_MARKET_SCHEMA=market` 且表未建时 `/fundamental` 500。**这是 data AGENTS §1（G3 段）已如实登记的已知限制，不是暗坑**。实测裁 b：data 读路径对齐到表实际所在的 `public`（读上游不拦，repoguard 允许），立即消 500；**代价** = 与「数据面归 data」大方向暂不一致，须登记 I-1 第二/第三例外并立退出任务（a：随数据面收敛把 DDL+写者搬 data，迁移成本高，不在本轮）。落点 DATA-FUNDAMENTALS-READ-PUBLIC [P2] + DOC-P3-MATRIX-TABLE-GRAIN 登记例外。
- **D7（W2-F5 k8s 清单去留）= a 退役 k8s 目录**。compose 已是唯一主路径（2026-11-11 定案，core AGENTS §5）；k8s 是第四轮审计就点过的无主面（readiness 打 `/api/health` 存活探针，`/readyz` 白建）。**代价** = 删 `deploy/k8s/` 目录（破坏性操作，施工另逐单授权，本 ODR 只记录决策+立单）；收益 = 顺带消 W7-F1 的 2 处 compose-vs-k8s deploy 漂移 + W5-F4「备份只覆盖非活跃面」混淆 + W2-F3 的 redis-deployment.yaml 残留。落点 CORE-K8S-EXIT [P2]。

### 发现摘要（W2-F1~F12 + W7-F1/F2）

| # | 严重度 | 问题 | 证据坐标 | 落点任务 |
|---|--------|------|----------|----------|
| W2-F1 | Medium | kit 无符号级导出面冻结（依赖图底座 breaking 面比 contracts 宽，今天只有 SCOPE 包级+版本矩阵） | kit docs/ 无 API.md/api-surface.txt；tools/ 只有 check_scope+check_release_matrix；对照 contracts 五护栏 | KIT-SURFACE-FREEZE [P1] |
| W2-F2 | Medium | core 无全量 migrate() 双跑重放回归网（机制比前提健全：守卫+哨兵+fail-loud，但重放安全无回归） | `pkg/storage/postgres.go:655-699` migrate() 逐条 Exec 无事务包裹；data_migrations 标记表 :338-341；只有 supply_chain_test.go:274-278 子集双跑；对照 data replay_pg_test.go 三指纹 | CORE-MIGRATION-REPLAY-GUARD [P1，A1] |
| W2-F3 | Medium | Redis 退役不彻底：core 三块死代码 + go.mod 依赖 + k8s 孤儿部署 | `pkg/storage/redis.go:39`/`pkg/trading/redis_order_store.go:24`/`pkg/marketdata/cached_provider.go:47` 零调用方；go.mod:12 go-redis v9.7.3；deploy/k8s/redis-deployment.yaml；wait-for-deps.sh:48 | CORE-REDIS-EXIT [P1] |
| W2-F4 | Medium | broker 静态 Bearer + 读侧免鉴权例外无 ADR 登记（strategy 10 条公开读路由同类） | broker `internal/httpapi/httpapi.go:74-89` requireToken 常量时间比较，空 token→503 fail-closed ✅；读侧 6 端点 :63-68 不鉴权；docs/adr/ 只有 0001/0002/0003 无 auth；strategy api-schema.md:86 成文但无 ADR | BROKER-AUTH-ADR [P2] + STRAT-AUTH-ADR [P2] |
| W2-F5 | Medium | k8s readiness 打存活探针，/readyz 白建（库断不摘流量） | core deploy/k8s/analysis-deployment.yaml readiness+liveness 均 /api/health；data-deployment.yaml 均 /health；三仓 /readyz 已建 k8s 不消费 | D7=a → CORE-K8S-EXIT [P2] |
| W2-F6 | Medium | orchestration 无身份限流、429 无 Retry-After（broker rate_limited 同样不带） | orch internal/httpapi/ 无 limit.go（data/risk/analytics/strategy 四仓均有）；唯一 429=queue_full（api.go:352）不带 Retry-After；broker httpapi.go:253 同 | ORCH-RATELIMIT [P2] + BROKER-RETRY-AFTER [P3] |
| W2-F7 | Low 簇 | dedup 命中 + 命名/分页/死注释残余 | factor.ts:20 死调 410（dedup UI-FACTOR-CITATION-RETIRED）；SaveFactorCacheBatch 零调用（dedup CORE-FACTOR-CACHE-WRITER）；/health vs /healthz 分裂；strategy Dockerfile 退役名；contracts fees 死示例注释；分页 offset 不一致 | X-LOW-CLEANUP [P3] + dedup 补证据 |
| W2-F8 | High→已修 | /api/screen + /api/stocks/count 死链反代，UI 真调、openapi 仍登记、deps_test 钉死 | core handlers_proxy.go:143-155 反代 data 无此二路由；ui market.ts:13,21 真调（Screener+DataQualityPanel）；**主任 8c5272d 已修**（screen 本地供数=裁决⑰姿势、count 派生 502、ingest/raw 410） | CORE-DEAD-PROXY-SCREEN-VERIFY [P1，验证修复] + UI-SCREEN-CONSUMER [P1] |
| W2-F9 | Medium | risk 运行期 PG-down→500 internal，与同文档「读不到事件→503」自相矛盾 | risk api.go:419-420 default→500；api-schema.md:335 vs :372 矛盾；data/analytics 同场景 503 | D5=a → RISK-PGDOWN-503 [P2] |
| W2-F10 | Medium | run.backtest_results 表粒度裁决未进 P3 矩阵 + factor_returns/ic_analysis 行过期 | core backtest_results.go:40 CREATE run.backtest_results（owner=core 裁决 data-service-contract-and-ownership.md:41）；P3 按 schema 粒度（run.*→orch）不符；:43 factor_returns/ic_analysis 仍写 owner=data（ADR-038 已裁归 core） | DOC-P3-MATRIX-TABLE-GRAIN [P2] |
| W2-F11 | Medium | stock_fundamentals 域归属错位（core 建 public，data 按 market 前缀读，已登记已知限制） | data reference.go:14-16,95；data AGENTS §1 G3 段已登记 | D6=b → DATA-FUNDAMENTALS-READ-PUBLIC [P2] + 例外登记 |
| W2-F12 | Low | analytics ErrReportConflict 无 wire 映射漏到 500；contracts 无可重试/终态机器分类 API | analytics errors.go:18 + pgstore.go:126 真使用，classify default→500（report_id 确定性派生实际难触发）；contracts engine/execution_errors.go:20-43 三类语义只在注释 | AN-REPORT-CONFLICT-409 [P3]；机器分类缺口登记不主张现在造 API |
| W7-F1 | Medium | core CI「Doc link check」基线红（归档死链 + deploy 漂移），本地全绿因判工作区 | check_doc_links.py --include-archive EXIT=1：c06770e 归档层级没改（约 17 处 cross-repo-* 缺 ../、../deploy/README.md 应 ../../）+ 2 条失效配置引用；check_deploy_consistency.py EXIT=1：13c4b40 `${DATABASE_NAME:-tellurion}` 参数化 4 处漂移（非真连错库） | CORE-CI-ARCHIVE-LINKS-FIX [P2] + CORE-DEPLOY-DRIFT-PARAM [P2，D7 联动] |
| W7-F2 | Medium | core CI「Build & Test」Test 步红——根因已坐实，非 runner flake | 三段真因：① `9fa052c` 红于 `pkg/alert` 日志汇 DATA RACE（`WebhookChannel.deliver` 与 `AlertManager.Fire` 写同一个 bytes.Buffer）→ `b25fb6a` 修；② `b25fb6a` 红于 `pkg/backtest` 种子 bar DATA RACE（`Load` 浅拷贝 + `Get` zero-copy + `processStockJob` 回写末根 bar）→ `fac3a3f` 修；③ `fac3a3f` 红于 qt31：5ms/call 在 `-race` 构建下前提不成立（插桩放大 wazero 热点）→ `4054f52` **按构建模式分档**（race 50ms / 普通保持 5ms，性能口径不放宽），本地 `-race -count=20` **20 PASS / 0 FAIL**。原「偶发 flake、重跑即绿」判断作废 | CORE-RUNNER-FLAKE-RESIDUAL 已关闭（两个真 race + 一处构建模式预算分档） |

### 已通过项（正证据，不立案）

- **D-S1 上下文映射 ✅**：repoguard 27 文件 72 PASS / 0 FAIL（package_wiring / ai_boundary / backtest_storage_decoupling / strategy_marketdata_isolation / canonical_layer / contract_identity 全绿）；12 仓 ↔ core 33 pkg 映射表见 findings-w2（仪器·计算/运行域/存储装配 + 横切留 core + 六服务自持 schema + shared kernel + generic subdomain）。
- **D-S2 映射模式 ✅**：contracts check_contract_shape 绿（零实现/无 Config 形状/无 DB import）；CT-06-B 把 52 个 core-only 根名迁回（C4 ≥2 使用方规则真在执行）；服务仓零 import core。
- **D-S3 P4 真减负 ✅**：core LOC -9.9%（ODR-068 已记）+ 退役护栏全 PASS（RetiredAITables/NoProductionWrites/StrategyDefinitionsPersistence/WalkForwardReports/LegacyLivePackage/DataPlanePackageDirectory）。
- **D-S6 已裁渗出护栏 ✅**：analytics_impl_freeze_test（ADR-039）+ storage_market_tables_retired_test（裁决⑰ index_daily 例外）PASS。
- **C-1 contracts 五护栏 ✅**：W0 真跑全 EXIT=0（387 符号 / 380 行冻结一致）。**C-2 pin 纪律 ✅**：check_contract_pin 18 腿+9 pin 实扫绿。
- **I-2 迁移机制 🔶→健全**：破坏性语句全有守卫（025 DO 存在性块 / available_date generation_expression 判断 / 065 IF EXISTS / strategy_state PK 按 pg_index 实际列集），fail-loud；缺口仅「全量重放回归网」= W2-F2，非机制缺陷。
- **C-4 错误语义 🔶**：broker 六类/analytics 三态/data 四类/orch 五类 文档↔代码闭合 ✅；缺口 = W2-F9（risk）+ W2-F12（analytics）。
- **C-5 OpenAPI 单一真相 🔶**：embed 直出 ✅ + ui 无副本 ✅；W2-F8 两条死链已被主任 8c5272d 修复（转验证）。
- **I-1 DDL 单 owner 🔶**：全仓扫描各守其 schema ✅；market.index_daily 裁决⑰护栏在 ✅；例外 = W2-F10（run.backtest_results 有裁决未进矩阵）+ W2-F11（stock_fundamentals 错位）。

## Consequences

**Positive**:
- core CI 基线红首次被坐实并拆出三个可施工修复单（归档死链 / deploy 参数化 / Test 步红：两个真 DATA RACE + race 构建预算分档），消除「本地绿掩盖 CI 红」的 QT-01 同型风险；
- Redis 退役收口（死代码+依赖+k8s 残留）与 k8s 无主面退役一并清理，部署面收敛到 compose 唯一主路径；
- kit 导出面冻结补齐后，依赖图底座的 breaking 改动有符号级机器闸（对齐 contracts）。

**Negative**:
- D6=b 是止血而非根治：stock_fundamentals 仍在 core public，与「数据面归 data」大方向暂不一致，须靠退出任务（a）随数据面收敛搬迁，否则例外长期化；
- D7=a 退役 k8s 是破坏性操作，施工前须确认无活跃 k8s 部署（compose 已定唯一主路径，但删目录不可逆，另逐单授权）；
- W7-F2 根因已坐实并修复（`pkg/alert` / `pkg/backtest` 两处真 DATA RACE；qt31 的 5ms 预算在 `-race` 下改为按构建模式分档），不再按「runner flake」挂账。

## Artifacts

- 新增本 ODR
- 更新 `docs/ADR.md` ODR Index（追加 ODR-069 行）
- 立单（六字段，证据坐标抄入 Context）：
  - `tellurion:docs/TASKS.md` — CORE-REDIS-EXIT / CORE-MIGRATION-REPLAY-GUARD / CORE-K8S-EXIT / CORE-DEAD-PROXY-SCREEN-VERIFY / CORE-CI-ARCHIVE-LINKS-FIX / CORE-DEPLOY-DRIFT-PARAM / CORE-RUNNER-FLAKE-RESIDUAL
  - `tellurion-kit:docs/TASKS.md` — KIT-SURFACE-FREEZE
  - `tellurion-broker:docs/TASKS.md` — BROKER-AUTH-ADR / BROKER-RETRY-AFTER
  - `tellurion-risk:docs/TASKS.md` — RISK-PGDOWN-503
  - `tellurion-strategy:docs/TASKS.md` — STRAT-AUTH-ADR
  - `tellurion-analytics:docs/TASKS.md` — AN-REPORT-CONFLICT-409
  - `tellurion-orchestration:docs/TASKS.md` — ORCH-RATELIMIT
  - `tellurion-data:docs/TASKS.md` — DATA-FUNDAMENTALS-READ-PUBLIC
  - `tellurion-docs:docs/TASKS.md` — DOC-P3-MATRIX-TABLE-GRAIN
  - `tellurion-ui:docs/TASKS.md` — UI-SCREEN-CONSUMER
  - 跨仓批 X-LOW-CLEANUP 见 ODR-073 落点
- dedup 命中只补证据：UI-FACTOR-CITATION-RETIRED（factor.ts:20）/ CORE-FACTOR-CACHE-WRITER（SaveFactorCacheBatch 零调用）

## Metrics

- W2 发现 **12 项**（High 1〔F8，已修转验证〕/ Medium 8〔F1/F2/F3/F4/F5/F6/F9/F10/F11 中 9 条 Medium〕/ Low 簇 2〔F7/F12〕）+ W7 收敛期 **2 项**（F1/F2 Medium）
- 判定表覆盖 D-S1~S6 / C-1~C6 / I-1~I-2 共 14 项；✅ 7（D-S1/S2/S3/S6/C-1/C-2 + I-2 机制健全）/ 🔶 6 / ✗ 1（C-5，已修）
- repoguard 72 PASS / 0 FAIL（E1）；core CI 基线红 2 job（E2 坐实 + E1 本地复现）

## Lessons Learned

1. **本地绿 ≠ CI 绿（QT-01 同型复发）**：W0 四检查器本地全绿是因为跑的是工作区且 13c4b40 未入库；CI 判提交内容。推前结论必须在干净 checkout 取（core AGENTS §8.5 规范 2 已写，本轮再次实证）。
2. **参数化与字面比对检查器的口径冲突**：`${DATABASE_NAME:-tellurion}` 缺省展开就是 tellurion（非真连错库），但 check_deploy_consistency.py 按字面比对不展开 shell 默认值 ⇒ 假红。检查器须学会展开 `:-default`，或口径对齐。
3. **机制健全 ≠ 有回归网**：core migrate() 守卫+哨兵+fail-loud 都到位，但「重放安全」本身没有可重复回归测试（QT-82 真库验证是一次性的）。健全机制仍需回归网钉住，否则下次改 DDL 无闸。
4. **已登记的已知限制不是暗坑，但要有退出任务**：stock_fundamentals 错位 data AGENTS 已如实登记，缺的是退出路径；登记+止血+退出任务三件齐才算闭环。

## 订正注记（2026-11-11，W7 台账立单时实测发现）

> ODR 只增不删：本节为追加注记，**不改写**上文已 Accepted 的 W2-F10 / W2-F11 判定行与 D6 裁决；原行保留作历史，施工范围与归属以本注记为准。

- **W2-F11 / D6 被主任「基本面归属裁决」取代（DATA-FUNDAMENTALS-READ-PUBLIC 作废）**：上文 W2-F11 + D6=b 裁的是「data `/fundamental` 兼容读面改读 `public.stock_fundamentals` 止血 + 登记 I-1 跨 schema 例外 + 留退出任务」。W7 立单时按当前源码 + `git log` 实测：主任已用**更干净的归属裁决**取代止血方案——
  - data 提交 **a454726**（`refactor(httpapi): 删除 /fundamental/{symbol} 读面（归属裁决归 core）`，已确认在 main）：`internal/httpapi/server.go:141-143`、`legacy_read.go:23-27`、`policy.go:41` 三处均注明「GET /fundamental/{symbol} 已于 2026-11-12 删除」，data 侧读面**整体删除**，不再需要跨 schema 止血。
  - core 提交 **c85abff**（`feat(analysis): 基本面读面归 core（GET /api/fundamental/{symbol}）`，已确认在 main）：`cmd/analysis/handlers_fundamental.go:42` 注册 `router.GET("/api/fundamental/:symbol", …)`，读面归 core（表 DDL 与唯一读写点本就在 core）。
  - 这比 D6=b 更彻底：不是「data 跨 schema 读 core 的表」，而是「读面直接归表的 owner」，I-1 跨 schema 例外**不再需要**。
- **处置**：`DATA-FUNDAMENTALS-READ-PUBLIC [P2]`（`tellurion-data:docs/TASKS.md`）标 **✅ 作废**（前提被主任归属裁决取代，非本单施工），原六字段保留作追溯、注明不再施工；data frontmatter 同步。W2-F11 的「已登记限制要有退出任务」教训仍成立，只是退出路径由主任的归属裁决直接走通，而非本波的止血单。
- **W2-F10 矩阵粒度收窄（DOC-P3-MATRIX-TABLE-GRAIN）**：上文 W2-F10 指 `run.*` / 因子派生表的 owner 粒度在多份矩阵里不一致。W7 立单时实测：主任已落 **ADR-037 / ADR-038**（factor_cache 无写者 / factor_returns·ic_analysis 派生表归 core），`SYSTEM-DESIGN.md §5` 已对齐，core 侧 `CORE-FACTOR-DERIVED-GUARD` 已 ✅（护栏钉住派生表 owner），`data-service-contract-and-ownership.md:49` 的基本面行已由主任 2026-11-12 订正。**残余只剩两处**：① `tellurion-docs:REPO-MAP.md:24` orchestration 行仍写「`run`（六表）」未显式区分 core 拥有的 `run.backtest_results`（结果面，见 core 矩阵 `:41`）；② core `docs/design/qt-decoupling/data-service-contract-and-ownership.md:43` 仍把 `factor_returns / ic_analysis` 列在「owner = tellurion-data（SPEC-R-02）」，与 ADR-038 冲突。
- **处置**：`DOC-P3-MATRIX-TABLE-GRAIN [P2]`（`tellurion-docs:docs/TASKS.md`）收窄到上述两处残余；其中 ② 是 **core 文件**，本单只登记跨仓指针（`tellurion:docs/design/qt-decoupling/data-service-contract-and-ownership.md:43`），**不从 docs 仓改 core 正文**（归属边界）。W2 发现总数与严重度不变，仅 F10 施工面收窄、F11 转作废。
- **教训补**：裁决（D6）不是终态——主任侧可能用更彻底的归属裁决取代审查时点的止血方案。立单前对每条「待施工」裁决都要按当前源码复核它是否已被上游施工取代；被取代的标作废并留证据，不重复派工，也不静默丢弃原裁决（保留作历史）。

## 订正注记（2026-11-12，I-2 迁移账本事实）

> ODR 只增不删：上文 W2-F2 行的「`migrate()` 逐条 Exec 无事务包裹」是 2026-11-11 审查时点的历史现场，**不改写**；本注记记录其后已落地的事实与本波口述中的一处错误。

- **账本已在且是启动路径**：core 提交 **07411fd**（CORE-MIGRATION-REPLAY-GUARD）已落「逐条迁移一个事务 + 同事务记账」：`pkg/storage/postgres.go:42` 的 `NewPostgresStore` 启动即调 `migrate()`（:679），账本表 `core_schema_migrations(version, checksum, applied_at)` 定义在 `:690`，`planMigrations`（:719）对「指纹不符」与「账本领先于代码」fail-closed 拒绝启动。W2-F2 因此已归档 ✅。
- **本波口述错误，作废**：此前「core 迁移无版本表、23 张表全量幂等重放」的表述**是错的**，以本条为准。实测（一次性 dockertest 容器走生产 `migrate()`）：账本 **85 行 / max(version)=85**，代码序列 `allMigrationStatements()` **85 条**，二次启动 `MAX(applied_at)` 不变（零重放）；「23」是 `postgres.go` 中 `CREATE TABLE` 字样出现的行数，不是迁移条数（迁移序列里以 `CREATE TABLE` 开头的语句为 25 条，其余为索引与 retention DDL）。全量重放只发生在**账本为空的存量库接管**场景，且要求语句幂等，已由 integration 用例覆盖。
- **当前部署库状态（如实）**：宿主 PG 的 `tellurion` 库 `information_schema.tables` 中**没有** `core_schema_migrations`——运行中的 `tellurion-analysis-service-1` 容器 StartedAt `2026-11-12T06:52:15Z`，早于 07411fd（`07:11:01Z`）19 分钟，镜像是账本合入前构建且未重建。该库下次以新镜像启动时会走「存量库接管」：建账并全量重放一次幂等 DDL，此后按账本增量执行。
