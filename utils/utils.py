import logging, json
import win32api
from time import timezone
from types import SimpleNamespace

logging.basicConfig(format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger_debugging = logging.getLogger('debuging_logger')
logger_debugging.setLevel(logging.INFO)

class BITFRONT_1:
    timezone:str
    responseTime:int
    statusCode:int
    statusMessage:str
    responseData:list

class BITFRONT_2(BITFRONT_1):
    responseData:dict

def check_requestSuccess(req):
    if req.status_code == 200:
        return True
    else:
        logger_debugging.error('requesting failed')
        return False
        
def check_responseSuccess(data:BITFRONT_1):
    try: 
        if data.statusCode == 1000 and data.statusMessage == 'SUCCESS':
            return True
        else:
            logger_debugging.warning(f'response failed becuase of {data.statusMessage} - {data.statusCode}')
            return False
    except:
        raise RuntimeError(f'wrong response {data}')

def jsonText_2_list_class(jsonText)->BITFRONT_1:
    return json.loads(jsonText, object_hook=lambda d: SimpleNamespace(**d))

def jsonText_2_dict_class(jsonText)->BITFRONT_2:
    return json.loads(jsonText, object_hook=lambda d: SimpleNamespace(**d))

class SOUND:   
    def __init__(self, duration = 100):
        self.duration = duration

    def error(self):
        win32api.Beep(1000, self.duration)

    def success(self):
        win32api.Beep(5000, self.duration)