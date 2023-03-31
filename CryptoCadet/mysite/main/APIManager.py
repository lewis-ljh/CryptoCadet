from binance import Client


def createClient():
    APIKEY = "g0t3354JYusdR55nj4kvzYFVM3iZ5jHZLD4GdPER0PyMNI8nxv9EBWsnNrgBuAq5"
    SECRETKEY = "wy0sE9VQUBUgVuBXdlfHJb0JH9JFKOtWJ4C6GnmdBk30TBTYD7oRQOKChPaog4uk"  
    client = Client(APIKEY, SECRETKEY)
    return client



def buyOrder(coinPair, amount):
    order = Client.create_order(
        symbol=coinPair, 
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=amount
    )

def sellOrder(coinPair, amount):
    client = createClient()
    order = client.create_order(
        symbol=coinPair,
        side=client.SIDE_SELL,
        type=client.ORDER_TYPE_MARKET,
        quantity=amount
    )


def validateSell():
    return False

def validateBuy():
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