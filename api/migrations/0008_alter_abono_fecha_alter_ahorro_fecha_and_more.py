# Generated by Django 4.0.3 on 2022-12-17 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_merge_20221216_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 17)),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 17)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 17)),
        ),
    ]
