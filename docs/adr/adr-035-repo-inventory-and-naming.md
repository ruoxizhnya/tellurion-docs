# ADR-035: 仓清单与命名 —— 项目定名 `tellurion`、应用短名 / 库全名、12 仓表与 M5 对账（原 ADR-D30）

> **Status**: **Accepted**（原 ADR-D30，若曦裁决；2026-10-22 由 DOC-09 升格归档于此，并把本轮待裁决 **A / D / E / F / G / H** 的处置作为附录写入本单——它们里最重的一条（D）正好决定「不建第 13 仓」，与本单同域）
> **Date**: 2026-10-19（裁决）／2026-10-22（升格 + 附录）
> **Category**: Architecture
> **Related**: [ADR-034](adr-034-repo-topology-and-ladder.md)（D29，拓扑与阶梯）· [ADR-032](adr-032-module-topology-and-coarse-grained-edge.md)（D24，跨进程边界）· [ADR-027](adr-027-modular-decomposition-to-independent-services.md)（服务口径，§2.6.4 服务数 3→5）· [ADR-033](adr-033-carrier-order-m0-market-first.md)（D25，策略线顺序）
> **核对（last-verified 2026-10-22）**：① 命名规则已替代 D29 §4 的 `quant-trading-*` 一套；② M5 对账已结案（2026-10-21，结论在 core `repo-inventory.md` §1.2）；③ 12 仓远端已建并 push（2026-10-20 14:10）；④ **可见性仍是 12 仓全 public**，转私有的 `GOPRIVATE` 前提已在 contracts / kit 两仓 AGENTS 各写一行（CT-02 ③-④ / QT-07 ③-S2-c）。

## Context

拆仓前有两个必须先钉死的名与实的问题，晚钉的代价都比早钉大：

1. **module path 的形状不是风格问题**。Go 要求「首段含点」才能被别的仓 `require`——项目短名 `tellurion` 作为应用 module 是特性（**它让任何仓都无法 import core 的实现包**），作为库 module 是缺陷（谁都 require 不到）。这两个身份必须在名字层面分开。
2. **六个能力边界仓不等于六个进程**。X 线候选是按能力画的，服务拓扑（ADR-027 §2.6.4）是按部署画的，两套口径没对账就升格建仓，会造出一批永远起不来的容器。

## Decision

### 一、命名规则（三条）

| 规则 | 内容 | 理由 |
|---|---|---|
| 应用 / 服务 | **单段短名** module path（如 `tellurion`、`tellurion-agent`） | 编译器**拒绝** `require`（`package tellurion/pkg/x is not in std`）——热路径的实现包在物理上无法被别的仓 import，这是一条护栏不是一个坑 |
| 库 | 全名 `github.com/ruoxizhnya/<仓名>` | 首段含点才可被 require；跨仓依赖只认版本号 |
| owner | 固定 `ruoxizhnya` | **否决换 org**（换 org 要改 12 份 go.mod + 全部远端 + CI secrets，收益是零；D29 §4 的这条结论在改名后仍然有效） |

项目定名 **`tellurion`**（Quant Lab 是产品名，tellurion 是仓族名）；仓清单里每仓一行「管什么 / 不管什么 / 拥有哪个 schema / 依赖谁」。

### 二、12 仓表（现状 + 待建 + 触发式）

| 类别 | 仓 | 今天 |
|---|---|---|
| 已有实现（4） | `tellurion`（core）· `tellurion-agent` · `tellurion-ui` · `tellurion-docs` | 代码已迁，远端已建 |
| 契约 / 工具（2） | `tellurion-contracts` · `tellurion-kit` | 仓与 go.mod 就位；符号待 QT-05 落 |
| 触发式服务（6） | `tellurion-data` · `tellurion-strategy` · `tellurion-risk` · `tellurion-analytics` · `tellurion-orchestration` · `tellurion-broker` | **有仓、有边界、无实现** |

⚠️ **「12 仓是上限 / 当前规划，不是承诺终态」**——这句是本单的承重条款，不得读成「架构就是 12 个仓」。

### 三、M5 对账（六仓 × ADR-027 §2 的服务口径，✅ 2026-10-21 结案）

| 结论 | 内容 |
|---|---|
| 仓 ≠ 进程 | **六个能力边界不等于六个进程**。服务拓扑里（ADR-027 §2.6.4，服务数 **3→5**）只有 `data` / `strategy` 有位置 |
| 四仓现状 | `risk` / `analytics` / `orchestration` / `broker` 今天只到「仓内实现 + core 侧 port」，**容器升格各需一条 ADR**（优先遵守「不同时拆多个服务」） |
| 服务数口径 | 3→5 是**服务数**；7 是 compose 容器数。core README 里那句「5→7」是口径混用，已订正 |
| R1~R6 冲突 | 六处冲突逐条登记在 core `repo-inventory.md` §1.2（升格前必须逐条解，不能带着冲突起进程） |
| 新开三条待裁 | **U6** reduction-service 仓位 · **U7** compliance / alert 归属 · **U8** `factor_hypothesis` owner —— 三条**不阻塞 port 收口，阻塞容器升格** |

