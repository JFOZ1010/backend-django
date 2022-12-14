# Generated by Django 4.0.3 on 2023-01-03 21:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_ahorro_docasociado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reunionvirtual',
            name='costo',
        ),
        migrations.AddField(
            model_name='reunion',
            name='fechaCreacion',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='reunion',
            name='reunionAsociado',
            field=models.ForeignKey(default='123456789', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='documento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reunionpresencial',
            name='id_reunion',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='presencialReunion', to='api.reunion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reunionvirtual',
            name='id_reunion',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='virtualReunion', to='api.reunion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 3)),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 3)),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 1, 3)),
        ),
        migrations.AlterField(
            model_name='reunion',
            name='asistencia',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reunion',
            name='hora',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='reunion',
            name='motivo',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='reunionpresencial',
            name='sitio',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reunionvirtual',
            name='enlace',
            field=models.CharField(max_length=200),
        ),
        migrations.AddConstraint(
            model_name='reunion',
            constraint=models.UniqueConstraint(fields=('reunionAsociado', 'idReunion'), name='unique_reunionAsociado_idReunion_combination'),
        ),
    ]
