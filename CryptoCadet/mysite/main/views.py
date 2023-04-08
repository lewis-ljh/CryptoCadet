from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic import CreateView

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
    
    currentUser = response.user
    ownedCoins = OwnedCoin.objects.all()
    coinName = response.POST.get("BuyOrSell")
    profile = Profile.objects.get(user = currentUser)
    price = getPrice(coinName)

    for coins in ownedCoins:
        coins.price = getPrice(coins.coinName)
        coins.save()


    if response.method=="POST":
        if response.POST.get("sell"):
            

            if validateSell(coinName, float(response.POST.get("HowMuch")), ownedCoins):
                order = Order.objects.create(user=currentUser, coinName=coinName, price=price, type="sell", time=datetime.now())
                order.save()

                for coins in ownedCoins:
                    if currentUser==coins.user and coinName==coins.coinName:
                        coins.amount = coins.amount - float(response.POST.get("HowMuch"))
                        coins.save()
                        profile.account_balance += float(response.POST.get("HowMuch"))*float(price)
                        profile.save()
                        break

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":False})
            


            
        if response.POST.get("buy"):
            coinName = response.POST.get("BuyOrSell")

            if validateBuy(currentUser, coinName, float(response.POST.get("HowMuch")), price):
                order = Order.objects.create(user=currentUser, coinName=coinName, price=price, type="buy", time=datetime.now())
                order.save()

                owned = False
                for coins in ownedCoins:
                    if currentUser==coins.user and coinName==coins.coinName:
                        owned = True
                        coins.amount = coins.amount + float(response.POST.get("HowMuch"))
                        coins.save()
                        profile.account_balance -= float(response.POST.get("HowMuch"))*float(price)
                        profile.save()
                        break

                if not owned:
                    ownedCoin = OwnedCoin.objects.create(user=currentUser, coinName=coinName, amount=float(response.POST.get("HowMuch")))

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":False})
            

    return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":True})


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
    try:
        tickets = Ticket.objects.all()
    except Ticket.DoesNotExist:
        tickets = None
    return render(response, "main/tickets.html", {'list': tickets})


def create_ticket(response):
    TicketFormSet = modelformset_factory(Ticket, fields=('title', 'query'))
    if response.method == 'POST':
        formset = TicketFormSet(response.POST, response.FILES, queryset=Ticket.objects.none())
        title_text = response.POST.get("form-0-title")
        query_text = response.POST.get("form-0-query")

        if formset.is_valid() and title_text != "" and query_text != "": 
            ticket = Ticket.objects.create(user=response.user, title=title_text, query=query_text)
            return tickets(response)
    else:
        formset = TicketFormSet(queryset=Ticket.objects.none())
    return render(response, "main/create-ticket.html", {'formset': formset, })

    