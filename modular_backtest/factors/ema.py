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


class EMA(CustomFactor):
    """Exponential Moving Average (EMA) factor.

    This factor computes the Exponential Moving Average for given closing prices
    over a specified time period.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of closing
            prices.
        params (tuple): The parameters for the factor, specifically the time
            period for EMA calculation.
    """

    inputs = (EquityPricing.close,)
    params = ("timeperiod",)

    @expect_bounded(timeperiod=(2, None))
    def __new__(cls, timeperiod: int = 30, *args, **kwargs):
        # unstable period
        """
        Create a new instance of the EMA factor.

        Args:
            timeperiod (int): The time period over which to compute the EMA. Default is 30.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            EMA: An instance of the EMA factor.
        """
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
    ):
        """Compute the EMA values.

        Args:
            today (pd.Timestamp): The current date.
            assets (pd.Index): The index of assets for which to compute the
                factor.
            out (np.ndarray): The output array to store the computed EMA
                values.
            close (np.ndarray): The closing prices of the assets.
            timeperiod (int): The time period over which to compute the EMA.
        """
        out[:] = np.apply_along_axis(
            lambda x: talib.EMA(x, timeperiod)[-1], 0, bn.push(close, axis=0)
        )
