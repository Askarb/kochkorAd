from django.db import migrations

from applications.webapp.models import Variable


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20180601_1530'),
    ]

    def add_variables(apps, schema_editor):
        Variable.objects.get_or_create(name='meta_title', defaults={'name': 'meta_title', 'value': 'Кочкор реклама'})
        Variable.objects.get_or_create(name='meta_description', defaults={
            'name': 'meta_description',
            'value': 'Крупнейший сайт бесплатных объявлений в Кыргызстане. Самый простой способ купить и продать б/у товар на доске объявлений kochkorcity.kg.'})
        Variable.objects.get_or_create(name='meta_keywords', defaults={
            'name': 'meta_keywords',
            'value': 'кочкор, реклама, жарнама, нарын, атбашы, жумгал, kochkor, naryn, бекер'
        })


    operations = [
        migrations.RunPython(add_variables),
    ]
