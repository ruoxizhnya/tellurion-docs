# ADR-006: Job Queue Technology Selection

**Date:** 2026-03-24
**Status:** Accepted — 实现选 **PostgreSQL-backed**（与本文原推荐相反，见裁决记录）

## Context

Decision 3 says "implement as job queue" but does not specify the technology. Options:
- **Redis-backed queue** (using LIST/Streams) — leverages existing Redis dependency, lightweight
- **PostgreSQL-backed queue** — no new dependencies, uses `backtest_jobs` table with status
- **Dedicated queue** (RabbitMQ, NATS) — more robust but adds operational complexity

## Decision

**Pending.** Recommendation: Redis-backed queue using Redis Streams, given Redis is already a Phase 1 infrastructure dependency.

## Consequences (when decided)

- Worker service implementation depends on this choice
- Queue reliability guarantees (at-least-once vs exactly-once delivery)
- Operational complexity

## 裁决记录（REV-15，2026-10-17）

- **事实**：队列早已是 **PostgreSQL-backed** 并跑了数月——`sync_jobs` / `backtest_jobs` 表承载状态，
  `pkg/sync/queue.go` 在同一进程内用 notify 通道唤醒 worker，**没有 Redis Streams**。
  本文「Recommendation: Redis-backed queue using Redis Streams」从未被采纳，而 Status 一直挂在
  OPEN，等于一条已固化的架构事实没有决策记录。
- **为什么没走 Redis**：队列的可靠性要求（状态可查、可重试、可取消、能按 job 订阅进度）
  与「已有 PG 事务 + 单一存储」重合度高；引入 Redis Streams 会多一套消费位点与死信语义要维护，
  而本系统的 worker 与 web 在同一部署单元里，进程内 notify 已足够唤醒（跨进程场景不存在）。
- **何时该翻案**：worker 与 web 拆成独立部署单元、或需要跨进程 fan-out / 消费组时，
  Redis Streams（或 NATS）才真正带来收益；届时新开 ADR 取代本文，而不是改本文。

**核验命令**（core 仓根目录）：

```bash
grep -n "sync_jobs\|backtest_jobs" pkg/storage/postgres.go | head -3   # PG 承载队列状态
grep -n "NotifyJobAvailable\|WaitForJob" pkg/sync/queue.go | head -3   # 进程内 notify，非 Redis
grep -rn "XAdd\|XReadGroup" pkg/ | head -3                            # 应无命中（无 Streams 消费组）
```
