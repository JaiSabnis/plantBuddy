# Generated by Django 3.0.6 on 2020-05-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0012_auto_20200530_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plants',
            field=models.ManyToManyField(blank=True, related_name='plants', to='hello.Plant'),
        ),
    ]
