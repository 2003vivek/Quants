import MetaTrader5 as mt
import pandas as pd
import time
import pandas_ta as ta
from datetime import datetime, timedelta

Login=YOUR_INTEGER_LOGIN_NUMBER

Password = 'YOUR_PASSWORD'
Server = 'YOUR_SERVER'


mt.initialize()
mt.login(Login,Password, Server)

# # BEGINNING


def bot():
    last_entry_price=0
    sl_price=0
    candle_data = mt.copy_rates_from_pos('XAUUSDm', mt.TIMEFRAME_D1, 0, 1000)   # getting the candle data
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)                                         # creating a pandas dataframes for data arrangement
    data_df = data_df.drop([ 'spread', 'real_volume'], axis=1)
    data_df['date'] = pd.to_datetime(data_df['time'], unit='s')
    data_df = data_df[['date','open', 'high', 'low', 'close', 'tick_volume']] # computing the previous bars data!!
    data_df.set_index('date', inplace=True)
    # print(data_df)
    current_close=data_df.iloc[-1,:]['close']
    # previous_close=data_df.iloc[-2,:]['close']
    # previous_to_previous_close=data_df.iloc[-3,:]['close']
    
    his = mt.history_orders_get(
        datetime.now()-timedelta(days=20),                               # FETCHING THE HISTORY OF ORDERS
        datetime.now()
        )                      # FETCHING POSITIONS
    # print(his)

    df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling', 'state',
                        'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'sl/tp_price', 'sl', 'tp', 'entry_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
    df = df[['ticket', 'volume_ini', 'entry_price',
                'comment', 'sl/tp_price', 'SYMBOL','type']]
    # print(df)

    for i in range(1, 50):
        if df.iloc[-i, :]['SYMBOL'] == 'XAUUSDm':
            result = df.iloc[-i, :]
            break
        else:
            pass
    # print(result)
    
    for k in range(1, 50):
        if df.iloc[-k, :]['SYMBOL'] == 'XAUUSDm' and df.iloc[-k, :]['comment'][0] + df.iloc[-k, :]['comment'][1] == 'py':           # Checking the entry price of last order in a shuffled history
            last_entry_price = df.iloc[-k, :]['entry_price']
            pos_type=df.iloc[-k,:]['type']
            # print(pos_type)
            # time.sleep(20)
            break
        # elif df.iloc[-k, :]['SYMBOL'] == 'XAUUSDm' and df.iloc[-k, :]['comment'][1]+df.iloc[-k, :]['comment'][2] == 'tp':
        #     break
        
    for i in range(1, 50):
        if df.iloc[-i, :]['SYMBOL'] == 'XAUUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'sl':      # Checking the stop loss price of the last order
            sl_price=df.iloc[-i, :]['sl/tp_price']
            volume=df.iloc[-i,:]['volume_ini']
            break
        # elif df.iloc[-i, :]['SYMBOL'] == 'XAUUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'tp':
        #     break
    position = mt.positions_get(symbol='XAUUSDm')
    # print(volume)
    # BEGINNING OF LOGICS...........................
    if position==() and result['comment'][1]+result['comment'][2]=='tp' and current_close+0.5 > max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']):
        print('place buy order')
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').ask                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_BUY,                                                # placing sell order
                "price": pr,
                "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                "tp":pr+10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='tp' and current_close-0.5 < min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']):
        print('it should go as sell')
        
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').bid                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
                "price": pr,
                "sl": max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                "tp":pr-10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl":max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==0 and sl_price < last_entry_price and current_close-0.5 < min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']):
        print('double volume should go in sell ... ')
        iterative_vol=(volume*2)/0.02
        
        for i in range(int(iterative_vol)):
            pr = mt.symbol_info_tick('XAUUSDm').bid                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.02,
                "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
                "price": pr,
                "sl": max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                "tp":pr-10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl":max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==0 and sl_price < last_entry_price and current_close+0.5> max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']):
        print(' double volume place buy order')
        iterative_vol=(volume*2)/0.02
        for i in range(int(iterative_vol)):
            pr = mt.symbol_info_tick('XAUUSDm').ask                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.02,
                "type": mt.ORDER_TYPE_BUY,                                                # placing sell order
                "price": pr,
                "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                "tp":pr+10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==1 and sl_price > last_entry_price and current_close-0.5 < min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']):
        print('double volume should go sell side ... ')
        iterative_vol=(volume*2)/0.02
        # print(iterative_vol)
        for i in range(int(iterative_vol)):
            pr = mt.symbol_info_tick('XAUUSDm').bid                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.02,
                "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
                "price": pr,
                "sl": max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                "tp":pr-10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl":max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==1 and sl_price > last_entry_price and current_close+0.5> max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']):
        print(' double volume place buy order')
        iterative_vol=(volume*2)/0.02
        for i in range(int(iterative_vol)):
            pr = mt.symbol_info_tick('XAUUSDm').ask                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.02,
                "type": mt.ORDER_TYPE_BUY,                                                # placing sell order
                "price": pr,
                "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                "tp":pr+10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==0 and sl_price > last_entry_price and current_close-0.5  < min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']):
        print('base volume should go sell side... ')
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').bid                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
                "price": pr,
                "sl": max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                "tp":pr-10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl":max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==0 and sl_price > last_entry_price and current_close+0.5 > max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']):
        print(' base volume place buy order')
        
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').ask                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_BUY,                                                # placing sell order
                "price": pr,
                "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                "tp":pr+10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==1 and sl_price < last_entry_price and current_close-0.5 < min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']):
        print('base volume should go sell side... ')
        
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').bid                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
                "price": pr,
                "sl": max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                "tp":pr-10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl":max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    elif position==() and result['comment'][1]+result['comment'][2]=='sl' and pos_type==1 and sl_price < last_entry_price and current_close+0.5 > max(data_df.iloc[-2,:]['high'],data_df.iloc[-3,:]['high']):
        print(' base volume place buy order')
        
        for i in range(2):
            pr = mt.symbol_info_tick('XAUUSDm').ask                                              
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "symbol": 'XAUUSDm',
                "volume": 0.01,
                "type": mt.ORDER_TYPE_BUY,                                                # placing sell order
                "price": pr,
                "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                "tp":pr+10,
                "deviation": 5,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt.ORDER_TIME_GTC,
                "type_filling": mt.ORDER_FILLING_IOC, }
            order = mt.order_send(request)
            print(order)
            new_info = mt.positions_get(symbol='XAUUSDm')

            if new_info != ():
                entry = new_info[0].price_open
                ticket = new_info[0].ticket
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": min(data_df.iloc[-2,:]['low'],data_df.iloc[-3,:]['low']),
                    "tp":entry+10
                }
                od = mt.order_send(req)
                print(od)
            else:
                pass
    else:
        print('_________  NO CONDITIONS ____________ ..')
while True:
    bot()
