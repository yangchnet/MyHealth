# Generated by Django 2.1.1 on 2019-03-01 05:40

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover1', imagekit.models.fields.ProcessedImageField(default=None, upload_to='decice/Cover')),
                ('cover2', imagekit.models.fields.ProcessedImageField(default=None, upload_to='decice/Cover')),
                ('cover3', imagekit.models.fields.ProcessedImageField(default=None, upload_to='decice/Cover')),
                ('cover4', imagekit.models.fields.ProcessedImageField(default=None, upload_to='decice/Cover')),
                ('cover5', imagekit.models.fields.ProcessedImageField(default=None, upload_to='decice/Cover')),
                ('label', models.TextField(default='', max_length=50, verbose_name='标签')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('price', models.FloatField(default=0.0, verbose_name='价格')),
                ('detailimage1', imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/detailimage')),
                ('detailimage2', imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/detailimage')),
                ('detailimage3', imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/detailimage')),
                ('detailimage4', imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/detailimage')),
                ('detailimage5', imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/detailimage')),
            ],
        ),
    ]
