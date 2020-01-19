
import AInvestor.ScheduledDataRetrieval.SDRWebCrawler as SDRWebCrawler
import AInvestor.Stocks as Stocks
global REQUEST_COUNT

def initTaskList():
    REQUEST_COUNT = 0
    SDRWebCrawler.buildStockList()
    stockArray = ['AAPL', 'AMD', 'FB', 'TSLA', 'GE', 'NIO', 'BP', 'ROKU', 'NFLX', 'BAC', 'AMZN', 'MSFT']
    stocks = dict([(stock_name, Stocks.Stock(stock_name)) for stock_name in stockArray])
    for i in stocks:
        REQUEST_COUNT = stocks.get(i).updateData(REQUEST_COUNT)
    print(REQUEST_COUNT)

def threeMinTaskList():
    pass

def hourlyTaskList():
    pass

def dailyTaskList():
    pass
