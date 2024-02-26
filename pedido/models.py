from django.db import models
from django.contrib.auth.models import User
from cupom import models as cupom

# Create your models here.
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    cupom_aplicado = models.ForeignKey(cupom.Cupom,on_delete = models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(
        default = 'C',
        max_length = 1,
        choices = (
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado')
        )
    )


    def __str__(self):
        return f'Pedido Número {self.pk}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.CharField(max_length=50)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'
    
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'