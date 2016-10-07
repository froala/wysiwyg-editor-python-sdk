from flask import Flask, request, send_from_directory, jsonify
app = Flask(__name__, static_url_path='')

import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image, S3
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

@app.route('/delete_file', methods=['POST'])
def delete_file():
    src = request.form.get('src')
    try:
      File.delete(src)
      return json.dumps('ok')
    except:
      raise Exception('Could not delete file')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    src = request.form.get('src')
    print src
    try:
      Image.delete(src)
      return json.dumps('ok')
    except:
      raise Exception('Could not delete image')

@app.route('/load_images')
def load_images():
    response = Image.list('/public/')
    return json.dumps(response)

@app.route('/amazon_hash')
def amazon_hash():
    config = {
        'bucket': os.environ['AWS_BUCKET'],
        'region': os.environ['AWS_REGION'],
        'keyStart': os.environ['AWS_KEY_START'],
        'acl': os.environ['AWS_ACL'],
        'accessKey': os.environ['AWS_ACCESS_KEY'],
        'secretKey': os.environ['AWS_SECRET_ACCESS_KEY']
    }
    response = S3.getHash(config)
    return jsonify(**response)
