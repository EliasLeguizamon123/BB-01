#!/user/bin/env python3
import time
import hmac
import hashlib
import requests 
import json
from env import BITSO_API_KEY, BITSO_API_SECRET


def main() :
    parameters = {}
    nonce = str(int(round(time.time() * 1000)))
    httpMethod = 'GET'
    reqPath = '/v3/account_status'
    # Create Signature
    message = nonce + httpMethod + reqPath
    
    if (httpMethod == 'POST'):
        message += json.dumps(parameters)

    signature = hmac.new(BITSO_API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    # Build auth header
    authHeader = 'Bitso %s:%s:%s' % (BITSO_API_KEY, nonce, signature)

    # Send Request

    if (httpMethod == 'GET'):
        response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': authHeader})
    elif (httpMethod == 'POST'):
        response = requests.post("https://api.bitso.com" + reqPath, json = parameters, headers={"Authorization": authHeader})
        
    print(type(response))
    
if __name__ == '__main__':
    main()