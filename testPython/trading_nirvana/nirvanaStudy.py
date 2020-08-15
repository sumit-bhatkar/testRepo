import nirvanaUtils as nv
import validations as v
import list_of_all_stocks as lst
import json
import numpy as np
import pandas as pd
import xlsxwriter

from datetime import datetime, date, timedelta
import dateutil.relativedelta
from nsepy import get_history

from multiprocessing import Pool    
import concurrent.futures
import time

def fetch_data_for_symbol(symbol):
    store_path = 'store/DB/01012016_{}.json'.format(symbol)
    sd = nv.read_store(store_path)
    return sd

def process_result_format_1(name,sd):
    if (sd.loc[0,'Symbol'] in lst.list_of_100_results) :
        nv.persist_excel_to_store(sd,'store/study/{}.xlsx'.format(name))
    return sd

def process_result_format_2(name,sd):
#     if (sd.loc[0,'Symbol'] in ['KPRMILL']) :
#         print(sd[sd.Date.between('2020-05-01', '2020-05-20')])
    print(sd[sd.Date.between('2020-05-01', '2020-05-20')][
                                                            {'Date',
                                                            'Close'}
                                                            ])
    return sd
                             
def study_strategy_for_stock(symbol, 
                             strategy_func = v.get_signal_using_strategy_1, 
                             buy_strat_func = v.get_buy_price_strategy_1, 
                             sale_strat_func = v.get_sell_price_strategy_1, 
                             proc_result_func = process_result_format_2
                             ):
    hold_period = 90
    name = f'{symbol}_strat_1_study'
    sd = fetch_data_for_symbol(symbol)
    sd = strategy_func(sd)
    sd = buy_strat_func(sd)
    sd = sale_strat_func(sd)
    sd['future_max'] = sd['High'].rolling(hold_period, min_periods=1).max().shift(0-hold_period)
    
    def get_profit(row):
        if row['sale_t'] <= row['future_max']  and row['signal_st1']:
            result = row['sale_t'] - row['buy'] 
        elif row['sale_t'] > row['future_max']  and row['signal_st1']:
            result = row['sale_l'] - row['buy'] 
        else :
            result = 0
        return result
    def get_s(row):
        if row['sale_t'] < row['future_max'] :
            return 1 
        else :
            return 0

    sd['profit'] = sd.apply(lambda row : get_profit(row), axis=1) 
    sd['success'] = sd.apply(lambda row : get_s(row), axis=1)
    sd['fail'] = sd.apply(lambda row : 0 if get_s(row) == 1 else 1, axis=1)

    proc_result_func(name,sd)
    return sd

def write_summary_excel(summary):
    writer = pd.ExcelWriter(f"store/study/Summary_Strategy_1_{datetime.strftime(datetime.now(),'%Y%m%d_%H%M%S')}.xlsx",
                        engine='xlsxwriter',
                        datetime_format='dd-mm-yy hh:mm:ss',
                        date_format='dd-mm-yy')
    summary.to_excel(writer, sheet_name='Summary')
    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Summary']
    # Add some cell formats.
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    format2 = workbook.add_format({'num_format': '0%'})
    worksheet.set_column('F:F', None, format1)
    worksheet.set_column('G:G', None, format2)
    worksheet.conditional_format('G2:G2000', {'type': '3_color_scale'})
    worksheet.autofilter('A1:XX1')
    writer.save()
    
print("-------------------- Start of Nirvana-v1.0 ---------------------------")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)
    
start = time.perf_counter()
summary = pd.DataFrame(columns=['Symbol','Signal', 'success','fail',
                                'profit','Hit_Rate',
                                'stokrsi_check',
                                'ema50_check','lowest_low_check',
                                'vol_trade_check','deliv_check','turnover_check',
                                ])
summary[['Symbol']] = summary[['Symbol']].astype('string')
#     for symbol in lst.list_of_stocks :
for symbol in ['KPRMILL'] :
    try :
        sd = study_strategy_for_stock(symbol)
    except Exception as e: 
        print(e)
        print("Oops! Error occurred.")
        continue
    
    tail=summary.__len__()
    summary.at[tail,'Symbol'] = symbol
    summary.at[tail,'Signal']           = sd.loc[365:,'signal_st1'].sum()
    summary.at[tail,'stokrsi_check']    = sd.loc[365:,'stokrsi_check'].sum()
    summary.at[tail,'ema50_check']      = sd.loc[365:,'ema50_check'].sum()
    summary.at[tail,'lowest_low_check'] = sd.loc[365:,'lowest_low_check'].sum()
    summary.at[tail,'vol_trade_check']  = sd.loc[365:,'vol_trade_check'].sum()            
    summary.at[tail,'turnover_check']   = sd.loc[365:,'turnover_check'].sum()
    summary.at[tail,'deliv_check']      = sd.loc[365:,'deliv_check'].sum()                                    
    summary.at[tail,'profit']           = sd[sd.signal_st1].loc[365:,'profit'].sum()
    summary.at[tail,'success']          = sd[sd.signal_st1].loc[365:,'success'].sum()
    summary.at[tail,'fail']             = sd[sd.signal_st1].loc[365:,'fail'].sum()
    summary.at[tail,'Hit_Rate']         = summary.at[tail,'success'] / (summary.at[tail,'success'] + summary.at[tail,'fail'] ) 

# write_summary_excel(summary)
print()
print(summary)
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')

# print("----------------------------------------------------------")    

print("-------------------- Nirvana Achieved ---------------------------")


            



