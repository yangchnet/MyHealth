# Generated by Django 2.1.1 on 2019-03-01 06:08

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20190301_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='cover1',
            field=imagekit.models.fields.ProcessedImageField(default=None, upload_to='device/Cover'),
        ),
        migrations.AlterField(
            model_name='device',
            name='cover2',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/Cover'),
        ),
        migrations.AlterField(
            model_name='device',
            name='cover3',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/Cover'),
        ),
        migrations.AlterField(
            model_name='device',
            name='cover4',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/Cover'),
        ),
        migrations.AlterField(
            model_name='device',
            name='cover5',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/Cover'),
        ),
        migrations.AlterField(
            model_name='device',
            name='detailimage1',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/detailimage'),
        ),
        migrations.AlterField(
            model_name='device',
            name='detailimage2',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/detailimage'),
        ),
        migrations.AlterField(
            model_name='device',
            name='detailimage3',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/detailimage'),
        ),
        migrations.AlterField(
            model_name='device',
            name='detailimage4',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/detailimage'),
        ),
        migrations.AlterField(
            model_name='device',
            name='detailimage5',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, null=True, upload_to='device/detailimage'),
        ),
    ]
