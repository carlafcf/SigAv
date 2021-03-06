from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from django.contrib import messages

import json

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Fase_postura, Movimento_diario_postura
from .forms import ProducaoForm, MovimentoDiarioProducaoForm1, MovimentoDiarioProducaoForm2
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
    queryset = Fase_postura.objects.filter(status='A')
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

def detalhes(request, pk):
    lote_postura = Fase_postura.objects.filter(pk=pk)[0]

    informacoes = {
        'producao': lote_postura
    }

    return render(request, "producao/detalhes.html", informacoes)

def buscar_lote_atual():
    if (len(Lote.objects.filter(Q(status="A") | Q(status="B"))) > 0):
        return Lote.objects.filter(Q(status="A") | Q(status="B"))[0]
    else:
        return None


def criar_registro_diario_1(request, pk):
    producao=Fase_postura.objects.filter(id=pk)[0]
    if (request.method == "POST"):
       
        form = MovimentoDiarioProducaoForm1(request.POST)

        if (form.is_valid()):
            data=form.cleaned_data['data']
            if len(Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)) == 0:
                movimento_diario = Movimento_diario_postura()
                movimento_diario.fase_postura=producao
                movimento_diario.data=form.cleaned_data['data']
                movimento_diario.mortalidade=form.cleaned_data['mortalidade']
                movimento_diario.primeira_coleta=form.cleaned_data['primeira_coleta']
                movimento_diario.ovos_quebrados=form.cleaned_data['ovos_quebrados']
                movimento_diario.save()

            else:
                movimento_diario=Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)[0]
                movimento_diario.primeira_coleta=form.cleaned_data['primeira_coleta']
                movimento_diario.mortalidade=form.cleaned_data['mortalidade'] + movimento_diario.mortalidade
                movimento_diario.ovos_quebrados=form.cleaned_data['ovos_quebrados'] + movimento_diario.ovos_quebrados
                movimento_diario.save()
           

            return redirect('producao:detalhes', pk=producao.id)
    else:

        form = MovimentoDiarioProducaoForm1()
 
    
    informacoes = {
        'form':form,
        'producao': producao
    }
    return render(request, "producao/criar_registro_diario.html", informacoes)


def criar_registro_diario_2(request, pk):
    producao=Fase_postura.objects.filter(id=pk)[0]
    if (request.method == "POST"):
       
        form = MovimentoDiarioProducaoForm2(request.POST)

        if (form.is_valid()):
            data=form.cleaned_data['data']
            if len(Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)) == 0:
                movimento_diario = Movimento_diario_postura()
                movimento_diario.fase_postura=producao
                movimento_diario.data=form.cleaned_data['data']
                movimento_diario.mortalidade=form.cleaned_data['mortalidade']
                movimento_diario.segunda_coleta=form.cleaned_data['segunda_coleta']
                movimento_diario.ovos_quebrados=form.cleaned_data['ovos_quebrados']
                movimento_diario.save()

            else:
                movimento_diario=Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)[0]
                movimento_diario.segunda_coleta=form.cleaned_data['segunda_coleta']
                movimento_diario.mortalidade=form.cleaned_data['mortalidade'] + movimento_diario.mortalidade
                movimento_diario.ovos_quebrados=form.cleaned_data['ovos_quebrados'] + movimento_diario.ovos_quebrados
                movimento_diario.save()
           

            return redirect('producao:detalhes', pk=producao.id)
    else:

        form = MovimentoDiarioProducaoForm2()
 
    
    informacoes = {
        'form':form,
        'producao': producao
    }
    return render(request, "producao/criar_registro_diario.html", informacoes)


