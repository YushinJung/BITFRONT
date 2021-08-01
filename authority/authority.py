import math, random, time, hmac, hashlib
from utils.utils import logger_debugging
from types import SimpleNamespace
from typing import Tuple, List

def get_headers(request_path, parameter, method, ID='demo', NONCE=None):
    NONCE = _get_correct_NONCE(NONCE)
    api_key, api_secret = _get_API_keys(ID)
    timestamp = _get_UNIX_epoch_UTC_timestamp()
    
    str_query = reformat_parameter(parameter)
    str_target = f'{NONCE}{timestamp}{method}{request_path}{str_query}'
    logger_debugging.debug(f"str_target {str_target}")
    signature = _get_signature(api_secret, str_target)
    headers = _get_headers(api_key, signature, timestamp, NONCE)
    logger_debugging.debug(headers)
    return headers
        
def reformat_parameter(parameter:dict)->str:
    list_parameter = []
    for key, val in parameter.items():
        list_parameter.append(f'{key}={val}')
    str_parameter = '&'.join(list_parameter)
    logger_debugging.debug(str_parameter)
    return str_parameter

def _get_API_keys(ID='jushin90')->Tuple[str, str]:
    d_ = f'API/{ID}'
    with open(d_, 'r') as handle:
        api_key = handle.readline().strip()
        api_secret = handle.readline().strip()
    return api_key, api_secret

def _get_correct_NONCE(NONCE):
    if NONCE == None:
        NONCE = random.randrange(9999, 100000)
    if type(NONCE) == int:
        logit10 = math.log10(NONCE)
        if logit10 > 5 or logit10 < 4:
            NONCE = random.randrange(9999, 100000)
    return NONCE

def _get_UNIX_epoch_UTC_timestamp(extra_number=3):
    return int(float(time.time()*10**extra_number))

def _get_headers(key, sign, timestamp, nonce, content_type='application/x-www-form-urlencoded'):
    headers = {
        "X-API-KEY": key, 
        "X-API-SIGN": sign,
        "X-API-TIMESTAMP": str(timestamp),
        "X-API-NONCE": str(nonce), 
        'content-type': content_type
    }
    return headers

def _get_signature(api_secret, str_target):
    signature = hmac.new(bytes(api_secret, 'latin-1'), msg=bytes(str_target, 'latin-1'), digestmod=hashlib.sha256).hexdigest()
    return signature



