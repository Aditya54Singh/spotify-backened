import mysql.connector

def get_db_and_cursor():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Motog42",
        database="spotify_clone",
        autocommit=True
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor
