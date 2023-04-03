from django.shortcuts import render
from .models import WatchCoin
# Create your views here.
def watchList(response):
    try:
        items = WatchCoin.objects.all().filter(user=response.user)
    except WatchCoin.DoesNotExist:
        items = None
    return render(response, "watchlist/watchlist.html" ,{"items":items})