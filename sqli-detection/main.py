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


root = tk.Tk()
root.title("SQLi Detection")
root.geometry("400x240")

tk.Label(root, text="Nhập câu bất kỳ", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

tk.Button(root, text="Phát hiện", font=("Arial", 14), command=detect_sqli).pack(pady=10)
root.bind("<Return>", detect_sqli) # Nhấn Enter để phát hiện

lableFrame = tk.LabelFrame(root, border=0)
lableFrame.pack(pady=10)
tk.Label(lableFrame, text="Trạng thái: ", font=("Arial", 14)).pack(side="left")
label = tk.Label(lableFrame, text="(chưa xác định)", font=("Arial", 14), fg="#a8a4a3")
label.pack(side="left")

root.mainloop()
