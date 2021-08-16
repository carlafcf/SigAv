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

@login_required
def listar_inativos(request):
    usuarios = Usuario.objects.filter(is_active=False)
    informacoes = {
        'lista_usuarios': usuarios
    }
    return render(request, 'usuario/listar_inativos.html', informacoes)

def alterar_status(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    if (usuario.is_active):
        usuario.is_active = False
    else:
        usuario.is_active = True
    usuario.save()
    return redirect('usuario:listar')
