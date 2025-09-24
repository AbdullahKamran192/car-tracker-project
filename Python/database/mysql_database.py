import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

try:
    conn = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE")
    )

    if conn.is_connected():
        print("Connected to the database")
    else:
        print("Failed to connect to the database")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")

mycursor = conn.cursor()

mycursor.execute("""CREATE TABLE IF NOT EXISTS Cars (
                 registration_number VARCHAR(50),
                 Make VARCHAR(50), Colour VARCHAR(50),
                 time DATETIME
                 )
                 """)


def getCar(reg_number):
    sql = "SELECT * FROM Cars WHERE registration_number = %s"
    mycursor.execute(sql, (reg_number,))
    return mycursor.fetchall()


def insertCar(reg_number, make, colour):
    sql = "INSERT INTO Cars VALUES (%s,%s,%s, NOW())"
    mycursor.execute(sql, (reg_number, make, colour))
    conn.commit()

