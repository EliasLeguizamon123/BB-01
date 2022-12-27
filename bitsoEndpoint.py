#!/user/bin/env python3
import time
import hmac
import hashlib
import requests
from termcolor import colored

from env import BITSO_API_KEY, BITSO_API_SECRET

# Globals
firstName = ''
lastName = ''
clientID = ''
httpMethod = 'GET'
usdActualPrice = 0
book = ''
high = ''
low = ''
change24 = ''
# Trading globals
balanceUSD = {}
balanceARS = {}
availableUSD = ''
lockedUSD = ''
totalUSD = ''
# Fees global
makerFee = 0

def bitsoGetPayload () : 
    global firstName, lastName, clientID
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
    lastName = payload['last_name']
    clientID = payload['client_id']
    print(clientID, firstName, lastName)

def getTickerUsdToArs() :
    global usdActualPrice, book, high, low, change24
    # Send Request
    reqPath = '/v3/ticker/?book=usd_ars'
    response = requests.get('https://api.bitso.com' + reqPath)
    payload = response.json()['payload']
    # Save globals
    usdActualPrice = float(payload['last'])
    book = payload['book']
    high = payload['high']
    low = payload['low']
    change24 = payload['change_24']
    if float(payload['last']) >  usdActualPrice:
        usdActualPrice = float(payload['last'])
        print('Actual price: ', colored(usdActualPrice, 'green'), 'Book: ', book, 'High Price: ', high,'Low Price: ',low)
    elif float(payload['last']) < usdActualPrice:
        usdActualPrice = float(payload['last'])
        print('Actual price: ', colored(usdActualPrice, 'red'), 'Book: ', book, 'High Price: ', high,'Low Price: ',low)
    else :
        usdActualPrice = float(payload['last'])
        print('Actual price: ', usdActualPrice, 'Book: ', book, 'High Price: ', high,'Low Price: ',low)

def getMyBalance() :
    global balanceUSD, balanceARS
    reqPath = '/v3/balance/'
    nonce = str(int(round(time.time() * 1000)))
    message = nonce + httpMethod + reqPath
    signature = hmac.new(BITSO_API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authHeader = 'Bitso %s:%s:%s' % (BITSO_API_KEY, nonce, signature)
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': authHeader})
    payload = response.json()['payload']
    balanceUSD = next(item for item in payload['balances'] if item['currency'] == 'usd')
    balanceARS = next(item for item in payload['balances'] if item['currency'] == 'ars')
# OBJECT Balance
# {currency: 'ars | usd', available: num, locked: num, total: num, pending_deposit: num, pending_withdrawal: num}

def getFeesForOperate() :
    global makerFee
    reqPath = '/v3/fees/'
    nonce = str(int(round(time.time() * 1000)))
    message = nonce + httpMethod + reqPath
    signature = hmac.new(BITSO_API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authHeader = 'Bitso %s:%s:%s' % (BITSO_API_KEY, nonce, signature)
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': authHeader})
    payload = response.json()['payload']
    actualFees = next(item for item in payload['fees'] if item['book'] == 'usd_ars')
    makerFee = actualFees['maker_fee_percent']
    comision = round((float(makerFee) *  usdActualPrice) / 100, 2)
    print('Actual maker fee: ',  makerFee )
    print('la operacion a hacer es el makerFee', makerFee, 'del precio actual USD', usdActualPrice, 'comision: ', comision)
    