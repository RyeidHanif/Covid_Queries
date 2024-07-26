from constants import API_URL
import requests
from row_class import CovidRowHandler
from io import StringIO
import csv


class Download:

    def rename_key(data_dict, old_key, new_key):
        if old_key in data_dict:
            data_dict[new_key] = data_dict[old_key]
            del data_dict[old_key]

    def check_spec_case(each_row):
        keys = list(each_row.keys())
        if "/" in keys[0] or "/" in keys[1]:
            each_row["Active"] = 0
            each_row["Incident_Rate"] = 0.0
            each_row["Case_Fatality_Ratio"] = 0.0
            Download.rename_key(each_row, "Province/State", "Province_State")
            Download.rename_key(each_row, "Country/Region", "Country_Region")
            Download.rename_key(each_row, "Last Update", "Last_Update")

        return each_row

    def download_files_only():
        response = requests.get(API_URL)
        files = response.json()
        return files

    def process_files(files):

        for file in files:
            file_rows = []

            file_name = file["name"]
            print(f"The current file being processed is : {file_name}")
            if not file_name.endswith(".csv"):
                continue
            download_url = file["download_url"]
            file_response = requests.get(download_url)
            file_response = file_response.text
            file_strio = StringIO(file_response)
            csv_dict_read = csv.DictReader(file_strio)

            for each_row in csv_dict_read:
                each_row = Download.check_spec_case(each_row)
                record = CovidRowHandler.from_dict(each_row)
                file_rows.append(record)
            yield file_rows
