from AInvestor.config import api
import AInvestor.Stocks as Stocks
import AInvestor.Logger as Logger
import statistics


class StockManager:
    def __init__(self):
        self.portfolio = None
        self.rules = None
        self.actionStream = []
        self.performance = 0.0
        self.funds = 0.0
        self.daytrade_count = 0
        self.update()
        self.buy('AAPL', 1, 320.0, 1)
        self.sell('AAPL', 1, 310.0, 1)
        self.log = Logger.Logger()
        self.log.append('info', 'Stock Manager started successfully')

    def buy(self, stock, amount, price, priority, params='market'):
        self.actionStream.append(Action(stock, amount, price, priority, "buy", params))

    def sell(self, stock, amount, price, priority, params='market'):
        self.actionStream.append(Action(stock, amount, price, priority, "sell", params))

    def probe(self, stock, priority):
        pass

    def status(self):
        self.update()
        print(('Current Projection is {}, we are invested in {}, net change from yesterday is {}%. Just relax.').format(
            'Positive', list(self.portfolio.keys()), round(self.performance, 3), '-100%'))

    def update(self):
        all_positions = api.list_positions()
        account_info = api.get_account()
        self.portfolio = dict([(pos.symbol, Stocks.Position(pos)) for pos in all_positions])
        self.performance = statistics.mean(list([float(stock.change_today) for stock in self.portfolio.values()]))
        self.funds = account_info.cash
        self.daytrade_count = account_info.daytrade_count
        Stocks.REQUEST_COUNT += 2

    def actionStream_start(self):
        while len(self.actionStream) > 0:
            a = next(iter(self.actionStream))
            api.submit_order(a.stock_name, a.qty, a.order_type, a.params, "gtc",
                             a.price if a.params == 'limit' else None)
            if len(self.actionStream) > 1:
                self.actionStream = self.actionStream[1:]
            else:
                self.actionStream = []


class Action:
    def __init__(self, name, qty, price, priority, order_type, params):
        self.stock_name = name
        self.qty = qty
        self.price = price
        self.priority = priority
        self.order_type = order_type
        self.params = params
