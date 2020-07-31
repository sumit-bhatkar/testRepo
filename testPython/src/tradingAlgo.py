import csv
import requests

CSV_URL = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_02062020.csv'

def getBhavdata():
    with requests.Session() as s:
        download = s.get(CSV_URL)
    
        decoded_content = download.content.decode('utf-8')
    
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)


getBhavdata()
print("=====================")