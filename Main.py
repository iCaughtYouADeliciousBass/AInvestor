import requests, json, alpaca_trade_api, numpy, pandas, multiprocessing, os, time
import AInvestor.Stocks as Stocks
import AInvestor.formulas as formulas
from AInvestor.config import *
from fastnumbers import isfloat
from fastnumbers import fast_float
from multiprocessing.dummy import Pool as ThreadPool
import matplotlib.pyplot as plt
import seaborn as sns

# from tidylib import tidy_document # for tidying incorrect html
sns.set_style('whitegrid')
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"




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
    print(formulas.momentum(stocks.get("AAPL").hour_data), 'hour', '30')



    #pool = multiprocessing.Pool(processes=6)
    #data = pool.map(match_stock_data, processData)
    #pool.close()
    #print(data)


