from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Lote, Registro_diario_lote

from django.db import connection

class CriarLote(CreateView):
    model = Lote
    fields = ['codigo', 'data_chegada', 'localidade', 'aptidao',
                'quantidade_aves_chegada', 'raca']
    template_name = 'lote/criar.html'
    # form

    def get_success_url(self):
        return reverse_lazy('lote:listar')

class ListarLotes(ListView):
    model = Lote
    template_name = 'lote/listar.html'
    # lote_list

class EditarLote(UpdateView):
    model = Lote
    fields = ['data_chegada', 'localidade', 'aptidao',
                'quantidade_aves_chegada', 'raca']
    template_name = 'lote/editar.html'
    success_url = reverse_lazy('lote:listar')
    # form

class DeletarLote(DeleteView):
    model = Lote
    template_name = 'lote/confirmacao_deletar.html'
    success_url = reverse_lazy('lote:listar')
    # object

class DetalharLote(DetailView):
    model = Lote
    template_name = 'lote/detalhes.html'
    # object
