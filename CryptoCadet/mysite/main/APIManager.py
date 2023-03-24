from binance import Client


def createClient():
    APIKEY = "g0t3354JYusdR55nj4kvzYFVM3iZ5jHZLD4GdPER0PyMNI8nxv9EBWsnNrgBuAq5"
    SECRETKEY = "wy0sE9VQUBUgVuBXdlfHJb0JH9JFKOtWJ4C6GnmdBk30TBTYD7oRQOKChPaog4uk"  
    client = Client(APIKEY, SECRETKEY)
    return client

"""

            Don't change


#def buyOrder(coinPair, amount):
#    order = Client.create_order(
#        symbol="BTCUSDT", #buy eth with usdt
#        side=Client.SIDE_BUY,
#        type=Client.ORDER_TYPE_MARKET,
#        quantity=0.015
#    )
#
#def sellOrder():
#    client = createClient()
#    order = client.create_order(
#        symbol="BTCUSDT",
#        side=client.SIDE_SELL,
#        type=client.ORDER_TYPE_MARKET,
#        quantity=0.00111
#    )

"""

def validateSell():
    return True
    

def getTickers():
    client = createClient()
    prices = client.get_all_tickers()
    return prices

def getUSDTCoins():
    a = getTickers()
    print(len(a))
    
    for x in range(len(a)):
        b = a[x]["symbol"]
        if b[len(b)-4:] == "USDT":
            print(a[x]["symbol"], ":", a[x]["price"])