编号不回收：U1 已裁、U3 已裁废，历史编号保留（同 ADR 只增不删的规则）。

### 四、远端与可见性

- 12 仓已在 `ruoxizhnya` 下创建并 push `main`（2026-10-20）；建仓脚本 `Workspace/push-tellurion-repos.sh` 幂等可复用。
- 旧仓 archive **⏸ 待确认**（archive 会让旧仓变只读）。
- ⚠️ **可见性：12 仓今天全部 `public`**（建仓脚本默认）。转私有的前提有两条，缺一条都会红：`GOPRIVATE=github.com/ruoxizhnya/*`（绕开 proxy）**加** git 凭证（`GOPRIVATE` 不解决认证，只配它会在 `git ls-remote` 那步 403）。这条已在 `tellurion-contracts:AGENTS.md` §2 与 `tellurion-kit` 各成文一行。

## 附录：本轮待裁决 A / D / E / F / G / H 的处置（裁决日 2026-10-21）

**这一批来自两张设计文档的「待裁决」表**：A~D 在 core `strategy-asset-service-api.md`，E~H 在 core `strategy-source-of-truth-and-cache.md`。
⚠️ 命名撞车警示：`refactor-plan-review-2026-10-20.md` 用的是**另一套字母**（M1~M9 / L1~L7 / C1 / H1~H5），**待裁决 H ≠ 评审的 H1~H5**，引用时务必带出处。

| 项 | 问题 | 处置（2026-10-21 裁决） |
|---|---|---|
| **A** | 策略 artifact 存哪 | **本地栈 PostgreSQL `BYTEA`，上限 8 MiB，超限 fail-loud**（不静默截断、不落本地盘）；保留 `storage='url'` 逃逸阀给外部对象存储 |
| **D** | 策略编译服务放哪 | **`tellurion-strategy:cmd/compiler` 独立进程**；**不建第 13 仓**；需修订 [ADR-027](adr-027-modular-decomposition-to-independent-services.md) §2.6.1。⇒ QT-41b 的 ⛔ 由此解除 |
| **E** | 制品缓存形态 | **内存 LRU + 磁盘内容寻址二级**（key = `artifact_hash`，与 §内容寻址不参与 semver 的口径一致） |
| **F** | 失效与传播 | **TTL 300s + promote 带新 hash**；**不引 webhook / 消息总线**（单人自托管下引入广播机制的代价大于收益） |
| **G** | 内置策略怎么进资产表 | **保留 `init` + 登记 `carrier=builtin`**（不给 builtin 另开一条旁路） |
| **H** | 外部载体的引用 | **纳入同一 `strategy_ref`，按 `carrier` 路由**；外部 hash 的语义单独成文，不混进 builtin/dsl/wasm 那一套 |

**唯一仍未裁**：**C** —— NT 内核是否实现同一 `on_bar` host API。
**不阻塞**：QT-01 已按「Go-only 内核」冻结兜底（修复出处见 core `refactor-plan-review-2026-10-20.md` 的 H5 条）。B 属更早一轮（2026-10-19），已并入 D25（→ [ADR-033](adr-033-carrier-order-m0-market-first.md)）。

## Consequences

**正面**

- 「不许 import core 实现包」从纪律变成编译器行为：短名 module 让越界直接编不过。
- 仓清单 + M5 对账让「拆几个进程」第一次有据可查，也留了明确的出口（12 不是承诺）。
- 附录那六条把策略资产这条线的六个悬项一次性清空，QT-41/41b 的前置随之打开。

**负面 / 代价**

- 命名双轨（应用短名 / 库全名）对外来读者反直觉，必须在每仓 `AGENTS.md` 里解释一遍。
- 「四仓无进程位置」意味着四个仓长期处于「有仓无部署」状态，占位仓的维护成本真实存在（三份契约 + 台账要养）。
- 可见性那一行是**未爆的雷**：今天 public 能用，转私有那天没配 `GOPRIVATE` + 凭证，core 的 CI 与镜像构建会同时红。

## 不做（明确排除）

- 不改 org（结论仍有效，见上）。
- 不在本单写各仓的表结构 / 端点正文（各仓 `docs/` 是真相源，本仓只索引 —— 复制的那一份一定会漂移）。
- 不新建第 13 仓（附录 D 已裁）。
- 不把 U6 / U7 / U8 三条待裁当已定（它们阻塞容器升格，正文在 core `repo-inventory.md` §3.1）。

## 出处

- core（仓清单与命名唯一真相）：[`docs/design/qt-decoupling/repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md) —— §0 命名规则 · §1 12 仓表 · §1.1 远端与可见性 · §1.2 M5 对账 · §3.1 U6/U7/U8
- core（附录 A~D 源问题）：[`docs/design/qt-decoupling/strategy-asset-service-api.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/strategy-asset-service-api.md)
- core（附录 E~H 源问题）：[`docs/design/qt-decoupling/strategy-source-of-truth-and-cache.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/strategy-source-of-truth-and-cache.md)
- core（裁决记录与字母撞车警示）：[`docs/design/qt-decoupling/README.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/README.md) · [`docs/design/qt-decoupling/refactor-plan-review-2026-10-20.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/refactor-plan-review-2026-10-20.md)
