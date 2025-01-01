from __future__ import annotations

from typing import TYPE_CHECKING, override

from pydantic import Field
from pydantic.dataclasses import dataclass

from modular_backtest.backends.signal import (
    Signal,
    SignalHandler,
    SignalSentiment,
)
from modular_backtest.models.abstract import SignalGeneration

if TYPE_CHECKING:
    from modular_backtest.backends.asset import AssetHandler
    from modular_backtest.types import BarData, Context


@dataclass
class StaticSignalGeneration(SignalGeneration):
    """
    A signal generation strategy that generates a constant signal for each asset.

    Attributes:
        sentiment (SignalSentiment): The sentiment of the signal. Defaults to
            SignalSentiment.NEUTRAL.
    """

    sentiment: SignalSentiment = Field(default=SignalSentiment.NEUTRAL)

    @override
    def run(
        self, context: Context, data: BarData, assets: AssetHandler
    ) -> SignalHandler:
        """
        Generates a constant signal for each asset.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.
            assets (AssetHandler): The assets of the algorithm.

        Returns:
            SignalHandler: The handler containing the generated signals.
        """
        signals_ = [Signal(asset=asset, sentiment=self.sentiment) for asset in assets]

        return SignalHandler(signals=signals_)
