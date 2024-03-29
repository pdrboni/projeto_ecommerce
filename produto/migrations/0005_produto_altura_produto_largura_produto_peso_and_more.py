# Generated by Django 5.0.2 on 2024-02-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_remove_variacao_variacao_produto_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='altura',
            field=models.FloatField(default=6, verbose_name='Altura (cm)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='largura',
            field=models.FloatField(default=6, verbose_name='Largura (cm)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='peso',
            field=models.FloatField(default=1, verbose_name='Peso (kg)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='profundidade',
            field=models.FloatField(default=6, verbose_name='Profundidade (cm)'),
            preserve_default=False,
        ),
    ]
