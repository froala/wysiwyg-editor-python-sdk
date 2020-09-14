import hmac
import hashlib
import base64
import copy
import os
import sys

class Utils(object):
    """
    Utils static class.
    """

    @staticmethod
    def hmac(key, string, hex=False):
        """
        Calculate hmac.
        Parameters:
            key: string
            string: string
            hex: boolean optional, return in hex, else return in binary
        Return:
            string: hmax in hex or binary
        """

        # python 2-3 compatible:
        try:
            hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg=string.encode('utf-8') if isinstance(string, str) else string, digestmod=hashlib.sha256) # v3
        except Exception:
            hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256) # v2

        return hmac256.hexdigest() if hex else hmac256.digest()

    @staticmethod
    def merge_dicts(a, b, path=None):
        """
        Deep merge two dicts without modifying them. Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
        Parameters:
            a: dict
            b: dict
            path: list
        Return:
            dict: Deep merged dict.
        """

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
        """
        Get filename extension.
        Parameters:
            filename: string
        Return:
            string: The extension without the dot.
        """
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def getServerPath():
        """
        Get the path where the server has started.
        Return:
            string: serverPath
        """
        return os.getcwd()

    @staticmethod
    def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):
        """
        Test if a file is valid based on its extension and mime type.
        Parameters:
            filename string
            mimeType string
            allowedExts list
            allowedMimeTypes list
        Return:
            boolean
        """

        # Skip if the allowed extensions or mime types are missing.
        if not allowedExts or not allowedMimeTypes:
            return False

        extension = Utils.getExtension(filename)
        return extension.lower() in allowedExts and mimetype in allowedMimeTypes

    @staticmethod
    def isValid(validation, filePath, mimetype):
        """
        Generic file validation.
        Parameters:
            validation: dict or function
            filePath: string
            mimetype: string
        """

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
