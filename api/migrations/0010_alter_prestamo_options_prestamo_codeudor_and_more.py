# Generated by Django 4.0.3 on 2022-12-28 23:54


import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_abono_cuentaahorro_alter_abono_fecha_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prestamo',
            options={'verbose_name': 'prestamo', 'verbose_name_plural': 'prestamos'},
        ),
        migrations.AddField(
            model_name='prestamo',
            name='codeudor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prestamoCodeudor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prestamo',
            name='deudor',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='prestamoDeudor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 28)),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 28)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 28)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='solicitudPrestamo',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
