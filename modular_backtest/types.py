from zipline.assets._assets import Asset
from zipline.protocol import BarData

type RealNumber = int | float
type OrderId = str | None

context_not_impl_msg = (
    "The Context class is only used for type hints for autocomplete and cannot be "
    "used directly, please use the `context` object passed to initialize(), "
    "handle_data(), before_trading_start(), and scheduled functions."
)


class Context:
    """Context class for the backtest engine.

    This class is used only for type hints and cannot be used directly. Please use
    the `context` object passed to `initialize()`, `handle_data()`,
    `before_trading_start()`, and scheduled functions.

    Attributes:
        recorded_vars: A dictionary of recorded variables.
        portfolio: The portfolio object.
        account: The account object.
    """

    def __init__(self):
        raise NotImplementedError(context_not_impl_msg)

    def __setattr__(self, name, value):
        raise NotImplementedError(context_not_impl_msg)

    def __getattr__(self, name):
        raise NotImplementedError(context_not_impl_msg)

    @property
    def recorded_vars(self):
        raise NotImplementedError(context_not_impl_msg)

    @property
    def portfolio(self):
        raise NotImplementedError(context_not_impl_msg)

    @property
    def account(self):
        raise NotImplementedError(context_not_impl_msg)


__all__ = ["BarData", "Asset", "Context", "RealNumber", "OrderId"]
