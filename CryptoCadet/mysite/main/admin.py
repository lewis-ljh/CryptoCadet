from django.contrib import admin
from .models import Coin, Order, OwnedCoin, Profile
# Register your models here.

 
 
admin.site.register(Coin)
admin.site.register(Order)
admin.site.register(OwnedCoin)
admin.site.register(Profile)