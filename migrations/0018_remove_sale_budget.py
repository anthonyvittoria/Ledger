# Generated by Django 2.2.2 on 2019-06-26 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0017_auto_20190626_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='budget',
        ),
    ]
