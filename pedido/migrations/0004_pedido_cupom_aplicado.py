# Generated by Django 5.0.2 on 2024-02-25 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cupom', '0002_alter_cupom_options'),
        ('pedido', '0003_alter_itempedido_variacao_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cupom_aplicado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cupom.cupom'),
        ),
    ]
