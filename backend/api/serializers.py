from unittest.mock import seal
from api import models
from rest_framework import serializers
from api.models import REC, VQA, IMG
import os
from django.conf import settings
class VQASerializer(serializers.ModelSerializer):
    # rec = serializers.SlugRelatedField(read_only=True, slug_field='referring_expression')
    class Meta:
        model = VQA
        fields = ('id', 'question', 'img', 'answer', 'rec')

class RECSerializer(serializers.ModelSerializer):
    vqas = VQASerializer(many=True, read_only=True)
    # vqas_browser = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='vqa-detail', read_only=True)
    class Meta:
        model = REC
        fields = ('id', 'referring_expression', 'img', 'result', 'result_image', 'vqas')

# class RECSerializer(serializers.HyperlinkedModelSerializer):
#     vqas = serializers.HyperlinkedRelatedField(
#         many=True, view_name='vqa-detail', read_only=True)
#     class Meta:
#         model = REC
#         fields = ('id', 'referring_expression', 'image', 'result', 'result_image', 'vqas')

class IMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMG
        fields = ('id', 'img')

    def create(self, validated_data):
        filename = 'custom/' + validated_data['img'].name
        print(filename)
        try:
            instance = IMG.objects.get(img=filename)
            return instance
        except:
            return IMG.objects.create(**validated_data)