from collections.abc import Iterator, Sequence
from uuid import UUID, uuid4

from pydantic import ConfigDict, Field, field_validator
from pydantic.dataclasses import dataclass

from modular_backtest.types import Asset, RealNumber

order_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class Order: ...


@dataclass(config=order_config)
class OrderShare(Order):
    """Represents an order to buy or sell a specific number of shares of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        shares (RealNumber): The number of shares to buy or sell.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    shares: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=order_config)
class OrderValue(Order):
    """Represents an order to transact a specific value of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        value (RealNumber): The monetary value of the asset to buy or sell.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    value: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=order_config)
class OrderPercent(Order):
    """Represents an order to transact a percent of the portfolio value of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        percent (RealNumber): The percentage of the portfolio value to buy or sell.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    percent: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=order_config)
class OrderTargetShare(Order):
    """Represents an order to buy or sell a target number of shares of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        target_shares (RealNumber): The target number of shares to reach.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    target_shares: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=order_config)
class OrderTargetValue(Order):
    """Represents an order to buy or sell a target monetary value of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        target_value (RealNumber): The target monetary value to reach.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    target_value: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=order_config)
class OrderTargetPercent(Order):
    """Represents an order to buy or sell a target percentage of the current position of an asset.

    Attributes:
        asset (Asset): The financial asset involved in the order.
        target_percent (RealNumber): The target percentage of the current position to reach.
        uuid (UUID): A unique identifier for the order, automatically generated.
    """

    asset: Asset
    target_percent: RealNumber
    uuid: UUID = Field(default_factory=uuid4)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class OrderHandler:
    """
    A container for a sequence of orders. Provides an interface for iterating,
    checking the length, adding orders, and clearing the container.

    Attributes:
        orders (Sequence[Order]): The sequence of orders in the container.
    """

    orders: Sequence[Order] = Field(default_factory=list)

    @field_validator("orders", mode="after")
    @classmethod
    def _orders_as_list(cls, value: Sequence[Order]) -> list[Order]:
        """
        Converts the orders field to a list in-place.

        Args:
            value (Sequence[Order]): The value to convert.

        Returns:
            list[Order]: The converted value.
        """
        return list(value)

    def __iter__(self) -> Iterator[Order]:
        """
        Returns an iterator over the orders in the container.

        Yields:
            Iterator[Order]: An iterator over the orders.
        """
        return iter(self.orders)

    def __len__(self) -> int:
        """
        Returns the number of orders in the container.

        Returns:
            int: The number of orders.
        """
        return len(self.orders)

    def push(self, order: Order) -> None:
        """
        Adds an order to the container.

        Args:
            order (Order): The order to add.
        """
        self.orders.append(order)  # type: ignore

    def clear(self) -> None:
        """
        Clears the container.
        """
        self.orders.clear()  # type: ignore
