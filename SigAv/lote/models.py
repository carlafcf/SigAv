from django.db import models
from datetime import date

STATUS = [
    ('A', 'Isolamento'),
    ('B', 'Liberados'),
    ('C', 'Finalizado'),
]

class Lote(models.Model):
    localidade = models.CharField(max_length=200)
    data_chegada = models.DateField(default=date.today)
    quantidade_inicial = models.IntegerField()
    quantidade_final = models.IntegerField(null=True, blank=True)
    # linhagem (pode ser mais de um)
    # aptidao (pode ser mais de um)
    status = models.CharField(max_length=1, choices=STATUS, default='A')

    def __str__(self):
        return str(self.data_chegada)

    class Meta:
        ordering = ('status','-data_chegada',)