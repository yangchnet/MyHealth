# Generated by Django 2.1.5 on 2019-02-12 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myhealth', '0009_auto_20190212_0833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commonreply',
            old_name='commont',
            new_name='reply',
        ),
    ]