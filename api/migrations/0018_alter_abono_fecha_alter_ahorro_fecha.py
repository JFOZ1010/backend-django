# Generated by Django 4.0.3 on 2023-01-05 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_abono_fecha_alter_ahorro_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abono',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ahorro',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]