# Generated by Django 2.2.2 on 2019-06-25 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0013_customer_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='sector',
        ),
    ]
