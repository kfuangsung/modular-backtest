from __future__ import annotations

import logging
import math
import warnings
from collections.abc import Mapping
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import yfinance as yf
import zipline.data.bundles.core as bundles
from more_itertools import batched
from pandas.errors import SettingWithCopyWarning
from tqdm import tqdm
from zipline.data.bundles.quandl import (
    parse_dividends,
    parse_pricing_and_vol,
    parse_splits,
)

from modular_backtest.data.utils import get_equity_symbols

if TYPE_CHECKING:
    import os

    from zipline.assets import AssetDBWriter
    from zipline.data.adjustments import SQLiteAdjustmentWriter
    from zipline.data.bcolz_daily_bars import BcolzDailyBarWriter
    from zipline.data.bcolz_minute_bars import BcolzMinuteBarWriter
    from zipline.utils.calendar_utils import TradingCalendar

NAME = "yahoo-finance"
UINT32_MAX = np.iinfo(np.uint32).max
log = logging.getLogger(__name__)

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("yfinance").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

OHLC = frozenset(["open", "high", "low", "close"])


def get_yahoo_symbols(environ: Mapping) -> list[str]:
    """
    Get the list of Yahoo Finance symbols from the environment.

    First, looks for the "YAHOO_SYMBOLS" environment variable. If it is not set,
    then uses the default list of equity symbols.

    Returns:
        list[str]: The list of Yahoo Finance symbols.
    """
    environ_symbols: str | None = environ.get("YAHOO_SYMBOLS", None)
    return environ_symbols.split(" ") if environ_symbols else get_equity_symbols()


def parse_data(data: pd.DataFrame):
    """
    Processes and cleans the input DataFrame containing financial data.

    The function performs the following operations:
    - Resets the index of the DataFrame.
    - Ensures that the "Dividends" and "Stock Splits" columns exist, initializing them to 0 if missing.
    - Fills missing values in the "Dividends", "Stock Splits", and "Volume" columns with 0.
    - Renames columns according to a predefined mapping.
    - Replaces negative values in the OHLC columns with NaN.
    - Forward fills missing values.
    - Drops any remaining rows with NaN values.

    Args:
        data (pd.DataFrame): The input DataFrame with financial data.

    Returns:
        pd.DataFrame: The cleaned and processed DataFrame.
    """

    columns_rename = {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Dividends": "ex_dividend",
        "Stock Splits": "split_ratio",
    }

    data.reset_index(inplace=True)
    if "Dividends" not in data.columns:
        data["Dividends"] = 0
    if "Stock Splits" not in data.columns:
        data["Stock Splits"] = 0

    data["Dividends"] = data["Dividends"].fillna(0)
    data["Stock Splits"] = data["Stock Splits"].fillna(0)
    data["Volume"] = data["Volume"].fillna(0)
    data.rename(columns=columns_rename, inplace=True)
    data[data[list(OHLC)] < 0] = np.nan
    data.ffill(axis=0, inplace=True)
    data.dropna(axis=0, inplace=True)

    return data


def fetch_yahoo_data(symbols, batch_size: int = 1000):
    """
    Downloads the historical data for the given list of symbols from Yahoo Finance.

    Args:
        symbols (list[str]): The list of symbols to download.
        batch_size (int, optional): The number of symbols to download in each batch. Defaults to 1000.

    Returns:
        pd.DataFrame: The downloaded data, with columns renamed and processed.
    """

    raw_data = pd.DataFrame()

    for symbol_batch in tqdm(
        batched(symbols, batch_size),
        total=math.ceil(len(symbols) / batch_size),
        desc="Batch",
    ):
        tickers = list(
            map(lambda x: x.replace(".", "-"), symbol_batch)
        )  # handle BRK.B -> BRK-B
        yf_data = yf.download(
            tickers,
            interval="1d",
            group_by="symbols",
            actions=True,
            threads=True,
            progress=True,
            repair=True,
        )

        if yf_data is None or yf_data.empty:
            raise ValueError("Failed to download data")

        assert isinstance(yf_data.columns, pd.MultiIndex)
        for symbol in yf_data.columns.levels[0]:
            data_ = yf_data.loc[:, symbol]
            data_ = parse_data(data_)
            if data_.empty:
                continue
            symbol = symbol.replace("-", ".")  # transform BRK-B -> BRK.B
            data_["symbol"] = symbol
            raw_data = pd.concat([raw_data, data_])

    raw_data["volume"] = raw_data["volume"].clip(lower=0, upper=UINT32_MAX)
    raw_data["ex_dividend"] = raw_data["ex_dividend"].clip(lower=0)
    raw_data["split_ratio"] = raw_data["split_ratio"].clip(lower=0)
    raw_data.replace({"split_ratio": 0.0}, 1.0, inplace=True)
    return raw_data


