from froala_editor import File
from .utils import Utils
from os import listdir
from os.path import isfile, join
from mimetypes import MimeTypes
import urllib
import os.path

class Image(object):

    defaultUploadOptions = {
        'fieldname': 'file',
        'validation': {
            'allowedExts': ['gif', 'jpeg', 'jpg', 'png', 'svg', 'blob'],
            'allowedMimeTypes': ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/x-png', 'image/png', 'image/svg+xml']
        },
        # string resize param from http://docs.wand-py.org/en/0.4.3/guide/resizecrop.html#transform-images
        # Examples: '100x100', '100x100!'. Find more on http://www.imagemagick.org/script/command-line-processing.php#geometry
        'resize': None
    }

    @staticmethod
    def upload(req, fileRoute, options = None):
        """
        Image upload to disk.
        Parameters:
            req: framework adapter to http request. See BaseAdapter.
            fileRoute: string
            options: dict optional, see defaultUploadOptions attribute
        Return:
            dict: {link: 'linkPath'}
        """

        if options is None:
            options = Image.defaultUploadOptions
        else:
            options = Utils.merge_dicts(Image.defaultUploadOptions, options)

        return File.upload(req, fileRoute, options)

    @staticmethod
    def delete(src):
        """
        Delete image from disk.
        Parameters:
            src: string
        """
        return File.delete(src)

    @staticmethod
    def list(folderPath, thumbPath = None):
        """
        List images from disk.
        Parameters:
            folderPath: string
            thumbPath: string
        Return:
            list: list of images dicts. example: [{url: 'url', thumb: 'thumb', name: 'name'}, ...]
        """

        if thumbPath == None:
            thumbPath = folderPath

        # Array of image objects to return.
        response = []

        absoluteFolderPath = Utils.getServerPath() + folderPath

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
