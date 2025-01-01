from __future__ import annotations

from typing import TYPE_CHECKING

from modular_backtest.backends.order import OrderHandler, OrderTargetPercent
from modular_backtest.models.abstract import OrderExecution

if TYPE_CHECKING:
    from modular_backtest.backends.allocation import AllocationHandler
    from modular_backtest.types import BarData, Context


class InstantOrderExecution(OrderExecution):
    """Executes orders instantly by converting allocations to target percent orders."""

    def run(
        self, context: Context, data: BarData, allocations: AllocationHandler
    ) -> OrderHandler:
        """Runs the order execution process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            allocations (AllocationHandler): The handler with allocation information.

        Returns:
            OrderHandler: The handler containing the generated orders.
        """
        orders_ = [
            OrderTargetPercent(alloc.asset, alloc.weight) for alloc in allocations
        ]
        return OrderHandler(orders_)
