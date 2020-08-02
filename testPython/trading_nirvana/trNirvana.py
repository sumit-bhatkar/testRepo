""" 
##########################################################################

NSE data plotting
"""
import nirvanaUtils as u
import json
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
from pandas._libs.tslib import format_array_from_datetime
from pip._internal import index

def get_data(symbol):
    print("----------------------------------------------------------")
    #plt.style.use('fivethirtyeight')
    from_date = datetime.strptime ('2020-07-10','%Y-%m-%d')
    to_date = datetime.strptime ('2020-08-01','%Y-%m-%d')
    from_date,to_date = u.get_time()
    print(from_date , "   " ,to_date)
    print("----------------------------------------------------------")
    
    #data=get_history(symbol='SBIN',start=from_date,end=to_date)
    data=get_history(symbol=symbol,start=from_date,end=to_date)
    
    #doc = data.to_json()
    #doc = data.iloc[0:5].to_json()
    #con = pd.read_json(doc,orient='columns' )
    #print(con)
    return data

def read_store ():
    print ("Reading from file")
    with open('store/data.txt') as json_file:
        json_data = json.load(json_file)
        
    data_frame = pd.read_json(json_data,orient='columns' )
    return data_frame
    
def persist_to_store (data_frame):
    json_data = data_frame.to_json()
    with open('store/data.txt', 'w') as outfile:
        json.dump(json_data, outfile)
    print("Saved to file")
    print("----------------------------------------------------------")

#sb = get_data('SBIN')
sb = read_store()
print(sb)
print("----------------------------------------------------------")
#sb = sb.drop(sb.index[0])
#persist_to_store(sb)

today = get_data('SBIN')
final = pd.concat ([sb,today[-3:-1]])
final = pd.concat ([final,today[-3:-1]])


print(final)
print("----------------------------------------------------------")
