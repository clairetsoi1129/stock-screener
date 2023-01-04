import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
# import pandas_datareader as web
from yahoo_fin import stock_info as si
import datetime as dt
import pandas as pd
import os

def download_yf_data(ticker, start, end):
    # df = web.DataReader(ticker, 'yahoo', start, end)
    df = pdr.get_data_yahoo(ticker, start, end)
    if not os.path.exists(f'stock_data'):
        os.makedirs("stock_data")
    df.to_csv(f'stock_data/{ticker}.csv')

def download_1year_data_by_tickers(tickers):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    download_yf_data(tickers, start, end)

def download_1year_data(ticker):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()
    download_yf_data(ticker, start, end)

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
    ticker_df = pd.read_csv("data/hsi_tickers.csv")
    tickers = ticker_df['代號'].values.tolist()
    return tickers

def tickers_gsptse():
    ticker_df = pd.read_csv("data/gsptse_tickers.csv")
    tickers = ticker_df['Ticker'].values.tolist()
    print(tickers)
    return tickers
