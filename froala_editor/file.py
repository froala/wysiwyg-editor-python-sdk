import os
import time
import hashlib
import sys

class File(object):

    @staticmethod
    def upload(req, fileRoute, fileOptions = None):

        fieldname = 'file'
        filename = req.getFilename(fieldname);
        extension = os.path.splitext(filename)[1]

        # Generate new random name.
        routeFilename = fileRoute + hashlib.sha1(str(time.time())).hexdigest() + extension

        fullNamePath = os.path.abspath(os.path.dirname(sys.argv[0])) +  routeFilename

        req.saveFile(fieldname, fullNamePath)

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