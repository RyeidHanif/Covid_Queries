import mysql.connector


configuration = {

    'user' : 'root',
    'password': 'Crispy16crackers' , 
    'host' : 'localhost',
    'database': 'covid_stats_db'
}

cnx = mysql.connector.connect(**configuration)
cursor = cnx.cursor()

query = (
           " SELECT Country_Region, SUM(confirmed) AS total_confirmed FROM covid_stats GROUP BY Country_Region ORDER BY total_confirmed DESC LIMIT 2;"
    )

cursor.execute(query)
results = cursor.fetchall()

# Print the results
for row in results:
    print(f"Country: {row[0]}, Total Confirmed: {row[1]}")


cursor.close()
cnx.close()