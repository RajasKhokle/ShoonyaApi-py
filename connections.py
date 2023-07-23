from api_helper import ShoonyaApiPy
import pyotp
import os
from breeze_connect import BreezeConnect
import urllib
from sqlalchemy import create_engine  # pip install psycopg2, pymysql,mysql-connector
import mysql.connector as connection  # pip install mysql-connector-python


# Setup Shoonya Connection Details
# TODO : Get the password and API details from the database and decrypt using salt from db and
#  pepper from windows keyring using Argon2id

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
        print("Connected Successfully to ", user)
        return api, ret_data
    except Exception as E:
        print("Following Exception has occurred - ", E)
        return None


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
    conn_string = 'postgresql://' + postgres_login + ":" + postgres_pwd + "@" + postgres_host + ":" + postgres_port + \
                  "/" + db_name
    db = create_engine(conn_string)
    conn = db.connect()
    return conn


def connect_mysql(db_name='trading'):
    mysql_host = "localhost"
    mysql_user = "root"
    mysql_password = os.getenv("MYSQL_SHOONYA_PWD")
    mysql_password = "Orion_777"
    mysql_port = '2603'
    try:
        db_connection_str = 'mysql+pymysql://' + mysql_user + ':' + mysql_password + '@' + mysql_host + ':' + \
                            mysql_port + '/' + db_name
        db_connection = create_engine(db_connection_str)
        return db_connection
    except Exception as e:
        print("Cannot connect to Mysql Db : ", str(e))

    # try:
    #     mydb = connection.connect(host=mysql_host, database=db_name, user=mysql_user, passwd=mysql_password,
    #                               use_pure=True, port=mysql_port)
    #     return mydb


def connect_dhan(user):
    return None


def connect_ibkr(user):
    return None
