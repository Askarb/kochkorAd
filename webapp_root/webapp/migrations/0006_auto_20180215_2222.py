# Generated by Django 2.0 on 2018-02-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20171125_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='rise_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ad',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
