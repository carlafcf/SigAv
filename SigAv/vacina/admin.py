from django.contrib import admin

from .models import Vacina, Aplicacao_vacina, Tempo_vacinacao

admin.site.register(Vacina)
admin.site.register(Aplicacao_vacina)
admin.site.register(Tempo_vacinacao)