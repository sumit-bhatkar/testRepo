import pandas as pd
import numpy as np
from pandas_datareader import data as web
import matplotlib.pyplot as plt
from pip._vendor.requests.api import head

def get_stock(stock,start,end):
 return web.DataReader(stock,'yahoo',start,end)['Close']

def get_high(stock,start,end):
 return web.DataReader(stock,'yahoo',start,end)['High']

def get_low(stock,start,end):
 tmp = web.DataReader(stock,'yahoo',start,end)['Low']
 print (tmp)
 return tmp

def STOK(close, low, high, n): 
 STOK = ((close - low.rolling(n).min() / (high.rolling(n).max() - low.rolling(n).min()) )) * 100
 return STOK

def STOD(close, low, high, n):
 STOK = ((close - low.rolling(n).min() / (high.rolling(n).max() - low.rolling(n).min()) )) * 100
 STOD = STOK.rolling(3).mean()
 return STOD

df = pd.DataFrame(get_stock('FB', '7/1/2020', '7/1/2020'))
df['High'] = get_high('FB', '7/1/2020', '7/30/2020')
df['Low'] = get_low('FB', '7/1/2020', '7/30/2020')
df['%K'] = STOK(df['Close'], df['Low'], df['High'], 14)
df['%D'] = STOD(df['Close'], df['Low'], df['High'], 14)
df.tail()

print (df['%K']) 
# df['%K'].plot()
# plt.show()




""" 
##########################################################################

NSE data plotting
from nsepy import get_history
from datetime import datetime
import dateutil.relativedelta

plt.style.use('fivethirtyeight')
to_date=datetime.now()
to_date=datetime.strftime(to_date,'%Y,%m,%d')
to_date=datetime.strptime(to_date,'%Y,%m,%d')
from_date=to_date-dateutil.relativedelta.relativedelta(month=6)
data=get_history(symbol='SBIN',start=from_date,end=to_date)
#print(data['High'])
data['Close'].plot()
#data['High'].plot()
#data['Low'].plot()

data['%K'] = STOK(data['Close'], data['Low'], data['High'], 14)
data['%D'] = STOD(data['Close'], data['Low'], data['High'], 14)
#data['%K'].plot()
print(data['High'], data['%K'])
#plt.show()
##########################################################################
"""

