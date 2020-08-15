import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd
import validations as v
import list_of_all_stocks as lst
from datetime import datetime, date, timedelta
import time

col_list = ['Date','Symbol','Series','Prev Close','Open','High','Low', 'Last', 'Close', 'VWAP', 'Volume', 'Turnover', 'Trades','Deliverable Volume','%Deliverble']
bd_col_list = ['DATE1', 'SYMBOL', 'SERIES', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'LAST_PRICE', 'CLOSE_PRICE', 'AVG_PRICE', 'TTL_TRD_QNTY', 'TURNOVER_LACS', 'NO_OF_TRADES', 'DELIV_QTY', 'DELIV_PER']

days_list = ['10082020','11082020','12082020','13082020','14082020']

def read_bhavdata():
    bd1 = pd.DataFrame()
    for day in days_list :
#         url =f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{day}.csv"
#         print(f'fetching {url}')
#         bd = pd.read_csv(url)
        bd = nv.read_store(f'store/bhavcopy_{day}.json')
#         nv.persist_to_store(bd,f'store/bhavcopy_{day}.json')
        bd = bd.rename(columns=lambda x: x.strip())
        bd = bd[bd['SERIES'].str.contains('|'.join(["EQ","BE"]))] 
        bd = bd[bd_col_list]
        bd.columns = col_list
        bd['Date'] = pd.to_datetime(bd.Date)
        bd['%Deliverble'] = pd.to_numeric(bd['%Deliverble'] , errors='coerce')
        bd1 = bd1.append(bd)
    return bd1

def fetch_data_for_symbol(df,symbol):
#     When reading from store use following
    store_path = 'store/DB/01012016_{}.json'.format(symbol)
#     start = time.perf_counter()
    sd1 = nv.read_store(store_path)
    sd = sd1.copy()
#     print(f'L1 {round(time.perf_counter()-start, 2)}')
    sd = sd[sd.Date > '2019-01-01'][col_list]
    sd = sd.append(df)
    sd = sd.sort_values(by='Date')
    sd = sd.drop_duplicates(subset='Date', keep="first")
    sd.reset_index(drop=True, inplace=True)
    nv.populate_heikin_ashi (sd)
#     print(f'L7 {round(time.perf_counter()-start, 2)}')
    sd["HA_RSI"] = nv.get_exp_rsi(sd["HA_Close"])
#     print(f'L8 {round(time.perf_counter()-start, 2)}')
    sd["Stoch_rsi_K"] , sd["Stoch_rsi_D"] = nv.get_stoch_rsi(sd["HA_RSI"],3,3,14)
#     print(f'L9 {round(time.perf_counter()-start, 2)}')
    sd['ema200'] = nv.get_td_ema(sd['Close'],200)
#     print(f'L10 {round(time.perf_counter()-start, 2)}')
    sd['ema50'] = nv.get_td_ema(sd['Close'],50)
#     print(f'L11 {round(time.perf_counter()-start, 2)}')
 
    sd1 = sd1.append(sd.tail(len(df.index)))
    sd1.reset_index(drop=True, inplace=True)
#     print(sd1.tail(10))
#     print(sd.tail(10))
#     print(sd[sd.Date.between('2019-05-01', '2019-05-10')][
#                                                         {'Date','ema200','ema50',
#                                                         'HA_RSI'}
#                                                         ])
#     print(sd1[sd1.Date.between('2019-05-01', '2019-05-10')][
#                                                         {'Date','ema200','ema50',
#                                                         'HA_RSI'}
#                                                         ])   
    nv.persist_to_store(sd1,store_path)
#     nv.persist_excel_to_store(sd,f'store/DB/01012016_{symbol}.xlsx')
#     print(f'L12 {round(time.perf_counter()-start, 2)}')
    return sd

def nirvana_prediction( bd ):
    time_taken = []
    time_taken.append(datetime.today())
    summary = pd.DataFrame()
    for symbol in lst.list_of_100_results :
        print('\nChecking for {}'.format(symbol))
        sd = fetch_data_for_symbol(bd[bd.Symbol == symbol], symbol)
        sd = v.get_signal_using_strategy_2(sd)
        time_taken.append(datetime.today())
        summary = summary.append(sd.tail(1), ignore_index=True)
   
    x = pd.Series(time_taken)
    print(x.diff().sum())
    print(summary[summary['signal_st1']])
    nv.persist_excel_to_store(summary,f"store/signal_summary_{datetime.strftime(datetime.now(),'%Y%m%d_%H%M%S')}.xlsx")



print("-------------------- Start of Nirvana-v1.0 ---------------------------")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

  
bd = read_bhavdata()
nirvana_prediction(bd)

print("-------------------- Nirvana Achieved ---------------------------")


            



