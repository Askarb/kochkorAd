# Generated by Django 2.0.3 on 2018-06-06 08:00

import applications.helpers.media_path
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20180603_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=applications.helpers.media_path.ad_path),
        ),
    ]
