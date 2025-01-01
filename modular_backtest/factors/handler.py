from pydantic.dataclasses import dataclass
from zipline.pipeline.factors import Factor
from pydantic import Field, ConfigDict
from zipline.pipeline import Pipeline

# zipline.pipeline.factors
# pipeline outputs DataFrame with (row, column) -> (asset[Asset], name[str])

# inputs are ordered -> inputs = [EquityPricing.high, EquityPricing.low, EquityPricing.close]
# def compute(self, today, assets, high, low, close)
# each of (high, low, close) are numpy.array with shape (window, len(assets))
# with latest data at the last row -> close[-1]


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class FactorHandler:
    """A container for a collection of :class:`~zipline.pipeline.factors.Factor`.

    Attributes:
        factors (dict[str, ~zipline.pipeline.factors.Factor]): The collection of
            :class:`~zipline.pipeline.factors.Factor`.

    """

    factors: dict[str, Factor] = Field(default_factory=dict)

    def __call__(self) -> Pipeline:
        """Returns a :class:`~zipline.pipeline.Pipeline` from the contained
        :class:`~zipline.pipeline.factors.Factor`.

        Returns:
            ~zipline.pipeline.Pipeline: A :class:`~zipline.pipeline.Pipeline`
                containing the contained :class:`~zipline.pipeline.factors.Factor`.
        """
        return self.make()

    def insert(self, name: str, factor: Factor) -> None:
        """Inserts a :class:`~zipline.pipeline.factors.Factor` into the
        container.

        Args:
            name (str): The name of the :class:`~zipline.pipeline.factors.Factor`.
            factor (~zipline.pipeline.factors.Factor): The
                :class:`~zipline.pipeline.factors.Factor` to insert.
        """
        if name in self.factors:
            raise ValueError(f"Factor {name} already exists")
        self.factors[name] = factor

    def make(self) -> Pipeline:
        """Returns a :class:`~zipline.pipeline.Pipeline` from the contained
        :class:`~zipline.pipeline.factors.Factor`.

        Returns:
            ~zipline.pipeline.Pipeline: A :class:`~zipline.pipeline.Pipeline`
                containing the contained :class:`~zipline.pipeline.factors.Factor`.
        """
        return Pipeline(columns=self.factors)
