from django.db import models
from datetime import date



APLICACAO = [
    ('A', 'X'),
    ('B', 'Y'),
    ('C', 'Z'),
]

ADMINISTRACAO = [
    ('A', 'X'),
    ('B', 'Y'),
    ('C', 'Z'),
]

class Vacina(models.Model):
    
    tipo = models.CharField(max_length=100)
    doses = models.CharField(max_length=50, choices=APLICACAO)




class Aplicacao_vacina(models.Model):
    
    fk_vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    #fk_lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)
    observacoes = models.CharField(max_length=400)
      



class Tempo_vacinacao(models.Model):
    
    fk_vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    via_administracao = models.CharField(max_length=100, choices=ADMINISTRACAO)
    periodo_administracao = models.CharField(max_length=100)
      

