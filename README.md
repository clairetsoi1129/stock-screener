# Stock Screener

This Volatility Contraction Pattern (VCP) screener was created with Python version 3.9 using yahoo finance API.

It will go through a list of stocks from benchmark stocks and watchlist stocks to look for high performance stocks with Volatility Contraction Pattern (VCP).

## Pre-requisite

1. Install the below package by following commands

> setup virtual environment
```
  python3 -m venv env
  source env/bin/activate
```

> get stock data from yfinance
```
  python3 -m pip install pandas yfinance pandas-datareader yahoo_fin
```

> calculate slope
```
  python3 -m pip install scipy 
```

> for plot graph
```
  python3 -m pip install plotly
```

> show progress bar when running
```
  python3 -m pip install tqdm 
```

> concurrent programming
```
  python3 -m pip install futures 
```

2. Create a sub-folders.  
 - "data" to store the watchlist and tickers that cannot be found using yahoo_fin.stock_info API
 - "output" to store the stocks which fulfill the VCP patterns

## How to run the program

1. Run the below

```
  python3 vcp_stock_screener.py 
```

2. This program will combine the watchlist stocks with the benchmark stocks to look for the top 30% high performance stocks and see which stocks has Volatility Contraction Pattern (VCP) pattern. 

3. After the program completed, it will generate the stock chart of the stocks which fulfill VCP requirement in output folder. 

## To-do
1. Rewrite the backtest
2. Change the watchlist to include more stocks in different markets
3. Migrate to DB instead of rely on yfinance data

## Disclaimer
- DO NOT use the result provided by the software 'solely' to make your trading decisions.
- Always backtest and analyze the stocks manually before you trade.
- The Author and the software will not be held liable for your losses.
