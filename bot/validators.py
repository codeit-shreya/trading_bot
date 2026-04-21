from bot.logging_config import setup_logging

logger = setup_logging()

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> None:
    """
    Validate all CLI inputs before sending to the API.
    Raises ValueError with a descriptive message on failure.
    """
    if not symbol or not symbol.isalnum():
        raise ValueError(f"Invalid symbol '{symbol}'. Must be alphanumeric (e.g. BTCUSDT).")

    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}."
        )

    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}.")

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders. Use --price <value>.")
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}.")

    logger.debug(
        "Validation passed | symbol=%s side=%s type=%s qty=%s price=%s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )
