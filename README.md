# Modular Backtest: A Backtesting Framework for Algorithmic Trading

![logo](https://raw.githubusercontent.com/kfuangsung/modular-backtest/refs/heads/main/docs/_static/original.png)

## About the project

Modular Backtest is a Python-based backtesting framework for algorithmic trading, designed with a strong emphasis on modularity and reusability. Built on top of [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded), a Pythonic algorithmic trading library, it provides a flexible foundation for developing and testing trading strategies.

The framework is organized into the following modules, each addressing a specific aspect of the backtesting process:

- **Asset selection**<br>
    Selects the assets to be included in the trading universe.

- **Signal generation**<br>
    Generates sentiment signals for the selected assets.

- **Portfolio construction**<br>
    Constructs portfolio allocations based on the generated signals.

- **Risk managements**<br>
    Adjusts portfolio allocations to manage risk effectively.

- **Order execution**<br>
    Creates buy/sell orders based on the constructed allocations.

- **Data**<br>
    Downloads and ingests historical equity price data via public APIs. Currently, it supports [Yahoo Finance](https://github.com/ranaroussi/yfinance).

- **Factors**<br>
    Computes statistics and technical indicators commonly used in trading.


## Getting started


### Installation

```bash
pip install modular-backtest
```

### Data ingestion 

After installed, add the line `from modular_backtest.data.bundles import yahoo` to `~/.zipline/extension.py` and then run
```bash
zipline ingest -b yahoo-finance
```

### Usages 

```python
from datetime import datetime
import pandas as pd
from modular_backtest.data.bundles import yahoo
from modular_backtest.engine import BacktestEngine
from modular_backtest.factors.handler import FactorHandler
from modular_backtest.models.asset_selection import ManualAssetSelection
from modular_backtest.models.handler import ModelHandler
from modular_backtest.models.order_execution import InstantOrderExecution
from modular_backtest.models.portfolio_construction import (
    EqualWeightPortfolioConstruction,
)
from modular_backtest.models.risk_management import VoidRiskManagement
from modular_backtest.models.signal_generation import StaticSignalGeneration

models = ModelHandler(
    ManualAssetSelection(["AAPL", "MSFT", "AMZN", "SPY", "QQQ"]),
    StaticSignalGeneration(),
    EqualWeightPortfolioConstruction(),
    InstantOrderExecution(),
    VoidRiskManagement(),
)

engine = BacktestEngine(models=models, factors=FactorHandler())

res = engine.run(
    start=datetime(2024, 1, 1), end=datetime(2024, 12, 31), bundle=yahoo.NAME
)

res.data.portfolio_value
# |                           |   portfolio_value |
# |:--------------------------|------------------:|
# | 2024-01-02 21:00:00+00:00 |          100000   |
# | 2024-01-03 21:00:00+00:00 |           99852.6 |
# | 2024-01-04 21:00:00+00:00 |           98775.5 |
# | 2024-01-05 21:00:00+00:00 |           98826.4 |
# | 2024-01-08 21:00:00+00:00 |          100890   |
# | 2024-01-09 21:00:00+00:00 |          101222   |
# | 2024-01-10 21:00:00+00:00 |          102281   |
# | 2024-01-11 21:00:00+00:00 |          102544   |
# | 2024-01-12 21:00:00+00:00 |          102735   |
# | 2024-01-16 21:00:00+00:00 |          102308   |
# | 2024-01-17 21:00:00+00:00 |          101740   |
# | 2024-01-18 21:00:00+00:00 |          103333   |
# | 2024-01-19 21:00:00+00:00 |          104815   |
# | 2024-01-22 21:00:00+00:00 |          104953   |
# | 2024-01-23 21:00:00+00:00 |          105534   |
# | 2024-01-24 21:00:00+00:00 |          105908   |
# | 2024-01-25 21:00:00+00:00 |          106253   |
# | 2024-01-26 21:00:00+00:00 |          106046   |
# | 2024-01-29 21:00:00+00:00 |          106948   |
# | 2024-01-30 21:00:00+00:00 |          106023   |
# | 2024-01-31 21:00:00+00:00 |          103769   |
# | 2024-02-01 21:00:00+00:00 |          105433   |
# | 2024-02-02 21:00:00+00:00 |          107957   |
# ...
# | 2024-12-26 21:00:00+00:00 |          135358   |
# | 2024-12-27 21:00:00+00:00 |          133499   |
# | 2024-12-30 21:00:00+00:00 |          131844   |
# | 2024-12-31 21:00:00+00:00 |          130903   |
```

### [Documentation](https://kfuangsung.github.io/modular-backtest/)

## License 

Distributed under the MIT License. See [`LICENSE`](https://github.com/kfuangsung/modular-backtest/blob/main/LICENSE) for more information.


## Maintainers

[modular-backtest](https://github.com/kfuangsung/modular-backtest) is currently maintained by [kfuangsung](https://github.com/kfuangsung) (kachain.f@outlook.com).

## Acknowledgments

- [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded): A Pythonic Algorithmic Trading Library (forked from [quantopian/zipline](https://github.com/quantopian/zipline))

## Disclaimer

Please  remember  that  past  performance  may  not  be  indicative  of  future  results.  Different  types  of 
investments involve varying degrees of risk, and there can be no assurance that the future performance 
of any specific investment, investment strategy, or product made reference to directly or indirectly in this 
page, will be profitable, equal any corresponding indicated historical performance level(s), 
or be suitable for your portfolio.

The hypothetical backtested performance does not represent the results of actual trading and does not and is not intended to indicate the past performance or future performance of investment strategy.

The hypothetical backtested performance results for each strategy include estimated values for transaction costs of buying and selling securities, which may not be accurate. Investment management fees (including without limitation management fees and performance fees), custody and other costs, and taxes are not included in performance results.

The hypothetical performance does not reflect the reinvestment of dividends and distributions therefrom, interest, capital gains and withholding taxes. 

Simulated returns may be dependent on the market and economic conditions that existed during the period. Future market or economic conditions can adversely affect the returns. 