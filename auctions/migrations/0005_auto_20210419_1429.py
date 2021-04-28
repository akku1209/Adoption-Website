# Generated by Django 3.0.8 on 2021-04-19 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('G', 'No Category'), ('S', 'Shivajinagar'), ('K', 'Kothrud'), ('V', 'Viman nagar'), ('A', 'Aundh'), ('B', 'Baner'), ('P', 'Pashan'), ('K', 'Kondhwa'), ('H', 'Hadapsar'), ('I', 'Kharadi'), ('R', 'Vishrantwadi'), ('M', 'Bavdhan'), ('O', 'Bibvewadi'), ('D', 'Dhanori'), ('T', 'Katraj'), ('G', 'Wagholi'), ('Y', 'Yerwada'), ('W', 'Wanowrie'), ('N', 'Nanded')], default='G', max_length=1)),
                ('contact', models.IntegerField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]