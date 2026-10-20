---
status: evergreen
last-verified: 2026-10-20
verified-by: 2026-10-20 拆仓后重构导航：新增 SYSTEM-DESIGN / REPO-MAP / SERVICE-INDEX 三份总体层索引；ARCHITECTURE 降级为历史 Reference；跨仓链接改绝对 URL（同批修 153 条）
---

# Quant Lab 文档入口

> **这是文档的唯一入口。** 所有其他文档通过本页导航，本页不复制其他文档的内容。

---

## 一句话

自托管的 A 股量化研究平台。**AI 是操作回测底座的实验员，人是实验室主任**——AI 负责试错，人负责判断。

---

## 总体层三份（先看这个）

| 我想…… | 读这个 |
|---|---|
| 理解**整个系统怎么设计**、四条主链路、边界原则 | [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md) |
| 查**哪个仓管什么、拥有哪块数据、依赖谁** | [REPO-MAP.md](REPO-MAP.md) |
| 判断**某功能该放哪个仓** | [SERVICE-INDEX.md](SERVICE-INDEX.md)（每仓 db/api/dataflow 直达） |

> 这三份是**索引与结构**，不含实现细节；实现细节在各仓 `docs/` 里，本仓不复制。

---

## 我该读哪一份？

| 我想…… | 读这个 | 状态 |
|---|---|---|
| 了解这个产品是什么、为谁做 | [PRODUCT.md](PRODUCT.md) | 待按新定位重写 |
| 了解设计原则 | [VISION.md](VISION.md) | 待重写（74KB 原文见 `archive/VISION-full.md`） |
| 了解系统怎么搭 | [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md) → 细节查 [ARCHITECTURE.md](ARCHITECTURE.md) | **SYSTEM-DESIGN 现行**；ARCHITECTURE 是**拆仓前历史 Reference**（端口/表数已失效） |
| 后端架构设计蓝图（模块化内核） | `tellurion:docs/design/kernel/`（kernel-pluggable-nt-ready.md → 已升格 [ADR-031](adr/adr-031-kernel-pluggable-nt-ready.md)） | Draft（D1–D5 已拍板；ADR-031 已 Accepted） |
| 解耦与模块化重构设计集（ADR-D1~D30） | `tellurion:docs/design/qt-decoupling/`（先读其 [README 索引](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/README.md)） | **部分已裁决**：D24/D25/D26/D28 已由用户拍板，**D29（分仓拓扑）与 D30（仓清单与命名）已裁决**，其余仍为草案。**引用任何 ADR-D 编号前先查索引**；正式升格走本仓 ADR-NNN（先例：kernel 蓝图 → ADR-031） |
| **仓清单与命名（ADR-D30，施工前必读）** | `tellurion:docs/design/qt-decoupling/repo-inventory.md` | **已裁决**——项目定名 **tellurion**、owner 保持 `ruoxizhnya` 不变、**应用/服务用单段短名 / 库用全名**、12 仓表 + 旧→新映射；**建新仓 / 改 `go.mod` 前先读**（工单 QT-60，未启动） |
| **分仓拓扑与命名（施工前必读）** | `tellurion:docs/design/qt-decoupling/repo-topology-and-naming.md` | **已裁决**——仓=模块/服务、跨仓只认 tag、`domain` 并入 contracts 仓、S0~S3 迁移阶梯；**动 `go.mod`/建新仓前先读** |
| **各仓功能边界（判断功能放哪）** | 本仓 [SERVICE-INDEX.md](SERVICE-INDEX.md) → 逐仓 `db-schema` / `api-schema` / `dataflow` | 现行（10 仓已建三份契约） |
| **P0 修复基线（实施前必读）** | `tellurion:docs/design/qt-decoupling/p0-remediation-design.md`（第一轮 20 项）+ `p0-round2-review.md`（第二轮：闭环核对 + N1~N9） | **现行基线**——两份合起来才完整；依赖顺序以 round2 §4 为准（wave-0 契约冻结在最前） |
| 查 API / 数据模型 / 契约 | [SPEC.md](https://github.com/ruoxizhnya/tellurion/blob/main/docs/SPEC.md) | 现行（Reference 类，可长） |
| 查某个架构决策的来龙去脉 | [ADR.md](ADR.md) → [adr/](adr/) | 现行（18 条） |
| 了解测试策略 | [TEST.md](TEST.md) | 现行 |
| 看阶段规划 | [ROADMAP.md](ROADMAP.md) | 现行 |
| 本地起步（环境 / 命令 / 已知坑） | [guides/local-dev.md](guides/local-dev.md) | 现行 |
| NT 侧车运维（版本升级 / 故障回退） | [guides/nt-sidecar-operations.md](guides/nt-sidecar-operations.md) | 现行 |
| 加数据源 / 加因子 / 跑一轮实验 | — | 待补（S1 / S3 开工前再写） |
| 实盘接口（核心抽象实盘-ready，仅 paper 实现） | [live-trading.md](https://github.com/ruoxizhnya/tellurion/blob/main/docs/live-trading.md) | 已标注 |
| **当前在做什么** | [TASKS.md](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) | 现行（只放未完成项） |
| 找历史记录 / 旧决策 / 取证报告 | [archive/](archive/) | **只读，不维护** |

**新来的人读这份顺序**：PRODUCT → ARCHITECTURE → SPEC。三份读完就能上手。

---

## 文档治理规则

**R1 · Frontmatter 强制**
每份文档顶部必须写 `status` / `last-verified` / `verified-by`。
**没有 `last-verified` 的文档 = 已腐烂**，可读但不可信。

**R2 · 状态只有三种**

| status | 含义 | 规则 |
|---|---|---|
| `evergreen` | 长期有效 | 随代码更新，`last-verified` 必须跟着走 |
| `active` | 当前进行中 | 完成即转 `archived` |
| `archived` | 历史快照 | **只读、不改、不进本页导航** |

**R3 · 常青层字数上限**
PRODUCT ≤3 页 / VISION ≤2 页 / ARCHITECTURE ≤5 页 / ROADMAP ≤2 页 / TASKS ≤5 页。
超限 → 细节外移到 `design/`。

**R4 · 何时该写 ADR**
只记「**高架构显著性 + 高撤销成本**」的决策。其余写进 git commit message。
判断测试：**半年后如果有人问"为什么当初这么选"，答不上来，才需要 ADR。**
不写 ADR 的情形：只是细节设计、只是规范策略、没有真实可行的备选方案。
被取代的 ADR 移入 `archive/superseded-adr/`，不在 `adr/` 保留。

**R5 · 文档必须可被验证**
CI 扫描常青文档里引用的文件路径、API 路径、表名、配置项，验证其真实存在。
**这是文档不腐烂的唯一可靠机制。**（当前 CI 缺失，见 TASKS.md P0）

---

## 归档层说明

`archive/` 下是历史记录，**只读，不维护，不进导航**，仅供参考与溯源：

| 目录 | 内容 |
|---|---|
| `archive/odr/` | ODR 001–064（实施与取证记录，与 git log 重复） |
| `archive/superseded-adr/` | 已被取代的 ADR 009/010/012/021 |
| `archive/TASKS-history.md` | 旧任务文档（217KB，含 Sprint 1–6） |
| `archive/VISION-full.md` | 旧愿景文档原文（74KB） |
| `archive/RESEARCH-equitydeep-legacy.md` | EquityDeep 旧详案（定位已变更） |
| `archive/2026-Q2/*` | 早期报告、计划、调研 |

---

## 维护本页

新增常青文档时，必须在上方导航表加一行。
文档进入 `archived` 状态时，必须从导航表移除。
