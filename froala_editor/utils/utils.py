import hmac
import hashlib
import base64

class Utils(object):

    @staticmethod
    def hmac(key, string, hex=False):

        hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256)
        return hmac256.hexdigest() if hex else hmac256.digest()