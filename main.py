"""Imports private data regarding the Database management system , call functions for the conext manager , downoading and injecting data """

from injector import Inject
from context_man import ContextManagerDB
from dotenv import load_dotenv, dotenv_values
import os
from download import Download
from loggingMod import logger

load_dotenv()
try:
    db_user = os.getenv("user")
    db_pswd = os.getenv("password")
    db_host = os.getenv("host")
    database = os.getenv("database")
except TypeError as e:
    print(f"Missing positional arguments in : {e}")

except Exception as e:
    logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    with ContextManagerDB(db_user, db_pswd, db_host, database) as db_manager:
        db_manager.create_table()
        injecting = Inject(db_manager.cnx, db_manager.cursor)
        injecting.inject_data()
