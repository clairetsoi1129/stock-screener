from scipy.stats import linregress
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def plot_stock_chart(ticker, hist, save):
    # stock = finvizfinance(ticker)
    # print(stock.TickerCharts())
    # display(Image(url=stock.TickerCharts()))
    hist['diff'] = hist['Close'] - hist['Open']
    hist.loc[hist['diff']>=0, 'color'] = 'green'
    hist.loc[hist['diff']<0, 'color'] = 'red'
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={'color':hist['color']}),secondary_y=True)
    fig.add_trace(go.Candlestick(x=hist.index,
                                open=hist['Open'],
                                high=hist['High'],
                                low=hist['Low'],
                                close=hist['Close'],
                                ))
    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=20).mean(),marker_color='orange',name='20 Day MA'))
    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=50).mean(),marker_color='yellow',name='50 Day MA'))
    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=150).mean(),marker_color='purple',name='150 Day MA'))
    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=200).mean(),marker_color='blue',name='200 Day MA'))
    # fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'),secondary_y=True)
    fig.update_layout(title={'text':ticker, 'x':0.5})
    fig.update_yaxes(range=[0,1000000000],secondary_y=True)
    fig.update_yaxes(visible=False, secondary_y=True)
    fig.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
    fig.update_xaxes(rangebreaks = [
                       dict(bounds=['sat','mon']), # hide weekends
                       #dict(bounds=[16, 9.5], pattern='hour'), # for hourly chart, hide non-trading hours (24hr format)
                       dict(values=["2021-12-25","2022-01-01"]) #hide Xmas and New Year
                                ])
    fig.show()

    if save:
        if not os.path.exists(f'output'):
            os.makedirs("output")

        saved_html = f'output/{ticker}.html'
        fig.write_html(saved_html)
        return saved_html
    return ""

def cal_slope(arr):
    y = np.array(arr)
    x = np.arange(len(y))
    slope, intercept, rvalue, pvalue, stderr = linregress(x,y)
    return slope

def convert_market_cap_to_mil(str_market_cap):
    if str_market_cap.endswith("T"):
        str_market_cap = str_market_cap.replace("T","").strip()
        return float(str_market_cap)*1000000
    elif str_market_cap.endswith("B"):
        str_market_cap = str_market_cap.replace("B","").strip()
        return float(str_market_cap)*1000
    elif str_market_cap.endswith("M"):
        str_market_cap = str_market_cap.replace("M","").strip()
        return float(str_market_cap)
    else:
        print("Unknown market cap:"+str_market_cap)
        return 0 