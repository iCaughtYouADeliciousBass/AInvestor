from AInvestor.config import api
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
import matplotlib.pyplot as plt
import numpy as np


class DataManager:
    def __init__(self):
        self.outStream = None
        self.inStream = None
        self.data = self.populate_data()

    def populate_data(self):
        SDRWebCrawler.buildStockList()
        stockArray = ['AAPL', 'MSFT']
        self.data = dict([(stock_name, Stocks.Stock(stock_name)) for stock_name in stockArray])

        print(('Stock List {} completed successfully, with a Request Count of {}').format(stockArray,
                                                                                          Stocks.REQUEST_COUNT))

    def plotData(x, type):
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


