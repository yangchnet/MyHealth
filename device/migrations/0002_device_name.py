# Generated by Django 2.1.1 on 2019-03-01 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.TextField(default='', max_length=30, verbose_name='品名'),
        ),
    ]