from binance import Client


def createClient():
    APIKEY = "g0t3354JYusdR55nj4kvzYFVM3iZ5jHZLD4GdPER0PyMNI8nxv9EBWsnNrgBuAq5"
    SECRETKEY = "wy0sE9VQUBUgVuBXdlfHJb0JH9JFKOtWJ4C6GnmdBk30TBTYD7oRQOKChPaog4uk"  
    client = Client(APIKEY, SECRETKEY)
    return client



def coinExists(coin):
    tickers = getTickers()
    for x in range(len(tickers)):
        if tickers[x]["symbol"] == coin:
            return True
    return False



def validateSell(coin):
    if coinExists(coin):
        # if user has enough money
        return True

def validateBuy(coin):
    if coinExists(coin):
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

def getPrice(symbol):
    client = createClient()
    prices = client.get_all_tickers()
    for x in range(len(prices)):
        if prices[x]["symbol"] == symbol:
            return prices[x]["price"]
        
    return None

