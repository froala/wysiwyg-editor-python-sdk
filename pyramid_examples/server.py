from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse

import os.path
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image
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

def load_images(request):
    response = Image.list('/public/')
    return Response(json.dumps(response))


if __name__ == '__main__':
    config = Configurator()

    config.add_route('get_main_html', '/')
    config.add_view(get_main_html, route_name='get_main_html')


    config.add_route('upload_file', '/upload_file')
    config.add_view(upload_file, route_name='upload_file')

    config.add_route('upload_image', '/upload_image')
    config.add_view(upload_image, route_name='upload_image')

    config.add_route('load_images', '/load_images')
    config.add_view(load_images, route_name='load_images')
    

    config.add_static_view('public', path='public/')
    config.add_static_view('static', path='../')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 7000, app)
    server.serve_forever()