# ------------------------Dependencies----------------------------------------------------------------------------------
from pandas.plotting import register_matplotlib_converters
from AInvestor.config import DATABASE_NAME, USERNAME, PASSWORD, ENDPOINT, PORT
import AInvestor.DataManager as DataManager
import AInvestor.StockManager as StockManager
import pymysql
import multiprocessing

# ------------------------Setup-----------------------------------------------------------------------------------------
register_matplotlib_converters()
__author__ = 'Michael Judd'
connection = pymysql.connect(host=ENDPOINT, user=USERNAME, passwd=PASSWORD, db=DATABASE_NAME, port=PORT)

def handler():
    cursor = connection.cursor()
    cursor.execute('SELECT * from SM_Transactions')
    rows = cursor.fetchall()


# ------------------------Main------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dm = DataManager.DataManager()
    sm = StockManager.StockManager()
    sm.status()
    #p1 = multiprocessing.Process(target=sm.actionStream_start)
    #p1.start()
    #p1.join()
    dm.process()
    #handler()
