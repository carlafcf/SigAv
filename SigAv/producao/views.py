from math import prod
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required


import json

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import Fase_postura, Movimento_diario_postura
from .forms import ProducaoForm, MovimentoDiarioProducaoForm1, MovimentoDiarioProducaoForm2
from lote.models import Lote


@login_required
def home(request):
    if (request.user.is_superuser):
        return home_admin(request)
    else:
        return home_bolsista(request)


def home_bolsista(request):

    producoes = Fase_postura.objects.filter(status='A')

    informacoes = {
        'lista_producoes': producoes
    }

    return render(request, 'bolsista/home_bolsista.html', informacoes)


def home_admin(request):
    fase_postura = Fase_postura.objects.filter(status='A')

    # MÉDIAS - CARDS

    qnt_aves_postura = 0
    media_postura_diaria_A = 0
    quantidade_postura_A = 0
    media_postura_diaria_B = 0
    quantidade_postura_B = 0
    media_postura_diaria_C = 0
    quantidade_postura_C = 0
    for fase in fase_postura:
        qnt_aves_postura += fase.quantidade_aves_final

        if fase.tipo_sistema == 'A':
            quantidade_postura_A = quantidade_postura_A+1
            media_postura_diaria_A = media_postura_diaria_A + fase.media_postura_diaria

        if fase.tipo_sistema == 'B':
            quantidade_postura_B = quantidade_postura_B+1
            media_postura_diaria_B = media_postura_diaria_B + fase.media_postura_diaria

        if fase.tipo_sistema == 'C':
            quantidade_postura_C = quantidade_postura_C+1
            media_postura_diaria_C = media_postura_diaria_C + fase.media_postura_diaria

    if (quantidade_postura_A != 0):
        media_postura_diaria_A = media_postura_diaria_A/quantidade_postura_A
    else:
        media_postura_diaria_A = "--"
    if (quantidade_postura_B != 0):
        media_postura_diaria_B = media_postura_diaria_B/quantidade_postura_B
    else:
        media_postura_diaria_B = "--"
    if (quantidade_postura_C != 0):
        media_postura_diaria_C = media_postura_diaria_C/quantidade_postura_C
    else:
        media_postura_diaria_C = "--"

    # QUANTIDADE DE OVOS - GRÁFICOS

    ultimo_12 = [] #[SET/2020, OUT/2020, NOV/2020, ..., AGO/2021]
    ovos_mes = []
    mes_atual = date.today().month #AGOSTO
    ano_atual = date.today().year-1 #2020
    if mes_atual == 12:
        label = str(ano_atual+1)
    else:
        label = str(ano_atual) + "-" + str(ano_atual+1)

    for i in range(1, 13):
        mes_atual += 1   #SETEMBRO
        if (mes_atual == 13):
            mes_atual = 1 
        if (mes_atual == 1):
            ano_atual += 1
        movimento_mes = Movimento_diario_postura.objects.filter(data__month = mes_atual, data__year = ano_atual)
        ovos_produzidos = 0
        for movimento in movimento_mes:
            if (movimento.primeira_coleta != None):
                ovos_produzidos += movimento.primeira_coleta
            if (movimento.segunda_coleta != None):
                ovos_produzidos += movimento.segunda_coleta

        ovos_mes.insert(i, ovos_produzidos)
        ultimo_12.insert(i, date(1900, mes_atual, 1).strftime('%B'))

    ovos_mes_2_anos = []
    mes_atual = date.today().month  #AGOSTO
    ano_atual = date.today().year-2  #2019
    if mes_atual == 12:
        label_2_anos = str(ano_atual+1)
    else:
        label_2_anos = str(ano_atual) + "-" + str(ano_atual+1)

    for i in range(1, 13):
        mes_atual += 1 #SETEMBRO
        if (mes_atual == 13):
            mes_atual = 1 
        if (mes_atual == 1):
            ano_atual += 1
        movimento_mes = Movimento_diario_postura.objects.filter(data__month=mes_atual, data__year=ano_atual)
        ovos_produzidos = 0
        for movimento in movimento_mes:
            if (movimento.primeira_coleta != None):
                ovos_produzidos += movimento.primeira_coleta
            if (movimento.segunda_coleta != None):
                ovos_produzidos += movimento.segunda_coleta

        ovos_mes_2_anos.insert(i, ovos_produzidos)

    ovos_mes_3_anos = []
    mes_atual = date.today().month   #AGOSTO
    ano_atual = date.today().year-3  #2018
    if mes_atual == 12:
        label_3_anos = str(ano_atual+1)
    else:
        label_3_anos = str(ano_atual) + "-" + str(ano_atual+1)

    for i in range(1, 13):
        mes_atual += 1 #SETEMBRO
        if (mes_atual == 13):
            mes_atual = 1 
        if (mes_atual == 1):
            ano_atual += 1
        movimento_mes = Movimento_diario_postura.objects.filter(data__month=mes_atual, data__year=ano_atual)
        ovos_produzidos = 0
        for movimento in movimento_mes:
            if (movimento.primeira_coleta != None):
                ovos_produzidos += movimento.primeira_coleta
            if (movimento.segunda_coleta != None):
                ovos_produzidos += movimento.segunda_coleta

        ovos_mes_3_anos.insert(i, ovos_produzidos)

    # ENVIO DE DADOS

    informacoes = {
        'qnt_aves_postura': qnt_aves_postura,
        'media_postura_diaria_A': media_postura_diaria_A,
        'media_postura_diaria_B': media_postura_diaria_B,
        'media_postura_diaria_C': media_postura_diaria_C,

        'ultimo_12': json.dumps(ultimo_12),
        'label': label,
        'label_2_anos': label_2_anos,
        'label_3_anos': label_3_anos,
        'ovos_mes': json.dumps(ovos_mes),
        'ovos_mes_2_anos': json.dumps(ovos_mes_2_anos),
        'ovos_mes_3_anos': json.dumps(ovos_mes_3_anos)
    }

    return render(request, 'home.html', informacoes)


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


