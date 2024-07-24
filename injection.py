import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values
import traceback
from Sqlqueries import SqlQueries
import datetime


load_dotenv()


class Inject :
    def __init__(self, cnx , cursor):
        #debug print statements
        
        
        self.cnx = cnx
        self.cursor = cursor
        self.cols_needed = [
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

        self.columns_str = ", ".join(self.cols_needed)
        

    
    def clean_data(self, df):
        cols_drop = ["FIPS", "Admin2", "Lat", "Long_", "Combined_Key"]
        df = df.drop(cols_drop, axis=1, errors = 'ignore')
        df["Country_Region"] = df["Country_Region"].fillna("NA")
        df["Province_State"] = df["Province_State"].fillna("NA")
        df["Last_Update"] = pd.to_datetime(df["Last_Update"], errors='coerce')
        df["Last_Update"] = df["Last_Update"].fillna(pd.NaT)
        df = df.fillna(0)
        return df
    
    def create_table(self):
        Table = SqlQueries.Create_Table

        try:
            print("Creating table {}".format(Table), "\n")
            self.cursor.execute(Table)
            print("Table created successfully")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("the table already exists")
            else:
                print("Error message", err)

    
    def inject_data(self):
        dir_path = r"C:\Users\ryeid.hanif_arbisoft\Covid_Queries\covid_files"
       
        for file_name in os.listdir(dir_path) :
                if file_name.endswith('csv'):
                    file_path = os.path.join(dir_path, file_name)
                    print(f"the current file being processed is {file_name}")

                    try:
                        df = pd.read_csv(file_path)
                    except Exception as e:
                        print(f"Error reading {file_name}: {e}")
                        continue
                    

                    if not all(col in df.columns for col in self.cols_needed):
                        print("this is a special case : handling it differently")
                        df_spec = pd.read_csv(file_path)

                        df = self.handle_spec_case_1(df_spec)

                    df = self.clean_data(df)
                    try:
                        for index, row in df.iterrows():
                            if pd.isna(row['Last_Update']):
                                continue
                            if index == 0 or index == 1:
                                continue
                            row = tuple(row)
                            data_insert = SqlQueries.data_insert_ready
                            data_to_be_inserted = row
                    
                            self.cursor.execute(data_insert, data_to_be_inserted)
                    except mysql.connector.errors.IntegrityError:
                            print(f"Data Duplication row : {row} will not be injected")
                            continue
                    except mysql.connector.Error as err:
                            print("An error occurred while execution :", err)

                    except FileNotFoundError as Fe:
                            print("your file was not found ", Fe)
            
                    except Exception as e:
                            print("an error occurred ", e)
                        
                else:
                    continue

                self.cnx.commit()

    def handle_spec_case_1(self,df):
        df = df.rename(columns = {
            "Province/State": "Province_State",
            "Country/Region": "Country_Region",
            "Last Update": "Last_Update",

        })

        df['Last_Update'] = pd.to_datetime(df['Last_Update'], format='%m/%d/%Y %H:%M', errors='coerce')
        df['Last_Update'] = df['Last_Update'].dt.strftime('%Y-%m-%d %H:%M:%S')

        for col in self.cols_needed:
             if col not in df.columns:
                df[col] = None
        return df 
    
