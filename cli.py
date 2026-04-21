#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI entry point.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.01
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.01 --price 50000
"""

import argparse
import sys

from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.client import get_client
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import validate_inputs

logger = setup_logging()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,  choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type",     required=True,  dest="order_type",
                        choices=["MARKET", "LIMIT"],  help="Order type")
    parser.add_argument("--quantity", required=True,  type=float, help="Order quantity")
    parser.add_argument("--price",    required=False, type=float, default=None,
                        help="Limit price (required for LIMIT orders)")
    return parser


def print_order_summary(symbol: str, side: str, order_type: str,
                        quantity: float, price: float | None) -> None:
    print("\n─── Order Request ───────────────────────────")
    print(f"  Symbol   : {symbol.upper()}")
    print(f"  Side     : {side}")
    print(f"  Type     : {order_type}")
    print(f"  Quantity : {quantity}")
    if price is not None:
        print(f"  Price    : {price}")
    print("─────────────────────────────────────────────")


def print_order_response(response: dict) -> None:
    print("\n─── Order Response ──────────────────────────")
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', '0')}")
    avg_price = response.get("avgPrice") or response.get("price", "N/A")
    print(f"  Avg Price    : {avg_price}")
    print("─────────────────────────────────────────────\n")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs before touching the API
    try:
        validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        print(f"\n[ERROR] Invalid input: {exc}")
        logger.error("Input validation failed | %s", exc)
        sys.exit(1)

    print_order_summary(args.symbol, args.side, args.order_type, args.quantity, args.price)

    # Initialise client
    try:
        client = get_client()
    except EnvironmentError as exc:
        print(f"\n[ERROR] {exc}")
        logger.error("Client init failed | %s", exc)
        sys.exit(1)

    # Place the order
    try:
        response = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print_order_response(response)
        print("[SUCCESS] Order placed successfully.\n")

    except BinanceAPIException as exc:
        print(f"\n[ERROR] Binance API error (code {exc.code}): {exc.message}")
        sys.exit(1)
    except BinanceRequestException as exc:
        print(f"\n[ERROR] Network error: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"\n[ERROR] Unexpected error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
