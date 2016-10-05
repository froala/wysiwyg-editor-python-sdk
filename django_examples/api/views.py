import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../")
import json

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings

from froala_editor import File, Image
from froala_editor import DjangoAdapter

def index(request):
    return render_to_response(os.path.join(settings.STATIC_DIR, 'common/index.html'))

def upload_file(request):
    response = File.upload(DjangoAdapter(request), '/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")

def upload_image(request):
    response = Image.upload(DjangoAdapter(request), '/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")

def load_images(request):
    response = Image.list('/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")
