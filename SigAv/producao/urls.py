from django.contrib import admin
from django.urls import path
from . import views

app_name = 'producao'

urlpatterns = [
    path('criar/', views.Criar_Producao.as_view(), name='criar'),
    path('listar/', views.Listar_Producao.as_view(), name='listar'),
    path('editar/<int:pk>', views.Editar_Producao.as_view(), name='editar'),
    path('deletar/<int:pk>', views.Deletar_Producao.as_view(), name='deletar'),
    path('detalhes/<int:pk>', views.detalhes, name='detalhes'),

    path('criar_registro_diario_producao_1/<int:pk>', views.criar_registro_diario_1, name='criar_registro_diario_1'),
    path('criar_registro_diario_producao_2/<int:pk>', views.criar_registro_diario_2, name='criar_registro_diario_2'),

    path('editar_registro/<int:pk>/', views.EditarRegistroDiario.as_view(), name='editar_registro'),
    path('deletar_registro/<int:pk>/', views.DeletarRegistroDiario.as_view(), name='deletar_registro'),

    
    path('cadastrar/', views.cadastrar, name='cadastrar'),

]