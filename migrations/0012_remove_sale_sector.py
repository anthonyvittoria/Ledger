# Generated by Django 2.2.2 on 2019-06-25 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0011_remove_location_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='sector',
        ),
    ]
