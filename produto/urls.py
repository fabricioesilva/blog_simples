from django.urls import path
from .admin import VariacaoAdmin
from . import views


app_name = 'produto'

urlpatterns = [
    path('', views.ListaProduto.as_view(), name='index'),
    path('export/', views.Export.as_view(), name='export'),
    path('<slug>', views.DetalhesProduto.as_view(), name='detalhes'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),
    path('busca/', views.Busca.as_view(), name='busca'),
]
    


