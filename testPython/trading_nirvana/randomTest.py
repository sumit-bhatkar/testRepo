""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as nv
import list_of_all_stocks as lst
import json
import numpy as np
import pandas as pd
from multiprocessing import Pool    
import concurrent.futures
import time


from datetime import datetime, date, timedelta
import dateutil.relativedelta
from nsepy import get_history

LOG_LVL_FATAL = 1
LOG_LVL_ERROR = 2
LOG_LVL_WARN  = 3
LOG_LVL_DEBUG = 4
LOG_LVL_INFO  = 5
LOG_LEVEL = LOG_LVL_ERROR
# 
# list_of_stocks = [ 
#         'TATAMOTORS',
#         'RELIANCE',
#         'BANDHANBNK',
#         'LAURUSLABS',
#         'HDFCBANK',
#         'SBIN',
#         'ICICIBANK',
#         'AXISBANK',
#         'SUNPHARMA',
#         'UPL',
#         'CIPLA',
#         'HDFC',
#         'KOTAKBANK',
#         'BPCL',
#         'INDUSINDBK',
#         'BAJFINANCE',
#         'INFY',
#         'TITAN',
#         'IBULHSGFIN',
#         'MARUTI',
#         'DIVISLAB',
#         'IDEA',
#         'DRREDDY',
#         'TCS',
#         ]

STOCK_RSI_FLAT_PERIOD = 6
STOCK_RSI_MAX_STD = 6
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 50
symbol = 'CAPLIPOINT' 
#SBIN


def fetch_data_from_site(symbol):
    symbol_data = nv.get_data(symbol)
#     file_name = 'store/01012016_{}.json'.format(s)
    nv.persist_to_store(symbol_data,'store/temp.txt') if LOG_LEVEL >= LOG_LVL_DEBUG else ""
#     nv.persist_to_store(symbol_data,file_name) 
    return symbol_data

def create_baseline(symbol_data):
    print("----------------------------------------------------------") if LOG_LEVEL >= LOG_LVL_DEBUG else ""
    symbol_data = nv.read_store('store/temp.txt') if LOG_LEVEL >= LOG_LVL_DEBUG else ""
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
    symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)
    nv.persist_to_store(symbol_data,'store/temp.txt')   if LOG_LEVEL >= LOG_LVL_DEBUG else ""
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
    print(cur_low - lowest_low.item())
    return (cur_low - lowest_low.item()) < MAX_CURR_LOW_DIFF

def work_on_data(symbol_data):
    print("----------------------------------------------------------")
    symbol_data = nv.read_store('store/temp.txt') if LOG_LEVEL >= LOG_LVL_DEBUG else ""
    
    
    
    stoch_ris_passed = validate_stoch_rsi(symbol_data)
    ema_200_50_passed = validate_ema_200_50(symbol_data)
    curr_low_passed = validate_curr_low(symbol_data)

    print(symbol_data) if LOG_LEVEL >= LOG_LVL_DEBUG else ""
      
    print("**********************************************************")  if LOG_LEVEL >= LOG_LVL_DEBUG else ""
    if stoch_ris_passed \
        and ema_200_50_passed \
        and curr_low_passed :
            print ('\t BUY - {}'.format(symbol))
    else:
            print ('\t DO NOT BUY - {}'.format(symbol))
                
    print("**********************************************************") if LOG_LEVEL >= LOG_LVL_DEBUG else ""



# print("-------------------- Start of Nirvana-v1.0 ---------------------------")
# symbol_data = fetch_data_from_site(symbol)
# symbol_data = create_baseline(symbol_data)
# symbol_data = work_on_data(symbol_data)
# list_of_stocks = [ 'CAPLIPOINT',
# #     'MUKTAARTS','MEGASOFT','SBIN',
# #         'LICNETFGSC','ONEPOINT','LFIC'
#     'SBIN'
#     ]


# for symbol in lst.list_of_stocks :
def create_db(symbol):
    file_name = 'store/DB/01012016_{}.json'.format(symbol)
    print(file_name)
    try :
        symbol_data = nv.get_data(symbol)
        nv.populate_heikin_ashi (symbol_data)
        symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
        symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
        symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
        symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)
        nv.persist_to_store(symbol_data,file_name)
#         time_taken.append(datetime.today())
    except :
        print("Oops! Error occurred.")



''' Start all your main processing here [for windows]'''
if __name__ == '__main__':
    print("-------------------- Start of Nirvana-v1.0 ---------------------------")
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(create_db, lst.list_of_stocks)
#     for result in results:
#         print(result)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
    print("-------------------- Nirvana Achieved ---------------------------")

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


            


