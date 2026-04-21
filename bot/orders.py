from bot.logging_config import setup_logging

logger = setup_logging()


def place_order(
    client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Simulate placing a MARKET or LIMIT futures order.

    Returns a mock response similar to Binance API.
    """

    params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info("Simulating order | params=%s", params)

    try:
        # 🔁 Simulated response (mock)
        response = {
            "orderId": 123456789,
            "symbol": symbol.upper(),
            "status": "FILLED",
            "side": side,
            "type": order_type,
            "executedQty": quantity,
            "avgPrice": price if order_type == "LIMIT" else "market_price",
        }

    except Exception as exc:
        logger.error("Unexpected error during simulated order | %s", exc)
        raise

    logger.info("Simulated order response | %s", response)
    return response