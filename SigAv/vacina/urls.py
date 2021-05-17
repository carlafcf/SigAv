from django.contrib import admin
from django.urls import path
from . import views

app_name = 'vacina'

urlpatterns = [
    path('criar/', views.CriarVacina.as_view(), name='criar'),
    path('listar/', views.ListarVacina.as_view(), name='listar'),
    path('editar/<int:pk>', views.EditarVacina.as_view(), name='editar'),
    path('deletar/<int:pk>', views.DeletarVacina.as_view(), name='deletar'),
    path('detalhes/<int:pk>', views.DetalharVacina.as_view(), name='detalhes'),
]