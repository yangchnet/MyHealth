# Generated by Django 2.1.5 on 2019-02-11 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myhealth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoruser',
            name='is_normal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='normaluser',
            name='is_normal',
            field=models.BooleanField(default=True),
        ),
    ]