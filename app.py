import config
import pytz
import time
import pandas as pd
import MetaTrader5 as mt5
from pathlib import Path
from datetime import datetime
from threading import Timer

MT5LOC = Path(config.MT5LOC)

def actualtime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("date and time =", dt_string)
    return str(dt_string)

def sync_60sec(op):
    info_time_new = datetime.strptime(str(actualtime()), '%d/%m/%Y %H:%M:%S')
    waiting_time = 60 - info_time_new.second

    t = Timer(waiting_time, op)
    t.start()

    print(actualtime(), 'waiting till next minute and 00 sec..')

def program(symbol):
    if not mt5.initialize(str(MT5LOC)):
        print("initialize() failed, error code=", mt5.last_error())
        quit()

    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.now()

    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, utc_from, 70)

    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

    print('\n', actualtime(), f'|| waiting for signals {symbol} ||\n')

def start():
    while True:
        program('USDJPY')

sync_60sec(start)



# ################################################################################
# # TEST BUY
# ################################################################################

# symbol = "USDJPY"
# symbol_info = mt5.symbol_info(symbol)
# if symbol_info is None:
#     print(symbol, "not found, can not call order_check()")
#     mt5.shutdown()
#     quit()
 
# # if the symbol is unavailable in MarketWatch, add it
# if not symbol_info.visible:
#     print(symbol, "is not visible, trying to switch on")
#     if not mt5.symbol_select(symbol,True):
#         print("symbol_select({}}) failed, exit",symbol)
#         mt5.shutdown()
#         quit()

# lot = 0.1
# point = mt5.symbol_info(symbol).point
# price = mt5.symbol_info_tick(symbol).ask
# deviation = 20

# print(point)
# print(price)

# request = {
#     "action": mt5.TRADE_ACTION_DEAL,
#     "symbol": symbol,
#     "volume": lot,
#     "type": mt5.ORDER_TYPE_BUY,
#     "price": price,
#     "sl": price - 100 * point,
#     "tp": price + 100 * point,
#     "deviation": deviation,
#     "magic": 234000,
#     "comment": "python script open",
#     "type_time": mt5.ORDER_TIME_GTC,
#     "type_filling": mt5.ORDER_FILLING_IOC,
# }

# result = mt5.order_send(request)
# print(result)

# # # check the execution result
# # print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
# # if result.retcode != mt5.TRADE_RETCODE_DONE:
# #     print("2. order_send failed, retcode={}".format(result.retcode))
# #     # request the result as a dictionary and display it element by element
# #     result_dict=result._asdict()
# #     for field in result_dict.keys():
# #         print("   {}={}".format(field,result_dict[field]))
# #         # if this is a trading request structure, display it element by element as well
# #         if field=="request":
# #             traderequest_dict=result_dict[field]._asdict()
# #             for tradereq_filed in traderequest_dict:
# #                 print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
# #     # print("shutdown() and quit")
# #     # mt5.shutdown()
# #     quit()
 
# # print("2. order_send done, ", result)
# # print("   opened position with POSITION_TICKET={}".format(result.order))
# # print("   sleep 2 seconds before closing position #{}".format(result.order))
# # time.sleep(2)

# ################################################################################