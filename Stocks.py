import datetime
import AInvestor.DataProcessing.formulas as Formulas
from AInvestor.config import api

REQUEST_COUNT = 0

class Stock:

    def __init__(self, stock_name: str):
        self.name = stock_name
        self.lastUpdated = datetime.datetime.now()
        self.day_data = StockData()
        self.hour_data = StockData()
        self.minute_data = StockData()
        self.update_data()

    def update_data(self, lim: int = 250):
        try:
            global REQUEST_COUNT
            # Data Retrieval Stuff
            barset = api.get_barset(self.name, 'day', limit=lim)
            self.day_data.data = barset[self.name]
            REQUEST_COUNT += 1
            barset = api.get_barset(self.name, '15Min', limit=lim * 4)
            self.hour_data.data = barset[self.name][0::4]
            REQUEST_COUNT += 1
            barset = api.get_barset(self.name, 'minute', limit=lim)
            self.minute_data.data = barset[self.name]
            REQUEST_COUNT += 1
            self.lastUpdated = datetime.datetime.now()
            self.length = lim
            self.recalculate_all()
        except:
            print("{} - Failed to retrieve stock info".format(self.name))


    def staleData(self):
        return self.lastUpdated - datetime.now() > datetime.timedelta(days=1)

    def recalculate_day(self):
        self.day_data.update()

    def recalculate_hour(self):
        self.hour_data.update()

    def recalculate_min(self):
        self.minute_data.update()

    def recalculate_all(self):
        self.recalculate_min()
        self.recalculate_hour()
        self.recalculate_day()


class StockData:
    def __init__(self):
        self.length = 0
        self.data = None
        self.MACD = None
        self.MA = None
        self.EMA = None
        self.Fibbonaci = None
        self.RSI = None
        self.Momentum = None

    def update(self):
        self.length = len(self.data)
        self.MACD = Formulas.MACD(self.data)
        self.MA = Formulas.MA(self.data)
        self.EMA = Formulas.EMA(self.data, 14)
        self.Fibbonaci = Formulas.FibbonaciRetracement(self.data)
        self.RSI = Formulas.RSI(self.data, 14)
        self.Momentum = Formulas.momentum(self.data)

class Position:
    def __init__(self, data):
        self.name = data.symbol
        self.quantity = data.qty
        self.current_price = data.current_price
        self.exchange = data.exchange
        self.purchase_price = data.avg_entry_price
        self.change_today = data.change_today
        self.intraday_change_pct = data.unrealized_intraday_plpc
        self.profit_loss_pct = (float(self.current_price) - float(self.purchase_price)) / float(self.purchase_price) * 100.0
