import datetime
import json
import base64

from .utils import Utils

class S3(object):

    @staticmethod
    def getHash(config):
        """
        Get signature for S3.
        Parameters:
            config: dict
            {
                bucket: 'bucketName',

                //http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
                region: 's3',
                keyStart: 'editor/',
                acl: 'public-read',
                accessKey: 'YOUR-AMAZON-S3-PUBLIC-ACCESS-KEY',
                secretKey: 'YOUR-AMAZON-S3-SECRET-ACCESS-KEY'
            }
         Return:
            dict:
            {
                bucket: bucket,
                region: region,
                keyStart: keyStart,
                params: {
                    acl: acl,
                    policy: policy,
                    'x-amz-algorithm': 'AWS4-HMAC-SHA256',
                    'x-amz-credential': xAmzCredential,
                    'x-amz-date': xAmzDate,
                    'x-amz-signature': signature
                }
            }
        """

        # Check default region.
        config['region'] = config['region'] if 'region' in config else 'us-east-1'
        config['region'] = 'us-east-1' if config['region'] == 's3' else  config['region']

        bucket = config['bucket']
        region = config['region']
        keyStart = config['keyStart']
        acl = config['acl']

        # These can be found on your Account page, under Security Credentials > Access Keys.
        accessKeyId = config['accessKey']
        secret = config['secretKey']

        dateString = datetime.datetime.now().strftime("%Y%m%d") # Ymd format.

        credential = '/'.join([accessKeyId, dateString, region, 's3/aws4_request'])
        xAmzDate = dateString + 'T000000Z'

        # Build policy.
        policy = {
            # 5 minutes into the future
            'expiration': (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            'conditions': [
                {'bucket': bucket},
                {'acl': acl },
                {'success_action_status': '201'},
                {'x-requested-with': 'xhr'},
                {'x-amz-algorithm': 'AWS4-HMAC-SHA256'},
                {'x-amz-credential': credential},
                {'x-amz-date': xAmzDate},
                ['starts-with', '$key', keyStart],
                ['starts-with', '$Content-Type', ''] # Accept all files.
            ],
        }
        # python 2-3 compatible:
        try:
            policyBase64 = base64.b64encode(json.dumps(policy).encode()).decode('utf-8') # v3
        except Exception:
            policyBase64 = base64.b64encode(json.dumps(policy)) # v2

        # Generate signature.
        dateKey = Utils.hmac('AWS4' + secret, dateString);
        dateRegionKey = Utils.hmac(dateKey, region)
        dateRegionServiceKey = Utils.hmac(dateRegionKey, 's3')
        signingKey = Utils.hmac(dateRegionServiceKey, 'aws4_request')
        signature = Utils.hmac(signingKey, policyBase64, True)

        return {
            'bucket': bucket,
            'region': 's3-' + region if region != 'us-east-1' else 's3',
            'keyStart': keyStart,
            'params': {
                'acl': acl,
                'policy': policyBase64,
                'x-amz-algorithm': 'AWS4-HMAC-SHA256',
                'x-amz-credential': credential,
                'x-amz-date': xAmzDate,
                'x-amz-signature': signature
            }
        }