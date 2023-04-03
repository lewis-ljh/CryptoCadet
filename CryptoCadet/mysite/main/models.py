from django.db import models


# Create your models here.
class Coin(models.Model):
    coinName = models.CharField(max_length=30)
    ticker = models.CharField(max_length=10)
    price = models.FloatField(max_length=5 ,null=True)

class Ticket(models.Model):
    num = models.AutoField(primary_key=True)
    user = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)
    query = models.CharField(max_length=500)
 