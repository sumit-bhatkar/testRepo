""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd
from datetime import datetime as dt
#import matplotlib.pyplot as plt
# from nsepy import get_history

def fetch_data_from_site():
    symbol_data = nv.get_data('SBIN','2020-07-01','2020-08-01')
    nv.persist_to_store(symbol_data,'store/temp.txt')

def filter_and_store(df):
    df = df[['Open','High','Low','Close']]
    nv.persist_to_store(df,'store/temp.txt')


print("----------------------------------------------------------")
symbol_data = nv.read_store('store/temp.txt')
# print("----------------------------------------------------------")
 
 
 
# print( symbol_data["Stoch_rsi_K"][14:])
# print(symbol_data[['Date',"HA_Close","HA_RSI"]]) 
# print (symbol_data.loc[50:,["Date","RSI"]]  ) 
# print (symbol_data[['Date','Open','High','Low','Close']])
print("----------------------------------------------------------")
            
# symbol_data = u.read_store()
# print(symbol_data)
#symbol_data = symbol_data.drop(symbol_data.index[0])

#Tested
# copy SBIN_store_2020-08-01.txt as temp.txt then apply following and store again
# nv.populate_heikin_ashi (symbol_data)
# symbol_data['Date']=pd.to_datetime(symbol_data['index'], unit='ms').dt.strftime('%Y-%m-%d')
# symbol_data["HA_RSI"] = nv.get_exp_rsi(symbol_data["HA_Close"])
# symbol_data["Stoch_rsi_K"] , symbol_data["Stoch_rsi_D"] = nv.get_stoch_rsi(symbol_data["HA_RSI"],3,3,14)
# nv.persist_to_store(symbol_data,'store/temp.txt')
# nv.persist_csv_to_store(symbol_data,'store/temp_csv.txt') 

# Untested
# symbol_data["RSI"] = nv.populate_rsi(symbol_data["Close"])
# symbol_data["HA_RSI"] = nv.populate_rsi(symbol_data["HA_Close"])


# print("----------------------------------------------------------")
