# Generated by Django 4.1.7 on 2023-03-30 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_coins_coin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='price',
            field=models.FloatField(max_length=5, null=True),
        ),
    ]
