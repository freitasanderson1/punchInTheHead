from django.db import models
from punchinthehead.models import Atleta

import uuid

IMAGEM_TYPE_CHOICES = (
  (1,'Frontal'),    
  (2,'Corpo'),  
  (3,'Meio Corpo'),  
  (4,'Outro'),
)
def caminho_imagem(instance, filename):
  tipo_imagem = dict(IMAGEM_TYPE_CHOICES).get(instance.tipo, "Outro")
  return f"Atletas/{tipo_imagem}/{filename}"
  
class Imagens(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  atleta = models.ForeignKey(Atleta, verbose_name='Atleta', help_text='Atleta associado', on_delete=models.CASCADE)
  arquivo = models.ImageField('Imagem', upload_to=caminho_imagem, null=False, blank=False)
  tipo = models.IntegerField('Tipo de Imagem', choices=IMAGEM_TYPE_CHOICES, default=1)

  class Meta:
    verbose_name = 'Imagem'
    verbose_name_plural = 'Imagens'
    ordering = ['atleta__sobrenome','atleta__nome','tipo']
  
  def __str__(self):
    return f'{self.atleta.sobrenome} {"{self.atleta.apelido}" if self.atleta.apelido else None} {self.atleta.sobrenome} - {self.get_tipo_display()}'