import os.path
import time
import hashlib
import sys

class File(object):

    @staticmethod
    def upload(req, fileRoute, fileOptions = None):

        filedname = 'file'
        filename = req.getFilename(filedname);
        extension = os.path.splitext(filename)[1]

        # Generate new random name.
        routeFilename = fileRoute + hashlib.sha1(str(time.time())).hexdigest() + extension

        fullNamePath = os.path.abspath(os.path.dirname(sys.argv[0])) +  routeFilename

        with open(fullNamePath, 'wb+') as destination:
            for chunk in req.getChunks(filedname):
                destination.write(chunk)

        # build and send response
        response = {}
        response['link'] = routeFilename
        return response