# ADR-040 · 风控快照形状的唯一真相：`contracts/risk`，risk 服务只留策略

- **Status**: Accepted
- **Date**: 2026-11-11
- **Deciders**: 主任（授权本轮按限界上下文 / DDD 判定）
- **Related**: CT-03（快照形状迁 contracts）、ADR-034 C1~C5（契约纪律）、ADR-036（服务拓扑）、`tellurion-docs:docs/design/ddd-boundary-review-2026-11-11.md` C5/D3

---

## 1. 背景与问题

`Snapshot` / `SnapshotRule` 在 `tellurion-contracts/risk/snapshot.go` 与 `tellurion-risk/internal/rule/snapshot.go` 各有一份，`Scope` / `RuleType` 也各有一份；四个跨仓哨兵在 `contracts/risk/errors.go` 与 `risk/internal/rule/errors.go` 文案逐字相同。合约侧注释写明这是 CT-03 的搬运，且**刻意不迁** `Bundle` / `ParseBundle` / `ForScope`（服务策略）。

风险不在「今天形状不同」，而在**两份定义会各自演进**：任何一侧改字段、改编码、改词表，另一侧不会红。

## 2. 决策

**D1 · 唯一真相 = `contracts/risk`。** 范围（CT-03 已落）：

- 形状：`Snapshot`、`SnapshotRule`、`Scope`（含 `ProcessLevel`）、`RuleType`；
- 编码：`Snapshot.Hash()` / `Verify()` / `Clone()`；
- 跨仓哨兵：`ErrInvalidRuleType` / `ErrInvalidScope` / `ErrInvalidParams` / `ErrSnapshotMismatch`。

**D2 · risk 服务保留私有（不进契约）：** `Bundle`、`ParseBundle`、`ForScope`、参数字典、默认值填充、审批状态机、pgstore 读写。理由是它们带 decode、默认值与进程内索引，属**服务策略**；把它们搬进 contracts 会让契约包变成实现包（违反 ADR-034 的「零实现」）。

**D3 · risk 侧改为引用而非复制。** 迁移形态：

- `internal/rule` 里的 `Snapshot` / `SnapshotRule` / `Scope` / `RuleType` 改为 contracts 的**类型别名**（不是复制字段集）；
- 四个哨兵改为 contracts 哨兵的别名（`var ErrInvalidParams = contractsrisk.ErrInvalidParams`），保证 `errors.Is` 跨仓成立；
- `SnapshotHash(rules)` 退化为薄封装（调用 `contractsrisk.Snapshot{Rules: rules}.Hash()`），不再自带一套编码；
- `Bundle` / `ParseBundle` 保留在本仓，`ParseBundle` 仍用 `DisallowUnknownFields` 解 contracts 的 `Snapshot`。

## 3. 迁移代价（明写）

| 项 | 代价 |
|---|---|
| 代码面 | `internal/rule` 与 `pgstore` 共 91 处 `Snapshot`/`SnapshotHash`/`ParseBundle` 引用（2026-11-11 grep 计数），以别名承接后**大部分无需改类型**，但要逐处确认没有依赖本仓私有方法 |
| 依赖面 | risk `go.mod` 从「零 import contracts」变为 require contracts（版本取当时最新已发布 tag）；这是 ADR-034 允许的边，不算破例 |
| 行为面 | **零数据迁移、零 hash 变化**：wire 形状与编码逐字节相同（`contracts/risk` 的 `DomainSnapshotHash` 与 `canonicalParams` 已按 risk 搬运），历史 `risk_rules_hash` 全部继续有效 |
| 测试面 | 现有 `snapshot_test.go` / `params_test.go` 的快照断言直接复用；新增一条「同一 fixture 两侧 hash 同值」的对拍腿 |

## 4. 验收

1. `tellurion-risk`：`gofmt -l` 空、`go build ./...`、`go vet ./...`、`go test ./... -count=1` 全绿；`go.mod` 出现 contracts require 且无 `replace`。
2. 对拍：真栈固定快照的 `risk_rules_hash` 与迁移前**逐字节一致**（本机基线 `84a95d7d…`，以 `tellurion:CORE-COMPOSE-UNIFY` 施工记录里的值为准）；`contracts/risk` 的 `snapshot_test.go` 与 risk 侧同一 fixture 产出同一 hex。
3. 破坏验证：临时把 `contracts/risk` 的 `DomainSnapshotHash` 改一个字符 ⇒ 两侧对拍同时红；还原复绿。这证明两侧确实共用一份编码，而不是各留一份。

## 5. 否决的候选

- **不迁，声明 risk 私有**：两份字段集会继续各自演进，且哨兵文案已经靠人工保持一致；治标不治本。否决。
- **把 `Bundle`/`ParseBundle` 一起搬进 contracts**：契约包会带 decode、默认值与索引，破坏「contracts 零实现」的边界（ADR-034）。否决。
- **在 contracts 里再包一层 risk 专用 DTO**：多一层无收益的映射，且会让 hash 编码出现两条路径。否决。

## 6. 退出 / 重开条件

- 本迁移**无外部前置**，可在任一常规发布窗口执行；不涉及柜台、密钥或产品取舍。
- 若迁移过程中发现 `contracts/risk` 与 risk 侧存在**编码不一致**（对拍红），先修 contracts 再迁移，且必须新立 ADR 说明历史 hash 是否作废；**不允许**为了迁移顺利单边更新对拍基线。

## 7. 不在本 ADR 范围

- 规则定义/审批/审计的业务语义（risk 自持）；
- core 的进程内裁决（`pkg/risk`，已消费 contracts/risk）；
- 下游 `contracts` 版本 pin 的推进顺序（见 `tellurion-docs:docs/REPO-MAP.md` 的「版本 pin 的推进顺序与前置」）。
