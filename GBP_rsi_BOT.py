import MetaTrader5 as mt
import pandas as pd
import time
import pandas_ta as ta
from datetime import datetime, timedelta
Login = 122157792
Password = '26Vivek2003'
Server = 'Exness-MT5Trial7'


mt.initialize()
mt.login(Login, Password, Server)

#  BEGINNING
def bot():
    last_entry_price=0
    sl_price=0
    candle_data = mt.copy_rates_from_pos('GBPAUDm', mt.TIMEFRAME_M5, 0, 1000)   # getting the candle data
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)                                         # creating a pandas dataframes for data arrangement
    data_df = data_df.drop(['open', 'spread', 'real_volume'], axis=1)
    data_df['date'] = pd.to_datetime(data_df['time'], unit='s')
    data_df = data_df[['date', 'high', 'low', 'close', 'tick_volume']]
    data_df.set_index('date', inplace=True)

    data_df['rsi'] = round(ta.rsi(data_df['close'], 14), 2)                  # calculating the rsi
    data_df['rsi_average']=round(ta.ema(data_df['rsi'], 7), 2)   # this is the 7 days rsi moving average....

    data_df['vwap'] = round(ta.vwap(data_df['high'], data_df['low'], data_df['close'], data_df['tick_volume']), 5)   # calculating vwap 
    # print(data_df)

    current_rsi = data_df.iloc[-1, :]['rsi']                                             # accessing the current rsi
    current_vwap = data_df.iloc[-1, :]['vwap']   # accessing the current vwap 
    current_rsi_average=data_df.iloc[-1,:]['rsi_average']
    
    his = mt.history_orders_get(
        datetime.now()-timedelta(days=5),                               # FETCHING THE HISTORY OF ORDERS
        datetime.now()
        )
    pos = mt.positions_get(symbol='GBPAUDm')                        # FETCHING POSITIONS
    # print(his)
    # time.sleep(20)

    df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling', 'state',
                        'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'sl/tp_price', 'sl', 'tp', 'entry_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
    df = df[['time_done','ticket', 'volume_ini', 'entry_price',
                'comment', 'sl/tp_price', 'SYMBOL','type']]
    df['time_done']=pd.to_datetime(df['time_done'],unit='s')
    # print(df)
    
    for i in range(1, 50):
        if df.iloc[-i, :]['SYMBOL'] == 'GBPAUDm':
            result = df.iloc[-i, :]
            # print(result)
            # time.sleep(20)
            
            
            break
        else:
            pass
    time_done_str =str( result['time_done'])

