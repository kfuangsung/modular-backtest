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


class ADX(CustomFactor):
    """Average Directional Index (ADX) factor.

    This factor computes the ADX for given high, low, and close prices over a specified time period.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of high, low, and close prices.
        params (tuple): The parameters for the factor, specifically the time period for ADX calculation.
    """

    inputs = (
        EquityPricing.high,
        EquityPricing.low,
        EquityPricing.close,
    )
    params = ("timeperiod",)

    @expect_bounded(timeperiod=(2, None))
    def __new__(cls, timeperiod: int = 14, *args, **kwargs):
        """Create a new instance of the ADX factor.

        Args:
            timeperiod (int): The time period over which to compute the ADX. Default is 14.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            ADX: An instance of the ADX factor.
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
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        timeperiod: int,
    ):
        """Compute the ADX values.

        Args:
            today (pd.Timestamp): The current date.
            assets (pd.Index): The index of assets for which to compute the factor.
            out (np.ndarray): The output array to store the computed ADX values.
            high (np.ndarray): High prices of the assets.
            low (np.ndarray): Low prices of the assets.
            close (np.ndarray): Close prices of the assets.
            timeperiod (int): The time period over which to compute the ADX.
        """
        high_ = bn.push(high, axis=0)
        low_ = bn.push(low, axis=0)
        close_ = bn.push(close, axis=0)

        for i in range(out.shape[0]):
            out[i] = talib.ADX(high_[:, i], low_[:, i], close_[:, i], timeperiod)[-1]
