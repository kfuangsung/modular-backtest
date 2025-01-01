from collections.abc import Iterator

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from modular_backtest.types import Asset


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Allocation:
    """Represents an allocation of a specific asset with a given weight.

    Attributes:
        asset (Asset): The asset being allocated.
        weight (int or float): The weight of the allocation, can be an integer or float.
    """
    asset: Asset = Field(frozen=True)
    weight: int | float = Field()


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class AllocationHandler:
    """Handles a collection of Allocation objects.

    Attributes:
        allocs (list[Allocation]): A list of Allocation objects.
    """

    allocs: list[Allocation] = Field(default_factory=list)

    def __iter__(self) -> Iterator[Allocation]:
        """Returns an iterator over the allocations.

        Returns:
            Iterator[Allocation]: An iterator over the Allocation objects.
        """
        return iter(self.allocs)

    def push(self, alloc: Allocation) -> None:
        """Adds an Allocation to the handler.

        Args:
            alloc (Allocation): The Allocation to be added.
        """
        self.allocs.append(alloc)

    def clear(self) -> None:
        """Clears all allocations from the handler."""
        self.allocs.clear()
