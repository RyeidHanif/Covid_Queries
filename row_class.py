"""This module is required for simplicity of the script and to prevent multiple lists of dictionaries from being used """

import datetime
from datetime import datetime


class CovidRowHandler:
    """
    Requires multiple attributes , each corresponding to one column in the database . The correponding attribute is then called upon when the object
    is converted into a tuple and executed
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

    def __init__(
        self,
        Province_State=None,
        Country_Region=None,
        Last_Update=None,
        Confirmed=None,
        Deaths=None,
        Recovered=None,
        Active=None,
        Incident_Rate=None,
        Case_Fatality_Ratio=None,
    ):
        self.Province_State = Province_State if not None else "N/A"
        self.Country_Region = Country_Region if not None else "N/A"
        self.Last_Update = self.clean_date(Last_Update)
        self.Confirmed = Confirmed if not None else 0
        self.Deaths = Deaths if not None else 0
        self.Recovered = Recovered if not None else 0
        self.Active = Active if not None else 0
        self.Incident_Rate = Incident_Rate if not None else 0
        self.Case_Fatality_Ratio = Case_Fatality_Ratio if not None else 0

    def clean_date(self, date_str):
        """
        in many CSV filles,  dates are in a plethora of different formats which MySql does not accept. Theyn eed to be converted first
        to the official datetiime format which this function does .
        Returns the date in the format : yyyy-mm-dd hh:mm:ss with zero padding
        """
        if not date_str:
            return "1970-02-03 11:59:59"

        try:
            if "T" in date_str:

                parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            elif "/" in date_str and len(date_str) > 10:

                parsed_date = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
            elif "/" in date_str:

                parsed_date = datetime.strptime(date_str, "%Y/%m/%d")
            elif "-" in date_str and len(date_str) > 10:

                parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:

                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")

            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "1970-02-03 11:59:59"
