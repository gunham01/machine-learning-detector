import pandas as pd
import csv
from feature_selector import select_features


def join_all_except_last(arr):
    return [",".join(arr[:-1]), arr[-1]]


# Hàm trích xuất các đặc trưng từ dataset trong file csv
def extract_features_from_filepath(filepath):
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

def read_dataset(filepath, csv_to_write=None):
    features_list = extract_features_from_filepath(filepath)

    df = pd.DataFrame(features_list)
    if csv_to_write is not None:
        df.to_csv(csv_to_write, index=False)

    x_set = df.drop("label", axis=1)
    y_set = df["label"]

    return x_set, y_set

# Hàm trích xuất các đặc trưng từ nhiều dataset
def read_datasets(filepaths, csv_to_write=None):
    features_list = []
    for filepath in filepaths:
        extracted_features = extract_features_from_filepath(filepath)
        features_list.extend(extracted_features)

    df = pd.DataFrame(features_list)
    if csv_to_write is not None:
        df.to_csv(csv_to_write, index=False)

    x_set = df.drop("label", axis=1)
    y_set = df["label"]

    return x_set, y_set
