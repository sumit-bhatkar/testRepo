from datetime import datetime, date, timedelta
import dateutil.relativedelta
import pandas as pd
import json

def some_func(a,b):
    print("each row " , a,b)
    if a>17 :
        return b*5
    else :
        return b
    

today = date.today()
timedelta(days = 1)
print(today)

list = [[today - timedelta(days = 3),11, 22, 31], 
       [today - timedelta(days = 3),12, 22, 31],
       [today - timedelta(days = 3),13, 22, 31],
       [today - timedelta(days = 3),14, 22, 31],
       [today - timedelta(days = 3),15, 22, 31],
       [today - timedelta(days = 3),16, 22, 31],
       [today - timedelta(days = 3),17, 22, 31],
       [today - timedelta(days = 3),18, 22, 31],
       [today - timedelta(days = 3),19, 22, 31],
       [today - timedelta(days = 3),20, 22, 31],
       [today - timedelta(days = 2), 21, 26, 35], 
       [today - timedelta(days = 1), 22, 28, 37], 
       [today, 14, 25, 32]] 
    
df = pd.DataFrame(list, columns =['Date', 'Close', 'Low','High'], dtype = float) 

# df['diff'] = df[(df['Close'] >11 )]

df['ha'] = df.apply(lambda x: some_func(x['Close'],x['High']),axis=1)

print(df)
# print(df.tail(2)) 
# print(df.Low.head(2))






