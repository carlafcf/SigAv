from django.forms import ModelForm
from .models import Lote, Registro_diario_lote

class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['data_chegada', 'localidade', 'aptidao',
                'quantidade_aves_chegada', 'raca']

class RegistroDiarioLoteForm(ModelForm):
    class Meta:
        model = Registro_diario_lote
        fields = ['data', 'peso', 'mortalidade']