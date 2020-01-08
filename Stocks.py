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



    def updateData(self, request_count):
        try:
            barset = api.get_barset(self.name, 'day', limit=30)
            self.day_data = barset[self.name]
            request_count += 1
            barset = api.get_barset(self.name, '15Min', limit=120)
            self.hour_data = barset[self.name][0::4]
            request_count += 1
            barset = api.get_barset(self.name, 'minute', limit=30)
            self.minute_data = barset[self.name]
            request_count += 1
            self.lastUpdated = datetime.datetime.now()

        except:
            print("{} - Failed to retrieve stock info".format(self.name))

        finally:
            return request_count

    def staleData(self):
        return self.lastUpdated - datetime.now() > datetime.timedelta(days=1)




