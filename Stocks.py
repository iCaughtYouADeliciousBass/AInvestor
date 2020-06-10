# ------------------------Dependencies----------------------------------------------------------------------------------
import datetime
import math
import AInvestor.DataProcessing.formulas as Formulas
import AInvestor.MachineLearning.ML as ML
from AInvestor.config import api

# ------------------------Globals---------------------------------------------------------------------------------------
REQUEST_COUNT = 0


# ------------------------Stock Class-----------------------------------------------------------------------------------


class Stock:

    def __init__(self, stock_name: str):
        #       Initial scalars and interval ranges for Machine Learning models
        self.name = stock_name
        self.price = 0.0
        self.length = 0
        self.interval_range = [100, 30, 15, 5, 1]
        #       Temp data to deal with update_data(avoid) issue (fix??)
        self.temp_day_data_data = None
        self.temp_hour_data_data = None
        self.temp_min_data_data = None
        self.update_data(avoid=1)
        #       Day / Hour / Min data that holds all stock data
        self.MA_scale = self.price
        self.MACD_scale = 100
        self.Momentum_scale = 10
        self.EMA_scale = self.price
        self.RSI_scale = 1
        self.scale_array = {"MA": self.MA_scale, "MACD": self.MACD_scale, "Momentum": self.Momentum_scale,
                            "EMA": self.EMA_scale, "RSI": self.RSI_scale}
        self.day_data = StockData(self.temp_day_data_data, self.interval_range, self.scale_array, self.price,
                                  self.name, "day")
        self.hour_data = StockData(self.temp_hour_data_data, self.interval_range, self.scale_array, self.price,
                                   self.name, "hour")
        self.minute_data = StockData(self.temp_min_data_data, self.interval_range, self.scale_array, self.price,
                                     self.name, "minute")
        self.lastUpdated = datetime.datetime.now()

    def update_data(self, lim: int = 250, avoid: int = 0):
        try:
            global REQUEST_COUNT
            # Data Retrieval Stuff
            barset = api.get_barset(self.name, 'day', limit=lim)
            self.temp_day_data_data = barset[self.name]
            REQUEST_COUNT += 1
            barset = api.get_barset(self.name, '15Min', limit=lim * 4)
            self.temp_hour_data_data = barset[self.name][0::4]
            REQUEST_COUNT += 1
            barset = api.get_barset(self.name, 'minute', limit=lim)
            self.temp_min_data_data = barset[self.name]
            self.price = barset[self.name][-1].c
            REQUEST_COUNT += 1
            self.lastUpdated = datetime.datetime.now()
            self.length = lim
            if not avoid:
                #       Need to fix this, there's an operation order problem here.
                self.recalculate_all(self.temp_day_data_data, self.temp_hour_data_data, self.temp_min_data_data)

        except ValueError:
            print("{} - Failed to retrieve stock info".format(self.name))

    def stale_data(self):
        return self.lastUpdated - datetime.now() > datetime.timedelta(days=1)

    def recalculate_day(self, d_data):
        self.day_data.update(d_data)

    def recalculate_hour(self, h_data):
        self.hour_data.update(h_data)

    def recalculate_min(self, m_data):
        self.minute_data.update(m_data)

    def recalculate_all(self, d_data, h_data, m_data):
        self.recalculate_min(m_data)
        self.recalculate_hour(h_data)
        self.recalculate_day(d_data)


# ------------------------Stock Data Class------------------------------------------------------------------------------


class StockData:
    def __init__(self, data, interval_range: list, scale_array: dict, price, name, increment):
        self.interval_range = interval_range
        self.data = data
        self.Fibbonaci = Formulas.FibbonaciRetracement(self.data)
        self.interval_one_hundred = Interval(self.interval_range[0], self.data[-self.interval_range[0]:],
                                             scale_array, price, name, increment)
        self.interval_thirty = Interval(self.interval_range[1], self.data[-self.interval_range[1]:],
                                        scale_array, price, name, increment)
        self.interval_fifteen = Interval(self.interval_range[2], self.data[-self.interval_range[2]:],
                                         scale_array, price, name, increment)
        self.hundred_model = ML.generate_model(self.interval_one_hundred)
        self.thirty_model = ML.generate_model(self.interval_thirty)
        self.fifteen_model = ML.generate_model(self.interval_fifteen)

    def update(self, data):
        self.data = data
        self.interval_one_hundred.data = self.data[-self.interval_range[0]:]
        self.interval_thirty.data = self.data[-self.interval_range[1]:]
        self.interval_fifteen.data = self.data[-self.interval_range[2]:]
        self.Fibbonaci = Formulas.FibbonaciRetracement(self.data)
        self.interval_one_hundred.recalculate(self.interval_one_hundred.interval)
        self.interval_thirty.recalculate(self.interval_thirty.interval)
        self.interval_fifteen.recalculate(self.interval_fifteen.interval)


# ------------------------Stock Data Class------------------------------------------------------------------------------


class Interval:
    def __init__(self, t, data, scale_dict, price, name, increment):
        self.name = name + "_" + str(t) + "_" + increment
        self.increment = increment
        self.price = price
        self.interval = t
        self.data = data
        self.model_exists = False
        self.model_data = None
        self.scale_dict = scale_dict
        self.MA = Formulas.MA(self.data)
        self.MACD = Formulas.MACD(self.data, int(self.interval / 2), self.interval)
        self.Momentum = Formulas.momentum(self.data)
        self.EMA = Formulas.EMA(self.data, int(math.sqrt(t)))
        self.RSI = Formulas.RSI(self.data, int(math.sqrt(t)))
        self.rescale()

    def recalculate(self, t):
        self.MA = Formulas.MA(self.data)
        self.MACD = Formulas.MACD(self.data, int(self.interval / 2), self.interval)
        self.Momentum = Formulas.momentum(self.data)
        self.EMA = Formulas.EMA(self.data, int(math.sqrt(t)))
        self.RSI = Formulas.RSI(self.data, int(math.sqrt(t)))
        self.rescale()

    def rescale(self):
        self.MA_scale(self.scale_dict.get("MA"))
        self.MACD_scale(self.scale_dict.get("MACD"))
        self.Momentum_scale(self.scale_dict.get("Momentum"))
        self.EMA_scale(self.scale_dict.get("EMA"))
        self.RSI_scale(self.scale_dict.get("RSI"))

    def MA_scale(self, factor: float):
        self.MA = ((self.MA - factor) / self.price - 1)

    def MACD_scale(self, factor: float):
        for i in range(len(self.MACD)):
            self.MACD[i] = self.MACD[i]*factor

    def Momentum_scale(self, factor: float):
        self.Momentum = self.Momentum * factor

    def EMA_scale(self, factor: float):
        for i in range(len(self.EMA)):
            self.EMA[i] = self.EMA[i] - factor

    def RSI_scale(self, factor):
        try:
            for i in range(len(self.RSI)):
                self.RSI[i] = self.RSI[i] * factor
        except IndexError:
            print("Nice RSI Scale Factor list, Iniel.")

# ------------------------Position Class--------------------------------------------------------------------------------


class Position:
    def __init__(self, data):
        self.name = data.symbol
        self.quantity = data.qty
        self.current_price = data.current_price
        self.exchange = data.exchange
        self.purchase_price = data.avg_entry_price
        self.change_today = data.change_today
        self.intraday_change_pct = data.unrealized_intraday_plpc
        self.profit_loss_pct = (float(self.current_price) - float(self.purchase_price)) / float(
            self.purchase_price) * 100.0
