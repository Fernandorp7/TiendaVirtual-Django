# Generated by Django 4.1.13 on 2023-12-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_remove_cliente_cliente_id_remove_compra_referencia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(default=0, upload_to='img/productos/'),
            preserve_default=False,
        ),
    ]