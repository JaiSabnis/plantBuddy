# Generated by Django 3.0.6 on 2020-05-18 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0008_auto_20200513_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='FanBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('fans', models.ManyToManyField(blank=True, related_name='fans', to=settings.AUTH_USER_MODEL)),
                ('founder', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='founder', to=settings.AUTH_USER_MODEL)),
                ('localPros', models.ManyToManyField(blank=True, related_name='localPros', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='flight',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='flights',
        ),
        migrations.AlterField(
            model_name='profile',
            name='friendRequests',
            field=models.ManyToManyField(blank=True, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Airport',
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
        migrations.DeleteModel(
            name='Passenger',
        ),
    ]