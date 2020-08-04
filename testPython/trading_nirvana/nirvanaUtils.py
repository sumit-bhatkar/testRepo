from datetime import datetime, date, timedelta
import json
from nsepy import get_history
import dateutil.relativedelta
import pandas as pd
from pip._internal import index
import csv
import requests

class CustomError(Exception):
     pass

def getBhavdata():
    url ="https://archives.nseindia.com/products/content/sec_bhavdata_full_02062020.csv"
    return pd.read_csv(url)

def get_data(symbol, from_date = '2016-01-01' ):
#     print("----------------------------------------------------------")
    from_date = datetime.strptime (from_date,'%Y-%m-%d')
    to_date = date.today()
#     print("Fetching data from {} to {}".format(from_date,to_date))
    data=get_history(symbol=symbol,start=from_date.date(),end=to_date)
    if data.empty :
        raise CustomError("Could not get data")
    data.reset_index(inplace=True)
#     print("Data Fetched")
#     print("----------------------------------------------------------")
    return data

def read_store (store_path='store/data.txt'):
    print ("Reading from file",store_path)
    with open(store_path) as json_file:
        json_data = json.load(json_file)
        
    data_frame = pd.read_json(json_data,orient='columns' )
    return data_frame
    
def persist_to_store (data_frame, store_path='store/data.txt'):
    json_data = data_frame.to_json()
    with open(store_path, 'w') as outfile:
        json.dump(json_data, outfile)
    print("Saved to file")
    print("----------------------------------------------------------")

def persist_csv_to_store(data_frame, store_path='store/data.txt'):
    data_frame.to_csv(store_path)
    print("Saved to file")
    print("----------------------------------------------------------")

def populate_heikin_ashi(df,length=0):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4
    idx = df.index.name
    if idx == None:
        idx = '_Temp_Idx_'
    df.index.name = '_Temp_Idx_'
    if length != 0 :
        length = len(df)-length
    df.reset_index(inplace=True)
    for i in range(length, len(df)):
        if i == 0:
            df.at[i, 'HA_Open'] = ((df.at[i, 'Open'] + df.at[i, 'Close']) / 2)
        else:
            df.at[i, 'HA_Open'] = ((df.at[i - 1, 'HA_Open'] + df.at[i - 1, 'HA_Close']) / 2)

    if idx != '_Temp_Idx_':
        df.set_index(idx, inplace=True)
    else :
        df.set_index('_Temp_Idx_', inplace=True)
        df.index.name =None
        
    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df

def get_rsi(series, period=14):
    #change = series['HA_Close'].diff()
    change = series.diff()
    gain, loss = change.copy(), change.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean().abs()
    rsi = avg_gain / avg_loss
    rsi = 100 - 100/(1+(rsi))
    return rsi

def get_td_ema (series,period=14,init_val=0):
    idx = series.index.name
    ema = pd.Series([],dtype='float64')
    alpha = 2 / (period + 1)
    for i in range(0, len(series)):
        if i == 0:
            ema.at[i] = init_val
        else:
            ema.at[i] = alpha * series.at[i] + (1 - alpha) * ema[i-1]
    return ema
    
    
def get_ema_for_rsi(series,period=14,init_val=0):
    idx = series.index.name
    ema = pd.Series([],dtype='float64')
    for i in range(0, len(series)):
        if i == 0:
            ema.at[i] = init_val
        else:
            ema.at[i] = ((ema.at[i-1]*(period-1)) + series.at[i])/period
#     print(ema)
    return ema

def get_exp_rsi(series, period=14):
    #change = series['HA_Close'].diff()
    change = series.diff()
    gain, loss = change.copy(), change.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
#     avg_gain = get_ema_for_rsi(gain,period,1.63)  # this is temp val given to SBIN
#     avg_loss = get_ema_for_rsi(loss.abs(),period,2.98)
    avg_gain = get_ema_for_rsi(gain,period)  # this is temp val given to SBIN
    avg_loss = get_ema_for_rsi(loss.abs(),period)
    rsi = avg_gain / avg_loss
    rsi = 100 - 100/(1+(rsi))
#     print(rsi)
    return rsi

def get_stoch_rsi(series, K=3, D=3, period=14):
    min = series.rolling(period).min()
    max = series.rolling(period).max()
    stoch_rsi_k = ((series - min)/(max-min)).rolling(K).mean()*100
    stoch_rsi_d = stoch_rsi_k.rolling(D).mean()
    return stoch_rsi_k, stoch_rsi_d

'''
This is etc stuff 
# drop columns
symbol_data = symbol_data.drop(
    ['Symbol','Series','Prev Close','Last','VWAP',]
    , axis=1)

# print ("{}{}{}{}{}".format(
#     symbol_data['Open'],symbol_data['High'],symbol_data['Low'],symbol_data['Close'],
#     symbol_data['HA_Close']))

# get only certain columns 
symbol_data = symbol_data[['Open','High','Low','Close']]
    
'''