from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse

import os.path
import json
import sys

import wand.image

# Extend path to load Froala Editor library from outside the server.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image, Video, S3
from froala_editor import PyramidAdapter

# Create public directory at startup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, 'public')
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)


def get_main_html(request):
    return FileResponse('../common/index.html')


def upload_file(request):
    options = {
        'validation': None
    }
    try:
        response = File.upload(PyramidAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


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
        response = File.upload(PyramidAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


def upload_image(request):
    try:
        response = Image.upload(PyramidAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


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
        response = Image.upload(PyramidAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


def upload_image_resize(request):
    options = {
      'resize': '300x300'
    }
    try:
        response = Image.upload(PyramidAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


def upload_video(request):
    try:
        response = Video.upload(PyramidAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


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
        response = Video.upload(PyramidAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


def delete_file(request):
    src = request.POST.get('src')
    try:
      File.delete(src)
      return Response(json.dumps('ok'))
    except:
      raise Exception('Could not delete file')


def delete_image(request):
    src = request.POST.get('src')
    try:
      Image.delete(src)
      return Response(json.dumps('ok'))
    except:
      raise Exception('Could not delete image')


def load_images(request):
    try:
        response = Image.list('/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return Response(json.dumps(response))


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
    return response


if __name__ == '__main__':
    config = Configurator()

    config.add_route('get_main_html', '/')
    config.add_view(get_main_html, route_name='get_main_html')


    config.add_route('upload_file', '/upload_file')
    config.add_view(upload_file, route_name='upload_file')

    config.add_route('upload_file_validation', '/upload_file_validation')
    config.add_view(upload_file_validation, route_name='upload_file_validation')

    config.add_route('upload_image', '/upload_image')
    config.add_view(upload_image, route_name='upload_image')

    config.add_route('upload_image_validation', '/upload_image_validation')
    config.add_view(upload_image_validation, route_name='upload_image_validation')

    config.add_route('upload_image_resize', '/upload_image_resize')
    config.add_view(upload_image_resize, route_name='upload_image_resize')

    config.add_route('upload_video', '/upload_video')
    config.add_view(upload_video, route_name='upload_video')

    config.add_route('upload_video_validation', '/upload_video_validation')
    config.add_view(upload_video_validation, route_name='upload_video_validation')

    config.add_route('delete_file', '/delete_file')
    config.add_view(delete_file, route_name='delete_file')

    config.add_route('delete_image', '/delete_image')
    config.add_view(delete_image, route_name='delete_image')

    config.add_route('load_images', '/load_images')
    config.add_view(load_images, route_name='load_images')

    config.add_route('amazon_hash', '/amazon_hash')
    config.add_view(amazon_hash, route_name='amazon_hash', renderer='json')

    config.add_static_view('public', path='public/')
    config.add_static_view('static', path='../')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 7000, app)
    print('* Running on http://127.0.0.1:7000/ (Press CTRL+C to quit)')
    server.serve_forever()
