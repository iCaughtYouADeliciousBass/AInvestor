from AInvestor.config import api
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
import AInvestor.Logger as Logger
import matplotlib.pyplot as plt
import numpy as np


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
        print("DAY DATA :: Name: {}, MA: {}, EMA: {},  RSI: {}, MACD: {}, Momentum: {}".format(stock.name,
                                                                                               stock.day_data.MA,
                                                                                               stock.day_data.EMA[-7:],
                                                                                               stock.day_data.RSI[-7:],
                                                                                               stock.day_data.MACD[-7:],
                                                                                               stock.day_data.Momentum))

        print("HOUR DATA :: Name: {}, MA: {}, EMA: {},  RSI: {}, MACD: {}, Momentum: {}".format(stock.name,
                                                                                                stock.hour_data.MA,
                                                                                                stock.hour_data.EMA[-7:],
                                                                                                stock.hour_data.RSI[-7:],
                                                                                                stock.hour_data.MACD[-7:],
                                                                                                stock.hour_data.Momentum))

        print("MINUTE DATA :: Name: {}, MA: {}, EMA: {},  RSI: {}, MACD: {}, Momentum: {}".format(stock.name,
                                                                                                  stock.minute_data.MA,
                                                                                                  stock.minute_data.EMA[-7:],
                                                                                                  stock.minute_data.RSI[-7:],
                                                                                                  stock.minute_data.MACD[-7:],
                                                                                                  stock.minute_data.Momentum))
        print("-------------------------------------------------------------------------------------------------------")

    def long_term_analysis(self):
        pass

    def process(self, params=None):
        for stock in self.data.values():
            self.short_term_analysis(stock)
