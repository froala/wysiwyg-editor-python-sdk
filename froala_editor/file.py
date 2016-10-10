import os
import time
import hashlib
import sys
from .utils import Utils
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
        extension = Utils.getExtension(filename)
        extension = '.' + extension if extension else ''

        # Generate new random name.

        # python 2-3 compatible:
        try:
            sha1 = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest() #  v3
        except Exception:
            sha1 = hashlib.sha1(str(time.time())).hexdigest() # v2
        routeFilename = fileRoute + sha1 + extension

        fullNamePath = os.path.abspath(os.path.dirname(sys.argv[0])) +  routeFilename

        req.saveFile(options['fieldname'], fullNamePath)

        if 'validation' in options:
            if not Utils.isValid(options['validation'], fullNamePath, req.getMimetype(options['fieldname'])):
                File.delete(routeFilename)
                raise Exception('File does not meet the validation.')

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