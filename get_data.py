from datetime import datetime
from pathlib import Path
import config
import MetaTrader5 as mt5
import pandas as pd

mt5Loc = Path(config.MT5LOC)
symbol = 'EURUSD'
lookback = 10000000
saveloc = f'data/{symbol}.csv'

# establish connection to MetaTrader 5 terminal
if not mt5.initialize(str(mt5Loc)):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# get 10 GBPUSD D1 bars from the current day
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, lookback)
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
# display each element of obtained data in a new line
print("Display obtained data 'as is'")
# for rate in rates:
#     print(rate)
 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
# rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
# rates_frame['time'] = rates_frame['time'].dt.tz_localize('utc') 
 
# display data
print("\nDisplay dataframe with data")
# print(rates_frame) 

rates_frame.to_csv(saveloc, index=False)