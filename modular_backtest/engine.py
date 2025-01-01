from collections.abc import Callable
from datetime import datetime
import pandas as pd
import zipline.api as algo
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from zipline import run_algorithm
from zipline.finance.commission import CommissionModel
from zipline.finance.slippage import SlippageModel

from .backends.commission import PerDollar
from .backends.slippage import VolumeShareSlippage
from .factors.handler import FactorHandler
from .models.handler import ModelHandler
from .result import BacktestResult
from .types import BarData, Context, RealNumber

type InitializeFunction = Callable[[Context], None]
type HandleDataFunction = Callable[[Context, BarData], None]
type BeforeTradingStartFunction = Callable[[Context, BarData], None]
type AnalyzeFunction = Callable[[Context, pd.DataFrame], None]


def make_initialize(
    models: ModelHandler,
    factors: FactorHandler,
    commission: CommissionModel,
    slippage: SlippageModel,
    benchmark: str | None = None,
) -> InitializeFunction:
    """
    Creates a Zipline initialize function that sets up a pipeline with the given factors,
    sets the given commission and slippage models, and schedules the given models to be
    called every day.

    Args:
        models: The models to be scheduled.
        factors: The factors to be used in the pipeline.
        commission: The commission model to be used.
        slippage: The slippage model to be used.
        benchmark: The benchmark asset to be used, or None to not use a benchmark.

    Returns:
        An initialize function that sets up the given models and pipeline.
    """

    def initialize(context: Context) -> None:
        algo.attach_pipeline(factors(), "factors")
        if benchmark is not None:
            algo.set_benchmark(algo.symbol(benchmark))
        algo.set_commission(commission)
        algo.set_slippage(slippage)
        algo.schedule_function(models)

    return initialize


def make_before_trading_start() -> BeforeTradingStartFunction:
    """
    Creates a Zipline before_trading_start function that fetches the factors
    from the pipeline and stores them in the context.

    Returns:
        A before_trading_start function that fetches the factors.
    """

    def before_trading_start(context: Context, data: BarData) -> None:
        factors = algo.pipeline_output("factors")
        context.factors = factors

    return before_trading_start


class BacktestEngine(BaseModel):
    """Runs a backtest of a given set of models.

    The models are scheduled to run every day, and the results are stored in a
    BacktestResult object.

    Args:
        models: The models to be scheduled.
        factors: The factors to be used in the pipeline.
        capital: The starting capital for the backtest.
        commission: The commission model to be used.
        slippage: The slippage model to be used.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    models: ModelHandler
    factors: FactorHandler
    capital: RealNumber = Field(default=100_000)
    commission: CommissionModel = Field(default_factory=PerDollar)
    slippage: SlippageModel = Field(default_factory=VolumeShareSlippage)
    _initialize: InitializeFunction = PrivateAttr()
    _before_trading_start: BeforeTradingStartFunction = PrivateAttr()

    def _make_functions(self):
        """
        Initializes the _initialize and _before_trading_start functions.

        Sets up the functions used for initialization and actions
        before trading starts in the backtest. These functions are
        generated using the provided models, factors, commission, and
        slippage settings.
        """

        self._initialize = make_initialize(
            self.models, self.factors, self.commission, self.slippage
        )
        self._before_trading_start = make_before_trading_start()

    def run(
        self, start: datetime, end: datetime, bundle: str = "quandl"
    ) -> BacktestResult:
        """Runs the backtest.

        Args:
            start: The start date of the backtest.
            end: The end date of the backtest.
            bundle: The data bundle to use. Defaults to "quandl".

        Returns:
            A BacktestResult object containing the results of the backtest.
        """
        assert start < end, "`start` must be before `end`"
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        self._make_functions()
        out = run_algorithm(
            start=start,
            end=end,
            initialize=self._initialize,
            before_trading_start=self._before_trading_start,
            capital_base=self.capital,
            bundle=bundle,
        )
        return BacktestResult.from_zipline_output(out)
