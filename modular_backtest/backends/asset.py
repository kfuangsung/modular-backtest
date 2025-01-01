from collections.abc import Iterator

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from modular_backtest.types import Asset


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class AssetHandler:
    """A handler for managing a collection of assets.

    Attributes:
        assets (list[Asset]): A list of assets managed by the handler.
    """

    assets: list[Asset] = Field(default_factory=list)

    def __iter__(self) -> Iterator[Asset]:
        """Return an iterator over the assets.

        Returns:
            Iterator[Asset]: An iterator over the assets in the handler.
        """
        return iter(self.assets)

    def __len__(self) -> int:
        """Return the number of assets in the handler.

        Returns:
            int: The number of assets.
        """
        return len(self.assets)

    def is_empty(self) -> bool:
        """Check if the handler has no assets.

        Returns:
            bool: True if there are no assets, False otherwise.
        """
        return len(self.assets) == 0

    def push(self, asset: Asset) -> None:
        """Add an asset to the handler.

        Args:
            asset (Asset): The asset to be added.
        """
        self.assets.append(asset)

    def clear(self) -> None:
        """Remove all assets from the handler."""
        self.assets.clear()
