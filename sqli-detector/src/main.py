import pandas as pd
import tkinter as tk
from models_training import best_model
from feature_selector import select_features

light_gray = "#a8a4a3"
arial_14 = ("Arial", 14)


def find_user(_ = None):
    username = entry.get()
    if detect_sqli(username):
        result_label.config(text="Độc hại", fg="red")
    else:
        result_label.config(text="Lành tính", fg="green")


def detect_sqli(content: str) -> bool:
    features = select_features(content)
    result = best_model.predict(pd.DataFrame([features]))
    return result[0] == 1


def clear_input():
    entry.delete(0, "end")
    result_label.config(text="", fg="black")


root = tk.Tk()
root.title("Phát hiện SQLi")
root.geometry("400x200")

tk.Label(root, text="Nhập query", font=arial_14).pack(pady=8, padx=4)

entry = tk.Entry(root, font=arial_14)
entry.pack(pady=8)

buttons_frame = tk.Frame(root, border=0)
buttons_frame.pack(pady=8)
tk.Button(buttons_frame, text="Phát hiện", font=arial_14, command=find_user).pack(
    side="left", padx=8
)
root.bind("<Return>", find_user)  # Nhấn Enter để phát hiện
tk.Button(buttons_frame, text="Xoá", font=arial_14, command=clear_input).pack(
    side="left", padx=8
)

result_label = tk.Label(root, font=arial_14)
result_label.pack(pady=8)

root.mainloop()
