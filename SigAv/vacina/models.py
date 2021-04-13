from django.db import models
from datetime import date
from lote.models import Lote #importa a classe que stá sendo referênciada através da chave estrangeira

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
    
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    doses = models.CharField(max_length=50, choices=APLICACAO)

    def __str__(self):
        return self.tipo
    
    class Meta:
        ordering = ('tipo','doses',)

class Aplicacao_vacina(models.Model):
    
    id = models.AutoField(primary_key=True)
    fk_vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    fk_lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)
    observacoes = models.CharField(max_length=400)
      
    def __str__ (self):
        return self.data

    class Meta:
        ordering = ('data','fk_vacina',)

class Tempo_vacinacao(models.Model):
    
    id = models.AutoField(primary_key=True) #evita comflitos com chaves Id já criadas
    fk_vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    via_administracao = models.CharField(max_length=100, choices=ADMINISTRACAO)
    periodo_administracao = models.CharField(max_length=100)

    def __str__(self):
        return self.fk_vacina
    
    class Meta:
        ordering= ('fk_vacina', 'via_administracao',)