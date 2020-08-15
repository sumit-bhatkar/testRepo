from datetime import datetime, date, timedelta

print("----------------------------------------------------------")
to_date=datetime.now()
print(type(to_date))
print(to_date)
to_date=datetime.strftime(to_date,'%Y,%m,%d')
print(type(to_date))
print(to_date)
to_date=datetime.strptime(to_date,'%Y,%m,%d')
print(type(to_date))
print(to_date)

today = date.today()
# start_day = (symbol_data['Date'].tail(1).item()) + timedelta(days = 1)
# print(type(start_day) , "  ",start_day)

start_day = date.today() - timedelta(days = 10)
print(type(start_day) , "  ",start_day)
print("----------------------------------------------------------")
