# Generated by Django 2.1.1 on 2019-03-02 04:57

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mhuser', '0004_auto_20190302_0456'),
    ]

    operations = [
        migrations.CreateModel(
            name='Explain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('context', ckeditor_uploader.fields.RichTextUploadingField(max_length=10000, verbose_name='留言')),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('match', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mhuser.Match')),
            ],
        ),
    ]