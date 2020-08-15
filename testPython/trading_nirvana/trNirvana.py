""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd
import nirvanaStudy as sd

from datetime import datetime, date, timedelta
import dateutil.relativedelta
from nsepy import get_history
from matplotlib.pyplot import axis
from numpy.core.fromnumeric import shape

STOCK_RSI_FLAT_PERIOD = 6
STOCK_RSI_MAX_STD = 2
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 10
EMA_50_THRESHOLD = 10

''' Screening Thresholds '''
TTQ_CHANGE_THRESHOLD = 100
TO_CHANGE_THRESHOLD = 200
DEL_PERCENT_THRESHOLD = 20

symbol = 'CAPLIPOINT' 
yesterday='12082020'
today='13082020'
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

def validate_stoch_rsi_flat(symbol_data,
                            flat_period = STOCK_RSI_FLAT_PERIOD, 
                            max_flat_std = STOCK_RSI_MAX_STD):
    data = symbol_data.tail(flat_period + 1)
    data['delta'] = (data["Stoch_rsi_K"] - data["Stoch_rsi_D"]).abs()
    data['diff'] = (data["Stoch_rsi_K"].diff()).abs()
    col_name = 'flatstokrsi_{}'.format(flat_period) 
    
    return data['delta'].std().item() < max_flat_std

def get_percent_difference(current_value,base_value):
    return (current_value - base_value) / base_value * 100

def validate_ema_200_50(symbol_data, ema50_threshold = EMA_50_THRESHOLD):
    print(symbol_data['ema50'].tail(1).item(), symbol_data['Close'].tail(1).item())
    return abs(get_percent_difference (
                    symbol_data['Close'].tail(1).item() , 
                    symbol_data['ema50'].tail(1).item()
                )) < ema50_threshold 
#     return True

def validate_curr_low(symbol_data,
                      low_period = LOWEST_LOW_PERIOD, 
                      diff_thr = MAX_CURR_LOW_DIFF):
    cur_low = symbol_data['Low'].iloc[-1].item()
    lowest_low = symbol_data.loc[low_period:,["Low"]].min().item()
    percent_difference =  get_percent_difference(cur_low, lowest_low)
    print(cur_low, lowest_low, abs(percent_difference))
    
    return percent_difference < diff_thr , lowest_low

def get_signal_using_strategy_1(symbol_data):

    stoch_ris_passed = validate_stoch_rsi_flat(symbol_data)
    ema_200_50_passed = validate_ema_200_50(symbol_data)
    curr_low_passed , lowest_low_value = validate_curr_low(symbol_data)
    
    print(stoch_ris_passed,ema_200_50_passed,curr_low_passed)

    if stoch_ris_passed \
        and ema_200_50_passed \
        and curr_low_passed :
            print ('BUY - {} : Close {} , 3 month Low {}'.format(symbol_data.symbol.tail(1).item(),symbol_data['Close'].tail(1).item(),lowest_low_value))
            return True
    else:
            print ('DO NOT BUY - {}'.format(symbol))
            return False

def fetch_data_for_symbol(symbol):
#     When reading from store use following
#     store_path = 'store/DB/01012016_{}.json'.format(symbol)
#     symbol_data = nv.read_store(store_path)

#     When calculation is not done before use these lines
    symbol_data = nv.get_data(symbol,'2018-01-01')
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    symbol_data['ema200'] = nv.get_td_ema(symbol_data['Close'],200)
    symbol_data['ema50'] = nv.get_td_ema(symbol_data['Close'],50)

    return symbol_data

def nirvana_prediction( list_of_stocks ):
    #TODO : Check empty frames
#     list_of_stocks.isempty()
#     list_of_stocks = [ 'CAPLIPOINT',
#         'MUKTAARTS','MEGASOFT','SBIN',
# #         'LICNETFGSC','ONEPOINT','LFIC'
#         'SBIN'
#         ]
    time_taken = []
    time_taken.append(datetime.today())
    summary = pd.DataFrame()
    for symbol in list_of_stocks :
        print('\nChecking for {}'.format(symbol))
        symbol_data = fetch_data_for_symbol(symbol)
        symbol_data = sd.get_signal_using_strategy_1(symbol_data)
        
        if symbol_data['signal_st1'].tail(1).item():
            print(f'Buy signal - close {symbol_data.Close.tail(1).item()}')
        else :
            print(f'Do not buy {symbol}')
        
        time_taken.append(datetime.today())
        summary = summary.append(symbol_data.tail(1), ignore_index=True)
#         try :
#             get_signal_using_strategy_1(symbol)
#             time_taken.append(datetime.today())
#         except Exception as e: 
#             print(e)
#             print("Oops! Error occurred.")
    
    x = pd.Series(time_taken)
#     print(x.diff())
    print(x.diff().sum())
    print(summary)
    nv.persist_excel_to_store(summary,f'store/signal_summary_{today}.xlsx')

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
#     bd1 = nv.read_store('store/bhav_20200803.txt')
#     bd2 = nv.read_store('store/bhav_20200804.txt')
    bd1,bd2 = nv.getBhavdata(yesterday,today)
    return bd1[bd1['SERIES'].str.contains('|'.join(["EQ","BE"]))] , \
        bd2[bd2['SERIES'].str.contains('|'.join(["EQ","BE"]))] 

def screen_strategy_1(st):
    st['tq%_x'] = st['TTL_TRD_QNTY_x'] / st['NO_OF_TRADES_x']
    st['tq%_y'] = st['TTL_TRD_QNTY_y'] / st['NO_OF_TRADES_y']
    st['tq_c'] = (st['tq%_y'] - st['tq%_x'])/(st['tq%_x'])*(100)
    st['to_c'] = (st['TURNOVER_LACS_y'] - st['TURNOVER_LACS_x'])/st['TURNOVER_LACS_x'] *100
    
    st.fillna(0)
    st = st.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return  st, st[
                    ( st.tq_c > TTQ_CHANGE_THRESHOLD       ) & 
                    ( st.to_c > TO_CHANGE_THRESHOLD        ) & 
                    ( pd.to_numeric(st.DELIV_PER_y , errors='coerce')> DEL_PERCENT_THRESHOLD ) 
                ] 

def screen_strategy_test(st):
    test_stocks = [ 
            'TATAMOTORS',
            'RELIANCE',
            'BANDHANBNK',
            'LAURUSLABS',
            'HDFCBANK',
            'SBIN'
        ]
    return  st, pd.DataFrame(test_stocks, columns =['SYMBOL'])
 
                    
def screen_from_bhavcopy_and_predict():
    bd1,bd2 = read_bhavdata()
    st = pd.merge(bd1, bd2, how='outer', on=['SYMBOL','SERIES', 'SYMBOL','SERIES'])
#     st, screened = screen_strategy_test(st)
    st, screened = screen_strategy_1(st)
    print(screened['SYMBOL'])
    nv.persist_excel_to_store(st,f'store/bhavcopy_screening_{today}.xlsx')
    nirvana_prediction(screened['SYMBOL'])     

print("-------------------- Start of Nirvana-v1.0 ---------------------------")
# symbol_data = fetch_data_from_site(symbol)
# symbol_data = create_baseline(symbol_data)
# get_signal_using_strategy_1(symbol)
screen_from_bhavcopy_and_predict()

# screen_from_bhavcopy_and_predict()
# study_strategy_for_stock('SBIN',get_signal_using_strategy_1)


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
print("-------------------- Nirvana Achieved ---------------------------")


            



