from dotenv import load_dotenv
import os

load_dotenv()

API_KEYS = os.getenv('API_KEYS')
BIN_ID = '6829af148561e97a50166af7'
BASE_URL = os.getenv('BASE_URL')
X_Master_Key = os.getenv('X_Master_Key')
BASE_URL_OPEN_LIBRARY = os.getenv('BASE_URL_OPEN_LIBRARY')
SQLALCHEMY_DATABASE_URL=os.getenv('SQLALCHEMY_DATABASE_URL')