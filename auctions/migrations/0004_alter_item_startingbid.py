# Generated by Django 4.1.2 on 2022-11-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_listing_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='startingbid',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
