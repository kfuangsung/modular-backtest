from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modular_backtest.backends import (
        AllocationHandler,
        AssetHandler,
        OrderHandler,
        SignalHandler,
    )
    from modular_backtest.types import BarData, Context


class AssetSelection(ABC):
    """Abstract base class for asset selection strategies.

    Asset selection strategies are used to select the assets to be traded based on
    the given data.

    Attributes:
        None

    Methods:
        run(context: Context, data: BarData) -> AssetHandler:
            Runs the asset selection process.

    Raises:
        None
    """

    @abstractmethod
    def run(self, context: Context, data: BarData) -> AssetHandler:
        """Runs the asset selection process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.

        Returns:
            AssetHandler: The handler containing the selected assets.
        """


class SignalGeneration(ABC):
    """Abstract base class for signal generation strategies.

    Signal generation strategies are responsible for generating signals based
    on the given data and assets.

    Attributes:
        None

    Methods:
        run(context, data, assets):
            Runs the signal generation process.

    Raises:
        None
    """

    @abstractmethod
    def run(
        self, context: Context, data: BarData, assets: AssetHandler
    ) -> SignalHandler:
        """Runs the signal generation process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            assets (AssetHandler): The assets of the algorithm.

        Returns:
            SignalHandler: The handler containing the generated signals.
        """
        pass


class PortfolioConstruction(ABC):
    """Abstract base class for portfolio construction strategies.

    Portfolio construction strategies are used to convert signals into
    allocations based on the given data.

    Attributes:
        None

    Methods:
        run(context, data, signals):
            Runs the portfolio construction process.

    Raises:
        None
    """

    @abstractmethod
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


class RiskManagement(ABC):
    """Abstract base class for risk management strategies.

    Risk management strategies are used to adjust the allocations based on
    the given context and data.

    Methods:
        run(context, data, allocations):
            Runs the risk management process.
    """

    @abstractmethod
    def run(
        self, context: Context, data: BarData, allocations: AllocationHandler
    ) -> AllocationHandler:
        """Runs the risk management process.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            allocations (AllocationHandler): The handler with allocation information.

        Returns:
            AllocationHandler: The handler containing the adjusted allocations.
        """
        pass


class OrderExecution(ABC):
    """Abstract base class for order execution strategies.

    Order execution strategies are used to execute the generated allocations.

    Args:
        context (Context): The context of the algorithm.
        data (BarData): The data of the algorithm.
        allocations (AllocationHandler): The handler with allocation information.

    Returns:
        OrderHandler: The handler containing the generated orders.
    """

    @abstractmethod
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
