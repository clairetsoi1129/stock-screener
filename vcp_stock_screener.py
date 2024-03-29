import pandas as pd #data manipulation and analysis package
import os
import sys

import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
from yahoo_fin import stock_info as si
import datetime as dt
import concurrent.futures
from tqdm import tqdm

from lib.util.download_yf_data import *
from lib.util.graph_util import *

def filter_stocks_by_rs_rating(market, benchmark_ticker, other_tickers, percentile):
    start = dt.datetime.now() - dt.timedelta(days=365)
    end = dt.datetime.now()

    # Calculate the benchmark returns in the period, currently support HSI and S&P500 
    benchmark_df = pdr.get_data_yahoo(benchmark_ticker, start, end)
    benchmark_df['Pct Change'] = benchmark_df['Close'].pct_change()
    benchmark_return = (benchmark_df['Pct Change'] + 1).cumprod()[-1]

    # Calculate the RS rating
    benchmark_tickers = find_tickers_by_benchmark(benchmark_ticker)

    #download the stock history if not done before
    tickers = benchmark_tickers + other_tickers
    tickers = list(dict.fromkeys(tickers))
    for ticker in tickers:
        if not os.path.exists(f'stock_data/{market}/{ticker}.csv'):
            print(f'benchmark - stock_data/{market}/{ticker}.csv')
            download_1year_data(market, str(ticker))

    return_list = []
    for ticker in tickers:
        try:
            df = pd.read_csv(f'stock_data/{market}/{ticker}.csv', index_col=0)
            df['Pct Change'] = df['Close'].pct_change()
            stock_return = (df['Pct Change']+1).cumprod()[-1]
            returns_compared = round((stock_return / benchmark_return), 2)
            return_list.append(returns_compared)
        except:
            print(f'loop - stock_data/{market}/{ticker}.csv')

    # Creating dataframe of only top 30%
    rs_df = pd.DataFrame(list(zip(tickers, return_list)), columns=['Ticker', 'Returns Compared With Benchmark'])
    rs_df['RS_Rating'] = rs_df['Returns Compared With Benchmark'].rank(pct=True) * 100
    rs_df = rs_df[rs_df['RS_Rating'] >= rs_df['RS_Rating'].quantile(percentile)]
    return rs_df

def filter_by_vcp_conditions(df):
    moving_averages = [10, 20, 30, 50, 150, 200]
    for ma in moving_averages:
        df['SMA_' + str(ma)] = round(df['Close'].rolling(window=ma).mean(), 2)
    df['Avg_vol_50'] = round(df['Volume'].rolling(window=50).mean(), 2)
    df['SMA_slope_30'] = df['SMA_30'].rolling(window = 20).apply(cal_slope)
    df['SMA_slope_200'] = df['SMA_200'].rolling(window = 20).apply(cal_slope)
    df['52_week_low'] = df['Close'].rolling(window = 5*52).min()
    df['52_week_high'] = df['Close'].rolling(window = 5*52).max()
    # latest_price = df['Close'][-1]
    # quote = si.get_quote_table(ticker)
    # val = si.get_stats_valuation(ticker)
    # pe_ratio = float(quote['PE Ratio (TTM)'])
    # peg_ratio = float(val[1][4])
    # market_cap = convert_market_cap_to_mil(quote['Market Cap'])
    # score = round(top_performer_df[top_performer_df['Ticker'] == ticker]['Score'].tolist()[0])

    # Condition 1: Price > 150 MA & 200 MA
    df['Condition1'] = (df['Close'] > df['SMA_150']) & (df['Close'] > df['SMA_200']) 
    # Condition 2: 150 MA > 200 MA
    df['Condition2'] = (df['SMA_150'] > df['SMA_200']) 
    # Condition 3: 200 MA trending up for at least 1 month
    df['Condition3'] = df['SMA_slope_200'] > 0.0
    # Condition 4: 50 MA > 150 MA & 200 MA
    df['Condition4'] = (df['SMA_50'] > df['SMA_150']) & (df['SMA_150'] > df['SMA_200']) 
    # Condition 5: Price > 50MA as the stock is coming out of a base (Not sure how to calculate base)
    df['Condition5'] = (df['Close'] > df['SMA_50'])
    # Condition 6: Price > 52-week low + 25%
    df['Condition6'] = (df['Close'] > df['52_week_low']* 1.25) 
    # Condition 7: Price > 52-week high - 25%
    df['Condition7'] = (df['Close'] > df['52_week_high']* 0.75) 
    # Condition 8: Pivot (5 day) Breakout
    winsize = 5
    df['Condition8'] = df['Close'] > ((df['Close']).rolling(window=winsize).mean()+ (df['Close']).rolling(window=winsize).max() + (df['Close']).rolling(window=winsize).min())/3 
    # Condition 9: Contraction below 10%
    for handlesize in range(5, 41): # handlesize can be 5 days to 40 days (2 months)
        df[f'Condition9.{handlesize}'] = (( df['Close']).rolling(window=handlesize).max() - (df['Close']).rolling(window=handlesize).min()) / (df['Close']).rolling(window=handlesize).min() < 0.1
    
    df['Condition9'] = df[['Condition9.5','Condition9.6','Condition9.7','Condition9.8','Condition9.9','Condition9.10',
        'Condition9.11','Condition9.12','Condition9.13', 'Condition9.14','Condition9.15','Condition9.16',
        'Condition9.17','Condition9.18','Condition9.19', 'Condition9.20','Condition9.21','Condition9.22',
        'Condition9.23','Condition9.24','Condition9.25', 'Condition9.26','Condition9.27','Condition9.28',
        'Condition9.29','Condition9.30','Condition9.31', 'Condition9.32','Condition9.33','Condition9.34',
        'Condition9.35','Condition9.36','Condition9.37', 'Condition9.38','Condition9.39','Condition9.40'
        ]].any(axis='columns')
    
    df['Has_fulfilled'] = df[['Condition1','Condition2','Condition3','Condition4','Condition5','Condition6','Condition7','Condition8','Condition9']].all(axis='columns')

    return df[['Close','Has_fulfilled']]
    # return df

