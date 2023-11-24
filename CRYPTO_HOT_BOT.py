import MetaTrader5 as mt
import pandas as pd
from datetime import datetime,  timedelta
import time
Login = 
Password = ''
Server = ''



mt.initialize()
mt.login(Login, Password, Server)

# # BEGINNING


def bot_20():
    candle_data = mt.copy_rates_from_pos('BTCUSDm', mt.TIMEFRAME_M1, 0, 10)
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)
    previous_bar_diff = data_df.iloc[-1, :]
    bar_diff = previous_bar_diff['high'] - previous_bar_diff['low']
    data_df = data_df.drop(['time', 'open', 'tick_volume', 'spread', 'real_volume'], axis=1)
    
    data_df['ma_3'] = data_df['close'].rolling(3).mean()
    data_df['ma_10'] = data_df['close'].rolling(10).mean()
    ma_3 = round(data_df.iloc[-1, 3], 6)
    ma_10 = round(data_df.iloc[-1, 4], 6)
    
    diff=data_df.iloc[-1,:]['high']
    diff2=data_df.iloc[-7,:]['low']
    logic=round(diff-diff2,5)
    # print(logic)
    # print(data_df)
    diff_negative=data_df.iloc[-1,:]['low']
    diff2_negative=data_df.iloc[-7,:]['high']
    logic2=diff_negative-diff2_negative
    # print(logic2)
    # diff1_negative=data_df.iloc[-1,:]
    # diff21_negative=data_df.iloc[-7,:]
    # print(diff1_negative)
    # print(diff21_negative)
    # time.sleep(20)
    
    if bar_diff >= 150:
        time.sleep(60*20)
        
    
    elif ma_3 > ma_10:
        if abs(logic) >=10:
            print('POSITIVE :: CROSSOVER')

            his = mt.history_orders_get(
                datetime.now()-timedelta(hours=3),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling','state', 'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'price_open', 'sl', 'tp', 'curr_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'comment', 'price_open','SYMBOL']]
            # print(df)
            for i in range(1,40):
                if df.iloc[-i,:]['SYMBOL']=='BTCUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
            pos = mt.positions_get(symbol='BTCUSDm')
            
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                writing_volume=open('btcvol.txt','w')
                new_vol=40.6
                writing_volume.write(str(new_vol))
                writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('BTCUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'BTCUSDm',
                    "volume": 0.1,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": pr,
                    "sl": pr - 15,
                    "tp": pr + 15,
                    "deviation": 5,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='BTCUSDm')

                if new_info != ():
                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = entry-stop_l
                    tp_entry_diff = target_p-entry

                    if sl_entry_diff == 15 and tp_entry_diff == 15:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry-15,
                            "tp": entry+15
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass
                

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')

                if vol >= 0.8 and vol < 12.8:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-40,
                        "tp": pr+40,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-40,
                                "tp": entry+40
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol ==0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-25,
                        "tp": pr+25,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 25 and tp_entry_diff == 25:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-25,
                                "tp": entry+25
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol == 0.4:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-40,
                        "tp": pr+40,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-40,
                                "tp": entry+40
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                elif vol < 0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-15,
                        "tp": pr+15,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 15 and tp_entry_diff == 15:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-15,
                                "tp": entry+15
                            }
                            od = mt.order_send(req)
                            print(od)
                            
                elif vol==12.8:
                    file=open('btcvol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/12.8
                    file.close()
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('BTCUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": 12.8,
                            "type": mt.ORDER_TYPE_BUY,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 2304000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)
                        tick=order.order

                        new_info = mt.positions_get(ticket=tick)

                        if new_info != ():
                            entry = new_info[0].price_open
                            target_p = new_info[0].tp
                            stop_l = new_info[0].sl
                            ticket = new_info[0].ticket
                            print(f'sl is : {stop_l}')
                            print(f'tp is : {target_p}')
                            sl_entry_diff = stop_l-entry
                            tp_entry_diff = entry - target_p

                            if sl_entry_diff == 40 and tp_entry_diff == 40:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                    }
                                od=mt.order_send(req)
                                print(od)
                        writing_volume=open('btcvol.txt','w')
                        new_vol=float(volume)*2
                        writing_volume.write(str(new_vol)) 
                        writing_volume.close()    
                else:
                    print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('LET IT MOVE 10 $...')

    elif ma_3 < ma_10:
        if abs(logic2) >=10:
            print('NEGATIVE : CROSSOVER')
            his = mt.history_orders_get(
                datetime.now()-timedelta(days=1),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling',
                                            'state', 'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'price_open', 'sl', 'tp', 'curr_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'comment', 'price_open','SYMBOL']]
            # print(df)
            for i in range(1,40):
                if df.iloc[-i,:]['SYMBOL']=='BTCUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
            pos = mt.positions_get(symbol='BTCUSDm')
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                writing_volume=open('btcvol.txt','w')
                new_vol=40.6
                writing_volume.write(str(new_vol))
                writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('BTCUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": 0.1,
                        "type": mt.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr + 15,
                        "tp": pr - 15,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='BTCUSDm')

                if new_info != ():

                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = stop_l-entry
                    tp_entry_diff = entry - target_p

                    if sl_entry_diff == 15 and tp_entry_diff == 15:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry+15,
                                "tp": entry-15
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')
                if vol >= 0.8 and vol < 12.8:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = stop_l-entry
                        tp_entry_diff = entry - target_p

                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITIONS')

                elif vol ==0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+25,
                            "tp": pr-25,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 25 and tp_entry_diff == 25:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+25,
                                    "tp": entry-25
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                elif vol==12.8:
                    file=open('btcvol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/12.8
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('BTCUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": 12.8,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 2304000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)

                        new_info = mt.positions_get(symbol='BTCUSDm')

                        if new_info != ():
                            entry = new_info[0].price_open
                            target_p = new_info[0].tp
                            stop_l = new_info[0].sl
                            ticket = new_info[0].ticket
                            print(f'sl is : {stop_l}')
                            print(f'tp is : {target_p}')
                            sl_entry_diff = stop_l-entry
                            tp_entry_diff = entry - target_p

                            if sl_entry_diff == 40 and tp_entry_diff == 40:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                    }
                                od=mt.order_send(req)
                                print(od)
                        writing_volume=open('btcvol.txt','w')
                        new_vol=float(volume)*2
                        writing_volume.write(str(new_vol))
                        writing_volume.close()
                    
                elif vol == 0.4:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol < 0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+15,
                            "tp": pr-15,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = stop_l-entry
                        tp_entry_diff = entry - target_p

                        if sl_entry_diff == 15 and tp_entry_diff == 15:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+15,
                                    "tp": entry-15
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                else:
                    print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('Waiting for negative crossover"s 10$')
    else:
        print('waiting for crossover')

def bot_200():
    candle_data = mt.copy_rates_from_pos('BTCUSDm', mt.TIMEFRAME_M1, 0, 10)
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)
    previous_bar_diff = data_df.iloc[-1, :]
    bar_diff = previous_bar_diff['high'] - previous_bar_diff['low']
    data_df = data_df.drop(['time', 'open', 'tick_volume', 'spread', 'real_volume'], axis=1)
    
    data_df['ma_3'] = data_df['close'].rolling(3).mean()
    data_df['ma_10'] = data_df['close'].rolling(10).mean()
    ma_3 = round(data_df.iloc[-1, 3], 6)
    ma_10 = round(data_df.iloc[-1, 4], 6)
    
    diff=data_df.iloc[-1,:]['high']
    diff2=data_df.iloc[-7,:]['low']
    logic=round(diff-diff2,5)
    # print(logic)
    # print(data_df)
    diff_negative=data_df.iloc[-1,:]['low']
    diff2_negative=data_df.iloc[-7,:]['high']
    logic2=diff_negative-diff2_negative
    # print(logic2)
    # diff1_negative=data_df.iloc[-1,:]
    # diff21_negative=data_df.iloc[-7,:]
    # print(diff1_negative)
    # print(diff21_negative)
    # time.sleep(20)
    
    if bar_diff >= 150:
        time.sleep(60*20)
    
    elif ma_3 > ma_10:
        if abs(logic) >=0.0006:
            print('POSITIVE :: CROSSOVER')

            his = mt.history_orders_get(
                datetime.now()-timedelta(hours=3),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling','state', 'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'price_open', 'sl', 'tp', 'curr_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'comment', 'price_open','SYMBOL']]
            # print(df)
            for i in range(1,40):
                if df.iloc[-i,:]['SYMBOL']=='BTCUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
            pos = mt.positions_get(symbol='BTCUSDm')
            
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                writing_volume=open('btcvol.txt','w')
                new_vol=204.8
                writing_volume.write(str(new_vol))
                writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('BTCUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'BTCUSDm',
                    "volume": 0.1,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": pr,
                    "sl": pr - 15,
                    "tp": pr + 15,
                    "deviation": 5,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='BTCUSDm')

                if new_info != ():
                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = entry-stop_l
                    tp_entry_diff = target_p-entry

                    if sl_entry_diff == 15 and tp_entry_diff == 15:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry-15,
                            "tp": entry+15
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass
                

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')

                if vol >= 0.8 and vol < 102.4:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-40,
                        "tp": pr+40,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-40,
                                "tp": entry+40
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol ==0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-25,
                        "tp": pr+25,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 25 and tp_entry_diff == 25:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-25,
                                "tp": entry+25
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol == 0.4:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-40,
                        "tp": pr+40,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-40,
                                "tp": entry+40
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                elif vol < 0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-15,
                        "tp": pr+15,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 15 and tp_entry_diff == 15:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-15,
                                "tp": entry+15
                            }
                            od = mt.order_send(req)
                            print(od)
                            
                elif vol==102.4:
                    file=open('btcvol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/102.4
                    volume.close()
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('BTCUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": 102.4,
                            "type": mt.ORDER_TYPE_BUY,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 2304000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)
                        tick=order.order

                        new_info = mt.positions_get(ticket=tick)

                        if new_info != ():
                            entry = new_info[0].price_open
                            target_p = new_info[0].tp
                            stop_l = new_info[0].sl
                            ticket = new_info[0].ticket
                            print(f'sl is : {stop_l}')
                            print(f'tp is : {target_p}')
                            sl_entry_diff = stop_l-entry
                            tp_entry_diff = entry - target_p

                            if sl_entry_diff == 40 and tp_entry_diff == 40:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                    }
                                od=mt.order_send(req)
                                print(od)
                        writing_volume=open('btcvol.txt','w')
                        new_vol=float(volume)*2
                        writing_volume.write(str(new_vol)) 
                        writing_volume.close()    
                else:
                    print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('LET IT MOVE 10$...')

    elif ma_3 < ma_10:
        if abs(logic2) >=0.0006:
            print('NEGATIVE : CROSSOVER')
            his = mt.history_orders_get(
                datetime.now()-timedelta(days=1),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling',
                                            'state', 'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'price_open', 'sl', 'tp', 'curr_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'comment', 'price_open','SYMBOL']]
            # print(df)
            for i in range(1,40):
                if df.iloc[-i,:]['SYMBOL']=='BTCUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
            pos = mt.positions_get(symbol='BTCUSDm')
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                writing_volume=open('btcvol.txt','w')
                new_vol=102.4
                writing_volume.write(str(new_vol))
                writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('BTCUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'BTCUSDm',
                        "volume": 0.1,
                        "type": mt.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr + 15,
                        "tp": pr - 15,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='BTCUSDm')

                if new_info != ():

                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = stop_l-entry
                    tp_entry_diff = entry - target_p

                    if sl_entry_diff == 15 and tp_entry_diff == 15:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry+15,
                                "tp": entry-15
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')
                if vol >= 0.8 and vol < 12.8:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = stop_l-entry
                        tp_entry_diff = entry - target_p

                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITIONS')

                elif vol ==0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+25,
                            "tp": pr-25,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 25 and tp_entry_diff == 25:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+25,
                                    "tp": entry-25
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                elif vol==102.4:
                    file=open('btcvol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/102.4
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('BTCUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": 102.4,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 2304000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)

                        new_info = mt.positions_get(symbol='BTCUSDm')

                        if new_info != ():
                            entry = new_info[0].price_open
                            target_p = new_info[0].tp
                            stop_l = new_info[0].sl
                            ticket = new_info[0].ticket
                            print(f'sl is : {stop_l}')
                            print(f'tp is : {target_p}')
                            sl_entry_diff = stop_l-entry
                            tp_entry_diff = entry - target_p

                            if sl_entry_diff == 40 and tp_entry_diff == 40:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                    }
                                od=mt.order_send(req)
                                print(od)
                        writing_volume=open('btcvol.txt','w')
                        new_vol=float(volume)*2
                        writing_volume.write(str(new_vol))
                        writing_volume.close()
                    
                elif vol == 0.4:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+40,
                            "tp": pr-40,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 40 and tp_entry_diff == 40:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+40,
                                    "tp": entry-40
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')

                elif vol < 0.2:
                    pr = mt.symbol_info_tick('BTCUSDm').bid
                    request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'BTCUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+15,
                            "tp": pr-15,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='BTCUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = stop_l-entry
                        tp_entry_diff = entry - target_p

                        if sl_entry_diff == 15 and tp_entry_diff == 15:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+15,
                                    "tp": entry-15
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                else:
                    print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('Waiting for negative crossover"s 10$')
    else:
        print('waiting for crossover')
    
def bot():
    timenow=time.localtime()
    start_time = time.strptime("13:15:00", "%H:%M:%S")
    end_time = time.strptime("1:15:00", "%H:%M:%S")
    if timenow >=start_time or timenow < end_time:
        bot_200()
    else:
        bot_20()
while True:
    bot()
