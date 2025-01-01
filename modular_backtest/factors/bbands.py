from __future__ import annotations

from typing import TYPE_CHECKING

import bottleneck as bn
import numpy as np
import talib
from talib._ta_lib import MA_Type
from zipline.pipeline.data import EquityPricing
from zipline.pipeline.factors import CustomFactor
from zipline.utils.input_validation import expect_bounded

if TYPE_CHECKING:
    import pandas as pd


class BBANDS(CustomFactor):
    """Bollinger Bands factor.

    This factor calculates the Bollinger Bands for a given time period and
    number of standard deviations. The Bollinger Bands are a technical
    indicator that consists of a moving average and two standard deviations
    plotted above and below the moving average.

    Attributes:
        inputs (tuple): The input data for the factor, consisting of the
            closing prices of the assets.
        params (tuple): The parameters for the factor, specifically the time
            period and the number of standard deviations.
        outputs (tuple): The output data for the factor, consisting of the
            upper band, the middle band, and the lower band.
    """

    inputs = (EquityPricing.close,)
    params = (
        "timeperiod",
        "nbdevup",
        "nbdevdn",
        "matype",
    )
    outputs = (
        "upperband",
        "middleband",
        "lowerband",
    )

    @expect_bounded(timeperiod=(2, None))
    def __new__(
        cls,
        timeperiod: int = 5,
        nbdevup: int = 2,
        nbdevdn: int = 2,
        matype: MA_Type = MA_Type.SMA,
        *args,
        **kwargs,
    ):
        """
        Create a new instance of the Bollinger Bands factor.

        Args:
            timeperiod (int): The time period over which to compute the Bollinger Bands.
            nbdevup (int): The number of standard deviations for the upper band.
            nbdevdn (int): The number of standard deviations for the lower band.
            matype (MA_Type): The type of moving average to use.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            BBANDS: An instance of the Bollinger Bands factor.
        """
        return super().__new__(
            cls,
            timeperiod=timeperiod,
            nbdevup=nbdevup,
            nbdevdn=nbdevdn,
            matype=matype,
            window_length=timeperiod,
            *args,
            **kwargs,
        )

    def compute(  # type: ignore
        self,
        today: pd.Timestamp,
        assets: pd.Index,
        out: np.recarray,
        close: np.ndarray,
        timeperiod: int,
        nbdevup: int,
        nbdevdn: int,
        matype: MA_Type,
    ) -> None:
        """
        Compute the Bollinger Bands for the given assets.

        This method calculates the upper, middle, and lower Bollinger Bands using
        the provided closing prices and parameters.

        Args:
            today (pd.Timestamp): The current date for which to compute the Bollinger Bands.
            assets (pd.Index): The index of assets for which to compute the factor.
            out (np.recarray): The output array to store the computed upper, middle, and lower bands.
            close (np.ndarray): The closing prices of the assets.
            timeperiod (int): The time period over which to compute the bands.
            nbdevup (int): The number of standard deviations for the upper band.
            nbdevdn (int): The number of standard deviations for the lower band.
            matype (MA_Type): The type of moving average to use.

        Returns:
            None
        """

        upperband, middleband, lowerband = np.apply_along_axis(
            lambda x: talib.BBANDS(x, timeperiod, nbdevup, nbdevdn, matype),
            0,
            bn.push(close, axis=0),
        )
        out.upperband = upperband[-1]
        out.middleband = middleband[-1]
        out.lowerband = lowerband[-1]
