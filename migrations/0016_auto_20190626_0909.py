# Generated by Django 2.2.2 on 2019-06-26 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0015_customer_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='month',
        ),
    ]
