import datetime

import requests, json, alpaca_trade_api, numpy, pandas, multiprocessing, os, time
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from AInvestor.config import *
import AInvestor.Stocks as Stocks
import AInvestor.formulas as formulas







def getStockData(val):
    api = alpaca_trade_api.REST(KEY, SECRET_KEY, BASE_URL)

    try:
        barset = api.get_barset(val, 'day', limit=30)
        return barset[val]
    except:
        print('{} does not exist as a stock option'.format(val))
        return 'NULL'


def pullMarketData(arr, interval, lim):
    request_count = 0
    stock_data_array = []
    for stock in arr:
        try:
            barset = api.get_barset(stock, interval, limit=lim)
            stock_data_array.append(barset[stock])
        except:
            print("{} doesn't exist as a stock".format(stock))
        request_count += 1
    return stock_data_array



def buy():
    return


def sell():
    return


def watch_market(arr):
    try:
        barset = api.get_barset(arr, 'day', limit=30)
        aapl_bars = barset[arr]
        week_open = aapl_bars[0].o
        week_close = aapl_bars[-1].c
        percent_change = (week_close - week_open) / week_open
        print('{} moved {}% in last 5 days'.format(arr, percent_change))
    except:
        print('{} does not exist as a stock option'.format(arr))
    return


def match_stock_data(name_array , data_array):
    output_dict = {}
    if len(name_array) == len(data_array):
        for i in range(name_array):
            output_dict[name_array[i]] = data_array[i]
    return output_dict

if __name__ == '__main__':
    request_count = 0
    stockArray = ['AAPL', 'AMD', 'FB', 'TSLA', 'GE', 'NIO', 'BP', 'ROKU', 'NFLX', 'BAC', 'AMZN', 'MSFT']
    stocks = dict([(stock_name, Stocks.Stock(stock_name)) for stock_name in stockArray])
    for i in stocks:
        request_count = stocks.get(i).updateData(request_count)

    #print(stocks.get("AAPL").hour_data)
    #print(formulas.momentum(stocks.get("AAPL").hour_data), 'hour', '30')
    #print(formulas.RSI(stocks.get("AAPL").day_data, len(stocks.get("AAPL").day_data), 'hour', 15))
    #print(formulas.MA(stocks.get("AAPL").day_data, len(stocks.get("AAPL").day_data), 'hour'))
    #print(formulas.MA(stocks.get("AAPL").minute_data, len(stocks.get("AAPL").minute_data), 'hour'))
    #EMA = formulas.EMA(stocks.get("AAPL").minute_data, len(stocks.get("AAPL").minute_data), 'minute')

    close_array = []
    time_array = []







    for i in range(len(stocks.get("AAPL").minute_data)-15):
        close_array.append(stocks.get("AAPL").minute_data[i+14].c)
        time_array.append(stocks.get("AAPL").minute_data[i+14].t)
    RSI = formulas.RSI(stocks.get("AAPL").minute_data, len(stocks.get("AAPL").minute_data), 'minute', 15)
    print(RSI)
    print('RSI LENGTH : {}'.format(len(RSI)))
    print('Y_ARRAY LENGTH : {}'.format(len(time_array)))
    plt.plot(time_array, RSI)
    plt.ylim(0,100)
    plt.show()

    #pool = multiprocessing.Pool(processes=6)
    #data = pool.map(match_stock_data, processData)
    #pool.close()
    #print(data)


