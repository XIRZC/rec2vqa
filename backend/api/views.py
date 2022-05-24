from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from api.models import REC, VQA, IMG
from api.serializers import RECSerializer, VQASerializer, IMGSerializer
from api.utils import log_to_terminal
from api.sender import sender_rec, sender_vqa, sender_det
from api.constants import MEDIA_ROOT

import uuid
import traceback

def socket(request):
    print('socket request data', request.GET)
    print('request socket_id', request.GET['socket_id'])
    print('request task', request.GET['task'])
    socket_id = request.GET['socket_id']
    task = request.GET['task']
    if task == 'rec':
        rec = REC.objects.filter(socket_id=socket_id)
        print('rec', rec)
        data = serializers.serialize('json', rec)
    else:  # vqa task
        vqa = VQA.objects.filter(socket_id=socket_id)
        print('vqa', vqa)
        data = serializers.serialize('json', vqa)
    return HttpResponse(data, content_type="text/json-comment-filtered")
    # return JsonResponse(data, safe=False)

# Create your views here.
class RECViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = REC.objects.all()
    serializer_class = RECSerializer

    def perform_create(self, serializer):
        #socket_id = uuid.uuid4()
        validated_data = serializer.validated_data
        print('rec validated_data', validated_data)
        try:
            img_name = validated_data['img'].img
            print('img_name', img_name)
            referring_expression = validated_data['referring_expression']
            socket_id = validated_data['socket_id']
    
            image_path = MEDIA_ROOT  / str(img_name)
    
            log_to_terminal(socket_id, {'terminal': 'Starting REC job...'})
            sender_rec(str(image_path), str(referring_expression), str(socket_id))
        except:
            log_to_terminal(socket_id, {'terminal': traceback.print_exc()})
        #serializer.save()
    

class VQAViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = VQA.objects.all()
    serializer_class = VQASerializer

    def perform_create(self, serializer):
        #socket_id = uuid.uuid4()
        validated_data = serializer.validated_data
        print('vqa validated_data', validated_data)
        try:
            question = validated_data['question']
            rec = validated_data['rec']
            socket_id = validated_data['socket_id']
    
            log_to_terminal(socket_id, {'terminal': 'Starting VQA job...'})
            sender_vqa(str(question), str(rec), str(socket_id))
        except:
            log_to_terminal(socket_id, {'terminal': traceback.print_exc()})
        #serializer.save()

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

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        print('validated_data', validated_data)
        filename = 'custom/' + validated_data['img'].name
        print(filename)
        try:
            instance = IMG.objects.get(img=filename)
        except:
            return serializer.save()

