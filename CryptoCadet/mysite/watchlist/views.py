from django.shortcuts import render, redirect
from .models import WatchCoin
from main.models import Coin
from django.contrib.auth.models import User
from .forms import WatchlistForm
# Create your views here.
def watchList(response):
    if response.method == "POST":
        form = WatchlistForm(response.POST)
        form.instance.user = response.user
        if form.is_valid():
            form.save()
            return redirect("/watchlist")
    else:
        form = WatchlistForm()
        form.instance.user = response.user
 
    try:
        items = WatchCoin.objects.all().filter(user=response.user)
    except WatchCoin.DoesNotExist:
        items = None
    return render(response, "watchlist/watchlist.html" ,{"items":items , "form":form})