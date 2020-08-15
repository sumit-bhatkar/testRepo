import nirvanaUtils as nv
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

list_of_stocks = [ 
#         'TITAN',
#         'BEL',
#         'BANDHANBNK',
#         'BLUESTARCO',
#         'AXISBANK',
#         'THERMAX',
        'KPRMILL',
#         'JUBILANT',
#         'JBMA',
        ]

STOCK_RSI_FLAT_PERIOD = 4
STOCK_RSI_MAX_STD = 1 ## change to 2
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 10
EMA_50_THRESHOLD = 10

''' Screening Thresholds '''
TTQ_CHANGE_THRESHOLD = 100
TO_CHANGE_THRESHOLD = 200
DEL_PERCENT_THRESHOLD = 20

def validate_stoch_rsi_flat(symbol_data,
                            flat_period = STOCK_RSI_FLAT_PERIOD, 
                            max_flat_std = STOCK_RSI_MAX_STD):
    col_name = 'flatstokrsi_{}'.format(flat_period) 
    symbol_data[col_name] = (symbol_data["Stoch_rsi_K"].shift(1) - symbol_data["Stoch_rsi_D"].shift(1)).abs().rolling(flat_period).std()
    symbol_data['flatstokrsi_check'] = (symbol_data[col_name] < max_flat_std) & (symbol_data["Stoch_rsi_K"].shift(1) < 8)  & (symbol_data["Stoch_rsi_D"].shift(1) -symbol_data["Stoch_rsi_K"].shift(1) < 1)
    return symbol_data['flatstokrsi_check'].tail(1).item() , symbol_data

def get_percent_difference(current_value,base_value):
    return (current_value - base_value) / base_value * 100

def validate_ema_200_50(symbol_data, ema50_threshold = EMA_50_THRESHOLD):
#     symbol_data['ema50_diff'] = get_percent_difference (
#                     symbol_data['Close'] , 
#                     symbol_data['ema50']
#                     )
    symbol_data['ema50_99'] = symbol_data['ema50'] * 0.99
    symbol_data['ema50_check'] = symbol_data['High'] <  (symbol_data['ema50'] * 0.99)
    return symbol_data['ema50_check'].tail(1).item() , symbol_data

def validate_curr_low(symbol_data,
                      low_period = LOWEST_LOW_PERIOD, 
                      diff_thr = MAX_CURR_LOW_DIFF):
    symbol_data['lowest_low'] = symbol_data['Low'].rolling(low_period).min()
    ## used symbol_data.percent_difference as I don't want to store it
    symbol_data.per_diff =  get_percent_difference(symbol_data['Low'], symbol_data['lowest_low']).abs()
    symbol_data['lowest_low_check'] = symbol_data.per_diff < diff_thr
    return symbol_data['lowest_low_check'].tail(1).item() , symbol_data

def validate_delivery_percent(symbol_data,
                            max_flat_std = STOCK_RSI_MAX_STD):
    symbol_data['deliv_check'] = (symbol_data['%Deliverble'] *100 ) > 30
    return symbol_data['deliv_check'].tail(1).item() , symbol_data

def validate_vol_per_trade(symbol_data,
                            max_flat_std = STOCK_RSI_MAX_STD):
    symbol_data['ttq'] = (symbol_data['Volume'] / symbol_data['Trades'])
    symbol_data['ttqold'] = (symbol_data['Volume'].shift(1) / symbol_data['Trades'].shift(1))
    symbol_data['vol_trade_check'] = ((symbol_data['ttq'] - symbol_data['ttqold'])/symbol_data['ttqold'] * 100) > 100

    return symbol_data['vol_trade_check'].tail(1).item() , symbol_data

def validate_turnover(symbol_data,
                            max_flat_std = STOCK_RSI_MAX_STD):
    symbol_data['turnover_check'] = ((symbol_data['Turnover'] - symbol_data['Turnover'].shift(-1))/symbol_data['Turnover'].shift(-1) * 100) > 200

    return symbol_data['turnover_check'].tail(1).item() , symbol_data

def get_signal_using_strategy_1(symbol_data):
    stoch_ris_passed,symbol_data = validate_stoch_rsi_flat(symbol_data)
    ema_200_50_passed,symbol_data = validate_ema_200_50(symbol_data)
    curr_low_passed , symbol_data = validate_curr_low(symbol_data)
    lowest_low_value = symbol_data.lowest_low.tail(1).item()
    delivery_percent_pass , symbol_data  = validate_delivery_percent(symbol_data)
    vol_per_trade_pass , symbol_data  = validate_vol_per_trade(symbol_data)
    turnover_pass , symbol_data  = validate_turnover(symbol_data)
    
#     symbol_data['signal_st1'] = (symbol_data['flatstokrsi_check']) &  \
#                                 (symbol_data['ema50_check']) & \
#                                 (symbol_data['lowest_low_check']) &\
#                                 (symbol_data['deliv_check']) &\
#                                 (symbol_data['vol_trade_check']) &\
#                                 (symbol_data['turnover_check'])
    symbol_data['signal_st1'] = (symbol_data['flatstokrsi_check']) &  \
                                (symbol_data['ema50_check']) & \
                                (symbol_data['lowest_low_check']) 
#                                 (symbol_data['deliv_check']) &\
#                                 (symbol_data['vol_trade_check']) &\
#                                 (symbol_data['turnover_check'])
    return symbol_data

def fetch_data_for_symbol(symbol):
    store_path = 'store/DB/01012016_{}.json'.format(symbol)
    symbol_data = nv.read_store(store_path)
    return symbol_data

