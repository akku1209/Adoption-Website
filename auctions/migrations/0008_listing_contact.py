# Generated by Django 3.0.8 on 2021-04-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='contact',
            field=models.IntegerField(null=True),
        ),
    ]
