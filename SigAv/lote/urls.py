from django.contrib import admin
from django.urls import path
from . import views

app_name = 'lote'

urlpatterns = [
    path('criar/', views.CriarLote.as_view(), name='create'),
    path('listar/', views.ListarLotes.as_view(), name='listar'),
    # path('deletar/', include('lote.urls')),
    # path('editar/'),
    # path('vacinar/'),
    # path('realocar/')
]