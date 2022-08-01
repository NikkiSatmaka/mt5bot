# References :
# - https://stackoverflow.com/questions/61776425/logic-for-real-time-algo-trading-expert

import pytz
import pandas as pd
import MetaTrader5 as mt5
import time
from datetime import datetime
from threading import Timer


def actualtime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #print("date and time =", dt_string)
    return str(dt_string)

def sync_60sec(op):
    info_time_new = datetime.strptime(str(actualtime()), '%d/%m/%Y %H:%M:%S')
    waiting_time = 60 - info_time_new.second

    t = Timer(waiting_time, op)
    t.start()

    print(actualtime(), f'waiting till next minute and 00 sec...')

def program(symbol):
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.now()

    ######### Change here the timeframe
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, utc_from, 70)

    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    # If you want to work only with open, high, low, close you could use
    #rates_frame = rates_frame.drop(['tick_volume', 'real_volume'], axis=1)

    print(f"\n", actualtime(),f"|| waiting for signals {symbol} ||\n")

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask

    request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": 1.0,
                "type": mt5.ORDER_TYPE_BUY_LIMIT,
                "price": price,
                "sl": price + 40 * point,
                "tp": price - 80 * point,
                "deviation": 20,
                "magic": 234000,
                "comment": "st_1_min_mod_3",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }


    condition_buy_1 = (
        (rates_frame.close.iloc[-2] > rates_frame.open.iloc[-2])& 
        (rates_frame.close.iloc[-2] > rates_frame.close.iloc[-3])
    )

    if condition_buy_1:
        #result = mt5.order_send(request)
        print('Sending Order!')


# starting mt5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()          
#------------------------------------------------------------------------------
#                   S T A R T I N G   M T 5 
#------------------------------------------------------------------------------
account_info=mt5.account_info()
if account_info!=None:       
    account_info_dict = mt5.account_info()._asdict()
    df=pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
    print("account_info() as dataframe:")
    print(df)
else:
    print(f"failed to connect to trade account, error code =", mt5.last_error())

mt5.shutdown()
#------------------------------------------------------------------------------
def trading_bot():
    symbol_1 = 'EURUSD'
    symbol_2 = 'EURCAD'
    while True:
        program(symbol_1)
        program(symbol_2)
        time.sleep(59.8) # it depends on your computer and ping

sync_60sec(trading_bot)