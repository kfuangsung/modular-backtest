from __future__ import annotations

from typing import TYPE_CHECKING

import bottleneck as bn
import numpy as np
import talib
from zipline.pipeline.data import EquityPricing
from zipline.pipeline.factors import CustomFactor
from zipline.utils.input_validation import expect_bounded

if TYPE_CHECKING:
    import pandas as pd


class SMA(CustomFactor):
    """Simple Moving Average (SMA) factor.

    This factor computes the Simple Moving Average for given closing prices
    over a specified time period.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of closing
            prices.
        params (tuple): The parameters for the factor, specifically the time
            period for SMA calculation.
    """

    inputs = (EquityPricing.close,)
    params = ("timeperiod",)

    @expect_bounded(timeperiod=(2, None))
    def __new__(cls, timeperiod: int = 30, *args, **kwargs):
        """Create a new instance of the SMA factor.

        Args:
            timeperiod (int): The time period over which to compute the SMA. Default is 30.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            SMA: An instance of the SMA factor.
        """
        return super().__new__(
            cls, timeperiod=timeperiod, window_length=timeperiod, *args, **kwargs
        )

    def compute(  # type: ignore
        self,
        today: pd.Timestamp,
        assets: pd.Index,
        out: np.ndarray,
        close: np.ndarray,
        timeperiod: int,
    ):
        """Compute the SMA values.

        Args:
            today (pd.Timestamp): The current date.
            assets (pd.Index): The index of assets for which to compute the factor.
            out (np.ndarray): The output array to store the computed SMA values.
            close (np.ndarray): The closing prices of the assets.
            timeperiod (int): The time period over which to compute the SMA.
        """
        out[:] = np.apply_along_axis(
            lambda x: talib.SMA(x, timeperiod)[-1], 0, bn.push(close, axis=0)
        )
