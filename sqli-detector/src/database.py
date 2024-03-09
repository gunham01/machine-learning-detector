from dotenv import dotenv_values
import mysql.connector

db_connector = mysql.connector.connect(host="localhost", user="root", password="")


def init():
    global db_connector
    db_cursor = db_connector.cursor()
    # Tạo database nếu chưa tồn tại
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS shopping_web_db")
    db_connector.close()

    db_connector = mysql.connector.connect(
        host="localhost", user="root", password="", database="shopping_web_db"
    )
    db_cursor = db_connector.cursor()
    # Tạo bảng user nếu chưa tồn tại
    db_cursor.execute(
        "CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))"
    )
    db_cursor.execute("SELECT COUNT(*) FROM user")
    count = db_cursor.fetchone()[0]  # type: ignore
    if count == 0:  # Nếu chưa có user nào trong database
        # Thêm dữ liệu mẫu
        db_cursor.execute(
            "INSERT INTO user (username, password) VALUES ('admin', 'admin'), ('user', 'user'), ('guest', 'guest')"
        )
        print(db_cursor.rowcount, "record(s) inserted.")

    db_connector.commit()
    db_connector.close()


def get_users_by_username(username):
    db_connector = mysql.connector.connect(
        host="localhost", user="root", password="", database="shopping_web_db"
    )
    db_cursor = db_connector.cursor()

    if dotenv_values()["SHOULD_USE_PREPARED_STATEMENT"] == "1":
        db_cursor.execute(
            "SELECT * FROM user WHERE username LIKE %s", (f"%{username}%",)
        )
    else:
        db_cursor.execute(f"SELECT * FROM user WHERE username LIKE '%{username}%'")

    users = db_cursor.fetchall()
    db_connector.close()
    return users


init()
