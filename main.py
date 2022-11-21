from bitsoEndpoint import bitsoGetPayload, getTickerUsdToArs
from time import sleep

def main() :
    bitsoGetPayload()
    while True:
        getTickerUsdToArs()
        sleep(1)
    
if __name__ == '__main__':
    main()