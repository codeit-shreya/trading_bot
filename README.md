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

## Assumptions

- The bot targets **USDT-M** perpetual futures on the testnet only.
- LIMIT orders use `timeInForce=GTC` (Good-Till-Cancelled) by default.
- API credentials are provided via environment variables (not hardcoded).
- Python 3.10+ is required (uses `X | Y` type-union syntax).
