# Generated by Django 4.0.3 on 2023-01-05 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 5)),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 5)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 5)),
        ),
    ]