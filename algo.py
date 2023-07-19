# Place Concurrent Orders for different shoonya accounts
# Started : 15/07/2023
# Developed By : Dr. Rajas Khokle
# Last Modified Date: 15/07/2023

# Import Libraries
import sys
import datetime
import logging
import time
import yaml
import pandas as pd
import pyotp
import os

sys.path.extend([r'C:\Users\khokl\OneDrive\Documents\pyproj\ShoonyaApi-py'])
from api_helper import ShoonyaApiPy, get_time

api = ShoonyaApiPy()


# Setup Shoonya Connection Details
# credentials
def login_shoonya(user='radhika'):
    user = user.lower()
    match user:
        case 'radhika':
            token = os.getenv('SHOONYA_TOTP_TOKEN_RAD')
            user = os.getenv("USER_ID_FIN_RAD")
            pwd = os.getenv("USER_PWD_FIN_RAD")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_RAD')
            app_key = os.getenv('SHOONYA_API_KEY_RAD')
            imei = os.getenv('SHOONYA_IMEI_RAD')

        case 'prakash':
            token = os.getenv('SHOONYA_TOTP_TOKEN_PRA')
            user = os.getenv("USER_ID_FIN_PRA")
            pwd = os.getenv("USER_PWD_FIN_PRA")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_PRA')
            app_key = os.getenv('SHOONYA_API_KEY_PRA')
            imei = os.getenv('SHOONYA_IMEI_PRA')

        case 'veena':
            token = os.getenv('SHOONYA_TOTP_TOKEN_VEE')
            user = os.getenv("USER_ID_FIN_VEE")
            pwd = os.getenv("USER_PWD_FIN_VEE")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_VEE')
            app_key = os.getenv('SHOONYA_API_KEY_VEE')
            imei = os.getenv('SHOONYA_IMEI_VEE')

        case 'reema':
            token = os.getenv('SHOONYA_TOTP_TOKEN_REE')
            user = os.getenv("USER_ID_FIN_REE")
            pwd = os.getenv("USER_PWD_FIN_REE")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_REE')
            app_key = os.getenv('SHOONYA_API_KEY_REE')
            imei = os.getenv('SHOONYA_IMEI_REE')

        case 'rajas':
            token = os.getenv('SHOONYA_TOTP_TOKEN_RAJ')
            user = os.getenv("USER_ID_FIN_RAJ")
            pwd = os.getenv("USER_PWD_FIN_RAJ")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_RAJ')
            app_key = os.getenv('SHOONYA_API_KEY_RAJ')
            imei = os.getenv('SHOONYA_IMEI_RAJ')

        case 'anuradha':
            token = os.getenv('SHOONYA_TOTP_TOKEN_ANU')
            user = os.getenv("USER_ID_FIN_ANU")
            pwd = os.getenv("USER_PWD_FIN_ANU")
            factor2 = pyotp.TOTP(token).now()
            vc = os.getenv('SHOONYA_VC_ANU')
            app_key = os.getenv('SHOONYA_API_KEY_ANU')
            imei = os.getenv('SHOONYA_IMEI_ANU')

    # make the api call

    ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    if ret is not None:
        print("User ", user, "Logged In:", ret['stat'])
    return ret


# Setup database Connection Details

# Connect to Database


# Connect to Shoonya
s_con_rad = login_shoonya('Radhika')
# Function to place order

# Order Details

# Place Order

# Web FrontEnd

#