class EditarRegistroDiario(UpdateView):
    model = Movimento_diario_postura
    fields = ['data', 'primeira_coleta', 'segunda_coleta', 'ovos_quebrados', 'mortalidade']
    template_name = 'producao/editar_registro_diario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fase_postura'] = self.object.fase_postura
        return context

    def form_valid(self, form):
        nova_mortalidade = form.save(commit=False).mortalidade
        mortalidade_anterior = Movimento_diario_postura.objects.filter(pk=self.object.pk)[0].mortalidade
        self.object.fase_postura.quantidade_aves_final = self.object.fase_postura.quantidade_aves_final + mortalidade_anterior - nova_mortalidade
        self.object.fase_postura.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('producao:detalhes', kwargs={'pk':self.object.fase_postura.pk})


class DeletarMovimentoDiario(DeleteView):
    model = Movimento_diario_postura

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.fase_postura.quantidade_aves_final = self.object.fase_postura.quantidade_aves_final + self.object.mortalidade
        self.object.fase_postura.save()
        return super(DeletarMovimentoDiario, self).delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('producao:detalhes', kwargs={'pk':self.object.fase_postura.pk})


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
                    tipo_sistema='B',
                    data_chegada=date.today(),
                    quantidade_aves_chegada=gaiola,
                    quantidade_aves_final=gaiola
                )
                fase_postura_gaiola.save()
            if free_range > 0:
                fase_postura_free_range = Fase_postura(
                    lote=lote_atual,
                    tipo_sistema='A',
                    data_chegada=date.today(),
                    quantidade_aves_chegada=free_range,
                    quantidade_aves_final=free_range
                )
                fase_postura_free_range.save()
            if caipira > 0:
                fase_postura_caipira = Fase_postura(
                    lote=lote_atual,
                    tipo_sistema='C',
                    data_chegada=date.today(),
                    quantidade_aves_chegada=caipira,
                    quantidade_aves_final=caipira
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
    movimento_diario = Movimento_diario_postura.objects.filter(fase_postura=lote_postura).order_by('-data')

    movimento_diario_graficos = movimento_diario.reverse()

    # Informações para o gráfico
    datas_mortalidade = []
    datas_coleta = []
    mortalidade = []
    ovos_quebrados = []
    coletas = []

    postura_media, mortalidade_media, quebra_ovos_media, semanas = definir_dados_semanais(movimento_diario_graficos)

    # for i, registro in enumerate(movimento_diario_graficos):
    #     datas_mortalidade.insert(i, str(registro.data))
    #     mortalidade.insert(i, registro.mortalidade)
    #     ovos_quebrados.insert(i, registro.ovos_quebrados)
    #     datas_coleta.insert(i, str(registro.data))
    #     coletas.insert(i, int(registro.primeira_coleta or 0) + int(registro.segunda_coleta or 0))

    # Informações para a tela

    informacoes = {
        'producao': lote_postura,
        'movimento_diario':movimento_diario,
        'datas_mortalidade': json.dumps(semanas),
        'mortalidade': json.dumps(mortalidade_media),
        'ovos_quebrados': json.dumps(quebra_ovos_media),
        'datas_coletas': json.dumps(semanas),
        'coletas': json.dumps(postura_media)

    }

    return render(request, "producao/detalhes.html", informacoes)


def definir_dados_semanais(registros_diarios):
    primeira_data = registros_diarios[0].data

    mortalidade_media = []
    coleta_media = []
    ovos_quebrados_media = []
    semanas = []

    mortalidade = 0
    coleta = 0
    ovos_quebrados = 0
    quantidade = 0
    semana = 1

    for i, registro in enumerate(registros_diarios):
        if (registro.data > (primeira_data + timedelta(days=13))):
            primeira_data=primeira_data + timedelta(days=14)
            mortalidade_media.append(round(mortalidade/quantidade, 2))
            ovos_quebrados_media.append(round(ovos_quebrados/quantidade, 2))
            coleta_media.append(round(coleta/quantidade, 2))
            semanas.append(semana)
            semana = semana + 1
            coleta = 0
            ovos_quebrados = 0
            mortalidade = 0
            quantidade = 0

        mortalidade = mortalidade + registro.mortalidade
        ovos_quebrados = ovos_quebrados + registro.ovos_quebrados
        coleta = coleta + (registro.primeira_coleta if registro.primeira_coleta != None else 0) + (registro.segunda_coleta if registro.segunda_coleta != None else 0)
        quantidade = quantidade + 1

    mortalidade_media.append(round(mortalidade/quantidade, 2))
    ovos_quebrados_media.append(round(ovos_quebrados/quantidade, 2))
    coleta_media.append(round(coleta/quantidade, 2))
    semanas.append(semana)

    return coleta_media, mortalidade_media, ovos_quebrados_media, semanas


def criar_registro_diario_1(request, pk, tipo):
    producao = Fase_postura.objects.filter(id=pk)[0]
    if (request.method == "POST"):

        form = MovimentoDiarioProducaoForm1(producao.id, request.POST)

        if (form.is_valid()):
            data = form.cleaned_data['data']
            if len(Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)) == 0:
                movimento_diario = Movimento_diario_postura()
                movimento_diario.fase_postura = producao
                movimento_diario.data = form.cleaned_data['data']
                movimento_diario.mortalidade = form.cleaned_data['mortalidade']
                movimento_diario.primeira_coleta = form.cleaned_data['primeira_coleta']
                movimento_diario.ovos_quebrados = form.cleaned_data['ovos_quebrados']
                movimento_diario.save()

                producao.media_postura_diaria = atualizar_media_fase_postura(producao.pk)
                producao.quantidade_aves_final = producao.quantidade_aves_final - movimento_diario.mortalidade
                producao.save()

            else:
                movimento_diario = Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)[0]
                movimento_diario.primeira_coleta = form.cleaned_data['primeira_coleta']
                movimento_diario.mortalidade = form.cleaned_data['mortalidade'] + movimento_diario.mortalidade
                movimento_diario.ovos_quebrados = form.cleaned_data['ovos_quebrados'] + movimento_diario.ovos_quebrados
                movimento_diario.save()

                producao.media_postura_diaria = atualizar_media_fase_postura(producao.pk)
                producao.quantidade_aves_final = producao.quantidade_aves_final - form.cleaned_data['mortalidade']
                producao.save()

            return redirect('producao:detalhes', pk=producao.id)
    else:

        form = MovimentoDiarioProducaoForm1(producao.id)

    informacoes = {
        'form': form,
        'producao': producao
    }

    if (request.user.is_superuser):
        return render(request, "producao/criar_registro_diario.html", informacoes)
    else:
        return render(request, "bolsista/criar_registro_diario.html", informacoes)


