import requests
from utils.utils import logger_debugging, check_responseSuccess, jsonText_2_list_class, jsonText_2_dict_class


def get_coinPair():
    req = requests.get('https://openapi.bitfront.me/v1/market/public/coins/pairPolicy')
    response_coinPair = jsonText_2_list_class(req.text)
    if not check_responseSuccess(response_coinPair):
        logger_debugging.warning('Failed')
        return False
    return response_coinPair.responseData

def get_TickValue(str_coinPairType):
    req = requests.get(f"https://openapi.bitfront.me/v1/market/public/currentTickValue?coinPair={str_coinPairType}")
    response_tickValue = jsonText_2_dict_class(req.text)
    if not check_responseSuccess(response_tickValue):
        logger_debugging.warning('Failed')
        return False
    return response_tickValue.responseData

def get_orderBook(str_coinPairType, depth=100):
    req = requests.get(f"https://openapi.bitfront.me/v1/market/public/orderBooks?coinPair={str_coinPairType}&depth={depth}")
    response_orderBook = jsonText_2_dict_class(req.text)
    if not check_responseSuccess(response_orderBook):
        logger_debugging.warning('Failed')
        return False
    return response_orderBook.responseData

def get_TradingInfo(str_coinPairType):
    coinPair = get_coinPair()
    str_backPairType = '.'.join(str_coinPairType.split('.')[::-1])
    for info in coinPair:
        if info.coinPairType == str_coinPairType:
            return info
        if info.coinPairType == str_backPairType:
            return info

if __name__ == '__main__':
    str_coinPairType = 'LN.BTC'
    trading_info = get_TradingInfo(str_coinPairType)
    print("trading_info\n", trading_info)
    orderBook = get_orderBook(str_coinPairType, depth=5)
    print("orderBook\n", orderBook)
    tickValue = get_TickValue(str_coinPairType)
    print("tickValue\n", tickValue)