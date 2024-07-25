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
            data_dict[new_key] = data_dict[
                old_key
            ]  # Add the new key with the same value
            del data_dict[old_key]  # Remove the old key

    def download(self):
        response = requests.get(API_URL)
        files = response.json()
        all_rows = []

        for file_info in files:
            file_rows = []

            if file_info["type"] == "file":  # checking if hte type is file
                file_name = file_info[
                    "name"
                ]  # for every file in al the thousand files name is the date
                print(f"The current file being processed is : {file_name}")
                if ".csv" in  file_name:
                    download_url = file_info[
                        "download_url"
                    ]  # need download url , use strio to then convert it to file like object
                    file_response = requests.get(download_url)
                    file_response = (
                        file_response.text
                    )  # convert it into a string to be processed by string io
                    file = StringIO(file_response)
                    csv_dict_read = csv.DictReader(
                        file
                    )  # converts it into a list of dictionaries

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
            batch = rows_to_insert[i:i + batch_size]
            try:
                self.cursor.executemany(data_insert_query, batch)
                self.cnx.commit()
                print(f"Batch {i // batch_size + 1} inserted successfully")
            except mysql.connector.Error as e:
                print(f"Error found as {e}")
                self.cnx.rollback()