# Convert the string to a datetime object
    time_done = datetime.strptime(time_done_str, "%Y-%m-%d %H:%M:%S")

    # Extract the date portion
    date_only = time_done.date()
    if result['comment'][1]+result['comment'][2] == 'tp' and date_only == datetime.now().date():
        print(" ")
        print(' --------------- DONE WITH TODAY S PROFIT MAANNN in GBPAUDm --------------------------------------- <<<<<<<<<<<')
        exit()
    # time.sleep(20)

    
    for k in range(1, 50):
        if df.iloc[-k, :]['SYMBOL'] == 'GBPAUDm' and df.iloc[-k, :]['comment'][0] + df.iloc[-k, :]['comment'][1] == 'py':           # Checking the entry price of last order in a shuffled history
            last_entry_price = df.iloc[-k, :]['entry_price']
            pos_type=df.iloc[-k,:]['type']
            break
        elif df.iloc[-k, :]['SYMBOL'] == 'GBPAUDm' and df.iloc[-k, :]['comment'][1]+df.iloc[-k, :]['comment'][2] == 'tp':
            break
        
    for i in range(1, 50):
        if df.iloc[-i, :]['SYMBOL'] == 'GBPAUDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'sl':      # Checking the stop loss price of the last order
            sl_price=df.iloc[-i, :]['sl/tp_price']
            volume=df.iloc[-i,:]['volume_ini']
            
            break
        elif df.iloc[-i, :]['SYMBOL'] == 'GBPAUDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'tp':
            break
    # try:
    #     entry_sl_diff=round(abs(last_entry_price-sl_price),5)                                       #Calculating entry SL difference....
    # except Exception as e:
    #     print(e)
    
    position = mt.positions_get(symbol='GBPAUDm')
    if position != ():
        if position[0].type == 0:  # means buy position
            pos_vol=position[0].volume
            entry = position[0].price_open
            ticket = position[0].ticket
            
            if  mt.symbol_info_tick('GBPAUDm').bid >= entry+0.0009 and mt.symbol_info_tick('GBPAUDm').bid < entry+0.001:# checking the sl trailing logic!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').bid >= entry+0.001 and mt.symbol_info_tick('GBPAUDm').bid <= entry+0.00110:# checking the sl trailing logic!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.0007,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif  pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').bid > entry+0.00130 and mt.symbol_info_tick('GBPAUDm').bid <= entry+0.00080:# checking the sl trailing logic!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP, # sending orders to the exchange for trailiing the stop loss
                    "position": ticket,
                    "sl": entry+0.0009,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').bid > entry+0.00240 and mt.symbol_info_tick('GBPAUDm').bid <= entry+0.00250:# checking the sl trailing logic!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00210,
                    "tp": current_vwap
                }
                od = mt.order_send(req)
                print(od)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').bid > entry+0.00280 and mt.symbol_info_tick('GBPAUDm').bid <= entry+0.00310:# checking the sl trailing logic!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00250,
                    "tp": current_vwap
                }
                od = mt.order_send(req)
                print(od)
            
            else:
                print('not reached 15 points in buy position')
                
        elif position[0].type == 1:  # means sell position
            pos_vol=position[0].volume
            entry = position[0].price_open
            ticket = position[0].ticket

            if  mt.symbol_info_tick('GBPAUDm').ask <= entry-0.0009 and mt.symbol_info_tick('GBPAUDm').ask > entry-0.001:# CHECKING THE SL TRAILING LOGICs!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').ask <= entry-0.00100 and mt.symbol_info_tick('GBPAUDm').ask >= entry-0.00110:# CHECKING THE SL TRAILING LOGICs!!!

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0007,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').ask <entry-0.00130 and mt.symbol_info_tick('GBPAUDm').ask >= entry-0.00080:

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0009,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').ask < entry-0.00240 and mt.symbol_info_tick('GBPAUDm').ask >= entry-0.00250:

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.00210,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            elif pos_vol==0.1 and mt.symbol_info_tick('GBPAUDm').ask < entry-0.00280 and mt.symbol_info_tick('GBPAUDm').ask >= entry-0.00310:

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.00250,
                    "tp": current_vwap
                }
                od1 = mt.order_send(req)
                print(od1)
            else:
                print('NOT REACHED 15 POINTS IN SELL POSITIONS')  
    if pos == () and mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'tp' and  data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69 : # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',
             "volume": 0.1,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.0008,
            "tp": pr-0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.0008,
                    "tp": entry-0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos==() and  mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'tp'  and current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',
            "volume": 0.1,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp":  entry+0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==1 and sl_price >last_entry_price and data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69: # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
             "volume": volume*2,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.00080,
            "tp": pr-0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00080,
                    "tp": entry-0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and  sl_price ==last_entry_price and data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69: # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
             "volume": volume,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.00080,
            "tp": pr-0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00080,
                    "tp": entry-0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==0 and sl_price <last_entry_price and data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69: # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
             "volume": volume*2,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.00080,
            "tp": pr-0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00080,
                    "tp": entry-0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==1 and sl_price < last_entry_price  and data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69: # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
             "volume": .1,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.0008,
            "tp": pr-0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.0008,
                    "tp": entry-0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==0 and sl_price > last_entry_price  and  data_df.iloc[-2,:]['rsi']>69 and current_rsi < 69: # checking condition for sell order
        pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
             "volume": .1,
            "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
            "price": pr,
            "sl": pr+0.0008,
            "tp": pr-0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = stop_l-entry
            tp_entry_diff = entry-target_p

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.0008,
                    "tp": entry-0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    # elif pos == () and  mt.symbol_info_tick('GBPAUDm').bid > current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and entry_sl_diff <=0.00139 and current_rsi >69 and current_rsi <68: # checking condition for sell order
    #     pr = mt.symbol_info_tick('GBPAUDm').bid                                                 
    #     request = {
    #         "action": mt.TRADE_ACTION_DEAL,
    #         "symbol": 'GBPAUDm',                                            # DOUBLING SELLL CONDITION
    #          "volume": 0.1,
    #         "type": mt.ORDER_TYPE_SELL,                                                # placing sell order
    #         "price": pr,
    #         "sl": pr+0.0015,
    #         "tp": pr-0.00080,
    #         "deviation": 5,
    #         "magic": 234000,
    #         "comment": "python script open",
    #         "type_time": mt.ORDER_TIME_GTC,
    #         "type_filling": mt.ORDER_FILLING_IOC, }
    #     order = mt.order_send(request)
    #     print(order)
    #     new_info = mt.positions_get(symbol='GBPAUDm')

    #     if new_info != ():
    #         entry = new_info[0].price_open
    #         target_p = new_info[0].tp
    #         stop_l = new_info[0].sl
    #         ticket = new_info[0].ticket
    #         print(f'sl is : {stop_l}')
    #         print(f'tp is : {target_p}')
    #         sl_entry_diff = stop_l-entry
    #         tp_entry_diff = entry-target_p

    #         if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
    #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
    #         else:
    #             req = {
    #                 "action": mt.TRADE_ACTION_SLTP,
    #                 "position": ticket,
    #                 "sl": entry+0.0015,
    #                 "tp": entry-0.00080
    #             }
    #             od = mt.order_send(req)
    #             print(od)
    #     else:
    #         pass
    
    elif pos==() and mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and  pos_type==1 and sl_price >last_entry_price  and  current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,                     # DOUBLING BUY CONDITION
            "symbol": 'GBPAUDm',
            "volume": volume*2,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp": entry+0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos==() and mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==0 and sl_price <last_entry_price and   current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,                     # DOUBLING BUY CONDITION
            "symbol": 'GBPAUDm',
            "volume": volume*2,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp": entry+0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos==() and mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==0 and sl_price ==last_entry_price and   current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,                     # DOUBLING BUY CONDITION
            "symbol": 'GBPAUDm',
            "volume": volume,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.00080,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp": entry+0.00080
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos==() and mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==1 and sl_price < last_entry_price and  current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,                     # DOUBLING BUY CONDITION
            "symbol": 'GBPAUDm',
            "volume": 0.1,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp": entry+0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    elif pos==() and mt.symbol_info_tick('GBPAUDm').ask < current_vwap and result['comment'][1]+result['comment'][2] == 'sl' and pos_type==0 and sl_price > last_entry_price and  current_rsi <30 and current_rsi > current_rsi_average:#buy condition
        pr = mt.symbol_info_tick('GBPAUDm').ask
        request = {
            "action": mt.TRADE_ACTION_DEAL,                     # DOUBLING BUY CONDITION
            "symbol": 'GBPAUDm',
            "volume": 0.1,
            "type": mt.ORDER_TYPE_BUY,                                                          # PLACING ORDER BUY
            "price": pr,
            "sl": pr - 0.0008,
            "tp": pr+0.0003,
            "deviation": 5,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC, }
        order = mt.order_send(request)
        print(order)
        new_info = mt.positions_get(symbol='GBPAUDm')

        if new_info != ():
            entry = new_info[0].price_open
            target_p = new_info[0].tp
            stop_l = new_info[0].sl
            ticket = new_info[0].ticket
            print(f'sl is : {stop_l}')
            print(f'tp is : {target_p}')
            sl_entry_diff = entry-stop_l
            tp_entry_diff = target_p-entry

            if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
            else:
                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.0008,
                    "tp": entry+0.0003
                }
                od = mt.order_send(req)
                print(od)
        else:
            pass
    
    else:
        print('>>>> WAITING AND COMPUTING ------ FOR GBPAUDm_____ <<<<<<')
        

while True:
    bot()
