""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd

from datetime import datetime, date, timedelta
import dateutil.relativedelta
from nsepy import get_history

STOCK_RSI_FLAT_PERIOD = 6
STOCK_RSI_MAX_STD = 6
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 50
symbol = 'CAPLIPOINT' 
#SBIN


def fetch_data_from_site(symbol):
    symbol_data = nv.get_data(symbol)
    nv.persist_to_store(symbol_data,'store/temp.txt')

def create_baseline():
    print("----------------------------------------------------------")
    symbol_data = nv.read_store('store/temp.txt')
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
    symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)
    nv.persist_to_store(symbol_data,'store/temp.txt')

def validate_stoch_rsi(symbol_data):
    data = symbol_data.tail(STOCK_RSI_FLAT_PERIOD + 1)
    data['delta'] = (data["Stoch_rsi_K"] - data["Stoch_rsi_D"]).abs()
    data['diff'] = (data["Stoch_rsi_K"].diff()).abs()
    
#     print (data['delta'].var())
#     print (data['delta'].std())
    return data['delta'].std().item() < STOCK_RSI_MAX_STD

def validate_ema_200_50(symbol_data):
    return True

def validate_curr_low(symbol_data):
    cur_low = symbol_data['Low'].iloc[-1]
    lowest_low = symbol_data.loc[LOWEST_LOW_PERIOD:,["Low"]].min()
    print(cur_low - lowest_low.item())
    return (cur_low - lowest_low.item()) < MAX_CURR_LOW_DIFF

def work_on_data():
    print("----------------------------------------------------------")
    symbol_data = nv.read_store('store/temp.txt')
    
    
    
    stoch_ris_passed = validate_stoch_rsi(symbol_data)
    ema_200_50_passed = validate_ema_200_50(symbol_data)
    curr_low_passed = validate_curr_low(symbol_data)

    print(symbol_data)
      
    print("**********************************************************")  
    if stoch_ris_passed \
        and ema_200_50_passed \
        and curr_low_passed :
            print ('\t You can buy - {}'.format(symbol))
    else:
            print ('\t Do not buy - {}'.format(symbol))
                
    print("**********************************************************")



print("-------------------- Start of Nirvana-v1.0 ---------------------------")
fetch_data_from_site(symbol)
create_baseline()
work_on_data()

'MUKTAARTS'
'SBIETFQLTY'
'HOVS'
'JMA'
'SMARTLINK'
'ICICI500'
'LICNETFGSC'
'ONEPOINT'
'LFIC'
print("-------------------- Nirvana Achieved ---------------------------")


            


