# Quant Crypto Auto-Trading Platform Skeleton

This repository provides an end-to-end blueprint for building a deployable quantitative cryptocurrency trading platform targeting OKX. It bundles a FastAPI backend, React/Vite frontend, async workers, and infrastructure automation for Docker-based deployment.

## A. Project Structure

```
.
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes/                # Market, order, strategy endpoints
│       ├── core/                      # Configuration
│       ├── models/                    # Pydantic schemas
│       └── services/                  # OKX clients, order engine, LLM orchestration
├── worker/                            # Async ingestion + execution workers
├── frontend/                          # Vite/React UI skeleton
├── db/                                # Database schema & migrations
├── docs/                              # Prompt templates & documentation
├── infra/                             # docker-compose & Dockerfiles
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
└── README.md
```

### Backend Modules
- **Market Data Service** – REST + WebSocket integration with OKX for 1s/1m candles and other feeds.
- **Order Engine** – Authenticated OKX trading endpoints with signature handling.
- **Strategy Service** – DeepSeek (LLM) orchestration for strategy generation & management.
- **Risk Controls** – Schema placeholders for max exposure, stop-loss, take-profit, and liquidation protection.

### Frontend Modules
- Vite + React dashboard scaffolding with panels for charts, strategies, risk controls, and manual order actions.

### Workers
- Async worker sample streaming candles from OKX and logging responses; extend to persist market data and trigger strategies.

### Infrastructure
- Dockerfiles per component and `docker-compose` stack for local development or staging.

## B. Backend Skeleton & WebSocket Example

Key entry point: [`backend/app/main.py`](backend/app/main.py) launches a FastAPI application with routed modules for market data, orders, and strategies. The market service wires REST + WebSocket OKX integrations (`backend/app/services/market_data.py`). WebSocket usage is illustrated via [`backend/app/services/okx_ws.py`](backend/app/services/okx_ws.py), subscribing to 1-second or 1-minute candles.

Worker example (`worker/market_data_worker.py`) demonstrates consuming the WebSocket feed asynchronously.

## C. Order Engine Interface

[`backend/app/services/order_engine.py`](backend/app/services/order_engine.py) exposes:
- `place_order` – submits signed OKX orders (market/limit/stop variants) with optional TP/SL.
- `cancel_order` – cancels by `ordId`.
- `list_orders` – retrieves open orders for reconciliation.

Signature logic follows OKX spec (`OK-ACCESS-*` headers). Extend to support advanced order types, position mode toggles, and account queries.

## D. DeepSeek Prompt Template

`docs/deepseek_prompt_template.md` supplies a structured template to instruct DeepSeek/LLM for automated strategy generation, backtesting code emission, and risk-control definitions. Populate the placeholders with run-time data before invoking the LLM API via `StrategyService`.

## E. Database Schema

PostgreSQL schema lives in `db/schema.sql` and covers:
- `strategies` – metadata, LLM payload.
- `orders` – exchange order linkage, margin config, TP/SL, leverage.
- `positions` – real-time exposure tracking.
- `trade_logs` – auditable execution & risk events.
- `backtest_results` – metrics and equity curves.
- `risk_rules` – per-strategy risk guardrails.

Indices enable efficient lookups across strategies and time-series logs.

## F. Deployment, CI/CD & Security

### Docker Compose
Run the entire stack via:
```bash
docker compose -f infra/docker-compose.yml up --build
```
Components:
- **api** – FastAPI + UVicorn backend.
- **worker** – market data ingestion & strategy execution tasks.
- **frontend** – React dashboard served with Vite dev server.
- **db** – PostgreSQL with schema seeded automatically.

### CI/CD Guidance
- Build and push component images (api/worker/frontend) to your registry per commit.
- Use GitHub Actions/GitLab CI to run unit tests (backend `pytest`, frontend `npm test`), linting, and Docker builds.
- Promote to staging/production using environment-specific compose files or Helm charts. Integrate health checks on `/health`.

### Security Recommendations
- **Secrets management** – never hardcode API keys. Load via `.env` (ignored from VCS) or secret stores (Vault, AWS Secrets Manager).
- **Network security** – restrict database access to internal network. Use TLS termination for public endpoints.
- **Access controls** – implement JWT/OAuth for UI/API authentication. Audit actions in `trade_logs`.
- **Monitoring** – push metrics/logs to centralized observability (Prometheus/Grafana, ELK).

## Tests & Verification Steps

1. **Backend** – `uvicorn backend.app.main:app --reload` then `curl http://localhost:8000/health`.
2. **Worker** – `python -m worker.market_data_worker` (requires OKX connectivity).
3. **Frontend** – `cd frontend && npm install && npm run dev`.
4. **Integration** – use `docker compose` to validate container orchestration.

Extend with automated unit/integration tests and contract tests for exchange + LLM adapters.
