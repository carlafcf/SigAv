from django.contrib import admin
from django.urls import path
from . import views

app_name = 'producao'

urlpatterns = [
    path('criar/', views.Criar_Producao.as_view(), name='criar'),
    path('listar/', views.Listar_Producao.as_view(), name='listar'),
    path('editar/<int:pk>', views.Editar_Producao.as_view(), name='editar'),
    path('deletar/<int:pk>', views.Deletar_Producao.as_view(), name='deletar'),
    path('detalhes/<int:pk>', views.Detalhar_Producao.as_view(), name='detalhes'),
]