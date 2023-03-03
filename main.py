from bitsoEndpoints import bitsoGetMyData, getTickerUsdToArs, getMyBalance, getFeesForOperate, getUserOrders, getUserTrades, scaldingOrders
from time import sleep

def main() :
    # Get my data
    bitsoGetMyData()
    # Get dolar price
    getTickerUsdToArs()
    # Get my balance
    scaldingOrders()
    # getFeesForOperate()
    # while True:
    #     # getTickerUsdToArs()
    # getUserOrders()
    #     sleep(3)
    
if __name__ == '__main__':
    main()
