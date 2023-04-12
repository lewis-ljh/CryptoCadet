from django.shortcuts import render, redirect
from .models import WatchCoin
from main.models import Coin
from django.contrib.auth.models import User
from .forms import WatchlistForm
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WatchCoin
from main.models import Coin
from .forms import WatchlistForm


@login_required
def watchList(request):
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        form.instance.user = request.user
        if form.is_valid() and form.cleaned_data['coin'] is not None:
            coin = form.cleaned_data['coin']
            # Check if the coin is already in the user's watchlist
            if WatchCoin.objects.filter(user=request.user, coin=coin).exists():
                form.add_error('coin', 'Coin is already in your watchlist.')
            else:
                form.save()
                return redirect("/watchlist")
    else:
        form = WatchlistForm()
        form.instance.user = request.user

    items = WatchCoin.objects.filter(user=request.user)
    return render(request, "watchlist/watchlist.html", {"items": items, "form": form})


def deleteItem(request,item_id):
    item = WatchCoin.objects.all().filter(id=item_id)
    item.delete()
    return redirect("/watchlist")