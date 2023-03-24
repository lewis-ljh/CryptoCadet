from binance import Client
APIKEY = "g0t3354JYusdR55nj4kvzYFVM3iZ5jHZLD4GdPER0PyMNI8nxv9EBWsnNrgBuAq5"
SECRETKEY = "wy0sE9VQUBUgVuBXdlfHJb0JH9JFKOtWJ4C6GnmdBk30TBTYD7oRQOKChPaog4uk"
Client = Client(APIKEY, SECRETKEY)

depth = Client.get_order_book(symbol='BNBBTC')
print(depth)

"""make an order"""
#order = Client.create_order(
#    symbol="ETHUSDT", #buy eth with usdt
#    side=Client.SIDE_BUY,
#    type=Client.ORDER_TYPE_MARKET,
#    quantity=0.015
#)

"""get all tickers"""
#prices = Client.get_all_tickers()
#print(prices)

#orders = Client.get_all_orders(symbol='BTCUSDT', limit=10) #10 most recent btc/usdt transactions
#for order in orders:
#    print(order["origQty"])
#