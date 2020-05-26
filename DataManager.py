# ------------------------Dependencies----------------------------------------------------------------------------------
from AInvestor.config import api
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
import AInvestor.Logger as Logger
import matplotlib.pyplot as plt
import numpy as np
import datetime


# ------------------------Data Manager Class----------------------------------------------------------------------------


class DataManager:
    def __init__(self):
        self.outStream = None
        self.inStream = None
        self.data = None
        self.log = Logger.Logger()
        self.populate_data()
        self.log.append('info', 'Data Manager started successfully')

    def populate_data(self):
        SDRWebCrawler.buildStockList()
        stockArray = ['AAPL', 'MSFT']
        self.data = dict([(stock_name, Stocks.Stock(stock_name)) for stock_name in stockArray])

        print(('Stock List {} completed successfully, with a Request Count of {}').format(stockArray,
                                                                                          Stocks.REQUEST_COUNT))

    def plot_data(x, type):
        if type == 'Fibbonaci':
            x_array = []
            y_array = []
            for i in range(x.length):
                x_array.append(x.day_data[i].t)
                y_array.append(x.day_data[i].c)
            plt.plot(x_array, y_array, color='blue', linewidth=1)
            for item in x.Fibbonaci.values():
                fibb_array = np.full((1, x.length), item)
                plt.plot(x_array, fibb_array[0], color='red', linewidth=1)
            plt.show()

    def short_term_analysis(self, stock):
        print("-------------------------------------------------------------------------------------------------------")
        trial_lim = 250
        stock.update_data(lim=trial_lim)
        self.log.append('info', 'Stock: {} data has been repopulated with a limit of {}.'.format(stock.name, trial_lim))

        x1 = np.array([stock.hour_data.interval_one_hundred.Momentum,
                       stock.hour_data.interval_thirty.Momentum, stock.hour_data.interval_fifteen.Momentum])
        x2 = np.array([stock.hour_data.interval_one_hundred.RSI[-1], stock.hour_data.interval_thirty.RSI[-1],
                       stock.hour_data.interval_fifteen.RSI[-1]])
        x3 = np.array([stock.hour_data.interval_one_hundred.MACD[-1], stock.hour_data.interval_thirty.MACD[-1],
                       stock.hour_data.interval_fifteen.MACD[-1]])
        x4 = np.array([stock.hour_data.interval_one_hundred.MA, stock.hour_data.interval_thirty.MA,
                       stock.hour_data.interval_fifteen.MA])
        x5 = np.array([stock.hour_data.interval_one_hundred.EMA[-1], stock.hour_data.interval_thirty.EMA[-1],
                       stock.hour_data.interval_fifteen.EMA[-1]])

        y1 = [len(stock.hour_data.interval_one_hundred.RSI), len(stock.hour_data.interval_thirty.RSI),
              len(stock.hour_data.interval_fifteen.RSI)]
        y2 = [len(stock.hour_data.interval_one_hundred.MACD), len(stock.hour_data.interval_thirty.MACD),
              len(stock.hour_data.interval_fifteen.MACD)]
        y3 = [len(stock.hour_data.interval_one_hundred.EMA), len(stock.hour_data.interval_thirty.EMA),
              len(stock.hour_data.interval_fifteen.EMA)]

#       Z1_1 = 100 int, Z1_2 = 30 int, Z1_3 = 15 int
        z1_1 = [1, y1[0], y2[0], y3[0], 1]
        z1_2 = [1, y1[1], y2[1], y3[1], 1]
        z1_3 = [1, y1[2], y2[2], y3[2], 1]



        print(stock.network.feed_forward(x1, x2, x3, x4, x5))

        print("-------------------------------------------------------------------------------------------------------")

    def long_term_analysis(self):
        pass

    def process(self, params=None):
        for stock in self.data.values():
            self.short_term_analysis(stock)
