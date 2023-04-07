from django.urls import path
from . import views
from watchlist import views as wlv
from exam import views as EView
from register import views as RView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("BuyAndSell/", views.BuyAndSell, name="BuyAndSell"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path("log-out/", views.logout, name="log-out"),
    path("cryptoList/", views.cryptoList, name="CryptoList"),
    path("tickets/", views.tickets, name="tickets"),
    path("personal_info/", views.ViewPersonalInformation.as_view(), name="personal_info"),
    path("register/", RView.register, name="register"),
    path('FillPersonalInfo/<int:user_id>/', RView.personal_info, name='personal_info'),
    path("watchlist/", wlv.watchList, name="watchlist"),
    path("deleteItem/<int:item_id>/", wlv.deleteItem,name="deleteItem"),
    path("previousTrades", views.previousTrades, name="previousTrades"),
    path("exam/", EView.take_quiz, name="exam"),
    path("create-ticket", views.create_ticket, name='create-ticket')

]
 