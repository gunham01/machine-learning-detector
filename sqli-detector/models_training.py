import pandas as pd
from feature_selector import select_features


# 1. Đọc dataset
filepath = "dataset/sqli.csv"
dataset = pd.read_csv(
    filepath,
    encoding="UTF-16",
    sep=",",
)

# 2. Trích chọn đặc trưng
features_list = []
for index, row in dataset.iterrows():
    selected_features = select_features(row["Sentence"])
    selected_features["label"] = row["Label"]
    features_list.append(selected_features)
df = pd.DataFrame(features_list)
df.to_csv("dataset/selected_features.csv", index=False)
