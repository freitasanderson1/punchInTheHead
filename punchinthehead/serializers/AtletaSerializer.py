from rest_framework import serializers

from punchinthehead.models import Atleta
from punchinthehead.serializers import ImagensSerializer

class AtletaSerializer(serializers.ModelSerializer):
  imagens = serializers.SerializerMethodField()
  
  class Meta:
    model = Atleta
    fields = '__all__'

  def get_imagens(self, obj):
    imgs = ImagensSerializer(obj.imagens_set.all(), many=True)
    return imgs.data if imgs else None
