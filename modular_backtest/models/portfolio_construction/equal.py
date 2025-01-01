from __future__ import annotations

from typing import TYPE_CHECKING, override

from pydantic.dataclasses import dataclass

from modular_backtest.backends.allocation import Allocation, AllocationHandler
from modular_backtest.models.abstract import PortfolioConstruction

if TYPE_CHECKING:
    from modular_backtest.backends.signal import SignalHandler
    from modular_backtest.types import BarData, Context


@dataclass
class EqualWeightPortfolioConstruction(PortfolioConstruction):
    """Equal weight portfolio construction.

    This strategy allocates the same weight to each asset in the universe.

    Attributes:
        None

    Methods:
        run(context: Context, data: BarData, signals: SignalHandler)
            -> AllocationHandler:
            Runs the portfolio construction process.

    Raises:
        None
    """

    @override
    def run(
        self, context: Context, data: BarData, signals: SignalHandler
    ) -> AllocationHandler:
        """Runs the portfolio construction process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            signals (SignalHandler): The handler with signal information.

        Returns:
            AllocationHandler: The handler containing the generated allocations.
        """
        w = 1 / len(signals) if len(signals) > 0 else 0.0
        allocs_ = [Allocation(asset=signal.asset, weight=w) for signal in signals]
        return AllocationHandler(allocs=allocs_)
