import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

#database connection
#You need a .env file with user and password
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='flight_game',
        user= os.getenv("user"),
        passwd=os.getenv("password"),
        autocommit=True
    )
    cursor = connection.cursogr()
    print("Connection established")
except mysql.connector.errors.ProgrammingError:
    print("Error connecting to database")