def criar_registro_diario_2(request, pk):
    producao = Fase_postura.objects.filter(id=pk)[0]
    if (request.method == "POST"):
        form = MovimentoDiarioProducaoForm2(producao.id, request.POST)

        if (form.is_valid()):
            data = form.cleaned_data['data']
            if len(Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)) == 0:
                movimento_diario = Movimento_diario_postura()
                movimento_diario.fase_postura = producao
                movimento_diario.data = form.cleaned_data['data']
                movimento_diario.mortalidade = form.cleaned_data['mortalidade']
                movimento_diario.segunda_coleta = form.cleaned_data['segunda_coleta']
                movimento_diario.ovos_quebrados = form.cleaned_data['ovos_quebrados']
                movimento_diario.save()

                producao.media_postura_diaria = atualizar_media_fase_postura(producao.pk)
                producao.quantidade_aves_final = producao.quantidade_aves_final - movimento_diario.mortalidade
                producao.save()

            else:
                movimento_diario = Movimento_diario_postura.objects.filter(data=data, fase_postura=producao)[0]
                movimento_diario.segunda_coleta = form.cleaned_data['segunda_coleta']
                movimento_diario.mortalidade = form.cleaned_data['mortalidade'] + movimento_diario.mortalidade
                movimento_diario.ovos_quebrados = form.cleaned_data['ovos_quebrados'] + movimento_diario.ovos_quebrados
                movimento_diario.save()

                producao.media_postura_diaria = atualizar_media_fase_postura(producao.pk)
                producao.quantidade_aves_final = producao.quantidade_aves_final - form.cleaned_data['mortalidade']
                producao.save()

            return redirect('producao:detalhes', pk=producao.id)
    else:

        form = MovimentoDiarioProducaoForm2(producao.id)

    informacoes = {
        'form': form,
        'producao': producao
    }
    if (request.user.is_superuser):
        return render(request, "producao/criar_registro_diario.html", informacoes)
    else:
        return render(request, "bolsista/criar_registro_diario.html", informacoes)


