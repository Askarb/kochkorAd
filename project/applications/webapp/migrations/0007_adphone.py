# Generated by Django 2.0.3 on 2018-06-03 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_meta_tag_variables'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='webapp.Ad')),
            ],
        ),
    ]
