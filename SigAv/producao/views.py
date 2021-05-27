from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Fase_postura
from .forms import ProducaoForm
from lote.models import Lote

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

def cadastrar(request):
    lote_atual = buscar_lote_atual()

    if (request.method == "POST"):
        form = ProducaoForm(request.POST)
        if form.is_valid():
            gaiola = form.cleaned_data['gaiola']
            free_range = form.cleaned_data['free_range']
            caipira = form.cleaned_data['caipira']

            if gaiola > 0:
                fase_postura_gaiola = Fase_postura(
                    lote=lote_atual,
                    tipo_sistema = 'B',
                    data_chegada = date.today(),
                    quantidade_aves_chegada = gaiola,
                    quantidade_aves_final = gaiola
                )
                fase_postura_gaiola.save()
            if free_range > 0:
                fase_postura_free_range = Fase_postura(
                    lote=lote_atual,
                    tipo_sistema = 'A',
                    data_chegada = date.today(),
                    quantidade_aves_chegada = free_range,
                    quantidade_aves_final = free_range
                )
                fase_postura_free_range.save()
            if caipira > 0:
                fase_postura_caipira = Fase_postura(
                    lote=lote_atual,
                    tipo_sistema = 'C',
                    data_chegada = date.today(),
                    quantidade_aves_chegada = caipira,
                    quantidade_aves_final = caipira
                )
                fase_postura_caipira.save()

            lote_atual.status = "C"
            lote_atual.save()
            return redirect("producao:listar")

    else:
        form = ProducaoForm()
    
    informacoes = {
        'lote': lote_atual,
        'form': form
    }

    return render(request, "producao/cadastrar.html", informacoes)

def buscar_lote_atual():
    if (len(Lote.objects.filter(Q(status="A") | Q(status="B"))) > 0):
        return Lote.objects.filter(Q(status="A") | Q(status="B"))[0]
    else:
        return None
