from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .APIManager import *

# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name":"Test"})


def viewCrypto(response):
    if response.method=="POST":
        if response.POST.get("sell"):
            if validateSell():
                return render(response, "main/home.html")
    return render(response, "main/viewList.html", {"tickers": getTickers()})

def logout(response):
    return render(response, "main/log-out.html")
