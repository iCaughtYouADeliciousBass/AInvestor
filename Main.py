import requests, json, alpaca_trade_api, numpy, pandas

from AInvestor.config import *
from AInvestor.formulas import *
from fastnumbers import isfloat
from fastnumbers import fast_float
from multiprocessing.dummy import Pool as ThreadPool
import matplotlib.pyplot as plt
import seaborn as sns
#from tidylib import tidy_document # for tidying incorrect html
sns.set_style('whitegrid')
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"



api = alpaca_trade_api.REST(KEY, SECRET_KEY, BASE_URL)


def buy():

    return


def sell():

    return


def watchMarket():
    barset = api.get_barset('AAPL', 'day', limit=5)
    aapl_bars = barset['AAPL']
    week_open = aapl_bars[0].o
    week_close = aapl_bars[-1].c
    percent_change = (week_close - week_open) / week_open
    print('AAPL moved {}% in last 5 days'.format(percent_change))

    return
