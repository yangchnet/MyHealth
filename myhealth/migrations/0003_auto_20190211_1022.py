# Generated by Django 2.1.5 on 2019-02-11 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myhealth', '0002_auto_20190211_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctoruser',
            name='is_normal',
        ),
        migrations.RemoveField(
            model_name='normaluser',
            name='is_normal',
        ),
    ]