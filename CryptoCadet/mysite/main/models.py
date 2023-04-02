from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Coin(models.Model):
    coinName = models.CharField(max_length=30)
    ticker = models.CharField(max_length=10)
    price = models.FloatField(max_length=5, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    account_balance = models.FloatField()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
