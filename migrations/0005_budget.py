# Generated by Django 2.2.2 on 2019-06-24 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0004_sector'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Ledger.Customer')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Ledger.Location')),
            ],
        ),
    ]
