from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("BuyAndSell/", views.BuyAndSell, name="BuyAndSell"),
    path("log-out/", views.logout, name="log-out"),
    path("cryptoList/", views.cryptoList, name="CryptoList"),
    path("tickets/", views.tickets, name="tickets"),
] 