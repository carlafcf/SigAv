#from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path

from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar/', views.CadastrarUsuario.as_view(), name='cadastrar'),
    path('editar/<int:pk>', views.EditarUsuario.as_view(), name = 'editar'),
    path('listar/', views.listar, name='listar'),
    path('listar_inativos/', views.listar_inativos, name='listar_inativos'),
    path('alterar_status/<int:status>/<int:pk>', views.alterar_status, name='alterar_status'),
]
