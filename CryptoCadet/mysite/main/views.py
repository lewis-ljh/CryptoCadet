from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from .APIManager import *
from .models import Coin, Address, Profile


# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name": "Test"})


class ViewPersonalInformation(View):
    template_name = "main/personal_info.html"

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            address = Address.objects.get(user=request.user)
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
    if response.method == "POST":
        if response.POST.get("sell"):
            if validateSell():
                return render(response, "main/home.html")

        if response.POST.get("buy"):
            if validateBuy():
                return render(response, "main/home.html")
    return render(response, "main/BuyAndSell.html", {"tickers": getTickers()})


def logout(response):
    return render(response, "main/log-out.html")


# Load the page for viewing coins -> when loading loop though all coins in DB and update price from API
def cryptoList(response):
    coins = Coin.objects.all()
    for coin in coins:
        dict = getTickers()
        # find each coin in the api return
        found = next(item for item in dict if item["symbol"] == coin.ticker)
        price = found['price']
        # set price and save it
        coin.price = price
        coin.save()
        # render crytpo list
    return render(response, "main/cryptoList.html", {"coins": coins})
