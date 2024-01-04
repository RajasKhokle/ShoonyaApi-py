import pandas as pd
import connections as conn
import helper_functions as func

path = "D:\Software_development\\"
security_type = 'options'
security_exchange = "NSE"
option_exchange = "NFO"
base_security = "NIFTY INDEX"
security_name = "NIFTY"

# Connect to Shoonya
s_con_rad, ret_rad = conn.login_shoonya('Radhika')
# s_con_vee, ret_vee = conn.login_shoonya('Veena')
s_con_pra, ret_pra = conn.login_shoonya('Prakash')
s_con_raj, ret_raj = conn.login_shoonya('Rajas')
s_con_anu, ret_anu = conn.login_shoonya('Anuradha')
s_con_ree, ret_ree = conn.login_shoonya('Reema')

# Create Symbol and Token Library
func.update_symbol_files()  # First update all the symbol files
df_nse = pd.read_csv(path + "NSE_symbols.txt")
df_nfo = pd.read_csv(path + "NFO_symbols.txt")
df_token = pd.concat([df_nse, df_nfo], ignore_index=True)
token_id = str(df_token[df_token['TradingSymbol'] == base_security]['Token'].iloc[0])

# Get the expiry dates
df_expiry = pd.read_csv(path + 'weekly_expiry.csv')  # This file contains weekly expiry dates for Nifty Options
df_expiry['expiry dates'] = df_expiry['expiry dates'].astype('datetime64[ns]')
df_expiry['expiry_diff'] = (df_expiry - dt.datetime.today()) / np.timedelta64(1, "D")
df_expiry = df_expiry[df_expiry['expiry_diff'] > 0]  # Get future expiry dates
nearest_expiry = df_expiry[df_expiry['expiry_diff'] == df_expiry['expiry_diff'].min()]['expiry dates'].iloc[
    0].strftime("%d%b%y")

# Get the current price of Nifty
nifty_current_price = float(s_con_pra.get_quotes(exchange=security_exchange, token=token_id)["lp"])
atm_strike = round(nifty_current_price / 50) * 50
# Find 3.5% away value and corresponding option symbols
percent = 0.035
minus_strike = round((atm_strike - percent * atm_strike) / 50) * 50
plus_strike = round((atm_strike + percent * atm_strike) / 50) * 50
minus_pe_sym = (security_name + nearest_expiry + "P" + str(minus_strike)).upper()
plus_ce_sym = (security_name + nearest_expiry + "C" + str(plus_strike)).upper()
print('CE Strike : ', plus_strike)
print('PE Strike : ', minus_strike)

# place sell market order and GTT order
# monitor for GTT order trigger
# Place another sell order
