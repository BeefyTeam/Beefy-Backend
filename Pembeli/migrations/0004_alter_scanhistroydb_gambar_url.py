# Generated by Django 4.2.1 on 2023-06-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pembeli', '0003_alter_pembelidb_photo_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanhistroydb',
            name='gambar_url',
            field=models.TextField(),
        ),
    ]
