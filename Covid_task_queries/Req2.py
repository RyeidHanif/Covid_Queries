import mysql.connector
import datetime

configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()

query = ("SELECT Country_Region , Province_State , Confirmed , Deaths  FROM covid_stats WHERE Last_Update BETWEEN  %s  AND %s LIMIT 100")
date1 = datetime.date(2021 , 11 , 3)
date2 = datetime.date(2022, 11, 3)
cursor.execute(query, (date1 ,date2))

for (Country_Region , Province_State , Confirmed , Deaths) in cursor :
    print(f"Here : {Country_Region}: {Province_State} : Confirmed Cases , {Confirmed} , Deaths : {Deaths}") 