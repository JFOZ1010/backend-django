# Generated by Django 4.0.3 on 2023-01-09 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_abono_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abono',
            name='prueba',
        ),
    ]
