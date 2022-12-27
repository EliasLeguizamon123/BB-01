from bitsoEndpoint import bitsoGetPayload, getTickerUsdToArs, getMyBalance, getFeesForOperate
from time import sleep

def main() :
    bitsoGetPayload()
    while True:
        getTickerUsdToArs()
        getFeesForOperate()
        sleep(1)
    
if __name__ == '__main__':
    main()