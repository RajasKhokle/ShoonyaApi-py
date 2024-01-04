import datetime as dt
# import math
# from api_helper import ShoonyaApiPy, get_time
# import json
import pandas as pd
import connections as conn
import numpy as np
import helper_functions as func
import requests as re

# Download the RBI file
RBI_URL = r"https://rbidocs.rbi.org.in/rdocs/Content/DOCs/SOVERIGNGOLDBONDS.xlsx"
RBI_Data = re.get(RBI_URL)
output = open('RBI_SGB_DATA.xlsx', 'wb')
output.write(RBI_Data.content)
output.close()
col_list = ['Tranche', 'ISIN ', 'Issue Date', 'Issue price/unit']
df = pd.read_excel("RBI_SGB_DATA.xlsx", skiprows=2, usecols=col_list)
# Get all the symbols for SGB
symbol = "SGB"
exchange = "NSE"
s_con_pra, ret_pra = conn.login_shoonya('Prakash')

path = "D:\Software_development\\"
df_nse = pd.read_csv(path + "NSE_symbols.txt")
df_nfo = pd.read_csv(path + "NFO_symbols.txt")
df_token = pd.concat([df_nse, df_nfo], ignore_index=True)
df_sgb = df_token[df_token['TradingSymbol'].str.contains("SGB")]
result = s_con_pra.get_quotes(exchange=exchange, token=df_sgb['Token'].iloc[0])
# Query the price and depth of all the SGBs

# Determine the best SGB to Buy
