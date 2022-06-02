from django.forms import ModelForm
from datetime import date
from django import forms
from django.db.models import Q
from .models import Lote, Registro_diario_lote

class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['data_chegada', 'localidade', 'aptidao',
                'quantidade_aves_chegada', 'raca']

class RegistroDiarioLoteForm(ModelForm):
    class Meta:
        model = Registro_diario_lote
        fields = ['data', 'mortalidade']

    def clean_data(self):
        data = self.cleaned_data['data']
        lote_atual = Lote.objects.filter(Q(status="A") | Q(status="B"))[0]

        if data > date.today() :
            raise forms.ValidationError("Não é possível realizar um registro para uma data futura.")
        elif (len(Registro_diario_lote.objects.filter(data=data, lote=lote_atual)) > 0):
            raise forms.ValidationError("Já foi adicionado um registro diário neste lote para esta data.")
        return data