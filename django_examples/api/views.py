from django.shortcuts import render_to_response
from django.conf import settings
import os

def index(request):
    return render_to_response(os.path.join(settings.STATIC_DIR, 'common/index.html'))


def upload_file(request):
    return 1;
