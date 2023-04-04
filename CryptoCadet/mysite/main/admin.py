from django.contrib import admin
from .models import Coin, Order, OwnedCoin
# Register your models here.

 
 
admin.site.register(Coin)
admin.site.register(Order)
admin.site.register(OwnedCoin)