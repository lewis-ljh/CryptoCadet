from django.db import models
from django.contrib.auth.models import User
from main.models import Coin
# Create your models here.

class WatchCoin(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE , null=True, blank=True)
    coin = models.ForeignKey(Coin ,on_delete=models.CASCADE , null=True, blank=True)

    def __str__(self):
        return self.coin.coinName