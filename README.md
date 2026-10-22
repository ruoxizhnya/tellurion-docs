# tellurion-docs — 总体设计知识库

> **这个仓只回答一个问题：整个系统是怎么设计的、边界为什么这么切。**
> 单个服务的实现细节**不在本仓**，在各自的服务仓里；本仓提供索引，不复制内容。

---

## 一、三种读法

| 你是谁 / 想干什么 | 从哪开始 |
|---|---|
| **新接手的 agent**，要知道"我能改什么" | [docs/REPO-MAP.md](docs/REPO-MAP.md) → 找到自己的仓 → 读该仓 `AGENTS.md` |
| **要判断某功能该放哪个仓** | [docs/SERVICE-INDEX.md](docs/SERVICE-INDEX.md) → 看该仓的 `db-schema` / `api-schema` / `dataflow` 三份契约 |
| **想知道某条决策为什么这么定** | [docs/ADR.md](docs/ADR.md)（跨领域）→ `docs/adr/`；单仓决策在该仓 `docs/adr/` |
| **要理解全局架构** | [docs/SYSTEM-DESIGN.md](docs/SYSTEM-DESIGN.md)（现行总体设计） |
| **当前在做什么 / 下一步** | 施工台账在 core：[`tellurion:docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) |

> `tellurion:path` 这种写法表示**另一个仓里的文件**，不可点击；需要点击时用完整 GitHub URL。

---

## 二、十二个仓

| 仓 | 角色 | 一句话边界 | 文档 |
|---|---|---|---|
| [`tellurion`](https://github.com/ruoxizhnya/tellurion) | **core** | 回测引擎 / 策略运行时 / 撮合 / 组合结算 / 仪器域存储 / 内核装配。**热路径全在这里，不出进程** | [docs](https://github.com/ruoxizhnya/tellurion/tree/main/docs) |
| [`tellurion-contracts`](https://github.com/ruoxizhnya/tellurion-contracts) | 库（契约） | 只定义跨边界交换的**形状**：port / DTO / 值对象 / 四契约 / 哨兵错误。**零实现、零 DB** | [docs](https://github.com/ruoxizhnya/tellurion-contracts/tree/main/docs) |
| [`tellurion-kit`](https://github.com/ruoxizhnya/tellurion-kit) | 库（工具） | 横切工具：logging / errors / decimal / statistics / httpclient / httpserver / `auth`+`authz` / observability / clock / sandbox / db。**零业务概念、零表结构** | [docs](https://github.com/ruoxizhnya/tellurion-kit/tree/main/docs) |
| [`tellurion-agent`](https://github.com/ruoxizhnya/tellurion-agent) | 应用（AI） | AI 实验员：探索 / 生成 / pipeline / 工具注册表。**运行期只走 HTTP 调 core** | [docs](https://github.com/ruoxizhnya/tellurion-agent/tree/main/docs) |
| [`tellurion-ui`](https://github.com/ruoxizhnya/tellurion-ui) | 应用（前端） | 只消费 HTTP，**不直连库、不复制 openapi** | [docs](https://github.com/ruoxizhnya/tellurion-ui/tree/main/docs) |
| [`tellurion-data`](https://github.com/ruoxizhnya/tellurion-data) | 服务（触发式） | 数据面唯一入口：connector → 归一化 → 存储 → aggregator；`market` / `ingest` 的 DDL owner | [docs](https://github.com/ruoxizhnya/tellurion-data/tree/main/docs) |
| [`tellurion-strategy`](https://github.com/ruoxizhnya/tellurion-strategy) | 服务（触发式） | 策略**资产**（定义 / 版本 / artifact）；**不计算信号** | [docs](https://github.com/ruoxizhnya/tellurion-strategy/tree/main/docs) |
| [`tellurion-risk`](https://github.com/ruoxizhnya/tellurion-risk) | 服务（触发式） | 规则真相源 + 聚合监控 + 熔断下发；**同步裁决不出仓** | [docs](https://github.com/ruoxizhnya/tellurion-risk/tree/main/docs) |
| [`tellurion-analytics`](https://github.com/ruoxizhnya/tellurion-analytics) | 服务（触发式） | 指标 / 归因 / 敏感性 / 蒙特卡洛，纯函数只读 | [docs](https://github.com/ruoxizhnya/tellurion-analytics/tree/main/docs) |
| [`tellurion-orchestration`](https://github.com/ruoxizhnya/tellurion-orchestration) | 服务（触发式） | job / batch / walkforward 排队与状态机；**只派活不裁决** | [docs](https://github.com/ruoxizhnya/tellurion-orchestration/tree/main/docs) |
| [`tellurion-broker`](https://github.com/ruoxizhnya/tellurion-broker) | 服务（触发式） | 交易通道适配；**无对账 + 幂等 + 熔断就不接真钱** | [docs](https://github.com/ruoxizhnya/tellurion-broker/tree/main/docs) |
| [`tellurion-docs`](https://github.com/ruoxizhnya/tellurion-docs) | 文档 | **本仓**：总体设计 / 跨领域 ADR / 运维指南 / 历史档案 | — |

---

## 三、单一真相源（同一件事只有一处能改）

| 问题 | 唯一真相源 |
|---|---|
| 仓名、module path、谁依赖谁 | [core `repo-inventory.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-inventory.md) |
| 拓扑 / R1~R6 不变量 / 跨仓规则 C1~C5 / S0~S3 阶梯 | [core `repo-topology-and-naming.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/design/qt-decoupling/repo-topology-and-naming.md) |
| 每个仓**拥有哪些表** | 该仓 `docs/db-schema.md`（本仓只索引，不复制） |
| 每个仓**对外什么接口** | 该仓 `docs/api-schema.md` |
| 数据怎么流、哪里 fail-closed | 该仓 `docs/dataflow.md` |
| 施工顺序与在做什么 | [core `docs/TASKS.md`](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md) |
| 跨领域架构决策 | 本仓 `docs/adr/`；单仓决策在该仓 `docs/adr/` |

> **豁免声明（2026-10-21 裁决，豁免+声明）**：`core` 与 `tellurion-docs` 豁免随仓三件薄规格（`db-schema` / `api-schema` / `dataflow`）与 `docs/adr/0001-*` 边界裁决单——API / DB / 流程真相直接由 `tellurion:docs/openapi.yaml` / `tellurion:pkg/storage/postgres.go` / `tellurion:docs/SPEC.md` 承载，详见 [docs/REPO-MAP.md](docs/REPO-MAP.md)。

---

## 四、本仓目录

| 路径 | 内容 |
|---|---|
| [`docs/SYSTEM-DESIGN.md`](docs/SYSTEM-DESIGN.md) | **现行总体设计**：分层 / 四条主链路 / 数据归属 / 边界原则 / 演进阶梯 |
| [`docs/REPO-MAP.md`](docs/REPO-MAP.md) | 12 仓地图：职责 / 拥有 schema / 对外面 / 依赖方向 / 状态 |
| [`docs/SERVICE-INDEX.md`](docs/SERVICE-INDEX.md) | 服务仓功能边界索引（每仓三份契约的直达链接） |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | ⚠️ **历史 Reference**（拆仓前实测），现状看 SYSTEM-DESIGN |
| [`docs/VISION.md`](docs/VISION.md) / [`docs/PRODUCT.md`](docs/PRODUCT.md) / [`docs/ROADMAP.md`](docs/ROADMAP.md) | 愿景 / 产品 / 路线图 |
| [`docs/ADR.md`](docs/ADR.md) + [`docs/adr/`](docs/adr/) | 跨领域架构决策（Accepted 后只读） |
| [`docs/guides/`](docs/guides/) | 本地起步 / 部署配置 / 数据依赖 / NT 侧车运维 |
| [`docs/design/`](docs/design/) | 跨领域功能规格（EquityDeep 等） |
| [`docs/archive/`](docs/archive/) | 历史档案（只读，不维护） |
| [`tools/check_doc_links.py`](https://github.com/ruoxizhnya/tellurion/blob/main/tools/check_doc_links.py) | 链接检查（活跃层必须 0 断链） |
| [`tools/check_repo_docs.py`](tools/check_repo_docs.py) | 12 仓文档齐套巡检（AGENTS / TASKS / 三件套 / adr / odr；core 与本仓按具名豁免） |

---

## 五、维护规则

1. **不复制，只索引**：服务仓的 db / api / dataflow 内容不搬进本仓，只放带绝对 URL 的索引行。
2. **跨仓引用必须是完整 URL**：`../../other-repo/...` 在独立 checkout 时必断（这是拆仓后 153 条坏链的成因）。
3. **`docs/adr/` 与 `docs/archive/` 不改正文**：历史决策保持原样；失效链接由链接检查豁免并计数。
4. **改一处，查一次**：`python tools/check_doc_links.py` 必须在活跃层报 0 断链（CI 同款）。