def alterar_status(request, pk):
    fase_postura = Fase_postura.objects.get(pk=pk)
    fase_postura.status = "B"
    fase_postura.save()

    return redirect('producao:listar')


def buscar_lote_atual():
    if (len(Lote.objects.filter(Q(status="A") | Q(status="B"))) > 0):
        return Lote.objects.filter(Q(status="A") | Q(status="B"))[0]
    else:
        return None


def atualizar_media_fase_postura(pk):
    fase_postura = Fase_postura.objects.get(pk=pk)
    qnt_dias = Movimento_diario_postura.objects.filter(fase_postura=fase_postura).count()

    contagem = 0
    for movimento in Movimento_diario_postura.objects.filter(fase_postura=fase_postura):
        if (movimento.primeira_coleta != None):
            contagem = contagem + movimento.primeira_coleta
        if (movimento.segunda_coleta != None):
            contagem = contagem + movimento.segunda_coleta

    return contagem/qnt_dias


def coleta_diaria(request, pk):
    fase_postura = Fase_postura.objects.get(pk=pk)
    mov_diario = Movimento_diario_postura.objects.filter(fase_postura=fase_postura, data=date.today())

    informacoes = {
        'mov_diario': mov_diario,
        'total_ovos': mov_diario[0].primeira_coleta + mov_diario[0].segunda_coleta if len(mov_diario) > 0 else 1,
        'producao': fase_postura
    }
    print(informacoes['total_ovos'])

    return render(request, "bolsista/coleta_diaria.html", informacoes)
