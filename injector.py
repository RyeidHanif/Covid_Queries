"""
This Module is responsible for first downloading every file using the API Key , converting it into a string , then a file like object and processing it 
the download function then injects the list of objects of the CovidHandler class into the covid database 
"""

import mysql.connector
from mysql.connector import errorcode
from Sqlqueries import SqlQueries
import datetime
from constants import API_URL
import logging
import requests
from io import StringIO
import csv
from datetime import datetime
from row_class import CovidRowHandler

logger = logging.getLogger()

logging.basicConfig(level=logging.INFO)


class Inject:
    """
    The inject class takes in attributes for initialization cnx and cursor , both of which are required for communication with the database
    They are not declared here but in the context manager to automatically enter and close the connection when required
    """

    cols_needed = [
        "Province_State",
        "Country_Region",
        "Last_Update",
        "Confirmed",
        "Active",
        "Deaths",
        "Recovered",
        "Incident_Rate",
        "Case_Fatality_Ratio",
    ]
    columns_str = ", ".join(cols_needed)

    def __init__(self, cnx, cursor):

        self.cnx = cnx
        self.cursor = cursor

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

    def rename_key(self, data_dict, old_key, new_key):
        if old_key in data_dict:
            data_dict[new_key] = data_dict[old_key]
            del data_dict[old_key]

    def download(self):
        """
        Each file is downloaded one by one .  A list of dictionaries (files) is iterated over to get the download URL for each file
        Each file is then converted to a string using .text and then a stringio object . The reason for that is t oallow the file to be processed
        without downloading it into the local disk .
        Returns a list of objects , with each object being a row in a file . in total 3.5 million objects
        the format is : [obj1 ,obj2 obj3]"
        """
        response = requests.get(API_URL)
        files = response.json()
        all_rows = []

        for file_info in files:
            file_rows = []

            if file_info["type"] == "file":
                file_name = file_info["name"]
                print(f"The current file being processed is : {file_name}")
                if ".csv" in file_name:
                    download_url = file_info["download_url"]
                    file_response = requests.get(download_url)
                    file_response = file_response.text
                    file = StringIO(file_response)
                    csv_dict_read = csv.DictReader(file)

                    for each_row in csv_dict_read:
                        keys = list(each_row.keys())
                        if "/" in keys[0] or "/" in keys[1]:
                            each_row["Active"] = 0
                            each_row["Incident_Rate"] = 0.0
                            each_row["Case_Fatality_Ratio"] = 0.0
                            self.rename_key(
                                each_row, "Province/State", "Province_State"
                            )
                            self.rename_key(
                                each_row, "Country/Region", "Country_Region"
                            )
                            self.rename_key(each_row, "Last Update", "Last_Update")

                        record = CovidRowHandler(
                            each_row.get("Province_State", None),
                            each_row.get("Country_Region", None),
                            each_row.get("Last_Update", None),
                            each_row.get("Confirmed", None),
                            each_row.get("Deaths", None),
                            each_row.get("Recovered", None),
                            each_row.get("Active", None),
                            each_row.get("Incident_Rate", None),
                            each_row.get("Case_Fatality_Ratio", None),
                        )
                        file_rows.append(record)
                    all_rows.extend(file_rows)
        return all_rows

    def inject_data(self, total_rows, batch_size=1000):
        """
        During data injecction , a batchsize of a 1000 is used to divide the rows into smaller parts so the system does not get overwhelmed with millions
        of execute and commit requests . This also allows for better debugging and print statements to tell which batch is being injected
        """
        data_insert_query = SqlQueries.data_insert_ready

        rows_to_insert = [
            (
                obj.Province_State,
                obj.Country_Region,
                obj.Last_Update,
                obj.Confirmed,
                obj.Deaths,
                obj.Recovered,
                obj.Active,
                obj.Incident_Rate,
                obj.Case_Fatality_Ratio,
            )
            for obj in total_rows
        ]

        total_count = len(rows_to_insert)
        for i in range(0, total_count, batch_size):
            batch = rows_to_insert[i : i + batch_size]
            try:
                self.cursor.executemany(data_insert_query, batch)
                self.cnx.commit()
                print(f"Batch {i // batch_size + 1} inserted successfully")
            except mysql.connector.Error as e:
                print(f"Error found as {e}")
                self.cnx.rollback()
