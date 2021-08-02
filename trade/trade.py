from authority import authority
import requests, time
from utils.utils import check_responseSuccess, check_requestSuccess,  jsonText_2_list_class, jsonText_2_dict_class, logger_debugging
from utils.coinpairs import COINPAIRS
from typing import List, Tuple

URL_BASE = 'https://openapi.bitfront.me'
coinpairs = COINPAIRS()

def get_balances(ID)->Tuple[bool, List]:
    logger_debugging.info('run')
    request_path='/v1/account/balances'
    parameter={}
    method='GET'
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_list_class(req.text)
        if check_responseSuccess(response):
            logger_debugging.info('success')
            return True, response.responseData
    return False, []

def get_balance(ID, coin)->Tuple[bool, dict]:
    flag, list_balance = get_balances(ID)
    if not flag:
        return False, {}
    for balance_info in list_balance.currency:
        if balance_info.currency == coin:
            return True, balance_info
    return False, {}

def get_order_info(ID, orderID)->Tuple[bool, dict]:
    logger_debugging.info('run')
    request_path=f'/v2/account/orders/{orderID}'
    parameter={
    }
    method='GET'
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            logger_debugging.info('success')
            return True, response.responseData
    return False, {}

def get_all_orders_info(ID, coinPair, max=100)->Tuple[bool, List]:
    logger_debugging.info('run')
    request_path='/v1/trade/openOrders'
    method='GET'
    if not coinpairs.check_exist(coinPair):
        logger_debugging.warning(f'no such pair of {coinPair}')
        return False, []
    currency, market = coinPair.split('.')
    parameter={
        'market':market, 
        'currency':currency, 
        'max':max
    }
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_list_class(req.text)
        if check_responseSuccess(response):
            list_order = response.responseData
            if len(list_order) == max:
                logger_debugging.warning(f'{max} order was got, but it may have more')
            logger_debugging.info('success')
            return True, list_order
    return False, []

def buy(ID, coinPair, quantity, price)->Tuple[bool,str]:
    logger_debugging.info('run')
    orderSide='BUY'
    request_path = '/v1/trade/limitOrders'
    parameter = {
        'quantity':quantity,
        'coinPair':coinPair,
        'price':price,
        'orderSide':orderSide
    }
    method = 'POST'
    if not coinpairs.check_exist(coinPair):
        return False, ''
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            orderID = response.responseData.orderID
            logger_debugging.info(f'{coinPair} buy {quantity} at {price} - {orderID}')
            return True, orderID
    return False, ''

def buy_direct(ID, coinPair, quantity) ->Tuple[bool, str]:
    logger_debugging.info('run')
    orderSide='BUY'
    request_path = '/v1/trade/marketOrders'
    parameter = {
        'quantity':quantity,
        'coinPair':coinPair,
        'orderSide':orderSide
    }
    method = 'POST'
    if not coinpairs.check_exist(coinPair):
        return False, ''
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            orderID = response.responseData.orderID
            logger_debugging.info(f'{coinPair} buy {quantity} - {orderID}')
            return True, orderID
    return False, ''

def sell(ID, coinPair, quantity, price)->Tuple[bool,str]:
    logger_debugging.info('run')
    orderSide='SELL'
    request_path = '/v1/trade/limitOrders'
    parameter = {
        'quantity':quantity,
        'coinPair':coinPair,
        'price':price,
        'orderSide':orderSide
    }
    method = 'POST'
    if not coinpairs.check_exist(coinPair):
        return False, ''
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            orderID = response.responseData.orderID
            logger_debugging.info(f'{coinPair} sell {quantity} at {price} - {orderID}')
            return True, orderID
    return False, ''

def sell_direct(ID, coinPair, quantity)->Tuple[bool, str]:
    logger_debugging.info('run')
    orderSide='SELL'
    request_path = '/v1/trade/marketOrders'
    parameter = {
        'quantity':quantity,
        'coinPair':coinPair,
        'orderSide':orderSide
    }
    method = 'POST'
    if not coinpairs.check_exist(coinPair):
        return False, ''
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            orderID = response.responseData.orderID
            logger_debugging.info(f'{coinPair} sell {quantity} - {orderID}')
            return True, orderID
    return False, ''

def cancel(ID, orderID, time_interval=0.5, timeout=2)->bool:
    logger_debugging.info('run')
    request_path=f'/v1/trade/orders/{orderID}'
    parameter={}
    method='DELETE'
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            if _check_cancel(ID, orderID, time_interval, timeout):
                return True
    return False

def _check_cancel(ID, orderID, time_interval, timeout):
    current_time = 0
    while current_time < timeout:
        time.sleep(time_interval)
        current_time += time_interval
        flag, order_info = get_order_info(ID, orderID)
        if not flag:
            logger_debugging.warning(f'fail to check order {orderID}')
            return False
        initialRequestAmount = order_info.initialRequestAmount
        remainAmount = order_info.remainAmount
        filledAmount = order_info.filledAmount
        orderSide = order_info.orderSide
        if filledAmount + remainAmount < initialRequestAmount:
            logger_debugging.info(f'Success - canceled {orderSide} {initialRequestAmount - filledAmount} / {initialRequestAmount}')
            return True
    return False

def cancel_all(ID, coinPair:str, time_interval=0.5, timeout=2)->bool:
    logger_debugging.info('run')
    if not coinpairs.check_exist(coinPair):
        return False
    request_path=f'/v1/trade/openOrders/{coinPair}'
    parameter={}
    method='DELETE'
    req = _send_request(request_path, parameter, method, ID)
    if check_requestSuccess(req):
        response = jsonText_2_dict_class(req.text)
        if check_responseSuccess(response):
            if _check_cancel_all(ID, coinPair, time_interval, timeout):
                return True
    return False

def _check_cancel_all(ID, coinPair, time_interval, timeout):
    current_time = 0
    while current_time < timeout:
        time.sleep(time_interval)
        current_time += time_interval
        flag, list_order = get_all_orders_info(ID, coinPair)
        if not flag:
            logger_debugging.warning('fail to check cancel all')
            return False
        if len(list_order) == 0 :
            logger_debugging.info(f'Success all order from {coinPair} is canceled')
            return True
    logger_debugging.warning(f'"Cancel All" requested, but {len(list_order)} orders remained')
    return False

def _send_request(request_path, parameter, method, ID):
    headers = authority.get_headers(request_path, parameter, method, ID=ID)
    data = authority.reformat_parameter(parameter)
    if method == 'GET':
        url = f'{URL_BASE}{request_path}?{data}'
        req = requests.get(url, headers=headers, data=data)
    elif method == 'POST':
        url = f'{URL_BASE}{request_path}'
        req = requests.post(url, headers=headers, data=data)
    elif method == 'DELETE':
        url = f'{URL_BASE}{request_path}?{data}'
        req = requests.delete(url, headers=headers, data=data)
    return req