import tkinter as tk
from models_training import best_model
from feature_selector import select_features


def detect_sqli(event=None):
    sentence = entry.get()
    features = select_features(sentence)
    result = best_model.predict([list(features.values())])  # type: ignore
    if result[0] == 1:
        label.config(text="độc hại", fg="red")
    else:
        label.config(text="lành tính", fg="green")


def clear_input():
    entry.delete(0, "end")
    label.config(text="(chưa xác định)", fg="#a8a4a3")


root = tk.Tk()
root.title("SQLi Detection")
root.geometry("400x240")

tk.Label(root, text="Nhập câu bất kỳ", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

buttons_frame = tk.Frame(root, border=0)
buttons_frame.pack(pady=10)
tk.Button(
    buttons_frame, text="Phát hiện", font=("Arial", 14), command=detect_sqli
).pack(side="left", padx=10)
root.bind("<Return>", detect_sqli)  # Nhấn Enter để phát hiện
tk.Button(buttons_frame, text="Xoá", font=("Arial", 14), command=clear_input).pack(
    side="left", padx=10
)


lables_frame = tk.LabelFrame(root, border=0)
lables_frame.pack(pady=10)
tk.Label(lables_frame, text="Trạng thái: ", font=("Arial", 14)).pack(side="left")
label = tk.Label(lables_frame, text="(chưa xác định)", font=("Arial", 14), fg="#a8a4a3")
label.pack(side="left")

root.mainloop()
