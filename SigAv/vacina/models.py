from django.db import models
from datetime import date
from lote.models import Lote #importa a classe que stá sendo referênciada através da chave estrangeira

APLICACAO = [
    ('A', 'X'),
    ('B', 'Y'),
    ('C', 'Z'),
]

ADMINISTRACAO = [
    ('A', 'Oral'),
    ('B', 'Y'),
    ('C', 'Z'),
]

class Vacina(models.Model):
    
    tipo = models.CharField(max_length=100)
    # doses = models.CharField(max_length=50, choices=APLICACAO)
    doses = models.PositiveIntegerField()

    def __str__(self):
        return self.tipo
    
    class Meta:
        ordering = ('tipo',)

class Aplicacao_vacina(models.Model):
    
    vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)
    observacoes = models.CharField(max_length=400, null=True, blank=True)
      
    def __str__ (self):
        return str(self.vacina) + " - " + str(self.lote)

    class Meta:
        ordering = ('lote','vacina',)

class Tempo_vacinacao(models.Model):
    
    vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    via_administracao = models.CharField(max_length=1, choices=ADMINISTRACAO)
    periodo_administracao = models.CharField(max_length=100)

    def __str__(self):
        return str(self.vacina)
    
    class Meta:
        ordering= ('vacina', 'periodo_administracao',)