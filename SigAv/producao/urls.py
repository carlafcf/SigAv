from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'producao'

urlpatterns = [
    path ('', views.home, name='home'),
    path('criar/', views.Criar_Producao.as_view(), name='criar'),
    path('listar/', views.Listar_Producao.as_view(), name='listar'),
    path('editar/<int:pk>', views.Editar_Producao.as_view(), name='editar'),
    path('deletar/<int:pk>', views.Deletar_Producao.as_view(), name='deletar'),
    path('detalhes/<int:pk>', views.detalhes, name='detalhes'),

    path('criar_registro_diario_producao_1/<int:pk>/<int:tipo>', views.criar_registro_diario_1, name='criar_registro_diario_1'),
    path('criar_registro_diario_producao_2/<int:pk>', views.criar_registro_diario_2, name='criar_registro_diario_2'),

    path('editar_registro/<int:pk>/', views.EditarRegistroDiario.as_view(), name='editar_registro'),
    path('deletar_movimento_diario/<int:pk>/', views.DeletarMovimentoDiario.as_view(), name='deletar_movimento_diario'),
 
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('alterar_status/<int:pk>', views.alterar_status, name='alterar_status'),

    path('coleta_diaria/<int:pk>', views.coleta_diaria, name='coleta_diaria'),
]



# url patterns das novas views
urlpatterns += [
    path('bolsista/', views.home_bolsista, name='bolsista'),
    path('', views.home_admin, name='home_admin')
]