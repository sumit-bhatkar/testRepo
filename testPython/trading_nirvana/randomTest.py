from datetime import datetime
import json
#import matplotlib.pyplot as plt
from nsepy import get_history
import dateutil.relativedelta
import pandas as pd
import csv
import requests

def get_data(symbol, from_date , to_date):
    print("----------------------------------------------------------")
    from_date = datetime.strptime (from_date,'%Y-%m-%d')
    to_date = datetime.strptime (to_date,'%Y-%m-%d')
    print("Fetching data from {} to {}".format(from_date,to_date))
    data=get_history(symbol=symbol,start=from_date,end=to_date)
    data.reset_index(inplace=True)
    print("Data Fetched")
    return data

def persist_to_store (data_frame, store_path='store/data.txt'):
    json_data = data_frame.to_json()
    with open(store_path, 'w') as outfile:
        json.dump(json_data, outfile)
    print("Saved to file")
    print("----------------------------------------------------------")
    
def fetch_data_from_site():
    symbol_data = get_data('SBIN','2020-07-01','2020-07-25')
    persist_to_store(symbol_data,'store/temp_1.txt')

def read_store (store_path='store/data.txt'):
    print ("Reading from file",store_path)
    with open(store_path) as json_file:
        json_data = json.load(json_file)
        
    data_frame = pd.read_json(json_data,orient='columns' )
    return data_frame
    
    
def populate_heikin_ashi(df,length=0):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4
    idx = df.index.name
    if idx == None:
        idx = '_Temp_Idx_'
        df.index.name = '_Temp_Idx_'
    print(idx)
    print(type(idx))
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
##############################################################################
# fetch_data_from_site()
sd = get_data('SBIN','2020-07-01','2020-07-25')

# sd.index.name = 'Date'
populate_heikin_ashi(sd)
persist_to_store(sd,'store/temp_1.txt')
##############################################################################

sd = read_store('store/temp_1.txt')
# sd.index.name = 'Date'
data = get_data('SBIN','2020-07-25','2020-08-03')
data = data.astype({'Date': 'datetime64[ns]'})

# data.reset_index(inplace=True)
# populate_heikin_ashi(sd)
# print(sd)
print(sd.dtypes)
print(data.dtypes)

sd = sd.append(data,ignore_index=True)
# sd.drop(columns=['index'],inplace=True)
# sd.reset_index(inplace=True,drop=True)

populate_heikin_ashi(sd,6)
 
# populate_heikin_ashi(sd,6)

# print (sd.at[1593561600000,'Date'])
# print (type(sd.at[1593561600000,'Date']))
# #  
# print (sd.at[20,'Date'])
# print (type(sd.at[20,'Date']))

print(sd)
# print(data)


