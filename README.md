# BITFRONT
API using BITFRONT

see https://bitfront-exchange.github.io/bitfront-api-docs/#/

## Packages
### market
 - This package doesn't need `API KEY`
 1. `get_coinPair`
    - get all information of trading pairs
 2. `get_TradindgInfo['coinA.coinB':str]`
    - get single information of `coinA.coinB` pair
 3. `get_TickValue['coinA.coinB':str]`
    - get tick value of `coinA.coinB` pair
 4. `get_orderBook['coinA.coinB':str, depth=100:int]`
    - get order book of `coinA.coinB` pair. 
    - `depth` is number of BIDS, and ASKS to get.
### trade
- This package needs `API KEY`
    - make 'API' directory
    - get API from 'BITFRONT'.
    - copy and paste public key at the first line, and secrete key at the second line.
    - file name will be used as `ID` below.
    ![image](https://user-images.githubusercontent.com/72333472/127771684-09e6883b-19a5-4975-86c3-ae54436d7000.png)

1. `get_balances[ID:str]->[bool, list]`
    - get all balance of your ID's account

2. `get_balance[ID:str, coin:str]->[bool, dict]`
    - get balance of specific coin

3. `get_order_info[ID:str, orderID:str]->[bool, dict]`
    - get order info from orderID

4. `get_all_orders_info[ID:str, coinPair:str, max=100]->[bool, list]`
    - get all order infos from market and currency.
    - coinPair can be think as `market coin` and `currency coin`.
        - `market coin` is the coin you use to buy/sell with.
        - `currency coin` is the coin you want to buy/sell.
    - maximum number order to get is 100.

4. `buy[ID:str, coinPair:str, quantity, price]->[bool, orderID:str]`
    - buy coins with limit order

5. `buy_direct[ID:str, coinPair:str, quantity:str,float]->[bool, str]`
    - by coins with market order

6. `sell[ID:str, coinPair:str, quantity, price]->[bool, orderID:str]`
    - sell coins with limit order

7. `sell_direct[ID:str, coinPair:str, quantity:str, float]->[bool,str]`
    - sell coins with market order

8. `cancel[ID:str, orderID:str, time_interval:float=0.5, timeout:float=2]`
    - cancel order based on `orderID`.
    - check whether order has been canceled every `time_interval` for `timeout`.
    - `time_interval` and `timeout` 's unit is second.

9. `cancel_all[ID:str, coinPair:str, time_interval:float=0.5, timeout:float=2]`
    - cancel all orders of `coinPair`.
    - check whether all orders are gone for `timeout` every `time_interval`.


### authority, utils
 - functions to handle authorization and some helper functions
 - no need to use to trade or check your account
