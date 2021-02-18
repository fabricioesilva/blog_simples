from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
# from django.http import HttpResponse
from .models import Produto, Variacao
from categoria.models import Categoria
from django.db.models import Q
from django.contrib import messages
from perfil.models import Perfil
from utils.utils import aplica_desconto


class ListaProduto(ListView):
    model = Produto
    template_name = 'produto/index.html'
    context_object_name = 'produtos'
    paginate_by = 3
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class DetalhesProduto(DetailView):      
    model = Variacao
    context_object_name = 'variacao'
    slug_url_kwarg = 'slug'
    template_name = 'produto/detalhes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        variacao_detalhe = context['variacao']
        
        if variacao_detalhe.desconto_var:
            preco_descontado = aplica_desconto(
                variacao_detalhe.preco,
                variacao_detalhe.desconto_var
            )
            context['variacao'].preco_descontado = preco_descontado

        object_list = [variacoes for variacoes in Variacao.objects.
            select_related('produto').filter(produto=variacao_detalhe.produto)]

        context['variacoes'] = object_list
        #     'variacoes': object_list,
        context['categorias'] = Categoria.objects.all()
        # }
        return context


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER',
         reverse('produto:index'))
        
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto em falta no estoque.')
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        produto = variacao.produto
        produto_id = produto.id
        produto_nome = produto.nome_generico
        slug = variacao.slug

        imagem = variacao.imagem
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(self.request, 'Sem produto no estoque.')
            return redirect(http_referer)
        else:
            variacao_estoque = variacao.estoque

        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        desconto = variacao.desconto_var
        if desconto:
            preco_unitario_descontado = aplica_desconto(
                preco_unitario,
                desconto
            )
        else:
            preco_unitario_descontado = preco_unitario
        
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.error(self.request, 'Estoque insuficiente.')
                quantidade_carrinho = variacao_estoque
                return redirect(http_referer)
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_descontado'] = \
                preco_unitario_descontado * quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_descontado': preco_unitario_descontado,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_descontado': preco_unitario_descontado,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()
        messages.success(
            self.request,
            'Produto adicionado ao carrinho. '
            f'Há {carrinho[variacao_id]["quantidade"]} do produto no carrionho.'
        )
        
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER',
            reverse('produto:carrinho')
            )
        carrinho = self.request.session.get('carrinho')

        variacao_id = self.request.GET.get('vid')
        
        # se não vier variacao_id que origina na <select name="vid"
        if not variacao_id:  
            return redirect(http_referer)

        # se não vier variacao_id que origina na <select name="vid"
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        messages.success(self.request,
        f'{carrinho[variacao_id]["produto_nome"]} foi removido do carrinho.'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()                
    
        return redirect(http_referer)


class ResumoDaCompra(View):
    # template_name = 'produto/index.html'
    # def get(self, *args, **kwargs):
    #     return render(self.request, self.template_name)

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.info(self.request, 'Faça login para continuar.')
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            return redirect('produto:index')
        
        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.info(self.request,
            'Complete dados do perfil para continuar'
            )
            return redirect('perfil:criar')
        
        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)


        return HttpResponse('Listar produtos')


class Carrinho(View):
    def get(self, request, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('produto:index'),
                                            )

        contexto = {
            'carrinho': self.request.session.get('carrinho', {}),
            'http_referer': http_referer,
        }

        try:
            return render(self.request, 'produto/carrinho.html', contexto)
        except Exception:
            return redirect('produto/index.html')


class Busca(ListaProduto):

    def get_queryset(self):

        qs = super().get_queryset()
        termo = self.request.GET.get('termo') or self.request.session['termo']

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(categoria__nome_cat__icontains=termo) |
            Q(variacao__nome__icontains=termo) |
            Q(nome_generico__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(marca__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        if not qs:
            messages.error(self.request, 'Nenhum produto encontrado.')
            return super().get_queryset()
        
        self.request.session.save()

        return qs
        

class Export(View):
    def get(self, *args, **kwargs):
        return HttpResponse('isso aí')

