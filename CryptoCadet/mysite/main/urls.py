from django.urls import path
from . import views
from watchlist import views as wlv

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("BuyAndSell/", views.BuyAndSell, name="BuyAndSell"),
    path("log-out/", views.logout, name="log-out"),
    path("cryptoList/", views.cryptoList, name="CryptoList"),
    path("personal_info/", views.ViewPersonalInformation.as_view(), name="personal_info"),
    path("watchlist/", wlv.watchList, name="watchlist"),
] 