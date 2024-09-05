import mysql.connector
from mysql.connector import errorcode
from Sqlqueries import SqlQueries
from loggingMod import logger
from download import Download


class Inject:

    def __init__(self, cnx, cursor):

        self.cnx = cnx
        self.cursor = cursor

    def inject_data(self):

        data_insert_query = SqlQueries.data_insert_ready
        i = 1
        files = Download.download_files_only()

        for file_rows in Download.process_files(files):

            rows_to_insert = [
                (
                    obj.province_state,
                    obj.country_region,
                    obj.last_update,
                    obj.confirmed,
                    obj.deaths,
                    obj.recovered,
                    obj.active,
                    obj.incident_rate,
                    obj.case_fatality_ratio,
                )
                for obj in file_rows
            ]
            try:
                self.cursor.executemany(data_insert_query, rows_to_insert)
                self.cnx.commit()
                print(f"file {i} executed ")
                i += 1

            except mysql.connector.Error as e:
                self.cnx.rollback()
                print(f"Error found as {e} in  file {i}")
                i += 1
                continue
