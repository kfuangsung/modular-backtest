from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, override

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from modular_backtest.backends.api import symbols
from modular_backtest.backends.asset import AssetHandler
from modular_backtest.models.abstract import AssetSelection

if TYPE_CHECKING:
    from modular_backtest.types import BarData, Context


@dataclass
class ManualAssetSelection(AssetSelection):
    """
    An asset selection strategy that selects symbols from those passed in the
    constructor.

    Attributes:
        symbols (Iterable[str]): The symbols to select.
    """

    symbols: Iterable[str]

    @field_validator("symbols", mode="after")
    @classmethod
    def _symbols_to_list(cls, v: Iterable[str]) -> list[str]:
        return list(v)

    @override
    def run(self, context: Context, data: BarData) -> AssetHandler:
        """Select the assets based on the symbols passed in the constructor.

        Args:
            context (Context): The context of the algorithm.
            data (BarData): The data of the algorithm.

        Returns:
            AssetHandler: The selected assets.
        """
        return AssetHandler(assets=symbols(*self.symbols))
