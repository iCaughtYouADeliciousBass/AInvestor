# ------------------------Dependencies----------------------------------------------------------------------------------
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from AInvestor.config import *
import AInvestor.Stocks as Stocks
import AInvestor.DataManager as DataManager
import AInvestor.StockManager as StockManager
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.DataProcessing.formulas as formulas

# ------------------------Random----------------------------------------------------------------------------------------
register_matplotlib_converters()
__author__ = 'Michael Judd'
REQUEST_COUNT = 0

# ------------------------Main------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dm = DataManager.DataManager()
    sm = StockManager.StockManager()
    sm.status()
    #SDR.initTaskList()


