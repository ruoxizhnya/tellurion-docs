# ADR-034: 分仓拓扑与 S0~S3 阶梯 —— 仓 = 模块/服务、R1~R6 自治不变量、C1~C5 契约纪律（原 ADR-D29）

> **Status**: **Accepted**（原 ADR-D29；2026-10-22 由 DOC-09 升格归档于此）。§7 的 **S1 形态已被 ADR-D31 替代**（代码直接写进新仓，全程不 `replace`），拓扑 / R1~R6 / S0·S2·S3 / C1~C5 不变。
> **Date**: 2026-10-19（裁决）／2026-10-22（升格）
> **Category**: Architecture
> **Related**: [ADR-027](adr-027-modular-decomposition-to-independent-services.md)（模块化拆解为独立服务）· [ADR-031](adr-031-kernel-pluggable-nt-ready.md)（四契约冻结内核边界）· [ADR-032](adr-032-module-topology-and-coarse-grained-edge.md)（D24，依赖方向的前一版）· [ADR-035](adr-035-repo-inventory-and-naming.md)（D30，仓清单与命名）· `tellurion:docs/design/qt-decoupling/repo-topology-and-naming.md`（源文，唯一拓扑真相）
> **核对（last-verified 2026-10-22）**：① 依赖方向已是订正后的 `kit ← contracts(含 domain) ← core`；② R 系列是 **R1~R6**（源文 README 与部分小节仍写「五条 R1~R5」，那是 2026-10-20 之前的数）；③ C5 的「保留一个版本周期」今天由 contracts 仓 `tools/check_release_matrix` + CHANGELOG 纪律承接（CT-02，2026-10-22）；④ 12 仓已全部建好并 push（2026-10-20），旧仓 archive 仍 ⏸ 待确认。

## Context

拆仓不是把目录搬出去，而是要同时回答四个问题，否则搬完就是四份新的债：

1. **一个仓到底代表什么** —— 一个能力？一个部署单元？一个 Go module？三者今天并不重合。
2. **拆完之后怎么自证** —— 单仓 checkout 编不过，跨仓边界就只是文档上的箭头。
3. **契约怎么演进** —— breaking 变更没有规则，`deprecated` 就永远不可能被删。
4. **什么时候算拆完了** —— 没有阶梯，就会有「为将来可能要拆提前建空仓」和「一步到位全拆」两种失败。

## Decision

### 一、仓 = 模块 / 服务（一个仓只承载一个可独立自证的东西）

- 库仓（`tellurion-kit` / `tellurion-contracts`）= 一个 Go module；
- 应用 / 服务仓 = 一个部署单元 + 一个 module；
- **占位仓的含义：有仓、有边界、无实现**。台账里出现本仓单号之前不要写实现（这条写进每个仓的 `AGENTS.md`）。

### 二、R1~R6 —— 每仓的自治不变量（可机械检查）

| # | 不变量 | 判据 |
|---|---|---|
| R1 | 单仓可构建 | 单独 checkout `go build ./...` 绿 |
| R2 | 单仓可自证 | `go vet` + `go test` 单仓绿，不 checkout 别的仓 |
| R3 | 有 `AGENTS.md` | 入口自洽：构建 / 边界 / 依赖版本 / 禁止项 |
| R4 | 有 `docs/TASKS.md` | 唯一台账；没有单号别开工 |
| R5 | 契约是版本依赖 | 跨仓只认 tag / 伪版本，**禁止仓外 `replace`** |
| **R6** | **功能边界有三份契约** | `docs/db-schema.md` / `api-schema.md` / `dataflow.md`，改代码必须同步（2026-10-20 新增） |

> ⚠️ **两处旧口径不得照抄**：① 「五条 R1~R5」是 R6 加入之前的数；② 2026-10-21 给 core 与本仓加了**豁免 + 声明**（真相由 `openapi.yaml` / `postgres.go` 内联 DDL / `SPEC.md` 承载，不再复制三份契约文件）。豁免是给这两个特例的，不是给新仓的。

### 三、S0~S3 阶梯（拆仓的顺序与收回条件）

| 阶段 | 内容 | 单号 | 收回判据 |
|---|---|---|---|
| S0 | 12 仓建成 + `v0.1.0` tag + `replace` 暂存 + CI 的 `agent-compat` 兜底 | QT-06 / QT-18 / QT-08 | 仓与远端全部就位（✅ 2026-10-20 已 push） |
| S1 | **契约层与工具层代码直接落进两个新仓**（形态由 D31 决定，非原「在 core 内建子 module」） | QT-05（主单落 contracts）/ QT-05-B（kit 腿） | 两仓单 checkout 可构建 |
| S2 | 伪版本 → 真 tag；core / agent 换 `require`；随仓接口规格载体（`API.md` / `SCOPE.md`）与护栏进 CI | QT-07 / QT-09 | `go list -m` 显示 `v0.1.0` 且**无 `=>`** |
| S3 | **agent 删掉 `replace tellurion => ../tellurion`**（唯一允许删它的时点） | QT-50 + QT-17 完成后 | 删掉 replace 后 agent `go build ./...` 仍然绿 |
| （S4） | X 线服务仓从「仓内实现」升格为容器 | QT-40~45 | 各需一条 ADR，见 [ADR-035](adr-035-repo-inventory-and-naming.md) 的 M5 对账 |

