"""This module is required for simplicity of the script and to prevent multiple lists of dictionaries from being used """

import datetime
from datetime import datetime


class CovidRowHandler:
    """
    Requires multiple attributes , each corresponding to one column in the database . The correponding attribute is then called upon when the object
    is converted into a tuple and executed
    """

    @classmethod
    def from_dict(cls, row_dict):
        return cls(
            province_state=row_dict.get("Province_State", None),
            country_region=row_dict.get("Country_Region", None),
            last_update=row_dict.get("Last_Update", None),
            confirmed=row_dict.get("Confirmed", None),
            deaths=row_dict.get("Deaths", None),
            recovered=row_dict.get("Recovered", None),
            active=row_dict.get("Active", None),
            incident_rate=row_dict.get("Incident_Rate", None),
            case_fatality_ratio=row_dict.get("Case_Fatality_Ratio", None),
        )

    def __init__(
        self,
        province_state=None,
        country_region=None,
        last_update=None,
        confirmed=None,
        deaths=None,
        recovered=None,
        active=None,
        incident_rate=None,
        case_fatality_ratio=None,
    ):
        self.province_state = province_state if not None else "N/A"
        self.country_region = country_region if not None else "N/A"
        self.last_update = self.clean_date(last_update)
        self.confirmed = confirmed if not None else 0
        self.deaths = deaths if not None else 0
        self.recovered = recovered if not None else 0
        self.active = active if not None else 0
        self.incident_rate = incident_rate if not None else 0
        self.case_fatality_ratio = case_fatality_ratio if not None else 0

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

    def __dir__(self):
        return [
            self.province_state,
            self.country_region,
            self.last_update,
            self.confirmed,
            self.deaths,
            self.recovered,
            self.active,
            self.incident_rate,
            self.case_fatality_ratio,
        ]
