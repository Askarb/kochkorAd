from django.db import migrations

from applications.webapp.models import Variable


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20180606_1400'),
    ]

    def change_language(apps, schema_editor):
        Variable.objects.get_or_create(name='change_language', defaults={'name': 'change_language', 'value': '0'})

    operations = [
        migrations.RunPython(change_language),
    ]
