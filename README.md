# Stock Screener

This Volatility Contraction Pattern (VCP) screener was created with Python version 3.9 using yahoo finance API.

It will go through a list of stocks from benchmark stocks and watchlist stocks to look for high performance stocks with Volatility Contraction Pattern (VCP).

## Pre-requisite

1. Install the below package by following commands

```
  pip3 install pandas yfinance pandas-datareader yahoo_fin
  pip3 install scipy # for calculate slop
  pip3 install plotly # for plot graph
  pip3 install tqdm # show progress bar when running
  pip3 install futures # concurrent programming

```

2. Create a sub-folders.  
 - "data" to store the watchlist and tickers that cannot be found using api
 - "output" to store the 

## How to run the program

1. To trigger alpha vantage version, run the below

```
  python3 vcp_stock_screener.py 

```

2. This program will combine the watchlist stocks with the benchmark stocks to look for the top 30% high performance stocks and see which stocks has Volatility Contraction Pattern (VCP) pattern. 

3. After the program completed, it will generate the stock chart of the stocks which fulfill VCP requirement in output folder. 

## To-do
1. Rewrite the backtest
2. Extend to include DOW and NASDAQ and ^GSPTSE in benchmark
3. Change the watchlist to include more stocks in different markets


## Disclaimer


# stock-screener
