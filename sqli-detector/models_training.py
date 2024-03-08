import pandas as pd
from feature_selector import select_features
import csv


def join_all_except_last(arr):
    return [",".join(arr[:-1]), arr[-1]]


# 1. Đọc dataset
filepath = "dataset/sqliv2.csv"
dataset = pd.read_csv(
    filepath,
    encoding="UTF-16",
    na_filter=False,
    sep=",",
    nrows=5,
    quoting=csv.QUOTE_NONE,
    on_bad_lines=join_all_except_last,
)

# 2. Trích chọn đặc trưng
features_list = []
for index, row in dataset.iterrows():
    selected_features = select_features(row["Sentence"])
    selected_features["label"] = row["Label"]
    features_list.append(selected_features)
df = pd.DataFrame(features_list)
df.to_csv("dataset/selected_features.csv", index=False)
