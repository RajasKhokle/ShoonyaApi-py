# Place Concurrent Orders for different shoonya accounts
# Started : 22/07/2023
# Developed By : Dr. Rajas Khokle
# Last Modified Date: 23/07/2023

# Import Libraries
import datetime as dt
# import math
# from api_helper import ShoonyaApiPy, get_time
# import json
import pandas as pd
import connections as conn
import numpy as np
import helper_functions as func

func.update_symbol_files()  # First update all the symbol files

# Connect to Postgres/mysql
try:
    mysql_conn = conn.connect_mysql()
    db_flag = True
except Exception as e:
    print("Cannot connect to MYSQL Server. IF you proceed, this transaction will not be recorded by the system.", e)
    db_flag = False
# postgres_con = conn.connect_postgres('finance')
path = "D:\Software_development\\"
# Connect to Shoonya
s_con_rad, ret_rad = conn.login_shoonya('Radhika')
s_con_vee, ret_vee = conn.login_shoonya('Veena')
s_con_pra, ret_pra = conn.login_shoonya('Prakash')
# s_con_raj, ret_raj = conn.login_shoonya('Rajas')
# s_con_anu, ret_anu = conn.login_shoonya('Anuradha')
# s_con_ree, ret_ree = conn.login_shoonya('Reema')

# User independent algo code is here
# Symbol input queries
nse_query = '''SELECT * FROM trading.nse_symbols'''
bse_query = '''SELECT * FROM trading.bse_symbols'''
nifty_query = '''SELECT * FROM trading.nifty50'''
cds_query = '''SELECT * FROM trading.cds_symbols'''
mcx_query = '''SELECT * FROM trading.mcx_symbols'''
nfo_query = '''Select * FROM trading.nfo_symbols'''
# Get current Nifty Value

# Define the security
security_type = 'options'
security_exchange = "NSE"
option_exchange = "NFO"
if db_flag:
    df_nse = pd.read_sql(nse_query, mysql_conn)
    df_nfo = pd.read_sql(nfo_query, mysql_conn)
else:
    df_nse = pd.read_csv(path + "NSE_symbols.txt")
    df_nfo = pd.read_csv(path + "NFO_symbols.txt")

df_token = pd.concat([df_nse, df_nfo], ignore_index=True)
base_security = "NIFTY INDEX"  # Should be changed to required index/stock
if base_security in ['NIFTY INDEX', 'NIFTY BANK', 'FINNIFTY']:
    index_flag = True
else:
    index_flag = False

# Get the token id of the security
token_id = str(df_token[df_token['TradingSymbol'] == base_security]['Token'].iloc[0])
# Security name is needed as base_security is the name present as Trading Symbol in db
# while security name is required for constructing the symbol name of the derivative contract

if base_security == "NIFTY INDEX":
    security_name = "NIFTY"
elif base_security == "NIFTY BANK":
    security_name = "BANKNIFTY"
elif base_security == "FINNIFTY":
    security_name = "FINNIFTY"
else:
    print("INDEX NOT in list")
    security_name = base_security
# Get the expiry dates
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
# nearest_lower_strike_price = math.floor(curr_sec_price / 50) * 50
# nearest_higher_strike_price = math.ceil(curr_sec_price / 50) * 50
nearest_atm_strike_price = str(round(curr_sec_price / 50) * 50)
atm_PE_option_tsym = (security_name + nearest_expiry + "P" + nearest_atm_strike_price).upper()
# chain = s_con_pra.get_option_chain(exchange=option_exchange, tradingsymbol=atm_PE_option_tsym,
#                                    strikeprice=nearest_atm_strike_price, count=15)
# df_chain = pd.DataFrame(chain['values'])
# print(df_chain)
atm_strike = round(curr_sec_price / 50) * 50
# Find 3.5% away value and corresponding option symbols
percent = 0.025
minus_strike = round((atm_strike - percent * atm_strike) / 50) * 50
plus_strike = round((atm_strike + percent * atm_strike) / 50) * 50
minus_pe_sym = (security_name + nearest_expiry + "P" + str(minus_strike)).upper()
plus_ce_sym = (security_name + nearest_expiry + "C" + str(plus_strike)).upper()
print('CE Strike : ', plus_strike)
print('PE Strike : ', minus_strike)

# Get option pricing
pe_token_id = str(df_token[df_token['TradingSymbol'] == minus_pe_sym]['Token'].iloc[0])
ce_token_id = str(df_token[df_token['TradingSymbol'] == plus_ce_sym]['Token'].iloc[0])
quote_pe = s_con_pra.get_quotes(exchange=option_exchange, token=pe_token_id)
quote_ce = s_con_pra.get_quotes(exchange=option_exchange, token=ce_token_id)
curr_pe_price = float(quote_pe["lp"])
curr_ce_price = float(quote_ce["lp"])
print('CE Strike : ', plus_strike, " @ price ", curr_ce_price)
print('PE Strike : ', minus_strike, " @ price ", curr_pe_price)
place_limit_order(sym=minus_pe_sym, lmt_price=curr_pe_price, action="S")

# Calculate no. of lots based on margin available and margin required
# place orders


# Keep track of Profit and Loss

# square off position

# Function to place order

# Order Details

# Place Order

# Web FrontEnd

# TODO: Function for trailing Stop Loss
# TODO: Function for updating the tick data in database
# TODO: Function for detecting the momentum and generating the buy and sell signals
# TODO: Function to calculate the option greeks
# TODO: Function for bet sizing according to the margins available
#
