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

LOG_LVL_FATAL = 1
LOG_LVL_ERROR = 2
LOG_LVL_WARN  = 3
LOG_LVL_DEBUG = 4
LOG_LVL_INFO  = 5
LOG_LEVEL = LOG_LVL_ERROR

STOCK_RSI_FLAT_PERIOD = 6
STOCK_RSI_MAX_STD = 6
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 50
symbol = 'CAPLIPOINT' 
#SBIN


def fetch_data_from_site(symbol):
    symbol_data = nv.get_data(symbol)
    nv.persist_to_store(symbol_data,'store/temp.txt') 
    return symbol_data

def create_baseline(symbol_data):
    print("----------------------------------------------------------") 
    symbol_data = nv.read_store('store/temp.txt') 
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
    symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)
    nv.persist_to_store(symbol_data,'store/temp.txt')   
    return symbol_data

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
#     print(cur_low - lowest_low.item())
    return (cur_low - lowest_low.item()) < MAX_CURR_LOW_DIFF , lowest_low.item() + 10

def work_on_data(symbol_data):
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
            print ('\t BUY - {}'.format(symbol))
    else:
            print ('\t DO NOT BUY - {}'.format(symbol))
                
    print("**********************************************************") 

def get_signal(symbol):
    symbol_data = nv.get_data(symbol)
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
    symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)
    
    stoch_ris_passed = validate_stoch_rsi(symbol_data)
    ema_200_50_passed = validate_ema_200_50(symbol_data)
    curr_low_passed , buy_value = validate_curr_low(symbol_data)
    
    if stoch_ris_passed \
        and ema_200_50_passed \
        and curr_low_passed :
            print ('BUY - {} at {}'.format(symbol,buy_value))
    else:
            print ('DO NOT BUY - {}'.format(symbol))


print("-------------------- Start of Nirvana-v1.0 ---------------------------")
# symbol_data = fetch_data_from_site(symbol)
# symbol_data = create_baseline(symbol_data)
# symbol_data = work_on_data(symbol_data)
# get_signal(symbol)

list_of_stocks = [ 'CAPLIPOINT',
    'MUKTAARTS','SBIETFQLTY','SBIN',
    'LICNETFGSC','ONEPOINT','LFIC'
    ]

time_taken = []
time_taken.append(datetime.today())
for symbol in list_of_stocks :
    print(symbol)
    try :
        get_signal(symbol)
#         print("nothing")
        time_taken.append(datetime.today())
    except :
        print("Oops! Error occurred.")

x = pd.Series(time_taken)
print(x.diff())

print("----------------------------------------------------------")    
# print(time_taken)    
# print ("testing info") if LOG_LEVEL >= LOG_LVL_INFO else ""
# print ("testing debug") if LOG_LEVEL >= LOG_LVL_DEBUG else ""
# print ("testing error") if LOG_LEVEL >= LOG_LVL_ERROR else ""
# print ("testing fatal") if LOG_LEVEL >= LOG_LVL_FATAL else ""
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


            


