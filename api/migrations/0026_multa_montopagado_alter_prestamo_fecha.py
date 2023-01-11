# Generated by Django 4.0.3 on 2023-01-09 00:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_abono_idsancion'),
    ]

    operations = [
        migrations.AddField(
            model_name='multa',
            name='montoPagado',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 9)),
        ),
    ]