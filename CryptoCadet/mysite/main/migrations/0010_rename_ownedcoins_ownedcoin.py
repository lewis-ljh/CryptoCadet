# Generated by Django 4.1.7 on 2023-04-04 09:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_alter_order_coinname_ownedcoins'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OwnedCoins',
            new_name='OwnedCoin',
        ),
    ]
