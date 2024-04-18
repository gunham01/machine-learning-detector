import pandas as pd
import csv
from feature_selector import select_features


def join_all_except_last(arr):
    return [",".join(arr[:-1]), arr[-1]]


# Hàm trích xuất các đặc trưng từ dataset trong file csv
def extract_features_from_dataset(filepath: str):
    # Đọc dataset
    training_dataset = pd.read_csv(
        filepath,
        encoding="UTF-16",
        sep=",",
        engine="python",
        quoting=csv.QUOTE_NONE,
        na_filter=False,
        on_bad_lines=join_all_except_last,
    )
    # Trích xuất các đặc trưng
    extracted_features = []
    for _, row in training_dataset.iterrows():
        selected_features = select_features(row["Sentence"])
        selected_features["label"] = row["Label"]
        extracted_features.append(selected_features)

    return extracted_features


def read_dataset(filepath):
    return pd.read_csv(
        filepath,
        encoding="UTF-16",
        sep=",",
        engine="python",
        quoting=csv.QUOTE_NONE,
        na_filter=False,
        on_bad_lines=join_all_except_last,
    )


# Hàm trích xuất các đặc trưng từ nhiều dataset
def extract_features_from_datasets(filepaths: list[str]):
    features_list = []
    for filepath in filepaths:
        extracted_features = extract_features_from_dataset(filepath)
        features_list.extend(extracted_features)
    return features_list

def split_features_to_data_and_label(features_list):
    df = pd.DataFrame(features_list)
    x = df.drop("label", axis=1)
    y = df["label"]
    return x, y