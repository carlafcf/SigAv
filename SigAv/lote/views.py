from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView
from .models import Lote

from django.db import connection

class CriarLote(CreateView):
    model = Lote
    fields = ['localidade', 'data_chegada', 'quantidade_inicial']
    template_name = 'lote/criar_lote.html'
    # form

    def get_success_url(self):
        return reverse_lazy('lote:listar')

class ListarLotes(ListView):
    model = Lote
    template_name = 'lote/listar_lotes.html'
    # lote_list

