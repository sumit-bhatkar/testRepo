from datetime import datetime
from datetime import datetime
import dateutil.relativedelta
from pandas._libs.tslib import format_array_from_datetime


# to_date=datetime.now()
# to_date=datetime.strftime(to_date,'%Y,%m,%d')
# to_date=datetime.strptime(to_date,'%Y,%m,%d')
# from_date=to_date-dateutil.relativedelta.relativedelta(month=6)
#data=get_history(symbol='SBIN',start=from_date,end=to_date)
#print (from_date,"    ", type(from_date))
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