def scanning_wrapper(ticker_string):
    ticker = yf.Ticker(ticker_string)
    ticker_history = ticker.history(period = 'max')
    
    data = filter_by_vcp_conditions(ticker_history)
    if data['Has_fulfilled'].tail(1).iloc[0] == True:
        print(ticker_string)
        print(data)
        url = plot_stock_chart(ticker_string, ticker_history, True)
        summarise = backtest(data)
        return {'stock': ticker_string, 'analysis': summarise, 'chart': url}
    return {'stock': ticker_string, 'analysis': None, 'chart': None}

def backtest(df_i):
    df = pd.DataFrame()
    df['Has_fulfilled'] = df_i['Has_fulfilled']

    # Find the N days later price
    df['Future_Close_1d'] = df_i['Close'].shift(periods = -1)
    df['Future_Close_3d'] = df_i['Close'].shift(periods = -3)
    df['Future_Close_5d'] = df_i['Close'].shift(periods = -5)
    df['Future_Close_7d'] = df_i['Close'].shift(periods = -7)

    # Back test the profit/loss made if we sell after 1, 3, 5, 7 days
    df['Result_1d'] = ( df['Future_Close_1d'] - df_i['Close']) / df_i['Close']
    df['Result_3d'] = ( df['Future_Close_3d'] - df_i['Close']) / df_i['Close']
    df['Result_5d'] = ( df['Future_Close_5d'] - df_i['Close']) / df_i['Close']
    df['Result_7d'] = ( df['Future_Close_7d'] - df_i['Close']) / df_i['Close']

    vcp_date = df[df['Has_fulfilled'] == True]
    print(vcp_date[['Result_1d','Result_3d','Result_5d','Result_7d']])

    # Show the statistics data, focus on 'mean' which represent how much profit/loss 
    # we make on average when selling the stock after N days 
    print(vcp_date[['Result_1d','Result_3d','Result_5d','Result_7d']].describe())
    return vcp_date

def quick_scan(ticker_list):
    with concurrent.futures.ProcessPoolExecutor(max_workers = 1) as executor:
        data_list= list(tqdm(executor.map(scanning_wrapper, ticker_list), total=len(ticker_list)))
    return data_list

def main():
    market = "ca" # choose from "hk","us","uk","ca"
    if (market == "hk"):
        benchmark_tickers = '^HSI'
    elif (market == "uk"):
        benchmark_tickers = '^FTSE'
    elif (market == "us"):
        benchmark_tickers = '^GSPC' #'^DJI','^NDX'
    elif (market == "ca"):
        benchmark_tickers = '^GSPTSE'
    else:
        sys.exit("Market not supported!")   

    try:
        watchlist_tickers_df = pd.read_csv(f"data/{market}/vcp_watchlist.csv")
        watchlist_tickers_list = watchlist_tickers_df['Ticker'].values.tolist()
    except:
        watchlist_tickers_list = []

    # Condition 0: Filter stocks by RS rating > 70
    tickers_df = filter_stocks_by_rs_rating(market, benchmark_tickers, watchlist_tickers_list, 0.70)
    tickers_list = tickers_df['Ticker'].values.tolist()
    quick_scan(tickers_list)

if __name__ == '__main__':
    main()