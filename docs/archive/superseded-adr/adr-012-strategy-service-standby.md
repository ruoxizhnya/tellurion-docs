# ADR-012: Strategy-Service Standby Decision

> **Status**: Closed（Superseded）— 服务已于 2026-10-17 删除，见文末「关闭记录（REV-16）」
> **Date**: 2026-04-11
> **Deciders**: Longshao

## Context

The project has a `strategy-service` (:8082) defined in docker-compose.yml with a complete implementation in `cmd/strategy/main.go`. However, analysis-service currently handles all strategy operations in-process via `strategy.DefaultRegistry` (populated by `pkg/strategy/plugins/` init functions). The strategy-service is never actually called because the local registry always finds strategies first.

Key issues:
1. **Two incompatible strategy registries**: `cmd/strategy/main.go` uses the old `strategy.Register()` factory pattern, while `cmd/analysis/main.go` uses `strategy.DefaultRegistry` with the canonical Strategy interface.
2. **AGENTS.md data flow diagram incorrectly shows** `GET /strategies → strategy-service :8082 (proxy)`, but the actual `/strategies` route queries local `StrategyDB` directly.
3. **Engine fallback logic** in `engine.go` tries local registry first, then falls back to strategy-service via HTTP — but the fallback never executes because all strategies are registered locally.

## Decision

**Keep strategy-service in standby status** with the following clarifications:

1. **Current state**: Strategy-service is not required for normal operation. All strategies run in-process within analysis-service.
2. **Future activation criteria**: Strategy-service will be activated when Phase 3 D3 (Go Plugin hot-swap) is implemented, which requires a separate process for dynamic strategy loading.
3. **Required work before activation**:
   - Migrate `cmd/strategy/main.go` to use `strategy.DefaultRegistry` instead of the old `strategy.Register()` factory
   - Ensure both services share the same canonical Strategy interface
   - Add proper proxy routes in `handlers_proxy.go` if external strategy lookups are needed
4. **Deprecation path**: If D3 is replaced by a simpler in-process plugin mechanism, strategy-service can be fully deprecated and removed from docker-compose.yml.

## Consequences

### Positive
- No unnecessary service to maintain or monitor
- Simpler deployment topology (2 services instead of 3)
- No latency from inter-service HTTP calls for strategy lookups

### Negative
- Strategy hot-swap requires analysis-service restart until D3 is implemented
- `cmd/strategy/main.go` code drifts if not kept in sync with canonical interface

### Mitigation
- Document the standby status clearly in ARCHITECTURE.md and AGENTS.md
- Correct the data flow diagram to reflect actual architecture
- Track the interface alignment as a prerequisite for D3 activation

---

## 关闭记录（REV-16，2026-10-17）

**裁决：删除 `cmd/strategy`（:8082）与 compose 段；`pkg/strategy` 库层保留。**

本文 2026-04-11 的「保持 standby」前提是：它至少还是个**占位**——等 D3（接口对齐）
完成后可以激活成远程 SignalProvider。这条前提在 OBS-11 之后彻底消失：

1. **OBS-11 删掉了信号端点与引擎侧 fallback**（`cmd/strategy/main.go` 自陈），服务只剩
   `/health` + 恒空的 `/strategies`（`registerStrategies` 不注册任何策略）。
2. **零调用方**：全仓非测试代码没有 `strategy_service` 读取点（`engine.go` 里只剩
   「已随 OBS-11 删除」的注释）——想激活也没有对接面了。
3. 因此 standby 不再「占位」，只余运维税：一个 compose 常驻容器 + healthcheck +
   镜像构建目标，每次部署都要为它买单，而它不能服务任何请求。

**为什么是删除而不是继续 standby**：占位价值来自「将来能低成本激活」。core 侧的
远程 SignalProvider 接口已被拆掉，将来若真需要远程形态，从 `pkg/strategy` 库层重建
一个服务很便宜（库层一行未动）。为想象中的将来付常驻成本不划算。

**落地证据**（core 仓）：`cmd/strategy/` 与 `config/strategy-service.yaml` 删除；
`docker-compose.yml` / `Makefile`（build-strategy、push-strategy 与聚合目标）/
`tools/local-stack.sh`（端口断言清单）/ `tools/check_deploy_consistency.py`
（服务白名单与 INFRA_ENV_REQUIRED）/ `deploy/k8s/configmap.yaml` 注释 / `e2e`
连通性用例同步；`go build ./...` 绿、`check_deploy_consistency.py` 绿。
