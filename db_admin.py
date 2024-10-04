# db_admin.py
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Groot@#1234",
        database="admin_management"
    )
    return connection

def verify_admin(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    connection.close()
    return result
