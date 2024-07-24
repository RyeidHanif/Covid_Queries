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


class SqlQueries:

    Create_Table = (
        "CREATE TABLE covid_stats ("
        "area_date_ID bigint PRIMARY KEY AUTO_INCREMENT, "
        "Province_State varchar(100), "
        "Country_Region varchar(100), "
        "Last_Update datetime, "
        "Confirmed bigint, "
        "Active bigint, "
        "Deaths bigint, "
        "Recovered bigint, "
        "Incident_Rate float(13,3), "
        "Case_Fatality_Ratio float(13,3), "
        "CONSTRAINT unique_cols UNIQUE (Country_Region, Province_State, Last_Update)"
        ")"
    )

    data_insert_ready = (
        "INSERT IGNORE INTO covid_stats"
        f"({columns_str} )"
        "VALUES (%s, %s, %s,%s,%s,%s,%s,%s, %s)"
    )