def gen_yahoo_asset_metadata(data, show_progress: bool):
    """
    Generate asset metadata for Yahoo Finance data.

    This function processes the input DataFrame to generate metadata for each
    asset symbol. It calculates the start and end dates of the data, assigns
    an exchange, and determines the auto-close date for each asset.

    Args:
        data (pd.DataFrame): A DataFrame containing asset data with columns
            "symbol" and "date".
        show_progress (bool): If True, logs the progress of metadata generation.

    Returns:
        pd.DataFrame: A DataFrame containing metadata for each asset, including
        "symbol", "start_date", "end_date", "exchange", and "auto_close_date".
    """

    if show_progress:
        log.info("Generating asset metadata.")

    data = data.groupby(by="symbol").agg({"date": ["min", "max"]})
    data.reset_index(inplace=True)
    data["start_date"] = data.date["min"]
    data["end_date"] = data.date["max"]
    del data["date"]
    data.columns = data.columns.get_level_values(0)

    data["exchange"] = "YAHOO"
    data["auto_close_date"] = data["end_date"].values + pd.Timedelta(days=1)
    return data


@bundles.register(NAME, calendar_name="NYSE", start_session=pd.Timestamp("1970-01-01"))
def yahoo_finance_bundles(
    environ: Mapping,
    asset_db_writer: AssetDBWriter,
    minute_bar_writer: BcolzMinuteBarWriter,
    daily_bar_writer: BcolzDailyBarWriter,
    adjustment_writer: SQLiteAdjustmentWriter,
    calendar: TradingCalendar,
    start_session: pd.Timestamp,
    end_session: pd.Timestamp,
    cache: Mapping,
    show_progress: bool,
    output_dir: os.PathLike,
):
    """
    Ingests financial data from Yahoo Finance into the zipline framework.

    This function fetches historical financial data for specified symbols
    from Yahoo Finance, processes the data, and writes it into the
    appropriate database tables for use with the zipline backtesting library.

    Args:
        environ (Mapping): Environment variables containing configuration
            such as the symbols to fetch.
        asset_db_writer (AssetDBWriter): Writer for the asset database.
        minute_bar_writer (BcolzMinuteBarWriter): Writer for minute-level bar data.
        daily_bar_writer (BcolzDailyBarWriter): Writer for daily bar data.
        adjustment_writer (SQLiteAdjustmentWriter): Writer for corporate actions.
        calendar (TradingCalendar): Trading calendar used for date calculations.
        start_session (pd.Timestamp): Start date for fetching data.
        end_session (pd.Timestamp): End date for fetching data.
        cache (Mapping): Cache for storing intermediate data.
        show_progress (bool): If True, display progress information.
        output_dir (os.PathLike): Directory for output data.

    Raises:
        ValueError: If data fetching fails.

    """

    raw_data = fetch_yahoo_data(get_yahoo_symbols(environ))
    asset_metadata = gen_yahoo_asset_metadata(
        raw_data[["symbol", "date"]], show_progress
    )
    exchanges = pd.DataFrame(
        data=[["YAHOO", "YAHOO", "US"]],
        columns=["exchange", "canonical_name", "country_code"],
    )
    asset_db_writer.write(equities=asset_metadata, exchanges=exchanges)
    symbol_map = asset_metadata.symbol
    sessions = calendar.sessions_in_range(start_session, end_session)
    raw_data.set_index(["date", "symbol"], inplace=True)
    daily_bar_writer.write(
        parse_pricing_and_vol(raw_data, sessions, symbol_map),
        show_progress=show_progress,
    )
    raw_data.reset_index(inplace=True)
    raw_data["symbol"] = raw_data["symbol"].astype("category")
    raw_data["sid"] = raw_data.symbol.cat.codes
    adjustment_writer.write(
        splits=parse_splits(
            raw_data[
                [
                    "sid",
                    "date",
                    "split_ratio",
                ]
            ].loc[raw_data.split_ratio != 1],
            show_progress=show_progress,
        ),
        dividends=parse_dividends(
            raw_data[
                [
                    "sid",
                    "date",
                    "ex_dividend",
                ]
            ].loc[raw_data.ex_dividend != 0],
            show_progress=show_progress,
        ),
    )
