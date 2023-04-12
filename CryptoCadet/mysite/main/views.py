from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic import CreateView
from django.urls import reverse
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
            address = Address.objects.get(user=request.user)
            if address:
                street_name, city, post_code, country = address.street_name, address.city, address.post_code, address.country
            else:
                street_name, city, post_code, country = None, None, None, None
            context = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "address": address,
                "street_name": street_name,
                "city": city,
                "post_code": post_code,
                "country": country,
                "phone_number": profile.phone_number,
                "account_balance": profile.account_balance,
                "owned_coins": OwnedCoin.objects.filter(user=request.user)
            }
        except Profile.DoesNotExist:
            context = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "address": None,
                "street_name": None,
                "city": None,
                "post_code": None,
                "country": None,
                "phone_number": None,
                "account_balance": None,
                "owned_coins": None
            }
        return render(request, self.template_name, context)


def BuyAndSell(response):

    currentUser = response.user
    ownedCoins = OwnedCoin.objects.all().filter(User=response.user)
    coinName = response.POST.get("BuyOrSell")
    profile = Profile.objects.get(user = currentUser)
    price = getPrice(coinName)

    for coins in ownedCoins:
        coins.price = getPrice(coins.coinName)
        coins.save()


    if response.method=="POST":
        if response.POST.get("sell"):


            if validateSell(coinName, response.POST.get("HowMuch"), ownedCoins):

                for coins in ownedCoins:
                    if currentUser==coins.user and coinName==coins.coinName:
                        if (coins.amount - float(response.POST.get("HowMuch")) >= 0):
                            order = Order.objects.create(user=currentUser, coinName=coinName, price=price, type="sell", time=datetime.now())
                            order.save()
                            coins.amount = coins.amount - float(response.POST.get("HowMuch"))
                            coins.save()
                            profile.account_balance += float(response.POST.get("HowMuch"))*float(price)
                            profile.save()
                            break
                        else:
                            return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":False})

                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":True})
            else:
                return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":False})
            


            
        if response.POST.get("buy"):
            coinName = response.POST.get("BuyOrSell")

            if validateBuy(currentUser, coinName, response.POST.get("HowMuch"), price):
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


    return render(response, "main/BuyAndSell.html", {"coins":OwnedCoin.objects.filter(user=currentUser), "found":None})


def previousTrades(response):
    trades = Order.objects.filter(user=response.user)
    return render(response, "main/previousTrades.html", {"trades":reversed(trades)})




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



def show_deposit_withdraw_form(request):
    if request.method == 'POST':
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            amount = float(form.cleaned_data['amount'])
            if amount <= 0:
                form.add_error('amount', 'Amount must be positive.')
                context = {'form': form}
                return render(request, 'main/deposit_withdraw.html', context)
            request.session['deposit_withdraw_amount'] = amount
            if form.cleaned_data['type'] == 'deposit':
                return redirect(reverse('deposit') + f'?amount={request.session["deposit_withdraw_amount"]}')
            elif form.cleaned_data['type'] == 'withdraw' and amount > request.user.profile.account_balance:
                form.add_error('amount', 'Withdraw amount cannot be greater than account balance.')
                context = {'form': form}
                return render(request, 'main/deposit_withdraw.html', context)
            else:
                # Withdrawal amount is valid, continue with redirect
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
                # change that to be in a form
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