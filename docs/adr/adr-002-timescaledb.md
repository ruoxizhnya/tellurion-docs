# ADR-002: TimescaleDB vs. Vanilla PostgreSQL for OHLCV Storage

**Date:** 2026-03-24
**Status:** Superseded — 实际实现为**原生 PostgreSQL**（见下方裁决记录）

## Context

Should OHLCV data use TimescaleDB's hypertable partitioning, or standard PostgreSQL partitioned tables?

## Decision

**Option A — TimescaleDB (current).**

Compression and time-series query performance are worth the operational complexity for a data-intensive system. If license concerns arise in a commercial context, migration to native partitioning is a one-week project with no architectural changes.

## Consequences

- TimescaleDB extension adds operational complexity
- Chunk-based compression reduces storage ~90%
- License considerations for production use (source-available license)

## 裁决记录（REV-15，2026-10-17）

- **裁决（2026-10-16 主任批准）：改判 Superseded，理由不是「选错」而是「没落地」。**
  生产库从未安装 TimescaleDB：`SELECT extname FROM pg_extension` 只有 `plpgsql`；
  `PostgresStore.migrate` 会尝试 `create_hypertable` 但**失败只 warn 不阻断**
  （`pkg/storage/postgres.go` 的 "Could not create hypertable (TimescaleDB may not be available)"），
  即系统一直优雅降级在原生 PG 上跑。**该 ADR 描述的选型没有在使用**，
  继续标 Accepted 会让读者以为 OLHCV 查询走的是压缩 + chunk 分区。
- **当前实现**：`ohlcv_daily_qfq` 是普通表 + `(symbol)` / `(trade_date)` 两个 B-tree 索引
  （`pkg/storage/postgres.go` 的 `migrate` 尾部）。数据量级（≈390 万行 / 5671 标的 / 727 交易日）下
  查询性能可接受，没有拆分的紧迫性。
- **保留为选项**：数据量再上一个量级（或需要压缩 / retention policy）时，重新评估 TimescaleDB；
  届时本文的「Option A」论证仍然有效，只需把这个 ADR 从 Superseded 翻回 Accepted 并落 hypertable。
  **不要**在没有 instlal 扩展的环境里把「hypertable 已建」当既成事实写进文档。

**核验命令**（core 仓根目录）：

```bash
psql "$TEST_DATABASE_DSN" -tAc "SELECT extname FROM pg_extension;"   # 应只有 plpgsql
grep -n "create_hypertable" pkg/storage/postgres.go                  # 只有 best-effort 尝试 + warn
```
