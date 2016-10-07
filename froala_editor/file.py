import os
import time
import hashlib
import sys
from utils import Utils
from wand.image import Image

class File(object):

    defaultUploadOptions = {
        'fieldname': 'file',
        'validation': {
            'allowedExts': ['txt', 'pdf', 'doc'],
            'allowedMimeTypes': ['text/plain', 'application/msword', 'application/x-pdf', 'application/pdf']
        }
    }

    @staticmethod
    def upload(req, fileRoute, options = None):

        if options is None:
            options = File.defaultUploadOptions
        else:
            options = Utils.merge_dicts(File.defaultUploadOptions, options)

        filename = req.getFilename(options['fieldname']);
        extension = os.path.splitext(filename)[1]

        # Generate new random name.
        routeFilename = fileRoute + hashlib.sha1(str(time.time())).hexdigest() + extension

        fullNamePath = os.path.abspath(os.path.dirname(sys.argv[0])) +  routeFilename

        req.saveFile(options['fieldname'], fullNamePath)

        # Check image resize.
        if 'resize' in options and options['resize'] is not None:
            with Image(filename=fullNamePath) as img:
                img.transform(resize=options['resize'])
                img.save(filename=fullNamePath)

        # build and send response
        response = {}
        response['link'] = routeFilename
        return response

    @staticmethod
    def delete(src):

        filePath = os.path.abspath(os.path.dirname(sys.argv[0])) + src
        try:
            os.remove(filePath)
        except OSError:
            pass