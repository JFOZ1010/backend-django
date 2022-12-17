# Generated by Django 4.0.3 on 2022-12-15 22:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abono',
            options={'verbose_name': 'Abono', 'verbose_name_plural': 'Abonos'},
        ),
        migrations.AddField(
            model_name='abono',
            name='abona',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='documento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ahorro',
            name='DocAsociado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='documento'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abono',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 15)),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='descripcion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 15)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 12, 15)),
        ),
        migrations.AlterField(
            model_name='user',
            name='documento',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]