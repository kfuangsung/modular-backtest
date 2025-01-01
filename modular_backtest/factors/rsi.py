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

PERIOD_MULTIPLIER = 2


class RSI(CustomFactor):
    """Relative Strength Index (RSI) factor.

    This factor computes the RSI for given closing prices over a specified time period.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of closing prices.
        params (tuple): The parameters for the factor, specifically the time period for RSI calculation.
    """

    inputs = (EquityPricing.close,)
    params = ("timeperiod",)

    @expect_bounded(timeperiod=(2, None))
    def __new__(cls, timeperiod: int = 14, *args, **kwargs):
        """Create a new instance of the RSI factor.

        Args:
            timeperiod (int): The time period over which to compute the RSI. Default is 14.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            RSI: An instance of the RSI factor.
        """
        # unstable period
        return super().__new__(
            cls,
            timeperiod=timeperiod,
            window_length=timeperiod * PERIOD_MULTIPLIER,
            *args,
            **kwargs,
        )

    def compute(  # type: ignore
        self,
        today: pd.Timestamp,
        assets: pd.Index,
        out: np.ndarray,
        close: np.ndarray,
        timeperiod: int,
    ) -> None:
        """Compute the RSI values.

        Args:
            today (pd.Timestamp): The current date.
            assets (pd.Index): The index of assets for which to compute the factor.
            out (np.ndarray): The output array to store the computed RSI values.
            close (np.ndarray): The closing prices of the assets.
            timeperiod (int): The time period over which to compute the RSI.
        """
        out[:] = np.apply_along_axis(
            lambda x: talib.RSI(x, timeperiod)[-1], 0, bn.push(close, axis=0)
        )
