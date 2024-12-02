from rest_framework import viewsets
from rest_framework.response import Response

from punchinthehead.models import Atleta
from punchinthehead.serializers import AtletaSerializer

class AtletaViewset(viewsets.ModelViewSet):
  serializer_class = AtletaSerializer
  queryset = Atleta.objects.all()
  
  def retrieve(self, request, *args, **kwargs):
      id = kwargs.get('pk')
      data = Atleta.objects.filter(id=id)

      ObjAtleta = AtletaSerializer(data, many=True).data[0] if data else None

      return Response(ObjAtleta)
  
  def create(self, request, *args, **kwargs):
    responseData = {'mensagem':'Não permitido!'}
    return Response(responseData)
  
  def destroy(self, request, *args, **kwargs):
    responseData = {'mensagem':'Não permitido!'}
    return Response(responseData)