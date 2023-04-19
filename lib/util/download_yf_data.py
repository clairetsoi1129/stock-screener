import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
# import pandas_datareader as web
from yahoo_fin import stock_info as si
import datetime as dt
import pandas as pd
import os

def download_yf_data(market,ticker, start, end):
    # df = web.DataReader(ticker, 'yahoo', start, end)
    print(f"**ticker:{ticker}")
    df = pdr.get_data_yahoo(ticker, start, end)
    if not os.path.exists(f'stock_data/{market}'):
        os.makedirs(f'stock_data/{market}')
    df.to_csv(f'stock_data/{market}/{ticker}.csv')

def download_1year_data_by_tickers(market,tickers):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    download_yf_data(market,tickers, start, end)

def download_1year_data(market,ticker):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    download_yf_data(market, ticker, start, end)

def find_tickers_by_benchmark(benchmark_ticker):
    if (benchmark_ticker == '^HSI'):
        benchmark_tickers = tickers_hsi()
    elif (benchmark_ticker == '^GSPTSE'):
        benchmark_tickers = tickers_gsptse()
    elif (benchmark_ticker == '^FTSE'):
        benchmark_tickers = si.tickers_ftse100()
        benchmark_tickers = [sub + ".L" for sub in benchmark_tickers]
    else:
        benchmark_tickers = si.tickers_sp500()
    return benchmark_tickers

def tickers_hsi():
    ticker_df = pd.read_csv("data/hk/benchmark_tickers.csv")
    tickers = ticker_df['代號'].values.tolist()
    return tickers

def tickers_gsptse():
    ticker_df = pd.read_csv("data/ca/benchmark_tickers.csv")
    tickers = ticker_df['Ticker'].values.tolist()
    print(tickers)
    return tickers

def tickers_us():
    benchmark_tickers = []
    benchmark_tickers.extend(si.tickers_sp500())
    benchmark_tickers.extend(si.tickers_dow())
    benchmark_tickers.extend(si.tickers_nasdaq())
    benchmark_tickers = list(dict.fromkeys(benchmark_tickers))

    df = pd.DataFrame(benchmark_tickers, columns=["Ticker"])
    df.to_csv('data/us/vcp_watchlist.csv', index=False)

tickers_us()
