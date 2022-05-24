from api import models
from rest_framework import serializers
import uuid

from api.models import REC, VQA, IMG

class VQASerializer(serializers.ModelSerializer):
    class Meta:
        model = VQA
        fields = ('id', 'socket_id', 'question', 'answer', 'rec')

class RECSerializer(serializers.ModelSerializer):
    vqas = VQASerializer(many=True, read_only=True)
    class Meta:
        model = REC
        fields = ('id', 'socket_id', 'referring_expression', 'img', 'result', 'result_image', 'vqas')

class IMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMG
        fields = ('id', 'img')

