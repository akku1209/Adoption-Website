# Generated by Django 3.0.8 on 2021-04-26 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article_list',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=500)),
                ('headline', models.CharField(max_length=256)),
                ('link', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Recommended_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec1', models.IntegerField()),
                ('rec2', models.IntegerField()),
                ('rec3', models.IntegerField()),
                ('rec4', models.IntegerField()),
                ('rec5', models.IntegerField()),
                ('idx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Article_list')),
            ],
        ),
    ]
