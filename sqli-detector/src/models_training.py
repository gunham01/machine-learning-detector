import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from feature_selector import select_features
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


# Hàm join tất cả các cột ngoại trừ cột cuối cùng
def join_all_except_last(arr):
    return [",".join(arr[:-1]), arr[-1]]


# Hàm trích xuất các đặc trưng từ dataset trong file csv
def extract_feature_from_csv_filepath(filepath):
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
    for _, row in training_dataset.iterrows():
        selected_features = select_features(row["Sentence"])
        selected_features["label"] = row["Label"]
        features_list.append(selected_features)

    return features_list


# 1. Đọc và trích xuất các đặc trưng từ các dataset
training_dataset_filepaths = [
    "../dataset/sqliv2.csv",
]
features_filepath = "../dataset/selected_features.csv"
features_list = []
for filepath in training_dataset_filepaths:
    features_list.extend(extract_feature_from_csv_filepath(filepath))

# 2. Lưu các đặc trưng đã trích xuất vào file csv
df = pd.DataFrame(features_list)
df.to_csv(features_filepath, index=False)

# 3. Huấn luyện các mô hình
# Tạo tập huấn luyện
x_train = df.drop("label", axis=1)
y_train = df["label"]


models = {
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decission Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=80),
}
for model in models.values():
    model.fit(x_train, y_train)


# 5. Đánh giá các mô hình bằng ma trận nhầm lẫn, accuracy, precision, recall, và F1 score
# Tạo tập kiểm thử
testing_dataset_filepath = "../dataset/sqli.csv"
testing_dataset_features_list = extract_feature_from_csv_filepath(
    testing_dataset_filepath
)
testing_df = pd.DataFrame(testing_dataset_features_list)
x_test = testing_df.drop("label", axis=1)
y_test = testing_df["label"]


# Hàm đánh giá 1 mô hình bằng ma trận
# nhầm lẫn, accuracy, precision, recall, và F1 score
def score_model(model):
    y_predict = model.predict(x_test)
    cm_df = pd.crosstab(y_test, y_predict, rownames=[""], colnames=[""])
    printable_cm = cm_df.to_string()
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    f1 = f1_score(y_test, y_predict)
    return printable_cm, accuracy, precision, recall, f1


highest_f1 = 0
best_model = None
best_model_name = ""
for model_name, model in models.items():
    cm, accuracy, precision, recall, f1 = score_model(model)
    print(f"{model_name}:")
    print(cm)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 score: {f1}")
    print("\n")

    if f1 > highest_f1:
        highest_f1 = f1
        best_model = model
        best_model_name = model_name

print(f"Thuật toán tốt nhất: {best_model_name}")
