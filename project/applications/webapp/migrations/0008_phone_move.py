from django.db import migrations

from applications.webapp.models import Ad, AdPhone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_adphone'),
    ]

    def move_phone_numbers(apps, schema_editor):
        try:
            for ad in Ad.objects.all():
                if ad.phone1:
                    AdPhone.objects.create(ad=ad, phone=ad.phone1)
                if ad.phone2:
                    AdPhone.objects.create(ad=ad, phone=ad.phone2)
        except:
            pass

    operations = [
        migrations.RunPython(move_phone_numbers),
    ]
