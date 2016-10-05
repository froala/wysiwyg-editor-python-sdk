
"""
Adapters to provide an interface to requests objects on every framework.

Inspired fro http://peterhudec.github.io/authomatic/ MIT license.

"""

"""
Interface
"""
class BaseAdapter(object):

    def riseError(self):
        raise NotImplementedError( "Should have implemented this method" )

    def getFilename(self):
        self.riseError()

    def getChunks(self):
        self.riseError()

class DjangoAdapter(BaseAdapter):

    def __init__(self, request):
        self.request = request

    def getFilename(self, fieldname):
        return self.request.FILES[fieldname].name

    def getChunks(self, fieldname):
        return self.request.FILES[fieldname].chunks();