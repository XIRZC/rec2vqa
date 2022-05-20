from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import REC, VQA, IMG
from api.serializers import RECSerializer, VQASerializer, IMGSerializer
from api.utils import log_to_terminal
from api.sender import sender_rec, sender_vqa, sender_det
from api.constants import MEDIA_ROOT

import uuid
import traceback

def det_post(reqeust):
    socket_id = uuid.uuid4()
    print(socket_id, request)
    try:
        img_name = request.POST.get('img')
        print('img_name', img_name)
        referring_expression = request.POST.get('referring_exression')
    
        image_path = MEDIA_ROOT / 'custom' / str(img_name)
    
        # run the rec wrapper
        log_to_terminal(socket_id, {'terminal': 'Starting detection job...'})
        sender_det(str(image_path), str(referring_expression), socket_id)
    except:
        log_to_terminal(socket_id, {'terminal': traceback.print_exc()})
    return render(request, 'post.html', {'socket_id': socket_id})

# Create your views here.
class RECViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = REC.objects.all()
    serializer_class = RECSerializer

    def perform_create(self, serializer):
        socket_id = uuid.uuid4()
        validated_data = serializer.validated_data
        print('rec validated_data', validated_data)
        try:
            img_name = validated_data['img'].img
            print('img_name', img_name)
            referring_expression = validated_data['referring_expression']
    
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
        socket_id = uuid.uuid4()
        validated_data = serializer.validated_data
        print('vqa validated_data', validated_data)
        try:
            question = validated_data['question']
            rec = validated_data['rec']
    
            log_to_terminal(socket_id, {'terminal': 'Starting VQA job...'})
            sender_rec(str(question), str(rec), str(socket_id))
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

