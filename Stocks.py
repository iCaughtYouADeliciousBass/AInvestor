import datetime
from AInvestor.config import api

class Stock:

    def __init__(self, stock_name):
        self.name = stock_name
        self.lastUpdated = datetime.datetime.now()
        self.month_data = []
        self.week_data = []
        self.day_data = []
        self.hour_data = []
        self.minute_data = []



    def updateData(self, requestCount, lim=250):
        try:
            barset = api.get_barset(self.name, 'day', limit=lim)
            self.day_data = barset[self.name]
            requestCount += 1
            barset = api.get_barset(self.name, '15Min', limit=lim*4)
            self.hour_data = barset[self.name][0::4]
            requestCount += 1
            barset = api.get_barset(self.name, 'minute', limit=lim)
            self.minute_data = barset[self.name]
            requestCount += 1
            self.lastUpdated = datetime.datetime.now()

        except:
            print("{} - Failed to retrieve stock info".format(self.name))

        finally:
            return requestCount

    def staleData(self):
        return self.lastUpdated - datetime.now() > datetime.timedelta(days=1)




