from froala_editor import File
from os import listdir
from os.path import isfile, join
from mimetypes import MimeTypes
import urllib
import sys
import os.path

class Image(object):

    defaultUploadOptions = {
        'fieldname': 'file',
        'validation': {
            'allowedExts': ['gif', 'jpeg', 'jpg', 'png', 'svg', 'blob'],
            'allowedMimeTypes': ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/x-png', 'image/png', 'image/svg+xml']
        }
    }

    @staticmethod
    def upload(req, fileRoute, fileOptions = None):
        return File.upload(req, fileRoute, fileOptions)

    @staticmethod
    def list(folderPath, thumbPath = None):

        if thumbPath == None:
            thumbPath = folderPath

        # Array of image objects to return.
        response = []

        absoluteFolderPath = os.path.abspath(os.path.dirname(sys.argv[0])) + folderPath

        # Image types.
        imageTypes = Image.defaultUploadOptions['validation']['allowedMimeTypes']

        # Filenames in the uploads folder.
        fnames = [f for f in listdir(absoluteFolderPath) if isfile(join(absoluteFolderPath, f))]

        for fname in fnames:
            mime = MimeTypes()
            mimeType = mime.guess_type(absoluteFolderPath + fname)[0]

            if mimeType in imageTypes:
                response.append({
                    'url': folderPath + fname,
                    'thumb': thumbPath + fname,
                    'name': fname
                })

        return response
