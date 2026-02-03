import os
import mysql.connector

def get_db_and_cursor():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT")),
        autocommit=True,
        connection_timeout=5
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor
