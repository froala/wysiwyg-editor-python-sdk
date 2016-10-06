
"""
Adapters to provide an interface to requests objects on every framework.

Inspired fro http://peterhudec.github.io/authomatic/ MIT license.

"""

"""
Interface
"""
class BaseAdapter(object):

    def riseError(self):
        raise NotImplementedError( "Should have implemented this method." )

    def getFilename(self, fieldname):
        self.riseError()

    def getChunks(self, fieldname, fullNamePath):
        self.riseError()


class DjangoAdapter(BaseAdapter):

    def __init__(self, request):
        self.request = request

    def checkFile(self, fieldname):
        if not self.request.FILES[fieldname]:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].name

    def saveFile(self, fieldname, fullNamePath):
        self.checkFile(fieldname)

        with open(fullNamePath, 'wb+') as destination:
            for chunk in self.request.FILES[fieldname].chunks():
                destination.write(chunk)


class FlaskAdapter(BaseAdapter):

    def __init__(self, request):
        self.request = request

    def checkFile(self, fieldname):
        if not self.request.files[fieldname]:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.files[fieldname].filename

    def saveFile(self, fieldname, fullNamePath):
        self.checkFile(fieldname)
        file = self.request.files[fieldname]
        file.save(fullNamePath)