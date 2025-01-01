import enum
from collections.abc import Iterator

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from modular_backtest.types import Asset


class SignalSentiment(enum.IntEnum):
    """Represents the sentiment of a signal."""

    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Signal:
    """Represents a trading signal.

    A trading signal is a suggestion to buy or sell an asset.

    Attributes:
        asset (Asset): The asset to which the signal refers.
        sentiment (SignalSentiment): The sentiment of the signal, i.e. whether it is a buy or sell signal.
    """

    asset: Asset = Field(frozen=True)
    sentiment: SignalSentiment = Field()


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class SignalHandler:
    """A container for a sequence of `Signal`s.

    Attributes:
        signals (list[Signal]): The sequence of `Signal`s in the container.

    Returns:
        Iterator[Signal]: An iterator over the signals in the container.
    """

    signals: list[Signal] = Field(default_factory=list)

    def __iter__(self) -> Iterator[Signal]:
        """Returns an iterator over the signals in the container."""
        return iter(self.signals)

    def __len__(self) -> int:
        """Returns the number of signals in the container."""
        return len(self.signals)

    def is_empty(self) -> bool:
        """Returns True if there are no signals in the container."""
        return len(self.signals) == 0

    def push(self, signal: Signal) -> None:
        """Adds a signal to the container."""
        self.signals.append(signal)

    def clear(self) -> None:
        """Clears all signals from the container."""
        self.signals.clear()
