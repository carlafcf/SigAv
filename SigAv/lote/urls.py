from django.contrib import admin
from django.urls import path
from . import views

app_name = 'lote'

urlpatterns = [
    path('criar/', views.criar_lote, name='criar'),
    path('listar/', views.ListarLotes.as_view(), name='listar'),
    path('listar_finalizados/', views.listar_finalizados, name='listar_finalizados'),
    path('editar/<int:pk>', views.EditarLote.as_view(), name='editar'),
    path('deletar/<int:pk>', views.DeletarLote.as_view(), name='deletar'),
    path('detalhes/', views.detalhes, name='detalhes'),
    path('detalhes_finalizado/<int:pk>', views.detalhes_finalizado, name='detalhes_finalizado'),

    path('criar_registro_diario_lote/', views.criar_registro_diario, name='criar_registro_diario'),
    path('editar_registro/<int:pk>/', views.EditarRegistroDiario.as_view(), name='editar_registro'),
    path('deletar_registro/<int:pk>/', views.DeletarRegistroDiario.as_view(), name='deletar_registro'),


    path('alterar_status/', views.alterar_status, name="alterar_status"),
]


