import statistics
from AInvestor.config import api
import AInvestor.Stocks as Stocks


class StockManager:
    def __init__(self):
        self.portfolio = None
        self.rules = None
        self.actionStream = None
        self.performance = 0.0
        self.update()

    def buy(self, stock, amount, priority):
        pass

    def sell(self, stock, amount, priority):
        pass

    def probe(self, stock, priority):
        pass

    def status(self):
        self.update()
        print(('Current Projection is {}, we are invested in {}, net change from yesterday is {}%. Just relax.').format('Positive', list(self.portfolio.keys()), round(self.performance, 3), '-100%'))

    def update(self):
        all_positions = api.list_positions()
        self.portfolio = dict([(pos.symbol, Stocks.Position(pos)) for pos in all_positions])
        self.performance = statistics.mean(list([float(stock.change_today) for stock in self.portfolio.values()]))
        Stocks.REQUEST_COUNT += 1
