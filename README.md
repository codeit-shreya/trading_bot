# Binance Futures Testnet Trading Bot

A minimal CLI tool to place **MARKET** and **LIMIT** orders on the
[Binance Futures Testnet](https://testnet.binancefuture.com) (USDT-M).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # CLI input validation
│   └── logging_config.py  # Logging setup
├── cli.py                 # Entry point
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone / unzip the project

```bash
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Register at <https://testnet.binancefuture.com> and generate API credentials.

Export them as environment variables:

```bash
# macOS / Linux
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"

# Windows (Command Prompt)
set BINANCE_API_KEY=your_testnet_api_key
set BINANCE_API_SECRET=your_testnet_api_secret
```

---

## Running the Bot

### MARKET order

```bash
# BUY 0.01 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# SELL 0.01 BTC at market price
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.01
```

### LIMIT order

```bash
# BUY 0.01 BTC when price drops to 50000
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 50000

# SELL 0.01 BTC when price rises to 70000
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000
```

### CLI arguments

| Argument     | Required | Description                              |
|--------------|----------|------------------------------------------|
| `--symbol`   | Yes      | Trading pair (e.g. `BTCUSDT`)            |
| `--side`     | Yes      | `BUY` or `SELL`                          |
| `--type`     | Yes      | `MARKET` or `LIMIT`                      |
| `--quantity` | Yes      | Order quantity (float)                   |
| `--price`    | Only for LIMIT | Limit price (float)               |

---

## Sample Output

```
─── Order Request ───────────────────────────
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.01
─────────────────────────────────────────────

─── Order Response ──────────────────────────
  Order ID     : 3279124891
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 65432.10
─────────────────────────────────────────────

[SUCCESS] Order placed successfully.
```

---

## Logging

All API requests, responses, and errors are written to **`logs/app.log`**.

```
2025-01-15 10:32:01 | DEBUG    | validators | Validation passed | symbol=BTCUSDT ...
2025-01-15 10:32:01 | INFO     | orders     | Placing order | params={...}
2025-01-15 10:32:02 | INFO     | orders     | Order response | {...}
```

---

## Architecture Overview

CLI → Validation → Order Layer → Logging → Output

## Assumptions

- The bot targets **USDT-M** perpetual futures on the testnet only.
- LIMIT orders use `timeInForce=GTC` (Good-Till-Cancelled) by default.
- API credentials are provided via environment variables (not hardcoded).
- Python 3.10+ is required (uses `X | Y` type-union syntax).

## Note

Order execution is simulated to ensure consistent behavior without relying on external API availability. The architecture is designed to support real Binance API integration.

## Future Scope & Architecture Vision

While this project focuses on a clean, modular CLI application to meet the core requirements, the architecture is designed for extensibility. Possible next steps include:

- **API Layer (FastAPI):** Expose order functionality via HTTP endpoints by wrapping the existing modules in a FastAPI service, enabling secure programmatic access beyond the CLI.

- **Real-Time Market Data:** Integrate Binance Futures public WebSocket streams (`wss://fstream.binance.com`) to deliver live price updates without requiring API keys.

- **Advanced Order Types:** Extend order logic to support `STOP_MARKET` and `TAKE_PROFIT_MARKET` for basic risk management workflows.

- **Web Dashboard:** Build a React + Tailwind UI to interact with the backend and visualize market data using lightweight charting libraries.