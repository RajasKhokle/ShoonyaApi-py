import pandas as pd
import connections as conn
import helper_functions as hf
import time


def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')


def event_handler_order_update(message):
    print("order event: " + str(message))



df_underlying = pd.DataFrame(columns=['ts', 'lp', 'ft'])
data_feed_list = []


def event_handler_quote_update(message, df_underlying):
    # e   Exchange
    # tk  Token
    # lp  LTP
    # pc  Percentage change
    # v   volume
    # o   Open price
    # h   High price
    # l   Low price
    # c   Close price
    # ap  Average trade price

    # print("quote event: {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(message))
    # data_feed_list.append(message)
    df_underlying = pd.concat(df_underlying, pd.DataFrame({'ts': [message['ts']],
                                                           'lp': [message['lp']], 'ft': [message['ft']]}),
                              ignore_index=True)
    # df_underlying.loc[len(df_underlying)] = [message['ts'], message['lp'], message['ft']]
    # pd.DataFrame({'ts': [message['ts']],
    #                                   'lp': [message['lp']], 'ft': [message['ft']]}), ignore_index=True)


# Establish the connection to the user
# Connect to Shoonya
s_con_rad, ret_rad = conn.login_shoonya('Radhika')
s_con_vee, ret_vee = conn.login_shoonya('Veena')
s_con_pra, ret_pra = conn.login_shoonya('Prakash')
# s_con_raj, ret_raj = conn.login_shoonya('Rajas')
# s_con_anu, ret_anu = conn.login_shoonya('Anuradha')
# s_con_ree, ret_ree = conn.login_shoonya('Reema')


# Subscribe to the ATM +/- 5 strikes with 5 second interval from ICICI direct
ret = s_con_rad.start_websocket(order_update_callback=event_handler_order_update,
                                subscribe_callback=event_handler_quote_update,
                                socket_open_callback=open_callback)
print(ret)
s_con_rad.subscribe("MCX|258988")
# Establish the momentum

# Establish if volatility is increasing or decreasing

# Place buy order

# Establish the reversal in underlying

# Exit from the position


# EOD get the order data from the shoonya system to load in the database
