from django.shortcuts import render

from rest_framework import viewsets
from api import models
from api import serializers

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    
