import mysql.connector

configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()
query = ("SELECT SUM(Deaths) AS total_global_deaths FROM covid_stats")
cursor.execute(query)

result = cursor.fetchall()

print(f"The total global deaths are : {result}")

cursor.close()
cnx.close()
