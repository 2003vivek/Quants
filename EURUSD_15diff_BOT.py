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

# # BEGINNING

opening_bal=1500
def bot():
    candle_data = mt.copy_rates_from_pos('EURUSDm', mt.TIMEFRAME_M1, 0, 10)
    # print(candle_data)
    data_df = pd.DataFrame(candle_data)
    previous_bar_diff = data_df.iloc[-1, :]
    bar_diff = previous_bar_diff['high'] - previous_bar_diff['low']
    data_df = data_df.drop(
        ['time', 'open', 'tick_volume', 'spread', 'real_volume'], axis=1)

    data_df['ma_3'] = ta.ema(data_df['close'],3)
    data_df['ma_10'] = ta.ema(data_df['close'],10)
    ma_3 = round(data_df.iloc[-1, 3], 6)
    ma_10 = round(data_df.iloc[-1, 4], 6)

    diff = data_df.iloc[-1, :]['close']
    diff2 = data_df.iloc[-7, :]['low']
    logic = round(diff-diff2, 5)

    diff_negative = data_df.iloc[-1, :]['close']
    diff2_negative = data_df.iloc[-7, :]['high']
    logic2 = round(diff_negative-diff2_negative, 5)

    position = mt.positions_get(symbol='EURUSDm')
    if position != ():
        if position[0].type == 0:  # means buy position
            entry = position[0].price_open
            ticket = position[0].ticket

            if mt.symbol_info_tick('EURUSDm').bid >= entry+0.00015:

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry+0.00015,
                    "tp": entry+0.0006
                }
                od = mt.order_send(req)
                print(od)
            
            else:
                print('not reached 15 points in buy position')
        elif position[0].type == 1:  # means sell position
            entry = position[0].price_open
            ticket = position[0].ticket

            if mt.symbol_info_tick('EURUSDm').ask <= entry-0.00015:

                req = {
                    "action": mt.TRADE_ACTION_SLTP,
                    "position": ticket,
                    "sl": entry-0.00015,
                    "tp": entry-0.0006
                }
                od = mt.order_send(req)
                print(od)
            else:
                print('not reached 15 points in sell position')

    if bar_diff >= 0.002:
        time.sleep(60*20)

    elif ma_3 > ma_10:
        if abs(logic) >= 0.0002:
            print('POSITIVE :: CROSSOVER')

            his = mt.history_orders_get(
                datetime.now()-timedelta(days=3),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling', 'state',
                              'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'sl/tp_price', 'sl', 'tp', 'entry_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'entry_price',
                     'comment', 'sl/tp_price', 'SYMBOL']]
            # print(df)

            for i in range(1, 50):
                if df.iloc[-i, :]['SYMBOL'] == 'EURUSDm':
                    result = df.iloc[-i, :]
                    break
                else:
                    pass
            try:
                vol = result['volume_ini']
                # print(vol)
                sl_price = result['sl/tp_price']
                # print(sl_price)
                # file=open('volume_file.txt','w')
                # file.write(str(vol))
                # file.close()
            except UnboundLocalError as e:
                print(e)
            count_sl = 0
            count_entry = 0
            diff0 = 0
            diff1 = 0
            diff2 = 0
            diff3 = 0
            entrylist = []
            sllist = []
            for i in range(1, 50):
                # if vol >=0.8:
                try:

                    if df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'sl':
                        # print(df.iloc[-i, :]['sl/tp_price'])
                        sllist.append(round(df.iloc[-i, :]['sl/tp_price'], 5))
                        count_sl += 1

                    elif df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'tp':
                        break

                    elif df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][0]+df.iloc[-i, :]['comment'][1] == 'py':
                        # print(df.iloc[-i, :]['entry_price'])
                        entrylist.append(round(df.iloc[-i, :]['entry_price'], 5))
                        count_entry += 1

                    if count_entry == 4 and count_sl == 4:
                        break
                except Exception as e:
                    print(e)
            #     else:
            #         break
            # if vol>=0.8:
            try:
                diff0 = round(abs(entrylist[0]-sllist[0]), 5)
                diff1 = round(abs(entrylist[1]-sllist[1]), 5)
                diff2 = round(abs(entrylist[2]-sllist[2]), 5)
                diff3 = round(abs(entrylist[3]-sllist[3]), 5)
                    
                    # diff4 = round(abs(entrylist[4]-sllist[4]), 5)
            except Exception as e:
                print(e)

            for k in range(1, 50):
                try:
                    if df.iloc[-k, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-k, :]['comment'][0] + df.iloc[-k, :]['comment'][1] == 'py':
                        last_entry_price = df.iloc[-k, :]['entry_price']
                        # print(last_entry_price)
                        break
                except Exception as e:
                    print(e)
            entry_sl_diff = round(abs(last_entry_price-sl_price), 5)
            # print(entry_sl_diff)
            # time.sleep(20)
            if entry_sl_diff > 0.0002 and entry_sl_diff < 0.0006:
                entry_sl_diff_new = 0.0006-entry_sl_diff
                entry_sl_diff_ = entry_sl_diff+entry_sl_diff_new
            # print(entry_sl_diff)
            # time.sleep(20)
            pos = mt.positions_get(symbol='EURUSDm')

            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                # file=open('martingalevol.txt','w')
                # data=100
                # file.write(str(data))
                # file.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('EURUSDm').ask
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSDm',
                    "volume": 0.1,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": pr,
                    "sl": pr - 0.0006,
                    "tp": pr + 0.0006,
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

                    if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry-0.0006,
                            "tp": entry+0.0006
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos==()  and diff0 == 0.00015 and diff1 == 0.00015 and diff2 == 0.00015 and diff3 == 0.00015 and vol>0.4 :
                pr = mt.symbol_info_tick('EURUSDm').ask
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSDm',
                     "volume": 0.1,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": pr,
                    "sl": pr - 0.0006,
                    "tp": pr + 0.0006,
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

                    if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                        print(
                            'POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry-0.0006,
                            "tp": entry+0.0006
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl' and entry_sl_diff >= 0.0001 and entry_sl_diff <= 0.0002:
                print('ENTERED IN SL LOGIC')
                # rd=open('volume_file.txt','r')
                # read_vol=rd.read()
                # volumes=float(read_vol)
                # rd.close()

                if vol >= 0.01 and vol < 100:
                    pr = mt.symbol_info_tick('EURUSDm').ask
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": vol,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-0.0006,
                        "tp": pr+0.0006,
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
                        if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-0.0006,
                                "tp": entry+0.0006
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl' and entry_sl_diff >= 0.00055:
                print('ENTERED IN SL LOGIC')
                # rd=open('volume_file.txt','r')
                # read_vol=rd.read()
                # volumes=float(read_vol)
                # rd.close()

                if vol >= 0.01 and vol < 100:
                    pr = mt.symbol_info_tick('EURUSDm').ask
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr-0.0006,
                        "tp": pr+0.0006,
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
                        if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry-0.0006,
                                "tp": entry+0.0006
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITION')
            else:
                print("--------------------WAITING---------------")
        else:
            print(' ############### LET IT MOVE 20 POINTS...')

    elif ma_3 < ma_10:
        if abs(logic2) >= 0.0002:
            print('NEGATIVE : CROSSOVER')
            his = mt.history_orders_get(
                datetime.now()-timedelta(days=3),
                datetime.now()
            )
            # print(his)

            df = pd.DataFrame(his, columns=['ticket', 'time_setup', 'time_setup_msc', 'time_done', 'time_done_msc', 'time_expiration', 'type', 'type_time', 'type_filling', 'state',
                              'magic', 'pos_id', 'pos_by_id', 'reason', 'volume_ini', 'vol_current', 'sl/tp_price', 'sl', 'tp', 'entry_price', 'price_sl', 'SYMBOL', 'comment', 'ex_id'])
            df = df[['ticket', 'volume_ini', 'entry_price',
                     'comment', 'sl/tp_price', 'SYMBOL']]
            # print(df)
            for i in range(1, 50):
                if df.iloc[-i, :]['SYMBOL'] == 'EURUSDm':
                    result = df.iloc[-i, :]
                    break
                else:
                    pass
            try:
                vol = result['volume_ini']
                sl_price = result['sl/tp_price']

            except UnboundLocalError as e:
                print(e)

            count_sl = 0
            count_entry = 0
            diff0 = 0
            diff1 = 0
            diff2 = 0
            diff3 = 0
            entrylist = []
            sllist = []
            for i in range(1, 50):
                # if vol>=0.8:
                try:

                    if df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'sl':
                        # print(df.iloc[-i, :]['sl/tp_price'])
                        sllist.append(round(df.iloc[-i, :]['sl/tp_price'], 5))
                        count_sl += 1

                    elif df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][1]+df.iloc[-i, :]['comment'][2] == 'tp':
                        break

                    elif df.iloc[-i, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-i, :]['comment'][0]+df.iloc[-i, :]['comment'][1] == 'py':
                        # print(df.iloc[-i, :]['entry_price'])
                        entrylist.append(round(df.iloc[-i, :]['entry_price'], 5))
                        count_entry += 1

                    if count_entry == 5 and count_sl == 5:
                        break
                except Exception as e:
                    print(e)
                # else:
                #     break
            # if vol>=0.8:
            try:
                diff0 = round(abs(entrylist[0]-sllist[0]), 5)
                diff1 = round(abs(entrylist[1]-sllist[1]), 5)
                diff2 = round(abs(entrylist[2]-sllist[2]), 5)
                diff3 = round(abs(entrylist[3]-sllist[3]), 5)
                    # diff4 = round(abs(entrylist[4]-sllist[4]), 5)
            except Exception as e:
                print(e)

            for k in range(1, 50):
                try:
                    if df.iloc[-k, :]['SYMBOL'] == 'EURUSDm' and df.iloc[-k, :]['comment'][0] + df.iloc[-k, :]['comment'][1] == 'py':
                        last_entry_price = df.iloc[-k, :]['entry_price']
                        break
                except Exception as e:
                    print(e)
            entry_sl_diff = round(abs(last_entry_price-sl_price), 5)
            # if entry_sl_diff > 0.0003 and entry_sl_diff < 0.0006:
            #     entry_sl_diff_new = 0.0006-entry_sl_diff
            #     entry_sl_diff_ = entry_sl_diff+entry_sl_diff_new

            pos = mt.positions_get(symbol='EURUSDm')
            if pos == () and result['comment'][1]+result['comment'][2] == 'tp':
                # writing_volume=open('martingalevol.txt','w')
                # new_vol=100
                # writing_volume.write(str(new_vol))
                # writing_volume.close()
                print('ENTERED IN TP LOGIC')
                pr = mt.symbol_info_tick('EURUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSDm',
                    "volume": 0.1,
                    "type": mt.ORDER_TYPE_SELL,
                    "price": pr,
                    "sl": pr + 0.0006,
                    "tp": pr - 0.0006,
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

                    if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                        print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry+0.0006,
                            "tp": entry-0.0006
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass
            elif pos==()  and diff0 == 0.00015 and diff1 == 0.00015 and diff2 == 0.00015 and diff3 == 0.00015 and vol>0.4:
                print('ENTERED IN TP LOGIC1')
                pr = mt.symbol_info_tick('EURUSDm').bid
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSDm',
                    "volume": 0.1,
                    "type": mt.ORDER_TYPE_SELL,
                    "price": pr,
                    "sl": pr + 0.0006,
                    "tp": pr - 0.0006,
                    "deviation": 5,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_IOC, }
                order = mt.order_send(request)
                (order)
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

                    if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                        print(
                            'POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                    else:
                        req = {
                            "action": mt.TRADE_ACTION_SLTP,
                            "position": ticket,
                            "sl": entry+0.0006,
                            "tp": entry-0.0006
                        }
                        od = mt.order_send(req)
                        print(od)
                else:
                    pass

            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl' and entry_sl_diff >= 0.0001 and entry_sl_diff <= 0.0002:
                print('ENTERED IN SL LOGIC2')
                if vol >= 0.01 and vol < 100:
                    pr = mt.symbol_info_tick('EURUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": vol,
                        "type": mt.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr+0.0006,
                        "tp": pr-0.0006,
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

                        if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry+0.0006,
                                "tp": entry-0.0006
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITIONS')
            elif pos == () and result['comment'][1]+result['comment'][2] == 'sl' and entry_sl_diff >= 0.00055:
                print('ENTERED IN SL LOGIC3')
                if vol >= 0.01 and vol < 100:
                    pr = mt.symbol_info_tick('EURUSDm').bid
                    request = {
                        "action": mt.TRADE_ACTION_DEAL,
                        "symbol": 'EURUSDm',
                        "volume": vol*2,
                        "type": mt.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr+0.0006,
                        "tp": pr-0.0006,
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

                        if sl_entry_diff == 0.0006 and tp_entry_diff == 0.0006:
                            print('POSITION MIGHT HAVE EXITED EVEN AFTER VOLUME > 0')
                        else:
                            req = {
                                "action": mt.TRADE_ACTION_SLTP,
                                "position": ticket,
                                "sl": entry+0.0006,
                                "tp": entry-0.0006
                            }
                            od = mt.order_send(req)
                            print(od)
                    else:
                        print('NO POSITIONS')
            else:
                print("--------------------WAITING---------------")
        else:
            print(' ############### LET IT MOVE 20 POINTS ...')
    else:
        print('waiting for crossover')


while True:
    bot()
