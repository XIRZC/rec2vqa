from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from api.models import REC, VQA, IMG
from api.serializers import RECSerializer, VQASerializer, IMGSerializer
from rest_framework.response import Response

# Create your views here.
class RECViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = REC.objects.all()
    serializer_class = RECSerializer
    

class VQAViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = VQA.objects.all()
    serializer_class = VQASerializer

class IMGViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = IMG.objects.all()
    serializer_class = IMGSerializer
    def perform_destroy(self, instance):
        filename = settings.MEDIA_ROOT / instance.img.name
        print(type(filename), filename)
        if filename.exists():
            filename.unlink()
        instance.delete()
