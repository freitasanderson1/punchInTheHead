from rest_framework import serializers
from django.contrib.sites.models import Site

from punchinthehead.models import Imagens

class ImagensSerializer(serializers.ModelSerializer):
  img = serializers.SerializerMethodField()

  class Meta:
    model = Imagens
    fields = ['img','tipo']

  
  def get_img(self, obj):
    current_site = Site.objects.get_current()
    img = current_site.domain + obj.arquivo.url
    return img