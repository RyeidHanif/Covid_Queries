import mysql.connector


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

        return self.cnx, self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()
