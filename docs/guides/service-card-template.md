---
status: evergreen
last-verified: 2026-11-11
verified-by: 首版模板 —— 与 guides/service-card.md 同批；字段注释覆盖"写什么/不写什么"
---

# 服务卡模板（SERVICE.md）

> **用法**：把下面两个代码块依次复制到目标仓根目录的 `SERVICE.md`，替换 `<...>`。
> 写之前先读 [服务卡规范](service-card.md) §5.4 的稳定/易变分界与 §5.5 的五问。
> 目标：**≤ 120 行**、5 分钟读完、正文不出现端口/URL/版本/数量。

---

## 1. Frontmatter

```yaml
---
service-card: 1
# 必填：卡片 schema 版本，当前固定 1

repo: <repo-name>
# 必填：目标仓目录名，必须与目录名一致；不要写 GitHub URL

kind: <service|application|library|frontend|docs>
# 必填：service = 六个能力服务；application = core/agent；library = contracts/kit；
#       frontend = ui；docs = 文档仓

lifecycle: <production|skeleton|suspended|retired>
# 必填：production = 今天有真实实现；skeleton = 有边界无实现；
#       suspended = 主体挂起；retired = 已退役保留仓

owner: <github-handle>
# 必填：决策人 GitHub handle；不写"团队"，不写邮箱

impact: <blocking|degrading|compile-time|none>
# 必填：blocking = 缺它主链路起不来/断；degrading = 局部功能降级；
#       compile-time = 只影响编译；none = 文档或无运行时
# 注意：这是"今天默认部署"的粗判；开关差异写在正文 §6，不要写进这里

requires: []
# 选填：编译期直接依赖的仓名（来自 go.mod）；只写仓名，不写版本
# 例：[tellurion-contracts, tellurion-kit]

required-by: []
# 库仓必填：编译期被哪些仓依赖；服务仓可空
# 只写仓名；用工作区 go.mod 扫描核对，不要手抄版本

calls: []
# 选填：运行期出边（HTTP/其他协议）；只写仓名
# 不写 URL、端口、超时；协议细节写在正文 §3

called-by: []
# 选填：运行期入边；只写仓名
# 不写调用方版本；失败影响写在正文 §3

truth:
  readme: README.md
  agents: AGENTS.md
  architecture: docs/ARCHITECTURE.md
  api: docs/api-schema.md        # contracts 用 docs/API.md；core 用 docs/openapi.yaml
  db: docs/db-schema.md          # 无表可写 null；core 可指向 docs/SPEC.md
  dataflow: docs/dataflow.md
  runbook: docs/runbook.md       # 没有就写 null，不要编一个
  tasks: docs/TASKS.md
# 必填：单一真相源。每个非 null 路径必须在本仓真实存在。
# 不要在这里复制内容，只放路径。

status: evergreen
last-verified: <YYYY-MM-DD>
verified-by: <谁、用什么方法核对>
# 必填：沿用 tellurion-docs 的 R1；没有 last-verified 的卡片视为已腐烂
---
```

---

## 2. 正文

```markdown
# 服务卡：<repo-name>

> **一句话**：<它替谁做什么，≤ 40 字；不写技术栈。>
>
> `kind` · `lifecycle` · `impact` · `owner`：与 frontmatter 一致。

## 1. 这是什么

<2~3 句：职责 + 在系统里的位置。只写稳定的；不要写"目前正在……"。>

**它拥有**：<schema 名 / 契约 package 名；没有写"无">
**它不拥有**：<一句话，防止读者误判；没有写"无">

## 2. 它不做什么

- <被明确排除的边界 1，来自 api-schema §5 / AGENTS §3>
- <边界 2>
- <边界 3>

> 只写"被明确排除"的，不写愿望、不写待办。这比"它能做什么"更能防止功能放错地方。

## 3. 与谁相连

### 调用它（入边）

| 来源 | 协议 | 用来做什么 | 本仓挂了会怎样 |
|---|---|---|---|
| `<repo>` | `<HTTP / gRPC / ...>` | <一句话> | <503 / 拒绝启动 / 降级 / 无影响> |

### 它调用（出边）

| 目标 | 协议 | 用来做什么 | 目标挂了会怎样 |
|---|---|---|---|
| `<repo 或外部系统>` | `<HTTP / PG / ...>` | <一句话> | <503 / 拒绝启动 / 降级 / 异步重试> |

> 不写 URL、端口、版本、超时。地址见 `config/` / `deploy/compose.yaml`；接口形状见 `docs/api-schema.md`。
> 外部系统（PG / 交易所 / LLM / 数据源）写名字即可，不写 DSN、不写 endpoint。

## 4. 运行时身份

- **常驻进程**：`<cmd/...>`；<没有进程写"纯库，无运行时"；多进程写清哪个常驻、哪个一次性>
- **存活/就绪语义**：`<探针路径>` = <语义>；`<探针路径>` = <语义>
  - 只写语义，不写端口；路径是稳定身份，不是接口清单。
  - 没有探针写"无（纯库 / 无监听）"。
- **部署真相**：`<deploy/compose.yaml>` / `<Dockerfile>` / `<config/...>`
- **端口**：不在此卡；见上述部署真相。
- **不写**：镜像 tag、副本数、启动命令全文、环境变量清单。

## 5. 数据与契约归属

| 维度 | 归属 | 真相源 |
|---|---|---|
| DB schema | `<market / ingest / 无>` | `docs/db-schema.md` |
| 跨仓 DTO / 契约 | `<contracts/... / 无>` | `docs/API.md` 或 `docs/api-schema.md` |
| 对外 HTTP | `<一句话范围，不列端点>` | `docs/api-schema.md` |

> 只写"拥有哪块"，不写表名清单、字段、导出符号数量。

## 6. 坏了怎么办

- **影响面**：<谁会被波及；是否 fail-closed；哪些功能仍可用>
- **先确认（按顺序，最多 3 条）**：
  1. <检查 1；如有 runbook，指向具体小节>
  2. <检查 2>
  3. <检查 3>
- **升级路径**：`owner` → 跨仓争议 → core `docs/TASKS.md`
- **runbook**：`<docs/runbook.md>` / "暂无；先看 README 快速开始"

> 不写完整排障手册、不写告警规则、不写 SLO。

## 7. 5 分钟后去哪

| 我想…… | 读这个 |
|---|---|
| 知道它承诺什么接口 | `docs/api-schema.md` |
| 知道它拥有哪些表 | `docs/db-schema.md` |
| 知道数据怎么流、哪里 fail-closed | `docs/dataflow.md` |
| 起停 / 排障 | `docs/runbook.md`（没有则 README 快速开始） |
| 当前在做什么 | `docs/TASKS.md` |
| 架构与决策 | `docs/ARCHITECTURE.md` / `docs/adr/` |

> 只放 5~7 行。不要把其他文档的正文搬进来。
```

---

## 3. 发布前检查

- [ ] `SERVICE.md` 放在仓根目录，`README.md` 顶部有一行指针。
- [ ] 正文 ≤ 120 行，7 段标题与顺序未改。
- [ ] 正文没有裸端口（`:8085`）、URL、DSN、镜像 tag、版本 pin、端点/表数量。
- [ ] 每一条"对方挂了会怎样"都写了行为，不是"需要注意"。
- [ ] `truth` 里每个非 `null` 路径都存在；没有 runbook 就写 `null`。
- [ ] `last-verified` 是今天，`verified-by` 写清核对方法。
- [ ] 如果卡片里出现了三个月后必变的数字，删掉并改成指针。
