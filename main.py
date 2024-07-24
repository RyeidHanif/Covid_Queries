import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os
import traceback
from Sqlqueries import SqlQueries
from injection import Inject
from context_man import ContextManagerDB




if __name__ == '__main__':
    with ContextManagerDB() as (cnx, cursor):
        injecting = Inject(cnx,cursor)
        injecting.create_table()
        injecting.inject_data()
        
