import MetaTrader5 as mt
import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime, timedelta
Login = 
Password = ''
Server = ''

mt.initialize()
mt.login(Login, Password, Server)

# def bot():
while True:
    print('RUNNING.......the bot()-----------')
    candle_data = mt.copy_rates_from_pos('XAUUSDm', mt.TIMEFRAME_M5, 0, 1000)
    
    data_df = pd.DataFrame(candle_data)
    data_df['date']=pd.to_datetime(data_df['time'],unit='s')
    data_df=data_df[['date','open','high','low','close','tick_volume']]
    data_df.set_index('date',inplace=True)
    data_df['vwap']=ta.vwap(data_df['high'],data_df['low'],data_df['close'],data_df['tick_volume'])
    
    data_df['ema_10'] = ta.ema(data_df['close'],10)
    data_df['ema_5'] = ta.ema(data_df['close'],1)
    # print(data_df)
    # time.sleep(20)
    current_vwap=data_df.iloc[-1,:]['vwap']
    current_5ema=data_df.iloc[-1,:]['ema_5']
    current_10ema=data_df.iloc[-1,:]['ema_10']
    
    his = mt.history_orders_get(
                datetime.now()-timedelta(days=3),
                datetime.now()
            )

    df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling', 'state','magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'sl/tp_price', 'sl', 'tp', 'entry_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
    df = df[['time_done','ticket', 'volume_ini', 'entry_price',
                'comment', 'sl/tp_price', 'SYMBOL','type']]
    df['time_done']=pd.to_datetime(df['time_done'],unit='s')
    # print(df)
    # print(df.iloc[-1,:]['time_done'])
    # time.sleep(9)
    for i in range(1, 50):
        if df.iloc[-i, :]['SYMBOL'] == 'XAUUSDm':
            result = df.iloc[-i, :]
            # print(result)
            # time.sleep(20)
            break
        else:
            pass
    try:
        vol = result['volume_ini']
    except Exception as e:
        print(e)
    time_done_str =str( result['time_done'])

# Convert the string to a datetime object
    time_done = datetime.strptime(time_done_str, "%Y-%m-%d %H:%M:%S")

    # Extract the date portion
    date_only = time_done.date()
    if result['comment'][1]+result['comment'][2] == 'tp' and date_only == datetime.now().date():
        print(" ")
        print(' --------------- DONE WITH TODAY S PROFIT MAANNN --------------------------------------- <<<<<<<<<<<')
        exit()
    
    pos_count=open('positive_count.txt','r')                # using file logic for storing the count values so that in one crossover only one order should go....
    positive_counter=pos_count.read()
    # print(positive_counter)
    pos_count.close()
    
    neg_count=open('negative_count.txt','r')                # using file logic for storing the count values so that in one crossover only one order should go....
    negative_counter=neg_count.read()
    # print(negative_counter)
    neg_count.close()
    # time.sleep(20)
    pos=mt.positions_get(symbol='XAUUSDm')
        
    if  pos==() and current_5ema > current_vwap and positive_counter == '0'  and result['comment'][1]+result['comment'][2] == 'tp':
        # print('entering in logic1')        
        pr = mt.symbol_info_tick('XAUUSDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'XAUUSDm',
            "volume": 0.2,
            "type": mt.ORDER_TYPE_BUY,
            "price": pr,
            "sl": pr-0.5,
            "tp": pr + 0.1,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info=mt.positions_get(symbol='XAUUSDm')
        if new_info!=():
            entry = new_info[0].price_open
            ticket = new_info[0].ticket
            req = {
                "action": mt.TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": entry-0.5,
                "tp":entry+0.1
                }
            od=mt.order_send(req)
            print(od)
            file=open('negative_count.txt','w')
            file.write('0')
            file.close()
            
            file1=open('positive_count.txt','w')
            file1.write('1')
            file1.close()
        else:
            print('NO POSITIONS')
    
        # print('entering in logic2')
    elif pos==() and current_5ema > current_vwap and positive_counter == '0'   and  result['comment'][1]+result['comment'][2] == 'sl':
        pr = mt.symbol_info_tick('XAUUSDm').ask                     # sending the double quantity bcz sl < entry i.e SL hit
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'XAUUSDm',
            "volume": vol*2,
            "type": mt.ORDER_TYPE_BUY,
            "price": pr,
            "sl": pr-0.5,
            "tp": pr + 0.5,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info=mt.positions_get(symbol='XAUUSDm')
        if new_info!=():
            entry = new_info[0].price_open
            ticket = new_info[0].ticket
            req = {
                "action": mt.TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": entry-0.5,
                "tp":entry+0.5
                }
            od=mt.order_send(req)
            print(od)
            file=open('negative_count.txt','w')
            file.write('0')
            file.close()
            
            file1=open('positive_count.txt','w')
            file1.write('1')
            file1.close()
        else:
            print('NO POSITIONS')
    
    
    elif  pos==() and  current_5ema < current_vwap and negative_counter=='0' and result['comment'][1]+result['comment'][2] == 'tp':
        # print('entering in logic6')
        pr = mt.symbol_info_tick('XAUUSDm').bid
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'XAUUSDm',
            "volume": 0.2,
            "type": mt.ORDER_TYPE_SELL,
            "price": pr,
            "sl": pr+0.5,
            "tp": pr - 0.1,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info=mt.positions_get(symbol='XAUUSDm')
        if new_info!=():
            entry = new_info[0].price_open
            ticket = new_info[0].ticket
            req = {
                "action": mt.TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": entry+0.5,
                "tp":entry-0.1
                }
            od=mt.order_send(req)
            print(od)
            file=open('negative_count.txt','w')
            file.write('1')
            file.close()
            
            file1=open('positive_count.txt','w')
            file1.write('0')
            file1.close()
        else:
            print('NO POSITIONS')
    
        # print('entering in logic7')
    elif pos==() and current_5ema < current_vwap   and negative_counter=='0' and   result['comment'][1]+result['comment'][2] == 'sl':
        pr = mt.symbol_info_tick('XAUUSDm').bid
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'XAUUSDm',
            "volume": vol*2,
            "type": mt.ORDER_TYPE_SELL,
            "price": pr,
            "sl": pr+0.5,
            "tp": pr - 0.5,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info=mt.positions_get(symbol='XAUUSDm')
        if new_info!=():
            entry = new_info[0].price_open
            ticket = new_info[0].ticket
            req = {
                "action": mt.TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": entry+0.5,
                "tp":entry-0.5
                }
            od=mt.order_send(req)
            print(od)
            file=open('negative_count.txt','w')
            file.write('1')
            file.close()
            
            file1=open('positive_count.txt','w')
            file1.write('0')
            file1.close()
        else:
            print('NO POSITIONS')
    
    
    else:
        print('NO CONDITIONS---')

# while True:
#     bot()