from django.db import models
from datetime import date


APTIDAO = [
    ('A', 'Corte'),
    ('B', 'Postura'),
]

RACA = [
    ('A', 'Lohmann white'),
    ('B', 'Lohmann Brown'),
    ('C', 'Linhagem 3'),
    ('D', 'Linhagem 4'),
]

STATUS = [
    ('A', 'Isolamento'),
    ('B', 'Liberados'),
    ('C', 'Finalizado'),
]

class Lote(models.Model):
    
    codigo = models.CharField(max_length=50, unique=True)
    aptidao = models.CharField(max_length=1, choices=APTIDAO, default='B')
    data_chegada = models.DateField(default=date.today)
    localidade = models.CharField(max_length=200)
    quantidade_aves_chegada = models.PositiveIntegerField()
    quantidade_aves_final = models.PositiveIntegerField(null=True, blank=True)
    raca = models.CharField(max_length=1, choices=RACA)
    status = models.CharField(max_length=1, choices=STATUS, default='A')

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ('status','data_chegada',)

class Registro_diario_lote(models.Model):
    
    peso = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    mortalidade = models.PositiveIntegerField(default=0)
    lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)

    def __str__(self):
        return str(self.lote) + " - " + str(self.data)

    class Meta:
        ordering = ('-lote','-data',)
