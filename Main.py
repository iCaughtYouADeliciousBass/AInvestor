# ------------------------Dependencies----------------------------------------------------------------------------------
from pandas.plotting import register_matplotlib_converters
import AInvestor.DataManager as DataManager
import AInvestor.StockManager as StockManager
import multiprocessing

# ------------------------Setup-----------------------------------------------------------------------------------------
register_matplotlib_converters()
__author__ = 'Michael Judd'

# ------------------------Main------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Initiate Data Manager, Stock Manager and Logger
    dm = DataManager.DataManager()
    sm = StockManager.StockManager()
    sm.status()
    #p1 = multiprocessing.Process(target=sm.actionStream_start)
    #p1.start()
    #p1.join()
    dm.process()