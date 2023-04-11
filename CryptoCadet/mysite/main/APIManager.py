from binance import Client
from .models import Profile, OwnedCoin

        

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



def validateSell(coin, amount, ownedCoins):
    if coin == "" or amount =="":
        return False
    if coinExists(coin):
        for coins in ownedCoins:
            if coins.coinName == coin and coins.amount >= float(amount):
                return True
    
    return False

def validateBuy(user, coin, amount, price):
    if coin == "" or amount =="":
        return False
    if coinExists(coin):
        if Profile.objects.get(user=user).account_balance>float(price)*float(amount):
            return True
        
    return False 
    

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
    if symbol == "":
        return None
    client = createClient()
    prices = client.get_all_tickers()
    for x in range(len(prices)):
        if prices[x]["symbol"] == symbol:
            return prices[x]["price"]
        
    return None

