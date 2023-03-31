from django.shortcuts import render
from .models import WatchCoin
# Create your views here.
def watchList(response):
    items = WatchCoin.objects.all()
    return render(response, "watchlist/watchlist.html" ,{"items":items})