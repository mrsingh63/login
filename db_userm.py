# db_userm.py or db_connection.py
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Groot@#1234",
        database="admin_db"
    )
    return connection

def fetch_all_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    connection.close()
    return data

def delete_record(record_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (record_id,))
    connection.commit()
    connection.close()
