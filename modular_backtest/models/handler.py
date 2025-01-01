from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from modular_backtest.backends.execution import execute_order
from modular_backtest.models.abstract import (
    AssetSelection,
    OrderExecution,
    PortfolioConstruction,
    RiskManagement,
    SignalGeneration,
)
from modular_backtest.types import BarData, Context


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class ModelHandler:
    """A handler class for the components of the trading algorithm.

    This class wraps the components of the trading algorithm and provides a
    convenient interface to run the algorithm.

    Attributes:
        asset_selection (AssetSelection): The asset selection strategy.
        signal_generation (SignalGeneration): The signal generation strategy.
        portfolio_construction (PortfolioConstruction): The portfolio construction
            strategy.
        order_execution (OrderExecution): The order execution strategy.
        risk_management (RiskManagement): The risk management strategy.

    Methods:
        __call__(context, data): Runs the algorithm by calling the run method.
        run(context, data): Runs the algorithm by calling each component's run
            method.
    """

    asset_selection: AssetSelection
    signal_generation: SignalGeneration
    portfolio_construction: PortfolioConstruction
    order_execution: OrderExecution
    risk_management: RiskManagement

    def __call__(self, context: Context, data: BarData) -> None:
        """Runs the algorithm by calling the run method.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
        """
        self.run(context, data)

    def run(
        self,
        context: Context,
        data: BarData,
    ) -> None:
        """Runs the algorithm by calling each component's run method.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
        """
        assets = self.asset_selection.run(context, data)
        signals = self.signal_generation.run(context, data, assets)
        allocations = self.portfolio_construction.run(context, data, signals)
        allocations = self.risk_management.run(context, data, allocations)
        orders = self.order_execution.run(context, data, allocations)
        execute_order(orders)
