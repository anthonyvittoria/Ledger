# Generated by Django 2.2.2 on 2019-07-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0025_auto_20190701_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
