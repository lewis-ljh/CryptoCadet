from django.urls import path
from . import views
from watchlist import views as wlv
from exam import views as ev
urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("BuyAndSell/", views.BuyAndSell, name="BuyAndSell"),
    path("log-out/", views.logout, name="log-out"),
    path("cryptoList/", views.cryptoList, name="CryptoList"),
    path("tickets/", views.tickets, name="tickets"),
    path("watchlist/", wlv.watchList, name="watchlist"),
    path("exam/", ev.take_quiz, name="exam"),
] 
