import sys

from tradingview_screener import Query


def get_equity_symbols(market: str = "america", limit: int = sys.maxsize) -> list[str]:
    """Retrieves a list of equity symbols from a specified market.

    Args:
        market (str): The market to retrieve symbols from. Defaults to "america".
        limit (int): The maximum number of symbols to retrieve. Defaults to sys.maxsize.

    Returns:
        list[str]: A list of equity symbols.
    """
    _, stocks = (
        Query()
        .set_markets(market)
        .select("name", "indexes")
        .limit(limit)
        .get_scanner_data()
    )
    stocks.set_index("ticker", inplace=True)
    stocks = stocks.filter(regex="^(?!OTC)", axis=0)
    stocks = stocks.query('~name.str.contains("/")')
    symbols: list[str] = stocks["name"].to_list()
    return symbols
