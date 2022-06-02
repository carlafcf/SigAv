from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Vacina, AplicacaoVacina, TempoVacinacao
from datetime import date


class VacinaForm(ModelForm):
  class Meta:
    model = Vacina
    fields = ['tipo', 'doses']


class AplicacaoVacinaForm(ModelForm):
  
  class Meta:
    model = AplicacaoVacina
    fields = ['data', 'observacoes']

  def __init__(self, vacina_id, *args, **kwargs):
    self.vacina_id = vacina_id
    super(AplicacaoVacina, self).__init__(*args, **kwargs)
  

  def clear_data(self):
    data = self.cleaned_data['data']

    if data > date.today() :
      raise forms.ValidationError("Não é possível realizar um registro para uma data futura.")
    elif (len(AplicacaoVacina.objects.filter(data=data, observacoes=observacoes)) > 0):
      raise forms.ValidationError("Uma vacina já foi realiza nesse lote")


class TempoVacinacaoForm(ModelForm):
  
  class Meta:
    model = TempoVacinacao
    fields = ['via_administracao', 'periodo_administracao']
