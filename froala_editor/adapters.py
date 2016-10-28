
import shutil

"""
Adapters to provide an interface to requests objects on every framework.

Inspired fro http://peterhudec.github.io/authomatic/ MIT license.

"""

class BaseAdapter(object):
    """
    Interface. Inherit this class to use the lib in your framework.
    """

    def __init__(self, request):
        """
        Constructor.
        Parameters:
            request: http request object from some framework.
        """
        self.request = request

    def riseError(self):
        """
        Use this when you want to make an abstract method.
        """
        raise NotImplementedError( "Should have implemented this method." )

    def getFilename(self, fieldname):
        """
        Get upload filename based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: filename
        """
        self.riseError()

    def getMimetype(self, fieldname):
        """
        Get upload file mime type based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: mimetype
        """
        self.riseError()

    def saveFile(self, fieldname, fullNamePath):
        """
        Save the upload file based on the fieldname on the fullNamePath location.
        Parameters:
            fieldname: string
            fullNamePath: string
        """
        self.riseError()


class DjangoAdapter(BaseAdapter):
    """
    Django Adapter: Check BaseAdapter to see what methods description.
    """

    def checkFile(self, fieldname):
        if fieldname not in self.request.FILES:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].name

    def getMimetype(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].content_type

    def saveFile(self, fieldname, fullNamePath):
        self.checkFile(fieldname)

        with open(fullNamePath, 'wb+') as destination:
            for chunk in self.request.FILES[fieldname].chunks():
                destination.write(chunk)


class FlaskAdapter(BaseAdapter):
    """
    Flask Adapter: Check BaseAdapter to see what methods description.
    """

    def checkFile(self, fieldname):
        if fieldname not in self.request.files:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.files[fieldname].filename

    def getMimetype(self, fieldname):
        self.checkFile(fieldname)
        return self.request.files[fieldname].content_type

    def saveFile(self, fieldname, fullNamePath):
        self.checkFile(fieldname)
        file = self.request.files[fieldname]
        file.save(fullNamePath)


class PyramidAdapter(BaseAdapter):
    """
    Pyramid Adapter: Check BaseAdapter to see what methods description.
    """

    def checkFile(self, fieldname):
        if fieldname not in self.request.POST:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.POST[fieldname].filename

    def getMimetype(self, fieldname):
        self.checkFile(fieldname)
        return self.request.POST[fieldname].type

    def saveFile(self, fieldname, fullNamePath):
        self.checkFile(fieldname)
        file = self.request.POST[fieldname].file

        file.seek(0)
        with open(fullNamePath, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)