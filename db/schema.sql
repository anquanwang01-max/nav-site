-- PostgreSQL schema for the quant trading platform

CREATE TABLE strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    llm_payload JSONB,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exchange_order_id TEXT,
    strategy_id UUID REFERENCES strategies(id),
    instrument TEXT NOT NULL,
    side TEXT NOT NULL,
    order_type TEXT NOT NULL,
    quantity NUMERIC(28, 10) NOT NULL,
    price NUMERIC(28, 10),
    leverage NUMERIC(10, 2),
    margin_mode TEXT,
    status TEXT NOT NULL,
    stop_loss NUMERIC(28, 10),
    take_profit NUMERIC(28, 10),
    reduce_only BOOLEAN DEFAULT FALSE,
    placed_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id UUID REFERENCES strategies(id),
    instrument TEXT NOT NULL,
    quantity NUMERIC(28, 10) NOT NULL,
    entry_price NUMERIC(28, 10) NOT NULL,
    mark_price NUMERIC(28, 10),
    unrealized_pnl NUMERIC(28, 10),
    leverage NUMERIC(10, 2),
    margin_mode TEXT,
    liquidation_price NUMERIC(28, 10),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE trade_logs (
    id BIGSERIAL PRIMARY KEY,
    order_id UUID REFERENCES orders(id),
    position_id UUID REFERENCES positions(id),
    message TEXT NOT NULL,
    level TEXT DEFAULT 'info',
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE backtest_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id UUID REFERENCES strategies(id),
    timeframe TEXT,
    parameters JSONB,
    metrics JSONB,
    equity_curve JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE risk_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id UUID REFERENCES strategies(id),
    rule_name TEXT NOT NULL,
    rule_config JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_orders_strategy_id ON orders(strategy_id);
CREATE INDEX idx_positions_strategy_id ON positions(strategy_id);
CREATE INDEX idx_trade_logs_created_at ON trade_logs(created_at);
