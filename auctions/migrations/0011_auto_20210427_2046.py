# Generated by Django 3.0.8 on 2021-04-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_delete_recommended_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_list',
            name='cos_sim',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='article_list',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
