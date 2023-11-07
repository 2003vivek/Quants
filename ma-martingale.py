import MetaTrader5 as mt
import pandas as pd
import time
from datetime import datetime, timedelta
Login = 121860569
Password = '26Vivek2003'
Server = 'Exness-MT5Trial7'



mt.initialize()
mt.login(Login, Password, Server)

# # BEGINNING


def bot():
    candle_data = mt.copy_rates_from_pos('EURUSDm', mt.TIMEFRAME_M1, 0, 10)
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)
    previous_bar_diff = data_df.iloc[-1, :]
    bar_diff = previous_bar_diff['high'] - previous_bar_diff['low']
    data_df = data_df.drop(['time', 'open', 'tick_volume', 'spread', 'real_volume'], axis=1)
    
    data_df['ma_3'] = data_df['close'].rolling(3).mean()
    data_df['ma_10'] = data_df['close'].rolling(10).mean()
    ma_3 = round(data_df.iloc[-1, 3], 6)
    ma_10 = round(data_df.iloc[-1, 4], 6)
    
    diff=data_df.iloc[-1,:]['close']
    diff2=data_df.iloc[-7,:]['low']
    logic=round(diff-diff2,5)
    
    diff_negative=data_df.iloc[-1,:]['close']
    diff2_negative=data_df.iloc[-7,:]['high']
    logic2=round(diff_negative-diff2_negative,5)
    
    if bar_diff >= 0.001:
        time.sleep(60*20)
    
    elif ma_3 > ma_10:
        if abs(logic) >=0.00045:
            print('POSITIVE :: CROSSOVER')

            his = mt.history_orders_get(
                datetime.now()-timedelta(days=1),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling','state', 'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'price_open', 'sl', 'tp', 'curr_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'comment', 'price_open','SYMBOL']]
            # print(df)
            
            for i in range(1,50):
                if df.iloc[-i,:]['SYMBOL']=='EURUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
           
            pos = mt.positions_get(symbol='EURUSDm')
            
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                file=open('martingalevol.txt','w')
                data=10.24
                file.write(str(data))
                file.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('EURUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSDm',
                    "volume": 0.01,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": pr,
                    "sl": pr - 0.0003,
                    "tp": pr + 0.0003,
                    "deviation": 5,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='EURUSDm')

                if new_info != ():
                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = entry-stop_l
                    tp_entry_diff = target_p-entry

                    if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry-0.0003,
                            "tp": entry+0.0003
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass
                

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')

                if vol >= 0.01 and vol <0.16:
                    pr = mt.symbol_info_tick('EURUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-0.0003,
                        "tp": pr+0.0003,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='EURUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-0.0003,
                                "tp": entry+0.0003
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                        
                elif vol >= 0.16:
                    if abs(logic) >=0.0006:
                        pr = mt.symbol_info_tick('EURUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'EURUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_BUY,
                            "price": pr,
                            "sl": pr-0.0003,
                            "tp": pr+0.0003,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)

                    new_info = mt.positions_get(symbol='EURUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = entry-stop_l
                        tp_entry_diff = target_p-entry
                        if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-0.0003,
                                "tp": entry+0.0003
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
                        
                    
                        
                elif vol>=10.24:
                    file=open('martingalevol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/10.24
                    file.close()
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('EURUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'EURUSDm',
                            "volume": 10.24,
                            "type": mt.ORDER_TYPE_BUY,
                            "price": pr,
                            "sl": pr-0.0003,
                            "tp": pr+0.0003,
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
                            sl_entry_diff = entry-stop_l
                            tp_entry_diff = target_p-entry

                            if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry-0.0003,
                                    "tp": entry+0.0003
                                    }
                                od=mt.order_send(req)
                                print(od)
                    writing_volume=open('martingalevol.txt','w')
                    new_vol=float(volume)*2
                    writing_volume.write(str(new_vol)) 
                    writing_volume.close()
                else:
                    print('NO VOLUME')
                    time.sleep(20)
                    

                # elif vol >= 0.08 and vol < 0.32:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #         "action": mt.TRADE_ACTION_DEAL,
                #         "symbol": 'EURUSDm',
                #         "volume": vol*2,
                #         "type": mt.ORDER_TYPE_BUY,
                #         "price": pr,
                #         "sl": pr-0.0003,
                #         "tp": pr+0.0003,
                #         "deviation": 5,
                #         "magic": 234000,
                #         "comment": "python script open",
                #         "type_time": mt.ORDER_TIME_GTC,
                #         "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = entry-stop_l
                #         tp_entry_diff = target_p-entry
                #         if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                 "action": mt.TRADE_ACTION_SLTP,
                #                 "position": ticket,
                #                 "sl": entry-0.0003,
                #                 "tp": entry+0.0003
                #             }
                #             od = mt.order_send(req)
                #             print(od)
                #     else:
                #         print('NO POSITION')

                # elif vol == 0.04:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #         "action": mt.TRADE_ACTION_DEAL,
                #         "symbol": 'EURUSDm',
                #         "volume": vol*2,
                #         "type": mt.ORDER_TYPE_BUY,
                #         "price": pr,
                #         "sl": pr-0.0003,
                #         "tp": pr+0.0003,
                #         "deviation": 5,
                #         "magic": 234000,
                #         "comment": "python script open",
                #         "type_time": mt.ORDER_TIME_GTC,
                #         "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = entry-stop_l
                #         tp_entry_diff = target_p-entry
                #         if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                 "action": mt.TRADE_ACTION_SLTP,
                #                 "position": ticket,
                #                 "sl": entry-0.0003,
                #                 "tp": entry+0.0003
                #             }
                #             od = mt.order_send(req)
                #             print(od)
                #     else:
                #         print('NO POSITION')
                # elif vol < 0.04:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #         "action": mt.TRADE_ACTION_DEAL,
                #         "symbol": 'EURUSDm',
                #         "volume": vol*2,
                #         "type": mt.ORDER_TYPE_BUY,
                #         "price": pr,
                #         "sl": pr-0.0003,
                #         "tp": pr+0.0003,
                #         "deviation": 5,
                #         "magic": 234000,
                #         "comment": "python script open",
                #         "type_time": mt.ORDER_TIME_GTC,
                #         "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = entry-stop_l
                #         tp_entry_diff = target_p-entry
                #         if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                 "action": mt.TRADE_ACTION_SLTP,
                #                 "position": ticket,
                #                 "sl": entry-0.0003,
                #                 "tp": entry+0.0003
                #             }
                #             od = mt.order_send(req)
                #             print(od)
                            
                
                # else:
                #     print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('LET IT MOVE 60 POINTS...')

    elif ma_3 < ma_10:
        if abs(logic2) >=0.00045:
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
            for i in range(1,50):
                if df.iloc[-i,:]['SYMBOL']=='EURUSDm':
                    result=df.iloc[-i,:]
                    break
                else:
                    pass
            try:
                vol=result['volume_ini']
            except UnboundLocalError as e:
                print(e)
            pos = mt.positions_get(symbol='EURUSDm')
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                writing_volume=open('martingalevol.txt','w')
                new_vol=10.24
                writing_volume.write(str(new_vol))
                writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('EURUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": 0.01,
                        "type": mt.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr + 0.0003,
                        "tp": pr - 0.0003,
                        "deviation": 5,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt.ORDER_TIME_GTC,
                        "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                print(order)
                new_info = mt.positions_get(symbol='EURUSDm')

                if new_info != ():

                    entry = new_info[0].price_open
                    target_p = new_info[0].tp
                    stop_l = new_info[0].sl
                    ticket = new_info[0].ticket
                    print(f'sl is : {stop_l}')
                    print(f'tp is : {target_p}')
                    sl_entry_diff = stop_l-entry
                    tp_entry_diff = entry - target_p

                    if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry+0.0003,
                                "tp": entry-0.0003
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl':
                print('ENTERED IN SL LOGIC')
                if vol >= 0.01 and vol < 0.16:
                    pr = mt.symbol_info_tick('EURUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'EURUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+0.0003,
                            "tp": pr-0.0003,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                    order = mt.order_send(request)
                    print(order)

                    new_info = mt.positions_get(symbol='EURUSDm')

                    if new_info != ():
                        entry = new_info[0].price_open
                        target_p = new_info[0].tp
                        stop_l = new_info[0].sl
                        ticket = new_info[0].ticket
                        print(f'sl is : {stop_l}')
                        print(f'tp is : {target_p}')
                        sl_entry_diff = stop_l-entry
                        tp_entry_diff = entry - target_p

                        if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+0.0003,
                                    "tp": entry-0.0003
                                }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITIONS')
                        
                elif vol >= 0.16:
                    if abs(logic2) >=0.0006:
                        pr = mt.symbol_info_tick('EURUSDm').bid
                        request = {
                        "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'EURUSDm',
                            "volume": vol*2,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+0.0003,
                            "tp": pr-0.0003,
                            "deviation": 5,
                            "magic": 234000,
                            "comment": "python script open",
                            "type_time": mt.ORDER_TIME_GTC,
                            "type_filling": mt.ORDER_FILLING_IOC, }
                        order = mt.order_send(request)
                        print(order)

                        new_info = mt.positions_get(symbol='EURUSDm')

                        if new_info != ():
                            entry = new_info[0].price_open
                            target_p = new_info[0].tp
                            stop_l = new_info[0].sl
                            ticket = new_info[0].ticket
                            print(f'sl is : {stop_l}')
                            print(f'tp is : {target_p}')
                            sl_entry_diff = stop_l-entry
                            tp_entry_diff = entry - target_p

                            if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                        "action": mt.TRADE_ACTION_SLTP,
                                        "position": ticket,
                                        "sl": entry+0.0003,
                                        "tp": entry-0.0003
                                    }
                                od = mt.order_send(req)
                                print(od)
                        else:
                            print('NO POSITIONS')
                        
                elif vol>=10.24:
                    file=open('martingalevol.txt','r')
                    volume=file.read()
                    filedata=float(volume)/10.24
                    file.close()
                    for i in range(int(filedata)):
                        pr = mt.symbol_info_tick('EURUSDm').bid
                        request = {
                            "action": mt.TRADE_ACTION_DEAL,
                            "symbol": 'EURUSDm',
                            "volume": 10.24,
                            "type": mt.ORDER_TYPE_SELL,
                            "price": pr,
                            "sl": pr+0.0003,
                            "tp": pr-0.0003,
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
                            tp_entry_diff = entry-target_p

                            if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                                print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                            else:
                                req = {
                                    "action": mt.TRADE_ACTION_SLTP,
                                    "position": ticket,
                                    "sl": entry+0.0003,
                                    "tp": entry-0.0003
                                    }
                                od=mt.order_send(req)
                                print(od)
                    writing_volume=open('martingalevol.txt','w')
                    new_vol=float(volume)*2
                    writing_volume.write(str(new_vol)) 
                    writing_volume.close()
                else:
                    print('NO VOLUME')
                    time.sleep(20)

                # elif vol >= 0.32:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #             "action": mt.TRADE_ACTION_DEAL,
                #             "symbol": 'EURUSDm',
                #             "volume": vol*2,
                #             "type": mt.ORDER_TYPE_SELL,
                #             "price": pr,
                #             "sl": pr+0.0006,
                #             "tp": pr-0.0006,
                #             "deviation": 5,
                #             "magic": 234000,
                #             "comment": "python script open",
                #             "type_time": mt.ORDER_TIME_GTC,
                #             "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = stop_l-entry
                #         tp_entry_diff = entry - target_p
                #         if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                     "action": mt.TRADE_ACTION_SLTP,
                #                     "position": ticket,
                #                     "sl": entry+0.0006,
                #                     "tp": entry-0.0006
                #                 }
                #             od = mt.order_send(req)
                #             print(od)
                #     else:
                #         print('NO POSITION')
             
                    
                # elif vol == 0.04:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #             "action": mt.TRADE_ACTION_DEAL,
                #             "symbol": 'EURUSDm',
                #             "volume": vol*2,
                #             "type": mt.ORDER_TYPE_SELL,
                #             "price": pr,
                #             "sl": pr+0.0003,
                #             "tp": pr-0.0003,
                #             "deviation": 5,
                #             "magic": 234000,
                #             "comment": "python script open",
                #             "type_time": mt.ORDER_TIME_GTC,
                #             "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = stop_l-entry
                #         tp_entry_diff = entry - target_p
                #         if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                     "action": mt.TRADE_ACTION_SLTP,
                #                     "position": ticket,
                #                     "sl": entry+0.0003,
                #                     "tp": entry-0.0003
                #                 }
                #             od = mt.order_send(req)
                #             print(od)
                #     else:
                #         print('NO POSITION')

                # elif vol < 0.04:
                #     pr = mt.symbol_info_tick('EURUSDm').bid
                #     request = {
                #             "action": mt.TRADE_ACTION_DEAL,
                #             "symbol": 'EURUSDm',
                #             "volume": vol*2,
                #             "type": mt.ORDER_TYPE_SELL,
                #             "price": pr,
                #             "sl": pr+0.0003,
                #             "tp": pr-0.0003,
                #             "deviation": 5,
                #             "magic": 234000,
                #             "comment": "python script open",
                #             "type_time": mt.ORDER_TIME_GTC,
                #             "type_filling": mt.ORDER_FILLING_IOC, }
                #     order = mt.order_send(request)
                #     print(order)

                #     new_info = mt.positions_get(symbol='EURUSDm')

                #     if new_info != ():
                #         entry = new_info[0].price_open
                #         target_p = new_info[0].tp
                #         stop_l = new_info[0].sl
                #         ticket = new_info[0].ticket
                #         print(f'sl is : {stop_l}')
                #         print(f'tp is : {target_p}')
                #         sl_entry_diff = stop_l-entry
                #         tp_entry_diff = entry - target_p

                #         if sl_entry_diff == 0.0003 and tp_entry_diff == 0.0003:
                #             print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                #         else:
                #             req = {
                #                     "action": mt.TRADE_ACTION_SLTP,
                #                     "position": ticket,
                #                     "sl": entry+0.0003,
                #                     "tp": entry-0.0003
                #                 }
                #             od = mt.order_send(req)
                #             print(od)
                #     else:
                #         print('NO POSITION')
                # else:
                #     print('waiting')
            else:
                print("--------------------WAITING---------------")
        else:
            print('Waiting for negative crossover"s 60 points')
    else:
        print('waiting for crossover')


while True:
    bot()

