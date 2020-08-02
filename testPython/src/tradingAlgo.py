import csv
import requests
import json

CSV_URL = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_02062020.csv'

def getBhavdata():
    with requests.Session() as s:
        download = s.get(CSV_URL)
    
        decoded_content = download.content.decode('utf-8')
    
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)

#getBhavdata()
print("========= Started ============")

def testTradingView():
    from main import TA_Handler,TradingView

    handler = TA_Handler()
    handler.symbol = "SBIN"
    handler.interval = "1M" # 15 Minutes
    handler.exchange = "NSE"
    handler.screener = "india"
    
    exch_smbl = handler.exchange.upper() + ":" + handler.symbol.upper()
    data = TradingView.data(exch_smbl, handler.interval)
    
    #print ('The Request is {}'.format(data))
    
    scan_url = TradingView.scan_url + handler.screener.lower() + "/scan"
    print ('The Request is {} {}'.format(scan_url,data))
    response = requests.post(scan_url, json=data)
    result = json.loads(response.text)["data"]
    print (result)
    #analysis = handler.get_analysis()
    
    #print(analysis.summary)

testTradingView()
print("========= End ============")




