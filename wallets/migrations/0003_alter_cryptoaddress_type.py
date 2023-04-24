# Generated by Django 4.2 on 2023-04-23 00:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0002_cryptoaddress_created_at_alter_cryptoaddress_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cryptoaddress",
            name="type",
            field=models.CharField(
                choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("LTC", "Litecoin")],
                max_length=10,
                verbose_name="Crypto currency type",
            ),
        ),
    ]
