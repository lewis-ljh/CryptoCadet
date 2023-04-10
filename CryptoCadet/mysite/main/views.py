from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from .APIManager import *
from .forms import DepositWithdrawForm, DepositForm, WithdrawForm
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
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=getUser(response)), "found":False})
            


            
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

from django.urls import reverse

from django.urls import reverse

def show_deposit_withdraw_form(request):
    if request.method == 'POST':
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            request.session['deposit_withdraw_amount'] = float(form.cleaned_data['amount'])
            if form.cleaned_data['type'] == 'deposit':
                return redirect(reverse('deposit') + f'?amount={request.session["deposit_withdraw_amount"]}')
            else:
                return redirect(reverse('withdraw') + f'?amount={request.session["deposit_withdraw_amount"]}')
    else:
        form = DepositWithdrawForm()
    context = {'form': form}
    return render(request, 'main/deposit_withdraw.html', context)




def deposit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = float(request.GET.get('amount', 0))
            profile.account_balance += amount
            profile.save()
            if 'deposit_withdraw_amount' in request.session:
                del request.session['deposit_withdraw_amount']
            messages.success(request, f'Deposit of {amount} was successful.')
            return redirect('home')
    else:
        amount = request.session.pop('deposit_withdraw_amount', None)
        if amount is None:
            messages.error(request, 'Invalid access to deposit page.')
            return redirect('home')
        form = DepositForm()
    context = {'form': form}
    return render(request, 'main/deposit.html', context)



def withdraw(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = float(request.GET.get('amount', 0))
            if amount > profile.account_balance:
                messages.error(request, f'Withdrawal of {amount} failed. Insufficient funds.')
            else:
                profile.account_balance -= amount
                profile.save()
                messages.success(request, f'Withdrawal of {amount} was successful.')
            return redirect('home')
    else:
        amount = request.session.pop('deposit_withdraw_amount', None)
        if amount is None:
            messages.error(request, 'Invalid access to withdraw page.')
            return redirect('home')
        form = WithdrawForm()
    context = {'form': form}
    return render(request, 'main/withdraw.html', context)