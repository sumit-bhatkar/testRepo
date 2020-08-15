STOCK_RSI_FLAT_PERIOD = 4
STOCK_RSI_MAX_STD = 1 ## change to 2
LOWEST_LOW_PERIOD = 90
MAX_CURR_LOW_DIFF = 10
EMA_50_THRESHOLD = 10

''' Screening Thresholds '''
TTQ_CHANGE_THRESHOLD = 100
TO_CHANGE_THRESHOLD = 200
DEL_PERCENT_THRESHOLD = 20

def validate_stoch_rsi_flat(sd,
                            flat_period = STOCK_RSI_FLAT_PERIOD, 
                            max_flat_std = STOCK_RSI_MAX_STD):
    col_name = 'flatstokrsi_{}'.format(flat_period) 
    sd[col_name] = (sd["Stoch_rsi_K"].shift(1) - sd["Stoch_rsi_D"].shift(1)).abs().rolling(flat_period).std()
    sd['stokrsi_check'] = (sd[col_name] < max_flat_std) & (sd["Stoch_rsi_K"].shift(1) < 8)  & (sd["Stoch_rsi_D"].shift(1) -sd["Stoch_rsi_K"].shift(1) < 1)
    return sd['stokrsi_check'].tail(1).item() , sd

def get_percent_difference(current_value,base_value):
    return (current_value - base_value) / base_value * 100

def validate_ema_200_50(sd, ema50_threshold = EMA_50_THRESHOLD):
#     sd['ema50_diff'] = get_percent_difference (
#                     sd['Close'] , 
#                     sd['ema50']
#                     )
    sd['ema50_99'] = sd['ema50'] * 0.99
    sd['ema50_check'] = sd['High'] <  (sd['ema50'] * 0.99)
    return sd['ema50_check'].tail(1).item() , sd

def validate_curr_low(sd,
                      low_period = LOWEST_LOW_PERIOD, 
                      diff_thr = MAX_CURR_LOW_DIFF):
    sd['lowest_low'] = sd['Low'].rolling(low_period).min()
    ## used sd.percent_difference as I don't want to store it
    sd.per_diff =  get_percent_difference(sd['Low'], sd['lowest_low']).abs()
    sd['lowest_low_check'] = sd.per_diff < diff_thr
    return sd['lowest_low_check'].tail(1).item() , sd

def validate_delivery_percent(sd,
                            max_flat_std = STOCK_RSI_MAX_STD):
    sd['deliv_check'] = (sd['%Deliverble'] *100 ) > 30
    return sd['deliv_check'].tail(1).item() , sd

def validate_vol_per_trade(sd,
                            max_flat_std = STOCK_RSI_MAX_STD):
    sd['ttq'] = (sd['Volume'] / sd['Trades'])
    sd['ttqold'] = (sd['Volume'].shift(1) / sd['Trades'].shift(1))
    sd['vol_trade_check'] = ((sd['ttq'] - sd['ttqold'])/sd['ttqold'] * 100) > 100

    return sd['vol_trade_check'].tail(1).item() , sd

def validate_turnover(sd,
                            max_flat_std = STOCK_RSI_MAX_STD):
    sd['turnover_check'] = ((sd['Turnover'] - sd['Turnover'].shift(-1))/sd['Turnover'].shift(-1) * 100) > 200

    return sd['turnover_check'].tail(1).item() , sd

'''======================================================================================='''
def get_signal_using_strategy_1(sd):
    stoch_ris_passed,sd = validate_stoch_rsi_flat(sd)
    ema_200_50_passed,sd = validate_ema_200_50(sd)
    curr_low_passed , sd = validate_curr_low(sd)
    lowest_low_value = sd.lowest_low.tail(1).item()
    delivery_percent_pass , sd  = validate_delivery_percent(sd)
    vol_per_trade_pass , sd  = validate_vol_per_trade(sd)
    turnover_pass , sd  = validate_turnover(sd)
    
    sd['signal_st1'] = (sd['stokrsi_check']) &  \
                                (sd['ema50_check']) & \
                                (sd['lowest_low_check']) 
#                                 (sd['deliv_check']) &\
#                                 (sd['vol_trade_check']) &\
#                                 (sd['turnover_check'])
    return sd

'''======================================================================================='''

def get_buy_price_strategy_1(sd):
    ## return value increased by 2% of close
    sd['buy'] = sd['Close'] * 1.01 
    return sd

def get_sell_price_strategy_1(sd):
    ## target and stoploss
    sd['sale_t'] = sd['Close'] * 1.15 
    sd['sale_l'] = sd['Close'] * 0.97
    return sd