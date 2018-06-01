from django.db import migrations

from applications.webapp.models import Variable


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_message_variable'),
    ]

    def set_initial_variables(apps, schema_editor):
        Variable.objects.get_or_create(name='email', defaults={'name': 'email', 'value': 'kochkorjarnama@gmail.com'})

    operations = [
        migrations.RunPython(set_initial_variables),
    ]
