import mysql.connector
from Sqlqueries import SqlQueries
from loggingMod import logger
import mysql.connector
from mysql.connector import errorcode


class ContextManagerDB:
    """
    Context manager in this instance is used for connection with the database covid_stats_db and imports credentials form the env file
    it automatically  opens and closes the connection with the database , preventing any issues in the programs
    """

    def __init__(self, user, password, host, database):
        self.config = {
            "user": user,
            "password": password,
            "host": host,
            "database": database,
        }

        self.cnx = None
        self.cursor = None

    def __enter__(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as e:
            print("Error :", e)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()

    def create_table(self):

        Table = SqlQueries.Create_Table

        try:
            logger.info("Creating table")
            self.cursor.execute(Table)
            logger.info("Table created successfully")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logger.error("the table already exists")
            else:
                logger.error("Error message: %s", err)
