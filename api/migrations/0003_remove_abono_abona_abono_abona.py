# Generated by Django 4.0.3 on 2022-12-10 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_abono_options_abono_abona_alter_abono_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abono',
            name='Abona',
        ),
        migrations.AddField(
            model_name='abono',
            name='abona',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='documento'),
            preserve_default=False,
        ),
    ]
