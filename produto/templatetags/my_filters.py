from django import template
from utils import utils


register = template.Library()

@register.filter
def formata_preco(preco):
    return utils.formata_preco(preco)

@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)

@register.filter
def calc_total_compra(carrinho):
    return utils.calc_total_compra(carrinho)


