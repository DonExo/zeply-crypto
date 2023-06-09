# Generated by Django 4.2 on 2023-04-22 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CryptoAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum")],
                        max_length=10,
                        verbose_name="Crypto currency type",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        max_length=128, verbose_name="Crypto currency address"
                    ),
                ),
            ],
        ),
    ]
