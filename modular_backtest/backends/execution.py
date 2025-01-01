import zipline.api as algo
from multimethod import multimethod

from modular_backtest.backends.order import (
    Order,
    OrderPercent,
    OrderShare,
    OrderTargetPercent,
    OrderTargetShare,
    OrderTargetValue,
    OrderValue,
)
from modular_backtest.types import OrderId
from modular_backtest.backends.order import OrderHandler


@multimethod
def execute_order(order: Order) -> NotImplementedError:
    """Executes an order.

    Args:
        order: The order to execute.

    Returns:
        The order id of the executed order.

    Raises:
        NotImplementedError: If the order type is not known.
    """
    return NotImplementedError("Unknown order type")


@execute_order.register  # type: ignore
def _(order: OrderShare) -> OrderId:
    return algo.order(order.asset, order.shares)


@execute_order.register  # type: ignore
def _(order: OrderValue) -> OrderId:
    return algo.order_value(order.asset, order.value)


@execute_order.register  # type: ignore
def _(order: OrderPercent) -> OrderId:
    return algo.order_percent(order.asset, order.percent)


@execute_order.register  # type: ignore
def _(order: OrderTargetShare) -> OrderId:
    return algo.order_target(order.asset, order.target_shares)


@execute_order.register  # type: ignore
def _(order: OrderTargetValue) -> OrderId:
    return algo.order_target_value(order.asset, order.target_value)


@execute_order.register  # type: ignore
def _(order: OrderTargetPercent) -> OrderId:
    return algo.order_target_percent(order.asset, order.target_percent)


@execute_order.register  # type: ignore
def _(order: OrderHandler) -> None:
    for ord_ in order:
        execute_order(ord_)
