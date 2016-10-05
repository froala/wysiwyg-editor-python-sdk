from froala_editor import File

class Image(object):

    @staticmethod
    def upload(req, fileRoute, fileOptions = None):
        return File.upload(req, fileRoute, fileOptions)