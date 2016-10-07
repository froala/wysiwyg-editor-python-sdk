from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse

import os.path
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image, S3
from froala_editor import PyramidAdapter

# Create public directory at startup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, 'public')
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)

def get_main_html(request):
    return FileResponse('../common/index.html')


def upload_file(request):
    response = File.upload(PyramidAdapter(request), '/public/')
    return Response(json.dumps(response))

def upload_image(request):
    response = Image.upload(PyramidAdapter(request), '/public/')
    return Response(json.dumps(response))

def upload_image_resize(request):
    options = {
      'resize': '300x300'
    }
    response = Image.upload(PyramidAdapter(request), '/public/', options)
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
    response = Image.list('/public/')
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
    response = S3.getHash(config)
    return response


if __name__ == '__main__':
    config = Configurator()

    config.add_route('get_main_html', '/')
    config.add_view(get_main_html, route_name='get_main_html')


    config.add_route('upload_file', '/upload_file')
    config.add_view(upload_file, route_name='upload_file')

    config.add_route('upload_image', '/upload_image')
    config.add_view(upload_image, route_name='upload_image')

    config.add_route('upload_image_resize', '/upload_image_resize')
    config.add_view(upload_image_resize, route_name='upload_image_resize')

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
