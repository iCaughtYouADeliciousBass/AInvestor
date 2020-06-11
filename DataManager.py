# ------------------------Dependencies----------------------------------------------------------------------------------
from AInvestor.config import api
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.MachineLearning.ML as ML
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
import AInvestor.Logger as Logger
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing

# ------------------------Data Manager Class----------------------------------------------------------------------------


class DataManager:
    def __init__(self):
        self.outStream = None
        self.inStream = None
        self.data = {}
        self.log = Logger.Logger()
        self.populate_data()
        self.log.append('info', 'Data Manager started successfully')

    def populate_data(self):
        SDRWebCrawler.buildStockList()
        stock_array = ['AAPL', 'MSFT', 'GNUS', 'GE', 'BAC', 'NIO', 'ZOM']
        p = multiprocessing.Pool(len(stock_array))
        p.map(self.generate_dict, stock_array)
        print(('Stock List {} completed successfully, with a Request Count of {}').format(stock_array,
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
        #self.log.append('info', 'Stock: {} data has been repopulated with a limit of {}.'.format(stock.name, trial_lim))
        print("Hundred Interval Minute Data: {}".format(stock.minute_data.hundred_model.feed_forward()))
        print("Thirty Interval Minute Data: {}".format(stock.minute_data.thirty_model.feed_forward()))
        print("Fifteen Interval Minute Data: {}".format(stock.minute_data.fifteen_model.feed_forward()))
        print("Hundred Interval Hour Data: {}".format(stock.hour_data.hundred_model.feed_forward()))
        print("Thirty Interval Hour Data: {}".format(stock.hour_data.thirty_model.feed_forward()))
        print("Fifteen Interval Hour Data: {}".format(stock.hour_data.fifteen_model.feed_forward()))
        print("Hundred Interval Day Data: {}".format(stock.day_data.hundred_model.feed_forward()))
        print("Thirty Interval Day Data: {}".format(stock.day_data.thirty_model.feed_forward()))
        print("Fifteen Interval Day Data: {}".format(stock.day_data.fifteen_model.feed_forward()))
        print("DONE")



    def long_term_analysis(self):
        pass

    def generate_dict(self, stock_name):
        self.data[stock_name] = Stocks.Stock(stock_name)

    def process(self, params=None):
        print("Starting Short Term Process...")
        for stock in self.data.values():
            self.short_term_analysis(stock)
