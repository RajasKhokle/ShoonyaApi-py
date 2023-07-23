import datetime as dt
# import math
import pandas as pd
from api_helper import ShoonyaApiPy, get_time
import json
import connections as conn
import numpy as np


def get_margins(user_api):
    limits = user_api.get_limits()
    df = pd.DataFrame(limits, index=[0, ])
    for col_name in df.columns.to_list():
        try:
            df[col_name] = df[col_name].astype('float')
        except ValueError:
            continue
    return df


def place_order_nse(user_id, user_api, exchange, bs, tsym, quantity, price_type, price, trigger, remark,
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

    return ret_data
