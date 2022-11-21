#!/user/bin/env python3
import time
import hmac
import hashlib
import requests
from env import BITSO_API_KEY, BITSO_API_SECRET

# Globals
firstName = ''
clientID = ''
httpMethod = 'GET'
usdActualPrice = ''
book = ''
high = ''
low = ''
change24 = ''

def bitsoGetPayload () : 
    global firstName, clientID

    nonce = str(int(round(time.time() * 1000)))
    
    reqPath = '/v3/account_status'
    # Create Signature
    message = nonce + httpMethod + reqPath
    
    # parameters = {}
    # if (httpMethod == 'POST'):
    #     message += json.dumps(parameters)

    signature = hmac.new(BITSO_API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    # Build auth header
    authHeader = 'Bitso %s:%s:%s' % (BITSO_API_KEY, nonce, signature)

    # Send Request
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': authHeader})    
    payload = response.json()['payload']

    # Save Global variables
    firstName = payload['first_name']
    clientID = payload['client_id']

def getTickerUsdToArs() :
    global usdActualPrice, book, high, low, change24

    # Send Request
    reqPath = '/v3/ticker/?book=usd_ars'
    response = requests.get('https://api.bitso.com' + reqPath)
    payload = response.json()['payload']

    # Save globals
    usdActualPrice = payload['last']
    book = payload['book']
    high = payload['high']
    low = payload['low']
    change24 = payload['change_24']

    print('Actual price: ', usdActualPrice, 'Book: ', book, 'High Price: ', high,'Low Price: ',low)