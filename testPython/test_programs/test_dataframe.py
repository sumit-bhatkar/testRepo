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

list1 = [
       ['test11',11, 21, 31], 
       ['test12',12, 22, 32],
       ['test13',13, 23, 33],
       ['test14',14, 24, 34],
       ['test15',15, 25, 35],
       ['test16',16, 26, 36],
       ['test17',17, 27, 37],
       ['test18',18, 28, 38],
       ['test19',19, 29, 39],
       ['test19',39, 59, 99],
       ['test10',10, 20, 30]]

list2 = [
       ['test11',41, 21, 31], 
       ['test15',45, 25, 35],
       ['test16',46, 26, 36],
       ['test14',44, 24, 34],
       ['test12',42, 22, 32],
       ['test13',43, 23, 33],
       ['test19',49, 29, 39],
       ['test19',79, 99, 39],
       ['test18',48, 28, 38],
       ['test20',20, 70, 88]]

list2 = [
       ['EQ',41, 21, 31], 
       [' EQ',45, 25, 35],
       ['EQ ',46, 26, 36],
       [' L12',44, 24, 34],
       ['PP',44, 24, 34],
       ['PEQ',44, 24, 34],
       ['BE',20, 70, 88]]           
df1 = pd.DataFrame(list1, columns =['Date', 'Close', 'Low','High'], dtype = float)
df2 = pd.DataFrame(list2, columns =['Date', 'Close', 'Low','High'], dtype = float)  

# df = pd.concat([df1, df2], axis=1, sort=True)
df = pd.merge(df1, df2, how='outer', on=['Date', 'Date'])
# df['diff'] = df[(df['Close'] >11 )]

# df['ha'] = df.apply(lambda x: some_func(x['Close'],x['High']),axis=1)

print(df1)
# print(df2)
print(df2 [df2['Date'].str.contains('|'.join(["EQ","BE"]) )])
# print(df)
# print(df.tail(2)) 
# print(df.Low.head(2))

    




