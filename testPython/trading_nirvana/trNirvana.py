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

def populate_rsi(df, period=14):
    #change = df['HA_Close'].diff()
    change = df.diff()
    gain, loss = change.copy(), change.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(period).ewm(alpha=0.5).mean()
    print (avg_gain)
    avg_loss = loss.rolling(period).mean().abs()
    rsi = avg_gain / avg_loss
    rsi = 100 - 100/(1+(rsi))
    return rsi

print("----------------------------------------------------------")
symbol_data = nv.read_store('store/temp.txt')
#symbol_data['Date']=pd.to_datetime(symbol_data['index'], unit='ms').dt.strftime('%Y-%m-%d')
# print("----------------------------------------------------------")
# 
# nv.populate_heikin_ashi (symbol_data)
symbol_data["RSI"] = populate_rsi(symbol_data["Close"])
# symbol_data["HA_RSI"] = nv.populate_rsi(symbol_data["HA_Close"])
# symbol_data['Date']=pd.to_datetime(symbol_data['index'], unit='ms').dt.strftime('%Y-%m-%d')
# 
# #symbol_data["RSI"] = nv.populate_rsi(symbol_data["Close"])
# 
# #nv.persist_to_store(symbol_data,'store/temp.txt')
print(symbol_data[["Close","RSI"]]) 
# print (symbol_data.loc[50:,["Date","RSI"]]  ) 
# nv.persist_csv_to_store(symbol_data,'store/temp_csv.txt') 


#print (symbol_data[['Date','Open','High','Low','Close']])
    
print("----------------------------------------------------------")
            
# symbol_data = u.read_store()
# print(symbol_data)
#symbol_data = symbol_data.drop(symbol_data.index[0])
#nv.persist_to_store(symbol_data)
# today = u.get_data('SBIN')
# final = pd.concat ([symbol_data,today[-3:-1]])
# final = pd.concat ([final,today[-3:-1]])
# print(final)

# nv.populate_heikin_ashi (symbol_data)
# symbol_data["RSI"] = populate_HA_rsi(symbol_data["Close"])
# symbol_data["HA_RSI"] = populate_HA_rsi(symbol_data["HA_Close"])
# print("----------------------------------------------------------")
