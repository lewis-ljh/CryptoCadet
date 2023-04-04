from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .APIManager import *
from .models import Coin, Order, OwnedCoin
from datetime import datetime
from django.contrib.auth.models import User

# from .forms import TicketForm

from .models import Ticket
from django.forms import modelformset_factory

# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name":"Test"})


def BuyAndSell(response):
    def getUser(request):
        return request.user
    
    coinName = response.POST.get("BuyOrSell")
    if response.method=="POST":
        if response.POST.get("sell"):
            if validateSell(coinName):
                order = Order.objects.create(user=getUser(response), coinName=coinName, price=getPrice(coinName), type="sell", time=datetime.now())
                order.save()

                ownedCoins = OwnedCoin.objects.all()
                for coins in ownedCoins:
                    if getUser(response)==coins.user and coinName==coins.coinName:
                        coins.amount = coins.amount - float(response.POST.get("HowMuch"))
                        coins.save()
                        break

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":False})
            


            
        if response.POST.get("buy"):
            coinName = response.POST.get("BuyOrSell")

            if validateBuy(coinName):
                order = Order.objects.create(user=getUser(response), coinName=coinName, price=getPrice(coinName), type="buy", time=datetime.now())
                order.save()

                ownedCoins = OwnedCoin.objects.all()
                owned = False
                for coins in ownedCoins:
                    if getUser(response)==coins.user and coinName==coins.coinName:
                        owned = True
                        coins.amount = coins.amount + float(response.POST.get("HowMuch"))
                        coins.save()
                        break
                
                if not owned:
                    ownedCoin = OwnedCoin.objects.create(user=getUser(response), coinName=coinName, amount=float(response.POST.get("HowMuch"))) 

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":False})
    return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":True})

def previousTrades(response):
    trades = Order.objects.filter(user=response.user)
    return render(response, "main/previousTrades.html", {"trades":trades})



def logout(response):
    return render(response, "main/log-out.html")

#Load the page for viewing coins -> when loading loop though all coins in DB and update price from API
def cryptoList(response):
    coins = Coin.objects.all()
    for coin in coins:
        dict = getTickers()
        #find each coin in the api return
        found =  next(item for item in dict if item["symbol"] == coin.ticker)
        price = found['price']
        #set price and save it 
        coin.price = price
        coin.save()
        #render crytpo list
    return render(response, "main/cryptoList.html" ,{"coins":coins})

def tickets(response):

    TicketFormSet = modelformset_factory(Ticket, fields=('title', 'query'))
    # queryset = Ticket.objects.filter(__name__.startswith('0'))
    if response.method == 'POST':
        formset = TicketFormSet(response.POST, response.FILES)
        if formset.is_valid():
            formset.save()

    else:
        formset = TicketFormSet()

    print(formset)

    # queryset = Author.objects.filter(name__startswith='O')
    # if request.method == "POST":
    #     formset = AuthorFormSet(request.POST, request.FILES,queryset=queryset,)
    #     if formset.is_valid():
    #         formset.save()
    #         # Do something.
    # else:
    #     formset = AuthorFormSet(queryset=queryset)




    return render(response, "main/tickets.html", {'formset': formset})