from bitsoEndpoints import bitsoGetMyData, getTickerUsdToArs, getMyBalance, getFeesForOperate, getUserOrders, getUserTrades
from time import sleep

def main() :
    bitsoGetMyData()
    # getMyBalance()
    while True:
        # getTickerUsdToArs()
        getUserOrders()
        sleep(3)
    
if __name__ == '__main__':
    main()