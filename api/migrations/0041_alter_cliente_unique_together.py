# Generated by Django 4.0.3 on 2023-01-24 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_alter_cliente_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cliente',
            unique_together=set(),
        ),
    ]
