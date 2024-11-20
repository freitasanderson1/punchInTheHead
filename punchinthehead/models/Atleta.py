from django.db import models

MODALIDADE_TYPE_CHOICES = (
  (1,'MMA'),    
  (2,'Kickboxing'),  
)

POSICAO_TYPE_CHOICES = (
  (1,'Destro'),    
  (2,'Canhoto'),  
  (3,'Ambidestro'),  
)

class Atleta(models.Model):
  codigo = models.CharField('Código do Atleta', max_length=20, null=True, blank=True)

  nome = models.CharField('Nome do Atleta', max_length=255)
  sobrenome = models.CharField('Sobrenome do Atleta', max_length=255)
  apelido = models.CharField('Sobrenome do Atleta', max_length=255, null=True, blank=True)

  altura = models.FloatField('Altura', null=True, blank=True)
  peso = models.FloatField('Peso', null=True, blank=True)
  alcance = models.FloatField('Envergadura', null=True, blank=True)
  
  modalidade = models.IntegerField('Modalidade que compete', choices=MODALIDADE_TYPE_CHOICES, default=1)
  posicao = models.IntegerField('Posição', choices=POSICAO_TYPE_CHOICES, default=1)
  
  data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
  estreia = models.DateField('Data de Estreia', null=True, blank=True)
  
  ativo = models.BooleanField(verbose_name='Está em atividade?', default=True)

  class Meta:
    verbose_name = 'Atleta'
    verbose_name_plural = 'Atletas'
    ordering = ['modalidade','nome']
  
  def __str__(self):
    return f'{self.nome} {f'"{self.apelido}"' if self.apelido else ""} {self.sobrenome}'