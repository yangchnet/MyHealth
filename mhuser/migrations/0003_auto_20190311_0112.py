# Generated by Django 2.1.5 on 2019-03-11 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhuser', '0002_remove_pressuredata_s_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='heartdata',
            name='diviceid',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='oxygendata',
            name='diviceid',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pressuredata',
            name='diviceid',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='temdata',
            name='diviceid',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
