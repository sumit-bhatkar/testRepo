from datetime import datetime
import json
#import matplotlib.pyplot as plt
from nsepy import get_history
import dateutil.relativedelta
import pandas as pd
#from pandas._libs.tslib import format_array_from_datetime
from pip._internal import index
import csv
import requests


#print(data['High'])
#data['Close'].plot()
#data['High'].plot()
#data['Low'].plot()
#data['%K'].plot()
# print(data['High'], data['%K'])
#plt.show()
def get_time():
    to_date=datetime.now()
    to_date=datetime.strftime(to_date,'%Y,%m,%d')
    to_date=datetime.strptime(to_date,'%Y,%m,%d')
    from_date=to_date-dateutil.relativedelta.relativedelta(month=6)
    #from_date=to_date-dateutil.relativedelta.relativedelta(day=10)
    return from_date,to_date

def getBhavdata():
    url ="https://archives.nseindia.com/products/content/sec_bhavdata_full_02062020.csv"
    return pd.read_csv(url)

def get_data(symbol, from_date , to_date):
    print("----------------------------------------------------------")
    #plt.style.use('fivethirtyeight')
    from_date = datetime.strptime (from_date,'%Y-%m-%d')
    to_date = datetime.strptime (to_date,'%Y-%m-%d')
    print("Fetching data from {} to {}".format(from_date,to_date))
    #data=get_history(symbol='SBIN',start=from_date,end=to_date)
    data=get_history(symbol=symbol,start=from_date,end=to_date)
    print("Data Fetched")
    #doc = data.to_json()
    #doc = data.iloc[0:5].to_json()
    #con = pd.read_json(doc,orient='columns' )
    #print(con)
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

def populate_heikin_ashi(df):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4
    idx = df.index.name
    df.reset_index(inplace=True)
    for i in range(0, len(df)):
        if i == 0:
            df.at[i, 'HA_Open'] = ((df.at[i, 'Open'] + df.at[i, 'Close']) / 2)
        else:
            df.at[i, 'HA_Open'] = ((df.at[i - 1, 'HA_Open'] + df.at[i - 1, 'HA_Close']) / 2)

    if idx:
        df.set_index(idx, inplace=True)
    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df

def populate_rsi(df, period=14):
    #change = df['HA_Close'].diff()
    change = df.diff()
    gain, loss = change.copy(), change.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean().abs()
    rsi = avg_gain / avg_loss
    rsi = 100 - 100/(1+(rsi))
    return rsi


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