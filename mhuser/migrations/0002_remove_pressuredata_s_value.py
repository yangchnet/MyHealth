# Generated by Django 2.1.5 on 2019-03-08 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mhuser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pressuredata',
            name='s_value',
        ),
    ]
