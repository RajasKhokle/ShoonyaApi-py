# Place Concurrent Orders for different shoonya accounts
# Started : 15/07/2023
# Developed By : Dr. Rajas Khokle
# Last Modified Date: 21/07/2023

# Import Libraries
import sys
import datetime
import logging
import time
import yaml
import pandas as pd
import pyotp
import os
from api_helper import ShoonyaApiPy, get_time
from breeze_connect import BreezeConnect
import urllib
import json
from sqlalchemy import create_engine
import mysql.connector as connection  # pip install mysql-connector-python


# Setup Shoonya Connection Details
# TODO : Get the password and API details from the database and decrypt using pepper stored in windows env variable

def login_shoonya(user_string='Prakash'):
    user_string = user_string.upper()[0:3]
    # API credentials
    token = os.getenv('SHOONYA_TOTP_TOKEN_' + user_string)
    user = os.getenv('USER_ID_FIN_' + user_string)
    pwd = os.getenv('USER_PWD_FIN_' + user_string)
    factor2 = pyotp.TOTP(token).now()
    vc = os.getenv('SHOONYA_VC_' + user_string)
    app_key = os.getenv('SHOONYA_API_KEY_' + user_string)
    imei = os.getenv('SHOONYA_IMEI_' + user_string)
    api = ShoonyaApiPy()
    try:
        ret_data = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    except Exception as E:
        print("Following Exception has occurred - ", E)
    return api, ret_data


def login_icici(user='veena'):
    user = user.upper()[0:3]
    secret_key = os.getenv('ICICI_SECRET_KEY_' + user)
    app_key = os.getenv('ICICI_APP_KEY_' + user)

    # Initialize SDK
    breeze = BreezeConnect(api_key=app_key)

    # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY Incase your api-key
    # has special characters(like +,=,!) then encode the api key before using in the url as shown below.

    print("https://api.icicidirect.com/apiuser/login?api_key=" + urllib.parse.quote_plus(app_key))
    session_key = "16110341"
    # Generate Session
    breeze.generate_session(api_secret=secret_key,
                            session_token=session_key)
    return breeze


# Setup database Connection Details

# Connect to Database
def connect_postgres(db_name='finance'):
    postgres_login = os.getenv('postgres_login')
    postgres_pwd = os.getenv("postgres_pwd")
    postgres_port = '5432'
    postgres_host = "localhost"
    db_name = 'finance'
    conn_string = 'postgresql://' + postgres_login + ":" + postgres_pwd + "@" + postgres_host + ":" + postgres_port + \
                  "/" + db_name
    db = create_engine(conn_string)
    conn = db.connect()
    return conn


def connect_mysql(db_name='trading'):
    mysql_host = "localhost"
    mysql_user = "shoonya"
    mysql_password = os.getenv("MYSQL_SHOONYA_PWD")
    mysql_password = "Shoonya@123"
    mysql_port = '2603'
    try:
        mydb = connection.connect(host=mysql_host, database=db_name, user=mysql_user, passwd=mysql_password,
                                  use_pure=True, port=mysql_port)
        return mydb

    except Exception as e:

        print("Cannot connect to Mysql Db : ", str(e))


# Connect to Shoonya
s_con_rad, ret_rad = login_shoonya('Radhika')
s_con_vee, ret_vee = login_shoonya('Veena')
s_con_pra, ret_pra = login_shoonya('Prakash')
# Get data
# Get current Nifty Value
security_exchange = 'NSE'
security_token = '26000'
ret = s_con_rad.get_quotes(exchange=security_exchange, token=security_token)
lp = float(ret['lp'])
atm_strike = round(lp / 50) * 50
# Find 3.5% away value and corresponding option symbols
percent = 0.035
minus_strike = round((atm_strike - percent * atm_strike) / 50) * 50
plus_strike = round((atm_strike + percent * atm_strike) / 50) * 50

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
