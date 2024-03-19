from dotenv import load_dotenv, dotenv_values
import pandas as pd

# Cảnh báo nếu chưa có file .env
load_dotenv(verbose=True)

import database
import tkinter as tk
from models_training import best_model
from feature_selector import select_features

light_gray = "#a8a4a3"
arial_14 = ("Arial", 14)


def find_user(event=None):
    username = entry.get()
    if username == "":
        user_list_title_label.config(text="Username không được để trống", fg="red")
        user_list_cotent_label.config(text="")
        return

    should_detect_sqli = dotenv_values()["SHOULD_DETECT_SQLI"] == "1"
    if should_detect_sqli and detect_sqli(username):
        user_list_title_label.config(text="Đầu vào chưa hợp lệ", fg="red")
        user_list_cotent_label.config(text="")
        return

    users = database.get_users_by_username(username)
    users_str_arr = (str(user) for user in users)
    user_list_title_label.config(text="Danh sách người dùng:", fg="black")
    if users:
        user_list_cotent_label.config(text="\n".join(users_str_arr), fg="green")
    else:
        user_list_cotent_label.config(text="Không tìm thấy", fg="red")


def detect_sqli(content: str) -> bool:
    features = select_features(content)
    result = best_model.predict(pd.DataFrame([features]))
    return result[0] == 1


def clear_input():
    entry.delete(0, "end")
    user_list_title_label.config(text="Danh sách người dùng:", fg="black")
    user_list_cotent_label.config(text="(trống)", fg=light_gray)


root = tk.Tk()
root.title("Tìm kiếm người dùng")
root.geometry("400x280")

tk.Label(root, text="Nhập username", font=arial_14).pack(pady=8, padx=4)

entry = tk.Entry(root, font=arial_14)
entry.pack(pady=8)

buttons_frame = tk.Frame(root, border=0)
buttons_frame.pack(pady=8)
tk.Button(buttons_frame, text="Tìm kiếm", font=arial_14, command=find_user).pack(
    side="left", padx=8
)
root.bind("<Return>", find_user)  # Nhấn Enter để phát hiện
tk.Button(buttons_frame, text="Xoá", font=arial_14, command=clear_input).pack(
    side="left", padx=8
)

user_list_title_label = tk.Label(root, text="Danh sách người dùng:", font=arial_14)
user_list_title_label.pack(pady=8)
user_list_cotent_label = tk.Label(root, text="(trống)", font=arial_14, fg=light_gray)
user_list_cotent_label.pack(pady=8)

root.mainloop()
