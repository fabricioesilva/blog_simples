from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    data_pedido = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado')
        )
    )

    def __str__(self):
        return f'Pedido número {self.pk}.'
    

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promo = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do pedido {self.pedido}.'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
