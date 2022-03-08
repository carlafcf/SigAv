from django.db import models
from datetime import date
from lote.models import Lote #importa a classe que stá sendo referênciada através da chave estrangeira
 
# essas aplicações (tipos de vacina), foram inseridas aqui baseadas do 
# no site da embarapa 
# link: https://www.agencia.cnptia.embrapa.br/gestor/frango_de_corte/arvore/CONT000fc6gr40002wx5eo0a2ndxypswho8b.html

APLICACAO = [

    ('A', 'Doença de Marek'),
    ('B', 'Doença de Gumboro'),
    ('C', 'Varíola Aviária'),
    ('D', 'Bronquite infecciosa das Galinhas'),
    ('E', 'Doença de Newcastle')
]

ADMINISTRACAO = [

    ('A', 'Oral'),
    ('B', 'Injetavél'),
    ('C', 'Membrana da Asa'),
]
class Vacina(models.Model):
    
    tipo  = models.CharField(max_length=1, choices=APLICACAO)
    doses = models.CharField(max_length=1, choices=ADMINISTRACAO)

    def __str__(self):
        return self.tipo
        
    class Meta:
        ordering = ('tipo', 'doses')

class AplicacaoVacina(models.Model):
    
    id_vacina = models.ForeignKey   (Vacina, on_delete=models.RESTRICT)
    id_lote = models.ForeignKey(Lote, on_delete=models.RESTRICT)
    data = models.DateField(default=date.today)
    observacoes = models.CharField(max_length=400, null=True, blank=True)
      
    def __str__ (self):
        return str(self.vacina) + " - " + str(self.id_lote)
    class Meta:
        ordering = ('data','observacoes')

class TempoVacinacao(models.Model):
    
    id_vacina = models.ForeignKey(Vacina, on_delete=models.RESTRICT)
    via_administracao = models.CharField(max_length=1, choices=ADMINISTRACAO)
    periodo_administracao = models.CharField(max_length=100)

    def __str__(self):
        return str(self.via_administracao) 
    class Meta:
        ordering= ('via_administracao', 'periodo_administracao')