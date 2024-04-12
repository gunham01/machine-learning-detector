import mysql.connector


def get_users_by_username(username):
    db_connector = mysql.connector.connect(
        host="localhost", user="root", password="", database="shopping_web_db"
    )
    db_cursor = db_connector.cursor()
    query_str = f"SELECT * FROM user WHERE username LIKE '%{username}%'"
    print(query_str)
    db_cursor.execute(query_str)
    users = db_cursor.fetchall()
    db_connector.close()
    return users
