from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='')

import os.path
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image
from froala_editor import FlaskAdapter

# Create public directory at startup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, 'public')
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)


@app.route('/')
def get_main_html():
    return send_from_directory('..', 'common/index.html')

@app.route('/public/<path:path>')
def get_public(path):
    return send_from_directory('public/', path)

@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('../', path)



@app.route('/upload_file', methods=['POST'])
def upload_file():
    response = File.upload(FlaskAdapter(request), '/public/')
    return json.dumps(response)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    response = Image.upload(FlaskAdapter(request), '/public/')
    return json.dumps(response)

@app.route('/load_images')
def load_images():
    response = Image.list('/public/')
    return json.dumps(response)
