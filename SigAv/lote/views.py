from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from django.contrib import messages

import json

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Lote, Registro_diario_lote
from .forms import LoteForm, RegistroDiarioLoteForm

def criar_lote(request):
    if (request.method == "POST"):
        form = LoteForm(request.POST)
        if (form.is_valid()):
            lote = Lote()
            lote.data_chegada = form.cleaned_data['data_chegada']
            lote.localidade = form.cleaned_data['localidade']
            lote.aptidao = form.cleaned_data['aptidao']
            lote.raca = form.cleaned_data['raca']
            lote.quantidade_aves_chegada = form.cleaned_data['quantidade_aves_chegada']
            lote.quantidade_aves_final = lote.quantidade_aves_chegada

            ano = lote.data_chegada.year
            quantidade_lotes_ano = Lote.objects.filter(data_chegada__year = ano).order_by('-codigo').count()
            lote.codigo = str(ano)+"."+format(quantidade_lotes_ano+1, "03d")
            lote.save()
            messages.success(request, 'Lote ' + lote.codigo + ' criado com sucesso.')
            return redirect('lote:detalhes')
    else:
        if (buscar_lote_atual() is None):
            ano = date.today().year
            quantidade_lotes_ano = Lote.objects.filter(data_chegada__year = ano).order_by('-codigo').count()
            form = LoteForm()
        else:
            messages.error(request, 'Não é possível cadastrar um novo lote de confinamento. ' +
                                        'Há um lote ocupando o espaço. '+
                                        'Transfira os animais para a postura para poder cadastrar um novo lote.')
            return redirect('lote:detalhes')                           
    return render(request, "lote/criar.html", {'form': form, 'codigo': str(ano)+"."+format(quantidade_lotes_ano+1, "03d")})

def criar_registro_diario(request):
    lote_atual = buscar_lote_atual()
    if (request.method == "POST"):
        form = RegistroDiarioLoteForm(request.POST)
        if (form.is_valid()):
            if (len(Registro_diario_lote.objects.filter(data=form.cleaned_data['data'], lote=lote_atual)) > 0):
                messages.error(request, 'Já foi adicionado um registro diário neste lote para esta data.')
            elif (form.cleaned_data['data'] > date.today()):
                messages.error(request, 'Não é possível realizar um registro para uma data futura.')
            else:
                registro_diario = Registro_diario_lote()
                registro_diario.data = form.cleaned_data['data']
                registro_diario.peso = form.cleaned_data['peso']
                registro_diario.mortalidade = form.cleaned_data['mortalidade']
                registro_diario.lote = lote_atual
                registro_diario.save()

                lote_atual.quantidade_aves_final = lote_atual.quantidade_aves_final - registro_diario.mortalidade
                lote_atual.save()
                return redirect('lote:detalhes')
    else:
        form = RegistroDiarioLoteForm()
    
    informacoes = {
        'form':form,
        'lote': lote_atual
    }
    return render(request, "lote/criar_registro_diario.html", informacoes)

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

class EditarRegistroDiario(UpdateView):
    model = Registro_diario_lote
    fields = ['data', 'mortalidade', 'peso']
    template_name = 'lote/editar_registro_diario.html'
    success_url = reverse_lazy('lote:detalhes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lote'] = self.object.lote
        return context

    def form_valid(self, form):
        nova_mortalidade = form.save(commit=False).mortalidade
        mortalidade_anterior = Registro_diario_lote.objects.filter(pk=self.object.pk)[0].mortalidade
        self.object.lote.quantidade_aves_final = self.object.lote.quantidade_aves_final + mortalidade_anterior - nova_mortalidade
        self.object.lote.save()
        return super().form_valid(form)

class DeletarRegistroDiario(DeleteView):
    model = Registro_diario_lote
    success_url = reverse_lazy('lote:detalhes')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.lote.quantidade_aves_final = self.object.lote.quantidade_aves_final + self.object.mortalidade
        self.object.lote.save()
        return super(DeletarRegistroDiario, self).delete(*args, **kwargs)

def detalhes(request):
    lote_atual = buscar_lote_atual()
    registros_diarios = Registro_diario_lote.objects.filter(lote=lote_atual).order_by("-data")
    registros_diarios_graficos = registros_diarios.reverse()
    
    # Informações para o gráfico
    datas_mortalidade = []
    datas_peso = []
    mortalidade = []
    pesos = []

    for i, registro in enumerate(registros_diarios_graficos):
        datas_mortalidade.insert(i, str(registro.data))
        mortalidade.insert(i, registro.mortalidade)
        if (registro.peso != None):
            datas_peso.insert(i, str(registro.data))
            pesos.insert(i, str(registro.peso))

    # Informações para a tela
    informacoes = {
        'lote': lote_atual,
        'registros_diarios': registros_diarios,
        'datas_mortalidade': json.dumps(datas_mortalidade),
        'mortalidade': json.dumps(mortalidade),
        'datas_peso': json.dumps(datas_peso),
        'pesos': json.dumps(pesos)
    }
    return render(request, "lote/detalhes.html", informacoes)

def buscar_lote_atual():
    if (len(Lote.objects.filter(Q(status="A") | Q(status="B"))) > 0):
        return Lote.objects.filter(Q(status="A") | Q(status="B"))[0]
    else:
        return None
