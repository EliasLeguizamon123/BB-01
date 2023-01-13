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
# User Trades and orders
trades = []
orders = []

def createHeader (reqPath):
    nonce = str(int(round(time.time() * 1000)))
    message = nonce + httpMethod + reqPath
    signature = hmac.new(BITSO_API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authHeader = 'Bitso %s:%s:%s' % (BITSO_API_KEY, nonce, signature)
    
    return authHeader
    
def bitsoGetMyData () : 
    global firstName, lastName, clientID
    reqPath = '/v3/account_status'
    # Send Request
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)})    
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
    response = requests.get('https://api.bitso.com' + reqPath, createHeader(reqPath))
    payload = response.json()['payload']
    # Save globals
    book = payload['book']
    high = payload['high']
    low = payload['low']
    change24 = payload['change_24']
    if float(payload['last']) >  usdActualPrice:
        usdActualPrice = float(payload['last'])
        print('Actual price:  ' + colored(usdActualPrice, 'green') + ' Book:  ' + book + ' High Price:  ' + high +' Low Price:  ' +low)
    elif float(payload['last']) < usdActualPrice:
        usdActualPrice = float(payload['last'])
        print('Actual price:  ' + colored(usdActualPrice, 'red') + ' Book:  ' + book + ' High Price:  ' + high +' Low Price:  ' +low)
    else :
        usdActualPrice = float(payload['last'])
        print('Actual price: ', usdActualPrice, 'Book: ', book, 'High Price: ', high, 'Low Price: ', low)

def getMyBalance() :
    global balanceUSD, balanceARS
    reqPath = '/v3/balance/'
    
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)})
    payload = response.json()['payload']
    balanceUSD = next(item for item in payload['balances'] if item['currency'] == 'usd')
    balanceARS = next(item for item in payload['balances'] if item['currency'] == 'ars')
    # print('balance USD: ', balanceUSD, 'balance ARS: \n', balanceARS)
# OBJECT Balance
# {currency: 'ars | usd', available: num, locked: num, total: num, pending_deposit: num, pending_withdrawal: num}

def getFeesForOperate() :
    global makerFee
    reqPath = '/v3/fees/'
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)})
    payload = response.json()['payload']
    actualFees = next(item for item in payload['fees'] if item['book'] == 'usd_ars')
    makerFee = actualFees['maker_fee_percent']
    comision = round((float(makerFee) *  usdActualPrice) / 100, 2)
    print('Actual maker fee: ',  makerFee )
    print('la operacion a hacer es el makerFee', makerFee, 'del precio actual USD', usdActualPrice, 'comision: ', comision)
    
def getUserTrades(): 
    global trades
    reqPath = '/v3/user_trades/?book=usd_ars'
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)})
    payload = response.json()['payload']
    trades = payload
    print('My trades: ' + colored(trades, 'yellow'))
    
def getUserOrders() :
    global orders
    reqPath = '/v3/open_orders/?book=usd_ars'
    response = requests.get('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)})
    payload = response.json()['payload']
    print(payload)
    
def cancelAllOrders() :
    reqPath = '/v3/orders/all'
    response = requests.delete('https://api.bitso.com' + reqPath, headers={'Authorization': createHeader(reqPath)} )
    payload = response.json()['payload']
    print(colored('Orders deleted: ' + payload, 'red'))
    
def placeAnOrder(side, type): 
    reqPath = '/v3/orders'
    data={'book': 'usd_ars', 'side': side, 'type': type}
    response = requests.post('https://api.bitso.com' + reqPath, data, headers={'Authorization': createHeader(reqPath)})
    payload = response.json()['payload']
    print('order placed successfully: ', payload)
    
def scaldingOrders () :
    global balanceARS, balanceUSD
    getMyBalance()
    availableUSD = round(float(balanceUSD['available']), 2)
    availableARS = round(float(balanceARS['available']), 2)
    if availableUSD <= 1 and availableARS >= 100 :
        buyUSD = availableARS / 2
        placeAnOrder('buy', 'market')