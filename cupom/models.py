from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Cupom(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Dono cupom')
    name = models.CharField(max_length=20)
    desconto = models.FloatField(verbose_name='Desconto')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'