import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../")
import json

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings

from froala_editor import File, Image, S3
from froala_editor import DjangoAdapter

def index(request):
    return render_to_response(os.path.join(settings.STATIC_DIR, 'common/index.html'))

def upload_file(request):
    response = File.upload(DjangoAdapter(request), '/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")

def upload_image(request):
    response = Image.upload(DjangoAdapter(request), '/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")

def delete_file(request):
    src = request.POST.get('src', '')
    try:
      File.delete(src)
      return HttpResponse('ok', content_type="application/json")
    except:
      raise Exception('Could not delete file')

def delete_image(request):
    src = request.POST.get('src', '')
    try:
      Image.delete(src)
      return HttpResponse('ok', content_type="application/json")
    except:
      raise Exception('Could not delete image')

def load_images(request):
    response = Image.list('/public/')
    return HttpResponse(json.dumps(response), content_type="application/json")

def amazon_hash(request):
    config = {
        'bucket': os.environ['AWS_BUCKET'],
        'region': os.environ['AWS_REGION'],
        'keyStart': os.environ['AWS_KEY_START'],
        'acl': os.environ['AWS_ACL'],
        'accessKey': os.environ['AWS_ACCESS_KEY'],
        'secretKey': os.environ['AWS_SECRET_ACCESS_KEY']
    }
    response = S3.getHash(config)
    return HttpResponse(json.dumps(response), content_type="application/json")
