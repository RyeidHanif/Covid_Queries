import mysql.connector


configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()

query = ("""
        SELECT Country_Region , Province_State , Confirmed
        FROM covid_stats
        WHERE Country_Region = 'Pakistan'

         """)

cursor.execute(query)

result = cursor.fetchall()
for row in result : 
    print(row)


cursor.close()
cnx.close()