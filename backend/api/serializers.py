from api import models
from rest_framework import serializers
from api.models import REC, VQA, IMG
class VQASerializer(serializers.ModelSerializer):
    # rec = serializers.ReadOnlyField(source='dependency.referring_expressioin')
    class Meta:
        model = VQA
        fields = ('id', 'question', 'image', 'answer')

class RECSerializer(serializers.ModelSerializer):
    vqas = VQASerializer(many=True, read_only=True)
    # vqas_browser = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='vqa-detail', read_only=True)
    class Meta:
        model = REC
        fields = ('id', 'referring_expression', 'image', 'result', 'result_image', 'vqas')

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