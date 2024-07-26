"""Imports private data regarding the Database management system , call functions for the conext manager , downoading and injecting data """

from injector import Inject
from context_man import ContextManagerDB
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
try:
    db_user = os.getenv("user")
    db_pswd = os.getenv("password")
    db_host = os.getenv("host")
    database = os.getenv("database")
except Exception as e:
    print(f"an error occurred: {e}")

if __name__ == "__main__":
    with ContextManagerDB(db_user, db_pswd, db_host, database) as (cnx, cursor):
        injecting = Inject(cnx, cursor)
        injecting.create_table()
        all_rows = injecting.download()
        injecting.inject_data(all_rows)
