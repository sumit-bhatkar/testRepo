import nirvanaUtils as nv
import json
import numpy as np
import pandas as pd

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
        'ABB',
        'JUBILANT',
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

symbol = 'CAPLIPOINT' 

def validate_stoch_rsi_flat(symbol_data,
                            flat_period = STOCK_RSI_FLAT_PERIOD, 
                            max_flat_std = STOCK_RSI_MAX_STD):
    col_name = 'flatstokrsi_{}'.format(flat_period) 
    symbol_data[col_name] = (symbol_data["Stoch_rsi_K"] - symbol_data["Stoch_rsi_D"]).abs().rolling(flat_period).std()
    symbol_data['flatstokrsi_check'] = (symbol_data[col_name] < max_flat_std) & (symbol_data["Stoch_rsi_K"] < 8)  & (symbol_data["Stoch_rsi_D"] -symbol_data["Stoch_rsi_K"] < 1)
    return symbol_data['flatstokrsi_check'].tail(1).item() , symbol_data

def get_percent_difference(current_value,base_value):
    return (current_value - base_value) / base_value * 100

def validate_ema_200_50(symbol_data, ema50_threshold = EMA_50_THRESHOLD):
    symbol_data['ema50_diff'] = get_percent_difference (
                    symbol_data['Close'] , 
                    symbol_data['ema50']
                    )
    symbol_data['ema50_check'] = symbol_data['High'] <  (symbol_data['ema50'] * 0.9)
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
    symbol_data['ttqold'] = (symbol_data['Volume'].shift(-1) / symbol_data['Trades'].shift(-1))
    symbol_data['vol_trade_check'] = ((symbol_data['ttq'] - symbol_data['ttqold'])/symbol_data['ttqold'] * 100) > 200

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
#     print("----------------------------------------------------------")    
#     print(stoch_ris_passed,ema_200_50_passed,curr_low_passed)
#     symbol = symbol_data['Symbol'].tail(1).item()
#     if stoch_ris_passed \
#         and ema_200_50_passed \
#         and curr_low_passed :
#             print ('BUY - {} : Close {} , 3 month Low {}'.format(symbol,symbol_data['Close'].tail(1).item(),lowest_low_value))
#             return True
#     else:
#             print ('DO NOT BUY - {}'.format(symbol))
#             return False
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
    print('--------------------------------------------------------------------')
    profit = symbol_data.loc[365:,['profit']].sum().item()
    s = symbol_data.loc[365:,['success']].sum().item()
    f = symbol_data.loc[365:,['fail']].sum().item()
    sp = s/(s+f)*100
    print('Total earnings = {}'.format(profit))
    print('Success ratio  = {}'.format(sp))
#     persist_to_store() ## this is for web display 
    nv.persist_excel_to_store(symbol_data,'store/study/{}.xlsx'.format(name))
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
        if row['sale_t'] < row['future_max'] :
            result = row['sale_t'] - row['buy'] 
        else :
            result = row['sale_l'] - row['buy'] 
        return result
    def get_s(row):
        if row['sale_t'] < row['future_max'] :
            return 1 
        else :
            return 0

    symbol_data['profit'] = symbol_data.apply(lambda row : get_profit(row), axis=1) 
    symbol_data['success'] = symbol_data.apply(lambda row : get_s(row), axis=1)
    symbol_data['fail'] = symbol_data.apply(lambda row : 0 if get_s(row) == 1 else 1, axis=1)


#     if (symbol_data['sale_t'] < max) :
#         symbol_data['profit']
#             
#     symbol_data['profit'] =  if symbol_data['sale_t'] < max
#     print(symbol_data)
#     rolling(xx,closed='left') == for future window 

    proc_result_func(name,symbol_data)
    return symbol_data



''' Start all your main processing here [for windows]'''
if __name__ == '__main__':
    print("-------------------- Start of Nirvana-v1.0 ---------------------------")
    
    # screen_from_bhavcopy_and_predict()
    
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = executor.map(study_strategy_for_stock, list_of_stocks)
    
    for symbol in list_of_stocks :
        study_strategy_for_stock(symbol)
    
    
    
    # print(bd1)
    # print(st['NO_OF_TRADES_x'])
    # print(st['NO_OF_TRADES_y'])
    # nv.persist_csv_to_store(st,'store/merge.csv')
# print("----------------------------------------------------------")    

print("-------------------- Nirvana Achieved ---------------------------")


            



