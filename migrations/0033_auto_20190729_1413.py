# Generated by Django 2.2.3 on 2019-07-29 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0032_auto_20190729_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='sector',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='Ledger.Sector'),
        ),
    ]
