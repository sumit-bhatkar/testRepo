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
from matplotlib.pyplot import axis

STOCK_RSI_FLAT_PERIOD = 6
STOCK_RSI_MAX_STD = 6
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 50

''' Screening Thresholds '''
TTQ_CHANGE_THRESHOLD = 100
TO_CHANGE_THRESHOLD = 200
DEL_PERCENT_THRESHOLD = 20

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
#     print(symbol_data)
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


def way_to_nirvana( list_of_stocks ):
    #TODO : Check empty frames
#     list_of_stocks.isempty()
#     list_of_stocks = [ 'CAPLIPOINT',
#         'MUKTAARTS','MEGASOFT','SBIN',
# #         'LICNETFGSC','ONEPOINT','LFIC'
#         'SBIN'
#         ]
    
    time_taken = []
    time_taken.append(datetime.today())
    for symbol in list_of_stocks :
        print('Checking for {}'.format(symbol))
        try :
            get_signal(symbol)
    #         print("nothing")
            time_taken.append(datetime.today())
        except :
            print("Oops! Error occurred.")
    
    x = pd.Series(time_taken)
    print(x.diff())
    print(x.diff().sum())

def store_bhavdata():
    url ="https://archives.nseindia.com/products/content/sec_bhavdata_full_04082020.csv" 
    bd = pd.read_csv(url)  #bhav_data
    bd.columns = bd.columns.str.strip()
    nv.persist_to_store(bd,'store/bhav_20200804.txt')
    url ="https://archives.nseindia.com/products/content/sec_bhavdata_full_03082020.csv" 
    bd = pd.read_csv(url)  #bhav_data
    bd.columns = bd.columns.str.strip()
    nv.persist_to_store(bd,'store/bhav_20200803.txt')

def read_bhavdata():
    bd1 = nv.read_store('store/bhav_20200803.txt')
    bd2 = nv.read_store('store/bhav_20200804.txt')
    return bd1[bd1['SERIES'].str.contains('|'.join(["EQ","BE"]))] , \
        bd2[bd2['SERIES'].str.contains('|'.join(["EQ","BE"]))] 
      

print("-------------------- Start of Nirvana-v1.0 ---------------------------")
# symbol_data = fetch_data_from_site(symbol)
# symbol_data = create_baseline(symbol_data)
# symbol_data = work_on_data(symbol_data)
# get_signal(symbol)

# way_to_nirvana()

bd1,bd2 = read_bhavdata()
st = pd.merge(bd1, bd2, how='outer', on=['SYMBOL','SERIES', 'SYMBOL','SERIES'])

st['tq%_x'] = st['TTL_TRD_QNTY_x'] / st['NO_OF_TRADES_x']
st['tq%_y'] = st['TTL_TRD_QNTY_y'] / st['NO_OF_TRADES_y']
st['tq_c'] = (st['tq%_y'] - st['tq%_x'])/(st['tq%_x'])*(100)

st['to_c'] = (st['TURNOVER_LACS_y'] - st['TURNOVER_LACS_x'])/st['TURNOVER_LACS_x'] *100

st.fillna(0)
st = st.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# print(type(st.DELIV_PER_y.at[1]))
# 
# print(type(st.DELIV_PER_y.at[3]))
# 
# pd.to_numeric(df['DataFrame Column'], errors='coerce')
# print(type(st.DELIV_PER_y.at[5]))


screened = st[
                ( st.tq_c > TTQ_CHANGE_THRESHOLD       ) & 
                ( st.to_c > TO_CHANGE_THRESHOLD        ) & 
                ( pd.to_numeric(st.DELIV_PER_y , errors='coerce')> DEL_PERCENT_THRESHOLD ) 
            ] 

# print(screened[['SYMBOL','tq_c','to_c','DELIV_PER_y']].sort_values (['tq_c','to_c'],ascending=False))
# print(screened.shape)
 
way_to_nirvana( screened['SYMBOL'] )   

# print(bd1)
# print(st['NO_OF_TRADES_x'])
# print(st['NO_OF_TRADES_y'])
# nv.persist_csv_to_store(st,'store/merge.csv')
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


            



