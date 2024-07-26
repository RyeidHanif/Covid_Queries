API_URL = "https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports"

COLS_NEEDED = [
    "province_state",
    "country_region",
    "last_update",
    "confirmed",
    "active",
    "deaths",
    "recovered",
    "incident_rate",
    "case_fatality_ratio",
]
COLUMNS_STR = ", ".join(COLS_NEEDED)
