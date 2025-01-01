from __future__ import annotations

from typing import TYPE_CHECKING

import bottleneck as bn
import talib
from zipline.pipeline.data import EquityPricing
from zipline.pipeline.factors import CustomFactor
from zipline.utils.input_validation import expect_bounded

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd

PERIOD_MULTIPLIER = 2


class ATR(CustomFactor):
    """Average True Range (ATR) factor.

    This factor computes the average true range for given high, low, and close
    prices over a specified time period.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of high, low,
            and close prices.
        params (tuple): The parameters for the factor, specifically the time
            period for ATR calculation.
    """

    inputs = (
        EquityPricing.high,
        EquityPricing.low,
        EquityPricing.close,
    )
    params = ("timeperiod",)

    @expect_bounded(timeperiod=(2, None))
    def __new__(cls, timeperiod: int = 14, *args, **kwargs):
        # unstable period
        """
        Create a new instance of the ATR factor.

        Args:
            timeperiod (int): The time period over which to compute the ATR. Default is 14.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            ATR: An instance of the ATR factor.
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
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        timeperiod: int,
    ) -> None:
        """Compute the ATR values.

        Args:
            today (pd.Timestamp): The current date.
            assets (pd.Index): The index of assets for which to compute the
                factor.
            out (np.ndarray): The output array to store the computed ATR
                values.
            high (np.ndarray): High prices of the assets.
            low (np.ndarray): Low prices of the assets.
            close (np.ndarray): Close prices of the assets.
            timeperiod (int): The time period over which to compute the ATR.
        """
        high_ = bn.push(high, axis=0)
        low_ = bn.push(low, axis=0)
        close_ = bn.push(close, axis=0)

        for i in range(out.shape[0]):
            out[i] = talib.ATR(high_[:, i], low_[:, i], close_[:, i], timeperiod)[-1]
