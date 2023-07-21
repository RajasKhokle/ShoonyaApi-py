# Place Concurrent Orders for different shoonya accounts
# Started : 15/07/2023
# Developed By : Dr. Rajas Khokle
# Last Modified Date: 21/07/2023

# Import Libraries
import sys
import datetime
import logging
import time
import pandas as pd
import os
from api_helper import ShoonyaApiPy, get_time
import urllib
import json
import connections as con

# Connect to Shoonya
s_con_rad, ret_rad = con.login_shoonya('Radhika')
s_con_vee, ret_vee = con.login_shoonya('Veena')
s_con_pra, ret_pra = con.login_shoonya('Prakash')
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
