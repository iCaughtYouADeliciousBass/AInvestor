# ------------------------Dependencies----------------------------------------------------------------------------------
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from AInvestor.config import *
import AInvestor.Stocks as Stocks
import AInvestor.ScheduledDataRetrieval.SDR as SDR
import AInvestor.DataProcessing.formulas as formulas

# ------------------------Random----------------------------------------------------------------------------------------
register_matplotlib_converters()
__author__ = 'Michael Judd'


# ------------------------Main------------------------------------------------------------------------------------------
if __name__ == '__main__':
    SDR.initTaskList()


