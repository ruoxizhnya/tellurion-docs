# ADR-033: 执行载体的落地顺序 —— M0 市场级先行 · abi v2 混合实例模型 · 提交边界固化 hash（原 ADR-D25）

> **Status**: **Accepted**（原 ADR-D25，若曦裁决；2026-10-22 由 DOC-09 升格归档于此）
> **Date**: 2026-10-19（裁决，与 D24 同轮）／2026-10-22（升格）
> **Category**: Architecture
> **Related**: [ADR-024](adr-024-expression-as-execution-target.md)（执行载体是表达式，LLM 生成的代码只是 artifact）· [ADR-028](adr-028-tiered-extension-of-strategy-expression-capability.md)（表达力分层）· [ADR-029](adr-029-ai-layer-2026-agent-practice-alignment.md)（其 §3 修订草案是本条的正式载体）· [ADR-032](adr-032-module-topology-and-coarse-grained-edge.md)（第 3 条「先资产后运行时」是 D24 的裁决，本单是它的顺序）· [ADR-031](adr-031-kernel-pluggable-nt-ready.md)（K9 四契约与内核可插拔）
> **核对（last-verified 2026-10-22）**：与 [ADR-029](adr-029-ai-layer-2026-agent-practice-alignment.md) 的升格状态逐条对齐 —— **D25 未被 ADR-024 取代也未被改写**（024 只管 `.so` 那一支的口径，见 core `README.md` 的适用范围注）；host 函数数量的现行数是 **12（v1 8 + v2 4），不是 13**（2026-10-21 订正）。

## Context

策略这条线已经有了执行载体的裁决（表达式，不是 LLM 生成的 Go 代码），但**落地顺序**没有定：
市场级（一次 `on_bar` 喂全市场）与单标的级（逐票喂）是两种不同的 host API 形状，选错顺序会把第一版 ABI 做成需要立刻破坏性重做的形状。

实测压力来自一个具体数字：市场级一轮 `on_bar` 调用量是 **727 次**（M0 场景），而逐票展开是它的 N 倍。这不是性能偏好，是 ABI 形状的决定性证据。

## Decision

三条，顺序是承重结构：

### ① J —— M0 市场级先行，混合为目标

**第一版（M0）做市场级：一次 `on_bar` 携带全市场截面**。目标态是市场级与单标的级混合。

> **不要颠倒顺序**（core `implementation-plan-mvp.md` 明文：「M0 先做市场级是 D25 的裁决」）。
> 颠倒的代价不是重写代码，是把 ABI 的破坏性变更推迟到已有策略资产落库之后 —— 那时它的影响面是库里的每一条策略。

### ② I —— abi v2 采用混合实例模型

- 取数签名：`get_bar(symbol_idx, t_offset, field_id)`；
- 作用域字段：`scope: market | symbol`；
- **未知值 fail-closed**：不认识 `scope` / `field_id` 的输入当场拒绝，不猜默认值（「缺失 ≠ 一个看起来合理的值」）；
- **破坏性变更只做一次**：abi v2 是把 v1 的形状一次性改对的那一版，之后不再允许同类重排。

现行数量口径：**host 函数 12 个 = v1 的 8 个 + v2 新增 4 个**。历史文档里出现过 13 这个数，2026-10-21 回源码核对后订正为 12（订正同时落在 core `repo-topology-and-naming.md` 与 contracts 仓 `docs/API.md` 的偏差登记里）。升格时**不得照抄 13**。

### ③ B —— `latest` 语法糖 + 提交边界固化 hash

策略里可以写 `latest`（取最新可用值），但**提交时把解析结果固化成 hash**：执行的是固化后的引用，不是每次重算的相对名。
内容寻址标识（`strategy_ref` / `artifact_hash` / `run_spec_hash`）**自带版本语义、不参与 semver**（口径见 contracts 仓 README 的版本规则）。

## Consequences

**正面**

- 第一版 ABI 就按最贵的形状（市场级）设计，后面加单标的级是加作用域而不是改签名。
- `scope` / `field_id` 的 fail-closed 让「用错字段」在加载期就报错，而不是产出一份看起来正常的错结果。
- 提交边界固化 hash 让复现性成为结构性保证：同一条意图 → 同一个 `artifact_hash` → 同一个结果。

**负面 / 代价**

- 市场级先行意味着 v1 的单标的写法要经历一次破坏性 ABI 变更（本条刻意把「只做一次」放在这里，代价是显式的）。
- `latest` 的糖衣有漂移风险：解析发生在提交期，若上游数据在提交与执行之间补录，固化的是「当时的最新」而不是「真实最新」——这是刻意的取舍（可复现优先）。
- 本条的正式载体是 [ADR-029](adr-029-ai-layer-2026-agent-practice-alignment.md) §3 的**修订草案**，该草案至今仍是「未升格」状态；本 ADR 记的是顺序裁决，不替代那份草案的内容。

## 不做（明确排除）

- 不借本单升格 ADR-029 的修订草案（那是另一条决定，状态照旧）。
- 不改执行载体裁决（表达式仍是执行目标，见 [ADR-024](adr-024-expression-as-execution-target.md)）。
- 不在本 ADR 里定 WASM host 的实现细节与 abi 逐函数表（源文在 core 的 kernel / protocol 设计集）。
- **`.so` 口径不属于本单**：D3 / D6 / D12~D17 那一批才是 ADR-024 管的 `.so` 一支。

## 出处

- core：[`docs/design/qt-decoupling/project-engineering-file.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/project-engineering-file.md)（ADR-D25 节，J / I / B 三条）
- core：[`docs/design/qt-decoupling/implementation-plan-mvp.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/implementation-plan-mvp.md)（「M0 先做市场级是 D25 的裁决，不要颠倒顺序」）
- core：[`docs/design/qt-decoupling/p0-remediation-design.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/p0-remediation-design.md)（D1 对齐与 A2/A3 前置）
- core：[`docs/design/qt-decoupling/repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md)（host 函数 12 个的订正落点）
- 本仓：[ADR-029](adr-029-ai-layer-2026-agent-practice-alignment.md) §3（本条的正式载体是其修订草案）
- core（修订草案本体，**不在本仓**）：[`docs/design/qt-decoupling/adr-029-amendment-host-api-v2.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/adr-029-amendment-host-api-v2.md) —— `:155` 给出 12 个函数的枚举（8 个 v1 + `get_bar2` / `get_series_len2` / `get_date2` / `emit_target2`），`:156` 是 2026-10-21 那条「原写 13、枚举实为 8+4=12」的订正，代码侧判据是 `contracts.HostFnCount()`（返回枚举结果而不是文档字面数）
