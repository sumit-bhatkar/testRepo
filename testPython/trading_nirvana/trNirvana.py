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


#import matplotlib.pyplot as plt
# from nsepy import get_history

def fetch_data_from_site():
    symbol_data = nv.get_data('SBIN','2020-01-01','2020-07-25')
    nv.persist_to_store(symbol_data,'store/temp.txt')

def filter_and_store(df):
    df = df[['Open','High','Low','Close']]
    nv.persist_to_store(df,'store/temp.txt')

def create_baseline():
    print("----------------------------------------------------------")
    symbol_data = nv.read_store('store/temp.txt')
    nv.populate_heikin_ashi (symbol_data)
    symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
    symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
    nv.persist_to_store(symbol_data,'store/temp.txt')
    print(symbol_data)

def update_records_till_today(symbol_data):
    today = date.today()
    start_day = (symbol_data['Date'].tail(1).item()) + timedelta(days = 1)
    data = get_history(symbol='SBIN',start=start_day.date(),end=today)
    length = len(data)
#     symbol_data = symbol_data.append(data,ignore_index=True)
#     print(data)
    return data, length

def work_on_data():
    print("----------------------------------------------------------")
    symbol_data = nv.read_store('store/temp.txt')
    print(symbol_data)
#     # symbol_data = nv.read_store('store/SBIN_store_20200504-20200731.txt')
#     # print("----------------------------------------------------------")
#     data, num_delta_records = update_records_till_today(symbol_data)
#     print(data)
#     
#     # symbol_data = symbol_data.drop ([143,144,145,146])
#     symbol_data = symbol_data.append(data,ignore_index=True)
#     symbol_data = nv.populate_heikin_ashi(symbol_data,num_delta_records)
#     symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
#     symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
#     
#     
#     
#     print("----------------------------------------------------------")
#     # print (symbol_data[['Open','High','Low','Close']])
#     # print(symbol_data[['Date',"HA_Close","HA_RSI"]]) 
#     # print (symbol_data.loc[50:,["Date","RSI"]]  ) 
#     # print( symbol_data["Stoch_rsi_K"][-10:])
#     print(symbol_data[-10:])

print("-------------------- Start of Nirvana-v1.0 ---------------------------")
# fetch_data_from_site()
# create_baseline()
work_on_data()
print("-------------------- Nirvana Achieved ---------------------------")


            
# symbol_data = u.read_store()
# print(symbol_data)
#symbol_data = symbol_data.drop(symbol_data.index[0])

#Tested
# copy SBIN_store_2020-08-01.txt as temp.txt then apply following and store again
# fetch_data_from_site()
# nv.populate_heikin_ashi (symbol_data)
# symbol_data['Date']=pd.to_datetime(symbol_data['index'], unit='ms').dt.strftime('%Y-%m-%d')
# symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
# symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
# nv.persist_to_store(symbol_data,'store/temp.txt')
# nv.persist_csv_to_store(symbol_data,'store/temp_csv.txt') 
# Untested

