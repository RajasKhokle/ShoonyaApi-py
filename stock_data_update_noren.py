import pandas as pd
import json
import time
from progressbar import ProgressBar
import connections

# Database Connection
conn = connections.connect_postgres(db_name='finance')
api, ret_data = connections.login_shoonya()
# API credentials

# TODO: Implement getting data for the days for which there is no data in the db
# TODO: Implement getting IEOD data for indexes and watchlist
# try:
#     df_max_ts = pd.read_sql('''SELECT max("TS") as "TS","Stock_name"
#                FROM stocks.shoonya_stocks group by "Stock_name"''', conn)
#     db_flag = True
# except Exception as E:
#     db_flag = False
#     print(E)

# Get historical data from the moment it is not present in the db

# Open websocket and start adding the data to the db

# start of our program
# Get the list of symbols in NSE
path = "D:\Software_development\\"
df_nse = pd.read_csv(path+'NSE_symbols.txt')
df_bse = pd.read_csv(path+'BSE_symbols.txt')
nse_symbols = df_nse['Symbol'].to_list()
bse_symbols = df_bse['Symbol'].to_list()
all_symbols = nse_symbols + bse_symbols
nifty_50_symbols = pd.read_csv('NIFTY50.csv')
symbols_in_db = pd.read_sql("SELECT distinct stock_name from stocks.shoonya_stocks", conn)
symbols_not_in_db = df_nse[~df_nse['Symbol'].isin(symbols_in_db['stock_name'])]['Symbol'].to_list()
# Get Daily data of given symbol
df_sym_data_list = []
exchange_name = 'NSE'
pb = ProgressBar()
for tsym in pb(symbols_not_in_db[0:5]):
    print("Downloading ", tsym)
    try:
        ret = api.get_daily_price_series(exchange=exchange_name, tradingsymbol=tsym, startdate=0)
    except:
        print('Cannot get data for ',tsym)
        continue
    data_list = []
    for line in ret:
        row = json.loads(line)
        data_list.append(row)
    df = pd.DataFrame(data_list)
    df['stock_name'] = tsym
    df['Exchange'] = exchange_name
    df_sym_data_list.append(df)
    time.sleep(5)

df_all_data = pd.concat(df_sym_data_list)
df_all_data['time'] = df_all_data['time'].astype('datetime64')
api.logout()
df_all_data.to_sql('shoonya_stocks', conn, index=False, if_exists='replace')