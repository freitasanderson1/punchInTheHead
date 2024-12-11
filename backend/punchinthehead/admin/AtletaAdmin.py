from django.contrib import admin

from punchinthehead.models import Atleta, Imagens

class ImagensInline(admin.StackedInline):
  model = Imagens
  extra = 0

@admin.register(Atleta)
class AtletaAdmin(admin.ModelAdmin):
  list_display = ['nome','sobrenome','apelido','altura','peso','alcance','modalidade','posicao','data_nascimento','estreia','ativo']
  search_fields = ['nome','sobrenome','apelido','altura','peso','alcance','modalidade','posicao','data_nascimento','estreia','ativo']
  inlines = [ImagensInline]