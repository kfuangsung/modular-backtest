from typing import Self

import pandas as pd
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class BacktestResult:
    """Holds the results of a backtest.

    Attributes:
        data (pd.DataFrame): The result of the backtest.
    """

    data: pd.DataFrame

    @classmethod
    def from_zipline_output(cls, out: pd.DataFrame) -> Self:
        """Creates a BacktestResult from a zipline output.

        Args:
            out (pd.DataFrame): The DataFrame returned by zipline.

        Returns:
            BacktestResult: A BacktestResult with the data from the backtest.
        """
        return cls(data=out)
