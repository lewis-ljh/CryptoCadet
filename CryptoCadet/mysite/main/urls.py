from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("viewList/", views.viewCrypto, name="viewCrypto"),
    path("log-out/", views.logout, name="log-out"),
] 