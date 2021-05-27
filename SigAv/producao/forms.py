from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from lote.models import Lote

class ProducaoForm(forms.Form):
    gaiola = forms.IntegerField(label='Gaiola', initial=0)
    free_range = forms.IntegerField(label='Free-range', initial=0)
    caipira = forms.IntegerField(label='Caipira', initial=0) 

    def clean_gaiola(self):
        gaiola = self.cleaned_data['gaiola']
        if gaiola < 0 :
            raise forms.ValidationError("O número de aves deve ser maior do que 0.")
        return gaiola
    
    def clean_free_range(self):
        free_range = self.cleaned_data['free_range']
        if free_range < 0 :
            raise forms.ValidationError("O número de aves deve ser maior do que 0.")
        return free_range
    
    def clean_caipira(self):
        caipira = self.cleaned_data['caipira']
        if caipira < 0 :
            raise forms.ValidationError("O número de aves deve ser maior do que 0.")
        return caipira

    def clean(self):
        super().clean()
        gaiola = self.cleaned_data.get("gaiola")
        free_range = self.cleaned_data.get("free_range")
        caipira = self.cleaned_data.get("caipira")

        lote_atual = Lote.objects.filter(Q(status="A") | Q(status="B"))[0]

        if (gaiola + free_range + caipira) != lote_atual.quantidade_aves_final:
            raise forms.ValidationError(
                "O número de aves redirecionada deve ser igual ao "
                "número de aves final do Lote de Confinamento ("
                +str(lote_atual.quantidade_aves_final)+
                ")."
            )