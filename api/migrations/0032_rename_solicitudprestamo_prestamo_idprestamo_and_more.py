# Generated by Django 4.0.3 on 2023-01-11 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_remove_abono_prueba'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestamo',
            old_name='solicitudPrestamo',
            new_name='idPrestamo',
        ),
        migrations.AddField(
            model_name='prestamo',
            name='pagoDeuda',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='codeudor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='documento'),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='deudor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]