合入门禁与冻结纪律随阶梯一起生效：**tag 不 push 等于没发版**；跨仓依赖只认版本号；`go.work` 只作本地联调、不入库。

### 四、C1~C5 —— 契约演进纪律

| # | 规则 | 今天的承接物 |
|---|---|---|
| C1 | 禁止仓外 `replace` | 各仓 AGENTS §3 + CI（唯一过渡例外：agent→core，S3 收回） |
| C2 | `go.work` 不入库 | `.gitignore` + CI 检查 |
| C3 | 契约测试同喂两侧实现 | QT-09 ③-③（未落） |
| C4 | 契约仓 AST 扫描：禁 `Config`/`Options`/`Impl` 命名、禁 DB import | QT-09 ⑤（未落）；本仓导出面核对已由 CT-01 承接 |
| **C5** | **破坏性变更必须保留旧接口一个版本周期**（契约仓保留 `deprecated` 符号至下一个 minor） | 版本规则表 + CHANGELOG + 兼容矩阵（`tellurion-contracts:CT-02` / `tellurion-kit:KT-02`）；机械「禁删 deprecated」护栏仍属 QT-09 ⑤ |

> **为什么 C5 单独说**：它的理由不是洁癖，是「两仓必须同时改才能编译 = agent 无法独立完成」。0.x 阶段允许 breaking，但必须 **bump MINOR + 写 CHANGELOG 条目**；「deprecated 至少留一个 MINOR」这条**只在 1.0 之后启用**。

### 五、依赖方向（本单的最终形态，替代 D24 第 1 条）

```
第三方库
   ↓
 tellurion-kit                 ← 零业务概念，依赖图底座
   ↑（只允许纯工具 decimal/errors）
 tellurion-contracts(含 domain) ← 所有跨边界的类型与 port 只能住这里
   ↑
 tellurion(core)               ← 热路径全在这里，不出进程
   ↑ 编译期（kit + contracts） / HTTP 运行期（粗粒度）
 tellurion-agent
```

反向边（`kit → contracts`、`contracts → core`、任何仓 import core 实现包）命中即红。

## Consequences

**正面**

- 「什么算拆完了」有了判据（R1~R6 + S3 那条判据），不再是主观进度。
- 占位仓有了明确语义：有仓、有边界、无实现，避免 agent 进去凭空造代码。
- C5 有了版本规则承接，`deprecated` 第一次具备「可被删」的条件。

**负面 / 代价**

- 阶梯很长，S3 依赖 QT-50 + QT-17 —— 在那之前 agent 的 R1 恒红，这是**已知过渡态**而不是意外。
- R6 加了三份契约的维护成本（每个仓 ×3），换来的是「PR 里代码动了文档没动该被打回」的可检查性。
- 仓数从 4 涨到 12 的规划与「六个能力边界 ≠ 六个进程」的裁决并存（M5 对账），拓扑短期内既不是 12 也不是 6，读起来别扭但如实。

## 不做（明确排除）

- 不照抄 D29 原文里被 D31 替代的 **S1 形态**（「在 core 内建 `contracts/` `kit/` 子 module，S2 再搬」已作废）与「S1 期 core 有 3 个 go module」。
- 不照抄 D29-1 的「终态 6 仓」——现行是 12 仓**上限 / 当前规划，不是承诺终态**（见 [ADR-035](adr-035-repo-inventory-and-naming.md)）。
- 不在本单写各仓的表 / 端点正文（那是各仓 `docs/` 的真相源，本仓只索引）。
- 不动 `git init` / 迁目录那条老腿（QT-07 ①/② 已随 Plan A 作废）。

## 出处

- core（唯一拓扑真相）：[`docs/design/qt-decoupling/repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md) —— §2 R1~R6 · §3.1 依赖表 · §5 结论 · §7 S0~S3 · §8 checklist · §9 C1~C5
- core（摘要与 D31 状态行）：[`docs/design/qt-decoupling/project-engineering-file.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/project-engineering-file.md)
- core（待裁决与裁决记录）：[`docs/design/qt-decoupling/README.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/README.md)
- 承接物：`tellurion-contracts:docs/API.md`（CT-01）· `tellurion-contracts:README.md` 版本规则（CT-02）· `tellurion-kit:docs/SCOPE.md`（KT-01）
