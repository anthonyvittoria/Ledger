# Generated by Django 2.2.2 on 2019-06-24 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesQuery', '0003_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('name', models.CharField(max_length=45, primary_key=True, serialize=False)),
            ],
        ),
    ]
