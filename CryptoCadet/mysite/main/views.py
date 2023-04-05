from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from .APIManager import *
from .models import Coin, Address, Profile


from .models import Coin, Order, OwnedCoin
from datetime import datetime
from django.contrib.auth.models import User

# from .forms import TicketForm

from .models import Ticket
from django.forms import modelformset_factory

# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name": "Test"})


class ViewPersonalInformation(View):
    template_name = "main/personal_info.html"

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            address = Address.objects.filter(user=request.user).first()
            context = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "address": address,
                "phone_number": profile.phone_number,
                "account_balance": profile.account_balance,
            }
        except Profile.DoesNotExist:
            context = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "address": None,
                "phone_number": None,
                "account_balance": None,
            }
        return render(request, self.template_name, context)



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

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=getUser(response)), "found":True})
            else:
<<<<<<< HEAD
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=getUser(response)), "found":False})
            
=======
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.all(), "found":False})

>>>>>>> d5a680be1abe25aaa32e96f2c1ae893c4e1e4bcc


            
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

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=response.user), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=response.user), "found":False})
    return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=response.user), "found":True})

def previousTrades(response):
    trades = Order.objects.filter(user=response.user)
    return render(response, "main/previousTrades.html", {"trades":trades})




def logout(response):
    return render(response, "main/log-out.html")


# Load the page for viewing coins -> when loading loop though all coins in DB and update price from API
def cryptoList(response):
    coins = Coin.objects.all()
    for coin in coins:
        dict = getTickers()
        #find each coin in the api return
        found =  next(item for item in dict if item["symbol"] == coin.ticker)
        price = found['price']
        # set price and save it
        coin.price = price
        coin.save()
        #render crytpo list
    return render(response, "main/cryptoList.html" ,{"coins":coins})

def tickets(response):

    TicketFormSet = modelformset_factory(Ticket, fields=('title', 'query'))
    # queryset = Ticket.objects.filter(__name__.startswith('0'))
    if response.method == 'POST':
        formset = TicketFormSet(response.POST, response.FILES, queryset=Ticket.objects.none())
        if formset.is_valid():
            print(response)
            formset.save()

    else:
        formset = TicketFormSet(queryset=Ticket.objects.none())

    # print(response.user)
    try:
        tickets = Ticket.objects.all()
    except Ticket.DoesNotExist:
        tickets = None


    return render(response, "main/tickets.html", {'formset': formset, 'list': tickets})