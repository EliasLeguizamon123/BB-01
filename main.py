from bitsoEndpoints import bitsoGetMyData, getTickerUsdToArs, getMyBalance, getFeesForOperate
from time import sleep

def main() :
    bitsoGetMyData()
    # getMyBalance()
    while True:
        getTickerUsdToArs()
        sleep(3)
    
if __name__ == '__main__':
    main()