from os.path import isfile
from sqlite3 import connect

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./dat/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()
