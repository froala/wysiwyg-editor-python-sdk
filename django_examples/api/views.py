import os
import sys
import json

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings

import wand.image

# Extend path to load Froala Editor library from outside the server.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../")

from froala_editor import File, Image, Video, S3
from froala_editor import DjangoAdapter


def index(request):
    return render_to_response(os.path.join(settings.STATIC_DIR, 'common/index.html'))

def upload_files(request):
    options = {
        'validation': None
    }
    try:
        response = File.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")

def upload_files_validation(request):

    def validation(filePath, mimetype):
        size = os.path.getsize(filePath)
        if size > 10 * 1024 * 1024:
            return False
        return True

    options = {
        'fieldname': 'myFile',
        'validation': validation
    }
    try:
        response = File.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_file(request):
    options = {
        'validation': None
    }
    try:
        response = File.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_file_validation(request):

    def validation(filePath, mimetype):
        size = os.path.getsize(filePath)
        if size > 10 * 1024 * 1024:
            return False
        return True

    options = {
        'fieldname': 'myFile',
        'validation': validation
    }
    try:
        response = File.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_video(request):
    options = {
        'validation': None
    }
    try:
        response = Video.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_video_validation(request):

    def validation(filePath, mimetype):
        size = os.path.getsize(filePath)
        if size > 50 * 1024 * 1024:
            return False
        return True

    options = {
        'fieldname': 'myFile',
        'validation': validation
    }
    try:
        response = Video.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_image(request):
    try:
        response = Image.upload(DjangoAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_image_validation(request):

    def validation(filePath, mimetype):
        with wand.image.Image(filename=filePath) as img:
            if img.width != img.height:
                return False
            return True

    options = {
        'fieldname': 'myImage',
        'validation': validation
    }
    try:
        response = Image.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def upload_image_resize(request):
    options = {
      'resize': '300x300'
    }
    try:
        response = Image.upload(DjangoAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
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

def delete_video(request):
    src = request.POST.get('src', '')
    try:
      Video.delete(src)
      return HttpResponse('ok', content_type="application/json")
    except:
      raise Exception('Could not delete video')


def load_images(request):
    try:
        response = Image.list('/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
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
    try:
        response = S3.getHash(config)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")
