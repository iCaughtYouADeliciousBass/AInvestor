import alpaca_trade_api

KEY = "PKTZZQZ38CEAPVHMNO8O"
SECRET_KEY = "heu7f5mBAnzPcmZ44AceoSdMtnGfBh8rcoQxJS4M"
BASE_URL = "https://paper-api.alpaca.markets"

ENDPOINT = "ainvestor.cu0fbx0vwc4k.ap-southeast-2.rds.amazonaws.com"
USERNAME = "admin"
PASSWORD = "1333"
DATABASE_NAME = "AInvestor"
PORT = 3306


api = alpaca_trade_api.REST(KEY, SECRET_KEY, BASE_URL)

