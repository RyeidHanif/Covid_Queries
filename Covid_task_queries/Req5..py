import mysql.connector


configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()

query = ("SELECT Country_Region , SUM(Case_Fatality_Ratio)/ COUNT(Province_State) AS Total_Case_Fatal_Ratio_c FROM covid_stats GROUP BY CountrY_Region ORDER BY Total_Case_Fatal_Ratio_c DESC LIMIT 10")

cursor.execute(query)

result = cursor.fetchall()
for row in result:
    print(row)


cursor.close()
cnx.close()