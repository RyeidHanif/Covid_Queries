import mysql.connector


configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()

query = ("SELECT Country_Region , SUM(Active) AS Total_Active_Cases FROM covid_stats WHERE Active = 0  GROuP BY Country_Region")

cursor.execute(query)
result = cursor.fetchall()
for tuple in result : 
    print(tuple)

cursor.close()
cnx.close