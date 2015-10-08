from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    fixtures = 'films people planets species starships transport vehicles'.split(' ')
    call_command('loaddata', *fixtures)


class Migration(migrations.Migration):

    dependencies = [
        ('starwars', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]
