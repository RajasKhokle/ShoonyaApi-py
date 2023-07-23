# Place Concurrent Orders for different shoonya accounts
# Started : 15/07/2023
# Developed By : Dr. Rajas Khokle
# Last Modified Date: 21/07/2023

# Import Libraries
import sys
import datetime as dt
import math
import logging
import time
import pandas as pd
import os
from api_helper import ShoonyaApiPy, get_time
import urllib
import json
import connections as conn
import numpy as np


# Get available Margins
def get_margins(user_api):
    limits = user_api.get_limits()
    df = pd.DataFrame(limits, index=[0, ])
    for col_name in df.columns.to_list():
        try:
            df[col_name] = df[col_name].astype('float')
        except ValueError:
            continue
    return df


def place_order_nse(user_api, bs, prod_type, tsym, quantity, price_type, price, trigger, remark):
    exchange = 'NSE'
    retention_duration = 'DAY'
    ret_data = user_api.place_order(buy_or_sell=bs, product_type=prod_type,
                                    exchange=exchange, tradingsymbol=tsym,
                                    quantity=quantity, discloseqty=0, price_type=price_type, price=price,
                                    trigger_price=trigger,
                                    retention=retention_duration, remarks=remark)
    print(ret_data)
    if ret_data is not None:
        if ret_data['stat'] == "Ok":
            # Store the order in database
            None
    return ret_data


path = "D:\Software_development\\"
# Connect to Shoonya
s_con_rad, ret_rad = conn.login_shoonya('Radhika')
s_con_vee, ret_vee = conn.login_shoonya('Veena')
s_con_pra, ret_pra = conn.login_shoonya('Prakash')
# s_con_raj, ret_raj = conn.login_shoonya('Rajas')
# s_con_anu, ret_anu = conn.login_shoonya('Anuradha')
# s_con_ree, ret_ree = conn.login_shoonya('Reema')

# Connect to Postgres
postgres_con = conn.connect_postgres('finance')
# User independent algo code is here
# Get data
# Symbol input queries
nse_query = '''SELECT * FROM stocks."NSE_symbols"'''
bse_query = '''SELECT * FROM stocks."BSE_symbols"'''
nifty_query = '''SELECT * FROM stocks."NIFTY50"'''
cds_query = '''SELECT * FROM stocks."CDS_symbols"'''
mcx_query = '''SELECT * FROM stocks."MCX_symbols"'''
nfo_query = '''Select * FROM stocks."NFO_symbols"'''
# Get current Nifty Value

# Define the security
security_type = 'options'
# Read token information file according to the derivative segment
if security_type == "options":
    security_exchange = "NSE"
    option_exchange = "NFO"
    # df_nse = pd.read_csv(path+"NSE_symbols.txt")  # Uncomment if postgresql server is not available
    df_nse = pd.read_sql(nse_query, postgres_con)
    # df_nfo = pd.read_csv(path+"NFO_symbols.txt")  # Uncomment if postgresql server is not available
    df_nfo = pd.read_sql(nfo_query, postgres_con)
    df_token = pd.concat([df_nse, df_nfo], ignore_index=True)
    base_security = "NIFTY INDEX"  # Should be changed to required index/stock
    if base_security in ['NIFTY INDEX', 'NIFTY BANK', 'FINNIFTY']:
        index_flag = True
    else:
        index_flag = False
elif security_type == "equity":
    security_exchange = "NSE"
    # df_token = pd.read_csv(path+"NSE_symbols.txt") # Uncomment if postgresql server is not available
    df_token = pd.read_sql(nse_query, postgres_con)
    base_security = "TCS-EQ"
elif security_type == "commodity":
    security_exchange = "MCX"
    # df_token = pd.read_csv(path+"MCX symbols.txt") # Uncomment if postgresql server is not available
    df_token = pd.read_sql(mcx_query, postgres_con)
elif security_type == "currency":
    security_exchange = "CDS"
    # df_token = pd.read_csv(path+"CDS_symbols.txt") # Uncomment if postgresql server is not available
    df_token = pd.read_sql(cds_query, postgres_con)

# Get the option chain Data

token_id = str(df_token[df_token['TradingSymbol'] == base_security]['Token'].iloc[0])
if security_type == "options":
    # Construct ATM Option trading symbol
    if index_flag:
        if base_security == "NIFTY INDEX":
            security_name = "NIFTY"
        elif base_security == "NIFTY BANK":
            security_name = "BANKNIFTY"
        elif base_security == "FINNIFTY":
            security_name = "FINNIFTY"
        else:
            print("INDEX NOT in list")
    df_expiry = pd.read_csv(path + 'weekly_expiry.csv')  # This file contains weekly expiry dates for Nifty Options
    df_expiry['expiry dates'] = df_expiry['expiry dates'].astype('datetime64[ns]')
    df_expiry['expiry_diff'] = (df_expiry - dt.datetime.today()) / np.timedelta64(1, "D")
    df_expiry = df_expiry[df_expiry['expiry_diff'] > 0]  # Get future expiry dates
    nearest_expiry = df_expiry[df_expiry['expiry_diff'] == df_expiry['expiry_diff'].min()]['expiry dates'].iloc[
        0].strftime("%d%b%y")
    # noinspection PyBroadException
    try:
        curr_sec_price = float(s_con_pra.get_quotes(exchange=security_exchange, token=token_id)["lp"])
    except:
        curr_sec_price = 17500
    nearest_lower_strike_price = math.floor(curr_sec_price / 50) * 50
    nearest_higher_strike_price = math.ceil(curr_sec_price / 50) * 50
    nearest_atm_strike_price = str(round(curr_sec_price / 50) * 50)
    atm_CE_option_tsym = (security_name + nearest_expiry + "C" + nearest_atm_strike_price).upper()
    atm_PE_option_tsym = (security_name + nearest_expiry + "P" + nearest_atm_strike_price).upper()
    chain = s_con_pra.get_option_chain(exchange=option_exchange, tradingsymbol=atm_PE_option_tsym,
                                       strikeprice=nearest_atm_strike_price, count=20)
    df_chain = pd.DataFrame(chain['values'])

    # Determine the ATM option pricing for CE and PE

    option_token_id = str(df_token[df_token['TradingSymbol'] == atm_CE_option_tsym]['Token'].iloc[0])
    atm_ce_data = s_con_pra.get_quotes(exchange=option_exchange, token=option_token_id)
    option_token_id = str(df_token[df_token['TradingSymbol'] == atm_PE_option_tsym]['Token'].iloc[0])
    atm_pe_data = s_con_pra.get_quotes(exchange=option_exchange, token=option_token_id)
    df_atm_data = pd.concat([pd.DataFrame(atm_ce_data, [0, ]), pd.DataFrame(atm_pe_data, [0, ])], ignore_index=True)

security_exchange = 'NSE'
security_token = '26000'
ret = s_con_pra.get_quotes(exchange=security_exchange, token=security_token)
curr_sec_price = float(s_con_pra.get_quotes(exchange=security_exchange, token=security_token)["lp"])
lp = float(ret['lp'])
atm_strike = round(lp / 50) * 50
# Find 3.5% away value and corresponding option symbols
percent = 0.035
minus_strike = round((atm_strike - percent * atm_strike) / 50) * 50
plus_strike = round((atm_strike + percent * atm_strike) / 50) * 50

# get option chain

# Create option symbols
# Get option pricing
# Calculate no. of lots based on margin available
# place orders


# Keep track of Profit and Loss

# square off position

# Function to place order

# Order Details

# Place Order

# Web FrontEnd

#
