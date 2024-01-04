import datetime as dt
# import math
# from api_helper import ShoonyaApiPy, get_time
# import json
# import numpy as np
import connections as conn
import requests
import zipfile
import os
import pandas as pd
import time

def get_margins(user_api):
    limits = user_api.get_limits()
    df = pd.DataFrame(limits, index=[0, ])
    for col_name in df.columns.to_list():
        try:
            df[col_name] = df[col_name].astype('float')
        except ValueError:
            continue
    return df


def update_symbol_files():
    root = 'https://shoonya.com/'
    masters = ['NSE_symbols.txt.zip', 'NFO_symbols.txt.zip', 'CDS_symbols.txt.zip', 'MCX_symbols.txt.zip',
               'BSE_symbols.txt.zip']
    for zip_file in masters:
        print(f'downloading {zip_file}')
        url = root + zip_file
        r = requests.get(url, allow_redirects=True)
        open(zip_file, 'wb').write(r.content)

        try:
            with zipfile.ZipFile(zip_file) as z:
                z.extractall()
                print("Extracted: ", zip_file)
        except Exception as e:
            print("Invalid file", e)
        try:
            os.remove(zip_file)
            print(f'remove: {zip_file}')
        except FileNotFoundError:
            continue
    text_file_list = ['NSE_symbols.txt', 'NFO_symbols.txt', 'CDS_symbols.txt', 'MCX_symbols.txt', 'BSE_symbols.txt',
                      'NIFTY50.csv']
    # postgres_conn = connections.connect_postgres('finance')
    mysql_con = conn.connect_mysql()
    for filename in text_file_list:
        try:
            df = pd.read_csv(filename)
            # df.to_sql(filename[0:-4], postgres_conn, if_exists='replace', index=False)

            df.to_sql(filename[0:-4].lower(), mysql_con, if_exists='replace', index=False)
            print("Successfully updated table ", filename[0:-4])
        except Exception as e:
            print('Failed to update table ', filename[0:-4], 'Due to Error', e)


def place_order(user_id, user_api, exchange, bs, tsym, quantity, price_type, price, trigger, remark,
                broker="FINVASIA", prod_type="M"):
    if exchange == "NFO":
        segment = 'FNO'
    elif (exchange == "NSE") | (exchange == "BSE"):
        segment = 'CASH'
    elif exchange == "CDS":
        segment = 'CURRENCY'
    elif exchange == 'MCX':
        segment = 'COMMODITY'
    else:
        print("Select The Correct Exchange")
        return None

    product_type_array = {'M': 'NORMAL', "I": "INTRADAY", "C": "DELIVERY", "B": "BRACKET", "H": "COVER"}
    product_type = product_type_array[prod_type]

    retention_duration = 'DAY'
    price_sent = price * 100  # convert price into paise for api consumption

    ret_data = user_api.place_order(buy_or_sell=bs, product_type=prod_type,
                                    exchange=exchange, tradingsymbol=tsym,
                                    quantity=quantity, discloseqty=0, price_type=price_type, price=price_sent,
                                    trigger_price=trigger,
                                    retention=retention_duration, remarks=remark)
    order_submit_time = dt.datetime.now()
    instrument_full_name = ret_data['cname']
    if bs == "B":
        amount = price * quantity
        premium = -amount
        margin = amount
    elif bs == "S":
        margin = ret_data['']
        amount = margin  # Put margin Blocked
        premium = price * quantity
    else:
        print("You must set bs to either B (BUY) or S(SELL)")
        return None
    print(ret_data)
    if ret_data is not None:
        if ret_data['stat'] == "Ok":
            # Store the order in database
            try:
                mysql_connection = conn.connect_mysql()
                order_dict = {'user_id': [user_id],
                              'exchange': [exchange],
                              'segment': [segment],
                              'order_submit_time': [order_submit_time],
                              'order_final_status_time': [ret_data['']],
                              'product_type': [product_type],
                              'order_buy_sell': [bs],
                              'symbol': [tsym],
                              'order_type': [price_type],
                              'order_price': [price],
                              'executed_price': [ret_data['']],
                              'order_final_status': [ret_data['']],
                              'order_quantity': [quantity],
                              'order_amount': [amount],
                              'premium': [premium],
                              'margin': [margin],
                              'leverage': [],
                              'trigger_price': [trigger],
                              'order_reason': [ret_data['']],
                              'broker_order_id': [ret_data['']],
                              'exchange_order_id': [ret_data['']],
                              'instrument_full_name': [instrument_full_name],
                              'broker': [broker]
                              }
                df_order = pd.DataFrame(order_dict)
                df_order.to_sql("orders", mysql_connection, if_exists='append', index=False)
            except Exception as e:
                print("Mysql DB is not present. Cannot Store the order into system but have placed the order with "
                      "the broker.", e)


    return ret_data


def predict_direction_option(shoonya_conn, security="NIFTY INDEX"):
    # connect to websocket data for underlying security and dump it into database
    # Find the derivative and double derivative
    # Get the 10,10 strike away data for PE and CE through websocket ande dump into database
    # Get their derivative and double derivative
    # Based on the derivatives of the underlying security and CE and PE prices and their averages generate the buy/sell
    # signal for a particular strike price

    # If Very strong positive underlying and ATM derivatives - Buy ATM - Exit if the strength declines
    # If Very Weak derivatives and negative derivatives of the ATM strike price - Sell PE and CE both -
    #   - exit the leg for which the derivative turns positive and underlying security's derivative also turns positive
    # If very weak derivative but only negative derivative of one of the PE or CE, then Sell that PE or CE only
    # exit condition same as above.
    option_data_past = []
    current_sod_price = 0
    last_eod_price = 0
    sod_atm_option_tsym = 0
    option_data_current = shoonya_conn.get_option_chain(exchange="NFO", tradingsymbol=sod_atm_option_tsym,
                                                        strikeprice=current_sod_price, count=15)
    direction = "Non-Directional"

    return direction
