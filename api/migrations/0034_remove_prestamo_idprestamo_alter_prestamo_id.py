# Generated by Django 4.0.3 on 2023-01-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_remove_abono_cuentaprestamo_prestamo_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestamo',
            name='idPrestamo',
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]