# Generated by Django 4.0.3 on 2023-01-09 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_remove_multa_asociadoreferente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='abono',
            name='prueba',
            field=models.CharField(max_length=50, null=True),
        ),
    ]