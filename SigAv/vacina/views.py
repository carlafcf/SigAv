from django.db import connection
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

import vacina

from .forms import AplicacaoVacinaForm, TempoVacinacaoForm, VacinaForm
from .models import AplicacaoVacina, TempoVacinacao, Vacina


class CriarVacina(CreateView):
    model = Vacina
    fields = ['tipo', 'doses']
    template_name = 'vacina/criar.html'
    # form

    def get_success_url(self):
        return reverse_lazy('vacina:listar')


class ListarVacina(ListView):
    model = Vacina
    template_name = 'vacina/listar.html'
    # lote_list


class EditarVacina(UpdateView):
    model = Vacina
    fields = ['tipo', 'doses']
    template_name = 'vacina/editar.html'
    success_url = reverse_lazy('vacina:listar')
    # form


class DeletarVacina(DeleteView):
    model = Vacina
    template_name = 'vacina/confirmacao_deletar.html'
    success_url = reverse_lazy('vacina:listar')
    # object


class DetalharVacina(DetailView):
    model = Vacina
    template_name = 'vacina/detalhes.html'
    # object


def Vacina(request):
    if(request.method == "POST"):
        form = VacinaForm(request.POST)
        if(form.is_valid()):
            vacina = Vacina()
            vacina.tipo = form.cleaned_data['tipo']
            vacina.doses = form.cleaned_data['doses']
        return render(request, 'vacina/criar')
