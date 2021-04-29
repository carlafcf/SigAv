from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Fase_postura

from django.db import connection

class Criar_Producao(CreateView):
    model = Fase_postura
    fields = ['lote', 'tipo_sistema', 'data_chegada', 'quantidade_aves_chegada', 'quantidade_aves_final',
                'observacoes']
    template_name = 'producao/criar.html'
    # form

    def get_success_url(self):
        return reverse_lazy('producao:listar')

class Listar_Producao(ListView):
    model = Fase_postura
    template_name = 'producao/listar.html'
    # lote_list

class Editar_Producao(UpdateView):
    model = Fase_postura
    fields = ['lote', 'tipo_sistema', 'data_chegada', 'quantidade_aves_chegada', 'quantidade_aves_final',
                'observacoes']
    template_name = 'producao/editar.html'
    success_url = reverse_lazy('producao:listar')
    # form

class Deletar_Producao(DeleteView):
    model = Fase_postura
    template_name = 'producao/confirmacao_deletar.html'
    success_url = reverse_lazy('producao:listar')
    # object

class Detalhar_Producao(DetailView):
    model = Fase_postura
    template_name = 'producao/detalhes.html'
    # object
