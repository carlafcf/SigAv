from django.contrib import admin

from .models import Vacina, AplicacaoVacina, TempoVacinacao

admin.site.register(Vacina)
admin.site.register(AplicacaoVacina)
admin.site.register(TempoVacinacao)