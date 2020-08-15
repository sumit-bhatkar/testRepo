""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd
import validations as v

from datetime import datetime, date, timedelta
import dateutil.relativedelta
from nsepy import get_history
from matplotlib.pyplot import axis
from numpy.core.fromnumeric import shape

''' Screening Thresholds '''
TTQ_CHANGE_THRESHOLD = 100
TO_CHANGE_THRESHOLD = 200
DEL_PERCENT_THRESHOLD = 20

yesterday='13082020'
today='14082020'

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
    time_taken = []
    time_taken.append(datetime.today())
    summary = pd.DataFrame()
    for symbol in list_of_stocks :
        print('\nChecking for {}'.format(symbol))
        symbol_data = fetch_data_for_symbol(symbol)
        symbol_data = v.get_signal_using_strategy_1(symbol_data)
        
        if symbol_data['signal_st1'].tail(1).item():
            print(f'Buy signal - close {symbol_data.Close.tail(1).item()}')
        else :
            print(f'Do not buy {symbol}')
        
        time_taken.append(datetime.today())
        summary = summary.append(symbol_data.tail(1), ignore_index=True)
   
    x = pd.Series(time_taken)
    print(x.diff().sum())
    print(summary)
    nv.persist_excel_to_store(summary,f'store/signal_summary_{today}.xlsx')

def read_bhavdata():
#     bd1 = nv.read_store('store/bhav_20200803.txt')
#     bd2 = nv.read_store('store/bhav_20200804.txt')
    bd1,bd2 = nv.getBhavdata(yesterday,today)
    ''' filter only EQ and BE series '''
    bd1 = bd1[bd1['SERIES'].str.contains('|'.join(["EQ","BE"]))] 
    bd2 = bd2[bd2['SERIES'].str.contains('|'.join(["EQ","BE"]))] 
    return pd.merge(bd1, bd2, how='outer', on=['SYMBOL','SERIES', 'SYMBOL','SERIES'])

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
    st = read_bhavdata()
#     st, screened = screen_strategy_test(st)
    st, screened = screen_strategy_1(st)
    print(screened['SYMBOL'])
    nv.persist_excel_to_store(st,f'store/bhavcopy_screening_{today}.xlsx')
    nirvana_prediction(screened['SYMBOL'])     

print("-------------------- Start of Nirvana-v1.0 ---------------------------")

screen_from_bhavcopy_and_predict()


print("-------------------- Nirvana Achieved ---------------------------")


            



