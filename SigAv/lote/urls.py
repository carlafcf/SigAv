from django.contrib import admin
from django.urls import path
from . import views

app_name = 'lote'

urlpatterns = [
    path('criar/', views.CriarLote.as_view(), name='criar'),
    path('listar/', views.ListarLotes.as_view(), name='listar'),
    path('editar/<int:pk>', views.EditarLote.as_view(), name='editar'),
    path('deletar/<int:pk>', views.DeletarLote.as_view(), name='deletar'),
    path('detalhes/<int:pk>', views.DetalharLote.as_view(), name='detalhes'),
]