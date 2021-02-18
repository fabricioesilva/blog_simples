from django.urls import path, include
# auth_view é usado por Geek university aula 107, para logout
from django.contrib.auth import views as auth_views
from . import views


app_name = 'perfil'


urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
