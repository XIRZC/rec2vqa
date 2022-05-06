from django.shortcuts import render

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
