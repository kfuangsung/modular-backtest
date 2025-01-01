from __future__ import annotations

from typing import TYPE_CHECKING

from modular_backtest.models.abstract import RiskManagement

if TYPE_CHECKING:
    from modular_backtest.backends.allocation import AllocationHandler
    from modular_backtest.types import BarData, Context


class VoidRiskManagement(RiskManagement):
    """Does not perform any risk management on the given allocations.

    The returned allocation handler is a copy of the input allocation handler.

    Attributes:
        None

    Methods:
        run(context: Context, data: BarData, allocations: AllocationHandler)
            -> AllocationHandler:
            Runs the risk management process.

    Raises:
        None
    """

    def run(
        self, context: Context, data: BarData, allocations: AllocationHandler
    ) -> AllocationHandler:
        """Runs the risk management process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            allocations (AllocationHandler): The handler with allocation information.

        Returns:
            AllocationHandler: The handler with the same allocations without any changes.
        """
        return allocations
