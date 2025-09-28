# DeepSeek Strategy Generation Prompt Template

Use this template when requesting new strategies, backtests, or risk reviews from DeepSeek (or another LLM).

```
You are an elite quantitative crypto trader and software engineer. Generate or refine a trading strategy that can be executed on OKX perpetual swaps.

## Objectives
- Trading Style: {trading_style}
- Timeframes: {timeframes}
- Target Instruments: {symbols}
- Risk Tolerance: {risk_tolerance}
- Capital Allocation: {capital_allocation}

## Deliverables
1. Strategy overview (narrative) with entry/exit logic, filters, and justification.
2. Executable code snippets for:
   - Realtime execution (language: {execution_language}).
   - Backtest module (language: {backtest_language}).
   - Optional PineScript indicator for TradingView visualization.
3. Explicit risk controls covering:
   - Position sizing rules.
   - Stop loss / take profit logic.
   - Daily loss limit enforcement.
   - Leverage usage and liquidation protection.
4. Monitoring checklist and metrics to alert on via webhook/email/Telegram.

## Context Data
- Recent performance summary: {performance_summary}
- Market regime assumption: {market_regime}
- Constraints: {constraints}

## Output Format (JSON)
{
  "strategy_name": "...",
  "summary": "...",
  "execution_code": "...",
  "backtest_code": "...",
  "risk_controls": ["..."],
  "deployment_steps": ["..."],
  "monitoring": {
     "metrics": ["..."],
     "alerts": [
        {"channel": "webhook", "condition": "..."},
        {"channel": "email", "condition": "..."}
     ]
  }
}

Ensure code blocks are syntactically correct and include configuration placeholders rather than secrets. Reference OKX REST/WebSocket endpoints where needed.
```
