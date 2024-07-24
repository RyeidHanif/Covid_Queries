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

query1 = ("""
        ALTER TABLE covid_stats
        ADD COLUMN increase_active
""")

query2 

query3 



cursor.close()
cnx.close()
