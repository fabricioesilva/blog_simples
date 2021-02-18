from django.urls import path
from . import views


urlpatterns = [
    path('categoria/<int:pk>', views.Categoria.as_view(), name='categoria')
]
