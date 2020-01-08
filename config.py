import alpaca_trade_api

KEY = "PKTZZQZ38CEAPVHMNO8O"
SECRET_KEY = "heu7f5mBAnzPcmZ44AceoSdMtnGfBh8rcoQxJS4M"
BASE_URL = "https://paper-api.alpaca.markets"

api = alpaca_trade_api.REST(KEY, SECRET_KEY, BASE_URL)
