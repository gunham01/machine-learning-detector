from pprint import pprint
import pandas as pd
import tkinter as tk
from models_training import best_model
from feature_selector import select_features
from database import get_users_by_username
from mysql.connector import Error
from models_training import selected_features_indices

light_gray = "#a8a4a3"
arial_14 = ("Arial", 14)


def on_detect(_=None):
    username = entry.get()
    if detect_sqli(username):
        result_label.config(text="Độc hại", fg="red")
    else:
        result_label.config(text="Lành tính", fg="green")


def on_find_users(_=None):
    username = entry.get()
    try:
        users = get_users_by_username(username)
    except Error as e:
        # result_label.config(text=str(e.msg), fg="red")
        result_label.config(text="Không tìm thấy", fg="red")
        return

    users_str = [str(user) for user in users]
    if users:
        result_label.config(text="\n".join(users_str), fg="green")
    else:
        result_label.config(text="Không tìm thấy", fg="red")


def detect_sqli(content: str) -> bool:
    features = select_features(content)
    x_predict = pd.DataFrame([features]).iloc[:, selected_features_indices]
    result = best_model.predict(x_predict)
    return result[0] == 1


def clear_input():
    entry.delete(0, "end")
    result_label.config(text="", fg="black")


root = tk.Tk()
root.title("Phát hiện SQLi")
root.geometry("400x350")

tk.Label(root, text="Nhập query", font=arial_14).pack(pady=8, padx=4)

entry = tk.Entry(root, font=arial_14)
entry.pack(pady=8)

buttons_frame = tk.Frame(root, border=0)
buttons_frame.pack(pady=8)
tk.Button(buttons_frame, text="Phát hiện", font=arial_14, command=on_detect).pack(
    side="left", padx=8
)
tk.Button(buttons_frame, text="Tìm kiếm", font=arial_14, command=on_find_users).pack(
    side="left", padx=8
)
tk.Button(buttons_frame, text="Xoá", font=arial_14, command=clear_input).pack(
    side="left", padx=8
)

result_label = tk.Label(root, font=arial_14, wraplength=320)
result_label.pack(pady=8)

root.mainloop()
