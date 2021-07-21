from django.views.generic import CreateView
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from usuario import forms
from usuario.models import Usuario

class CadastrarUsuario(CreateView):
    form_class = forms.UsuarioForm
    success_url = reverse_lazy('usuario:listar')
    template_name = 'usuario/cadastrar.html'

class EditarUsuario(LoginRequiredMixin, generic.UpdateView):
    model = Usuario
    form_class = forms.UsuarioEditarForm
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('usuario:listar')

@login_required
def listar(request):
    usuarios = Usuario.objects.filter(is_active=True)
    informacoes = {
        'lista_usuarios': usuarios
    }
    return render(request, 'usuario/listar.html', informacoes)

def alterar_status(request, status, pk):
    usuario = Usuario.objects.get(pk=usuario)
    if (status==1):
        usuario.is_active = True
    else:
        usuario.is_active = False
    usuario.save()
    return redirect('usuario:listar')

@login_required
def listar_inativos(request):
    usuarios = Usuario.objects.filter(is_active=False)
    informacoes = {
        'lista_usuarios': usuarios
    }
    return render(request, 'usuario/listar_inativos.html', informacoes)
