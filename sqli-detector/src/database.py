from dotenv import dotenv_values
import mysql.connector

def get_users_by_username(username):
    db_connector = mysql.connector.connect(
        host="localhost", user="root", password="", database="shopping_web_db"
    )
    db_cursor = db_connector.cursor()
    db_cursor.execute(f"SELECT * FROM user WHERE username LIKE '%{username}%'")
    users = db_cursor.fetchall()
    db_connector.close()
    return users