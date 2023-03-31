from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .APIManager import *
from .models import Coin
# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name":"Test"})


def BuyAndSell(response):
    if response.method=="POST":
        if response.POST.get("sell"):
            if validateSell():
                return render(response, "main/home.html")
            
        if response.POST.get("buy"):
            if validateBuy():
                return render(response, "main/home.html")
    return render(response, "main/BuyAndSell.html", {"tickers": getTickers()})

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