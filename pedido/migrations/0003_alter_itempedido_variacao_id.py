# Generated by Django 5.0.2 on 2024-02-20 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_pedido_qtd_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempedido',
            name='variacao_id',
            field=models.CharField(max_length=50),
        ),
    ]