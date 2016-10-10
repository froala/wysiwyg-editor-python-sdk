import hmac
import hashlib
import base64
import copy
import os

class Utils(object):

    @staticmethod
    def hmac(key, string, hex=False):

        # python 2-3 compatible:
        try:
            hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg=string.encode('utf-8') if isinstance(string, str) else string, digestmod=hashlib.sha256) # v3
        except Exception:
            hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256) # v2

        return hmac256.hexdigest() if hex else hmac256.digest()

    @staticmethod
    # Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
    def merge_dicts(a, b, path=None):
        aClone = copy.deepcopy(a);
        # Returns deep b into a without affecting the sources.
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    aClone[key] = Utils.merge_dicts(a[key], b[key], path + [str(key)])
                else:
                    aClone[key] = b[key]
            else:
                aClone[key] = b[key]
        return aClone

    @staticmethod
    def getExtension(filename):
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    # Test if a file is valid based on its extension and mime type.
    def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):

        if not allowedExts or not allowedMimeTypes:
            return False

        extension = Utils.getExtension(filename)
        return extension.lower() in allowedExts and mimetype in allowedMimeTypes

    @staticmethod
    #Generic file validation.
    def isValid(validation, filePath, mimetype):

        # No validation means you dont want to validate, so return affirmative.
        if not validation:
            return True

        # Validation is a function provided by the user.
        if callable(validation):
            return validation(filePath, mimetype)

        if isinstance(validation, dict):
            return Utils.isFileValid(filePath, mimetype, validation['allowedExts'], validation['allowedMimeTypes'])

        # Else: no specific validating behaviour found.
        return False