# Generated by Django 5.0.2 on 2024-02-14 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_produto_estoque_alter_produto_preco_marketing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='estoque',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
