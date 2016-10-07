import hmac
import hashlib
import base64
import copy

class Utils(object):

    @staticmethod
    def hmac(key, string, hex=False):

        hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256)
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