from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido
from utils.utils import cart_total_qtd, calc_total_compra


class DispatchLoginRiqueredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs
    

class Pagar(DispatchLoginRiqueredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
            'Faça login para continuar.'
            )
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:index')
        
        carrinho = self.request.session.get('carrinho')
        carrinho_id_vars = [v for v in carrinho]
        bd_variacao = list(Variacao.objects.select_related('produto').filter(
            id__in=carrinho_id_vars)
        )

        for variacao in bd_variacao:
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unit = carrinho[vid]['preco_unitario']
            preco_unit_promocional = carrinho[vid]['preco_unitario_descontado']
            pnome = carrinho[vid]['produto_nome']

            if estoque == 0:
                del carrinho[vid]
                messages.error(self.request, 'Produto indisponível no estoque.'
                )
                self.request.session.save()
                return redirect('produto:resumodacompra')
            
            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unit
                carrinho[vid]['preco_quantitativo_descontado'] = estoque * \
                    preco_unit_promocional
                
                self.request.session.save()
                messages.error(self.request, 'Ultima(s) unidade(s) do produto')
                
                return redirect('produto:resumodacompra')
        
        qtd_total_carrinho = cart_total_qtd(carrinho)
        valor_total_compra = calc_total_compra(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_compra,
            qtd_total=qtd_total_carrinho,
            status='C'            
        )
        pedido.save()
        messages.success(self.request, 'Pedido salvo com sucesso!')

        self.request.session['pedido'] = pedido.id
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promo=v['preco_quantitativo_descontado'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem']
                ) for v in carrinho.values()
            ]
        )
        
        del self.request.session['carrinho']
        return redirect(reverse('pedido:pagar', kwargs={'pk': pedido.pk}))


class Detalhes(DispatchLoginRiqueredMixin, DetailView):
    model = Pedido
    template_name = 'pedido/detalhes.html'
    context_object_name = 'pedido'
    pk_url_kwarg = 'pk'


class ListaPedidos(DispatchLoginRiqueredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'    
    template_name = 'pedido/listapedido.html'
    paginate_by = 5
    ordering = ['-id']