def get_buy_price_strategy_1(symbol_data):
    ## return value increased by 2% of close
    symbol_data['buy'] = symbol_data['Close'] * 1.01 
    return symbol_data

def get_sell_price_strategy_1(symbol_data):
    ## target and stoploss
    symbol_data['sale_t'] = symbol_data['Close'] * 1.15 
    symbol_data['sale_l'] = symbol_data['Close'] * 0.97
    return symbol_data

def screen_strategy_test(st):
    test_stocks = [ 
            'TATAMOTORS',
            'RELIANCE',
            'BANDHANBNK',
            'LAURUSLABS',
            'HDFCBANK',
            'SBIN'
        ]
def process_result_format_1(name,symbol_data):
#     print('--------------------------------------------------------------------')
#     print( symbol_data[symbol_data.signal_st1].loc[365:,['flatstokrsi_check','success','fail','profit']].sum())
    list_to_save =['KPRMILL'
                   ]
    if (symbol_data.loc[0,'Symbol'] in lst.list_of_100_results) :
        nv.persist_excel_to_store(symbol_data,'store/study/{}.xlsx'.format(name))
    print(name)
    nv.persist_excel_to_store(symbol_data,'store/study/{}_1.xlsx'.format(name))
    return symbol_data
                             
def study_strategy_for_stock(symbol, 
                             strategy_func = get_signal_using_strategy_1, 
                             buy_strat_func = get_buy_price_strategy_1, 
                             sale_strat_func = get_sell_price_strategy_1, 
                             proc_result_func = process_result_format_1
                             ):
    hold_period = 90
    name = f'{symbol}_strat_1_study'
    symbol_data = fetch_data_for_symbol(symbol)
    symbol_data = strategy_func(symbol_data)
    symbol_data = buy_strat_func(symbol_data)
    symbol_data = sale_strat_func(symbol_data)
    symbol_data['future_max'] = symbol_data['High'].rolling(hold_period, min_periods=1).max().shift(0-hold_period)
    
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

    symbol_data['profit'] = symbol_data.apply(lambda row : get_profit(row), axis=1) 
    symbol_data['success'] = symbol_data.apply(lambda row : get_s(row), axis=1)
    symbol_data['fail'] = symbol_data.apply(lambda row : 0 if get_s(row) == 1 else 1, axis=1)

    proc_result_func(name,symbol_data)
    return symbol_data



''' Start all your main processing here [for windows]'''
if __name__ == '__main__':
    print("-------------------- Start of Nirvana-v1.0 ---------------------------")
    
    start = time.perf_counter()
#     screen_from_bhavcopy_and_predict()
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = executor.map(study_strategy_for_stock, list_of_stocks)
    summary = pd.DataFrame(columns=['Symbol','Signal', 'success','fail',
                                    'profit','Hit_Rate',
                                    'flatstokrsi_check',
                                    'ema50_check','lowest_low_check',
                                    'vol_trade_check','deliv_check','turnover_check',
                                    ])
    summary[['Symbol']] = summary[['Symbol']].astype('string')
#     for symbol in lst.list_of_stocks :
    for symbol in list_of_stocks :
        try :
            symbol_data = study_strategy_for_stock(symbol)
        except Exception as e: 
            print(e)
            print("Oops! Error occurred.")
            continue
        
        tail=summary.__len__()
        summary.at[tail,'Symbol'] = symbol
        summary.at[tail,'Signal'] \
            = symbol_data.loc[365:,'signal_st1'].sum()
        summary.at[tail,'flatstokrsi_check'] \
            = symbol_data.loc[365:,'flatstokrsi_check'].sum()
        summary.at[tail,'ema50_check'] \
            = symbol_data.loc[365:,'ema50_check'].sum()
        summary.at[tail,'lowest_low_check'] \
            = symbol_data.loc[365:,'lowest_low_check'].sum()
        summary.at[tail,'vol_trade_check'] \
            = symbol_data.loc[365:,'vol_trade_check'].sum()            
        summary.at[tail,'turnover_check'] \
            = symbol_data.loc[365:,'turnover_check'].sum()
        summary.at[tail,'deliv_check'] \
            = symbol_data.loc[365:,'deliv_check'].sum()                                    
        summary.at[tail,'profit'] \
            = symbol_data[symbol_data.signal_st1].loc[365:,'profit'].sum()
        summary.at[tail,'success'] \
            = symbol_data[symbol_data.signal_st1].loc[365:,'success'].sum()
        summary.at[tail,'fail'] \
            = symbol_data[symbol_data.signal_st1].loc[365:,'fail'].sum()
        summary.at[tail,'Hit_Rate'] \
            = summary.at[tail,'success'] / (summary.at[tail,'success'] + summary.at[tail,'fail'] ) 

    writer = pd.ExcelWriter("store/study/Summary_Strategy_1.xlsx",
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
    
    # Set the column width and format.
    worksheet.set_column('F:F', None, format1)
    
    # Set the format but not the column width.
    worksheet.set_column('G:G', None, format2)
    worksheet.conditional_format('G2:G2000', {'type': '3_color_scale'})
    worksheet.autofilter('A1:XX1')
    writer.save()
#     nv.persist_excel_to_store(summary,'store/study/Summary_Strategy_1.xlsx')
    print(summary)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
    # print(bd1)
    # print(st['NO_OF_TRADES_x'])
    # print(st['NO_OF_TRADES_y'])
    # nv.persist_csv_to_store(st,'store/merge.csv')
# print("----------------------------------------------------------")    

print("-------------------- Nirvana Achieved ---------------------------")


            



