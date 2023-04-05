from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Coin(models.Model):
    coinName = models.CharField(max_length=30)
    ticker = models.CharField(max_length=10)
    price = models.FloatField(max_length=5 ,null=True, blank=True)

    def __str__(self):
        return self.coinName

class Ticket(models.Model):
    num = models.AutoField(primary_key=True)
    user =  models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)
    query = models.CharField(max_length=500)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    coinName = models.CharField(max_length=10)
    price = models.FloatField(max_length=5 ,null=True)
    type = models.CharField(max_length=4, null=True)
    time = models.DateTimeField()

class OwnedCoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coinName = models.CharField(max_length=10)
    amount = models.FloatField()
    price = models.FloatField(max_length=5, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    account_balance = models.FloatField(default=0.0)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
