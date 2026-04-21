from bot.logging_config import setup_logging

logger = setup_logging()


def get_client():
    """
    Return a dummy client.

    This keeps the structure intact while allowing the app
    to run without real Binance API credentials.
    """

    logger.debug("Using dummy client (API calls are simulated).")

    return None