# ------------------------Dependencies----------------------------------------------------------------------------------
from pandas.plotting import register_matplotlib_converters
import AInvestor.DataManager as DataManager
import AInvestor.StockManager as StockManager

# ------------------------Setup-----------------------------------------------------------------------------------------
register_matplotlib_converters()
__author__ = 'Michael Judd'

# ------------------------Main------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dm = DataManager.DataManager()
    sm = StockManager.StockManager()
    sm.status()
    dm.process()

