"""this module is needed to separate SQL queries from the rest of the programs for ease of understanding """

from constants import COLS_NEEDED, COLUMNS_STR


class SqlQueries:
    """
    contains 2 queries : one for creating the table with a unique constraint of three columns combined
    data insert then uses column string to assign column names and %s placeholders to add the tuple during the execution which contains the row's actual values
    """

    Create_Table = (
        "CREATE TABLE covid_stats ("
        "area_date_ID bigint PRIMARY KEY AUTO_INCREMENT, "
        "province_state varchar(100), "
        "country_region varchar(100), "
        "last_update datetime, "
        "confirmed bigint, "
        "active bigint, "
        "deaths bigint, "
        "recovered bigint, "
        "incident_rate float(13,3), "
        "case_fatality_ratio float(13,3), "
        "CONSTRAINT unique_cols UNIQUE (country_region, province_state, last_update)"
        ")"
    )

    data_insert_ready = (
        "INSERT IGNORE INTO covid_stats"
        f"({COLUMNS_STR} )"
        "VALUES (%s, %s, %s,%s,%s,%s,%s,%s, %s)"
    )
