# Generated by Django 4.2.1 on 2023-06-03 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Penjual', '0002_rename_id_penjual_produkdb_id_toko'),
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='ID_BARANG',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Penjual.produkdb'),
        ),
    ]
