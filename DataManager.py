# ------------------------Dependencies----------------------------------------------------------------------------------
from AInvestor.config import api
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.MachineLearning.ML as ML
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
import AInvestor.Logger as Logger
import matplotlib.pyplot as plt
import numpy as np


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
        stockArray = ['AAPL', 'MSFT', 'GNUS', 'GE', 'BAC', 'NIO', 'ZOM']
        self.data = dict([(stock_name, Stocks.Stock(stock_name)) for stock_name in stockArray])

        print(('Stock List {} completed successfully, with a Request Count of {}').format(stockArray,
                                                                                          Stocks.REQUEST_COUNT))

    def plot_data(self, x, plot_type):
        if plot_type == 'Fibbonaci':
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
        print("---------------- " + stock.name + " -------------------------------------------------------------------")
        trial_lim = 250
        stock.update_data(lim=trial_lim)
        self.log.append('info', 'Stock: {} data has been repopulated with a limit of {}.'.format(stock.name, trial_lim))

        x1 = np.array([stock.hour_data.interval_one_hundred.Momentum,
                       stock.hour_data.interval_thirty.Momentum, stock.hour_data.interval_fifteen.Momentum])
        x2 = np.array([stock.hour_data.interval_one_hundred.RSI, stock.hour_data.interval_thirty.RSI,
                       stock.hour_data.interval_fifteen.RSI])
        x3 = np.array([stock.hour_data.interval_one_hundred.MACD, stock.hour_data.interval_thirty.MACD,
                       stock.hour_data.interval_fifteen.MACD])
        x4 = np.array([stock.hour_data.interval_one_hundred.MA, stock.hour_data.interval_thirty.MA,
                       stock.hour_data.interval_fifteen.MA])
        x5 = np.array([stock.hour_data.interval_one_hundred.EMA, stock.hour_data.interval_thirty.EMA,
                       stock.hour_data.interval_fifteen.EMA])

        y1 = [len(stock.hour_data.interval_one_hundred.RSI), len(stock.hour_data.interval_thirty.RSI),
              len(stock.hour_data.interval_fifteen.RSI)]
        y2 = [len(stock.hour_data.interval_one_hundred.MACD), len(stock.hour_data.interval_thirty.MACD),
              len(stock.hour_data.interval_fifteen.MACD)]
        y3 = [len(stock.hour_data.interval_one_hundred.EMA), len(stock.hour_data.interval_thirty.EMA),
              len(stock.hour_data.interval_fifteen.EMA)]

        fifteen_inp_array = [[stock.minute_data.interval_fifteen.Momentum], stock.minute_data.interval_fifteen.RSI,
                             stock.minute_data.interval_fifteen.MACD, stock.minute_data.interval_fifteen.EMA,
                             [stock.minute_data.interval_fifteen.MA]]
        thirty_inp_array = [[stock.minute_data.interval_thirty.Momentum], stock.minute_data.interval_thirty.RSI,
                            stock.minute_data.interval_thirty.MACD, stock.minute_data.interval_thirty.EMA,
                            [stock.minute_data.interval_thirty.MA]]
        hundred_inp_array = [[stock.minute_data.interval_one_hundred.Momentum],
                             stock.minute_data.interval_one_hundred.RSI,
                             stock.minute_data.interval_one_hundred.MACD, stock.minute_data.interval_one_hundred.EMA,
                             [stock.minute_data.interval_one_hundred.MA]]

        fifteen_temp_array, thirty_temp_array, hundred_temp_array = [], [], []

        for i in range(len(fifteen_inp_array)):
            if len(fifteen_inp_array[i]) == 1:
                fifteen_temp_array.append(0)
            else:
                fifteen_temp_array.append(len(fifteen_inp_array[i]))

        for i in range(len(thirty_inp_array)):
            if len(thirty_inp_array[i]) == 1:
                thirty_temp_array.append(0)
            else:
                thirty_temp_array.append(len(thirty_inp_array[i]))

        for i in range(len(hundred_inp_array)):
            if len(hundred_inp_array[i]) == 1:
                hundred_temp_array.append(0)
            else:
                hundred_temp_array.append(len(hundred_inp_array[i]))

        fifteen_size_array = [[5], fifteen_temp_array]
        thirty_size_array = [[5], thirty_temp_array]
        hundred_size_array = [[5], hundred_temp_array]

        print("Fifteen Interval Minute Data: {}".format(ML.generate_model(fifteen_size_array, fifteen_inp_array)))
        print("Thirty Interval Minute Data: {}".format(ML.generate_model(thirty_size_array, thirty_inp_array)))
        print("Hundred Interval Minute Data: {}".format(ML.generate_model(hundred_size_array, hundred_inp_array)))

    def long_term_analysis(self):
        pass

    def process(self, params=None):
        print("Starting Short Term Process...")
        for stock in self.data.values():
            self.short_term_analysis(stock)
