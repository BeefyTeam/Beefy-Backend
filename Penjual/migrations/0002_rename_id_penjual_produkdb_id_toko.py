# Generated by Django 4.2.1 on 2023-05-31 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Penjual', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produkdb',
            old_name='ID_PENJUAL',
            new_name='ID_TOKO',
        ),
    ]
