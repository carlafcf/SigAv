from django.db import models
from datetime import date
from lote.models import Lote #importa a classe que stá sendo referênciada através da chave estrangeira


TIPODECRIACAO = [
    ('A', 'X'),
    ('B', 'Y'),
    ('C', 'Z'),
]

STATUS = [
    ('A', 'Isolamento'),
    ('B', 'Liberados'),
    ('C', 'Finalizado'),
]

class Fase_postura(models.Model):
    
    id = models.AutoField(primary_key=True) #evita comflitos com chaves Id já criadas
    fk_lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    tipo_sistema = models.CharField(max_length=100, choices=TIPODECRIACAO)
    data_chegada = models.DateField(default=date.today)
    quantidade_aves_chegada = models.PositiveIntegerField()
    quantidade_aves_final = models.PositiveIntegerField(null=True, blank=True)
    observacoes = models.CharField(max_length=400)

    def __str__(self):
        return self.tipo_sistema
    
    class Meta:
        ordering = ('data_chegada','quantidade_aves_final',)

class Movimento_diario_postura(models.Model):
    
    id = models.AutoField(primary_key=True)
    fk_fase_postura = models.ForeignKey(Fase_postura, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)
    mortalidade = models.PositiveIntegerField()
    primeira_coleta = models.PositiveIntegerField()
    segunda_coleta = models.PositiveIntegerField()
    ovos_quebrados = models.PositiveIntegerField()
    percentual_postura = models.PositiveIntegerField()

    def __str__(self):
        return self.mortalidade
    
    class Meta:
        ordering = ('data','mortalidade',)