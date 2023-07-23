import requests
import zipfile
import os
import connections
import pandas as pd


def update_symbol_files():
    root = 'https://shoonya.finvasia.com/'
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
            print("Invalid file",e)
        try:
            os.remove(zip_file)
            print(f'remove: {zip_file}')
        except FileNotFoundError:
            continue
    text_file_list = ['NSE_symbols.txt', 'NFO_symbols.txt', 'CDS_symbols.txt', 'MCX_symbols.txt', 'BSE_symbols.txt',
                      'NIFTY50.csv']
    # postgres_conn = connections.connect_postgres('finance')
    mysql_con = connections.connect_mysql()
    for filename in text_file_list:
        try:
            df = pd.read_csv(filename)
            # df.to_sql(filename[0:-4], postgres_conn, if_exists='replace', index=False)

            df.to_sql(filename[0:-4].lower(), mysql_con, if_exists='replace', index=False)
            print("Successfully updated table ", filename[0:-4])
        except Exception as e:
            print('Failed to update table ', filename[0:-4], 'Due to Error', e)


