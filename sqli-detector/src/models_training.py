import json
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from dataset_reader import (
    extract_features_from_dataset,
    extract_features_from_datasets,
)
from sklearn.metrics import (
    confusion_matrix,
)
from tabulate import tabulate


# 1. Đọc và trích xuất các đặc trưng từ các dataset
training_dataset_filepaths = [
    "../dataset/sqliv2.csv",
]
features_filepath = "../dataset/selected_features.csv"
features_list = extract_features_from_datasets(training_dataset_filepaths)

# 2. Lưu các đặc trưng đã trích xuất vào file csv
df = pd.DataFrame(features_list)
df.to_csv(features_filepath, index=False)

# 3. Huấn luyện các mô hình
# Tạo tập huấn luyện với đẩy đủ đặc trưng
x_train = df.drop("label", axis=1)
y_train = df["label"]


# Lưu tập huấn luyện với những đặc trưng đã chọn vào file csv
selected_features_indices = json.load(open("selected_features_index.json"))
x_train = x_train.iloc[:, selected_features_indices]
train_data = pd.concat([x_train, y_train], axis=1)
train_data.to_csv("../dataset/selected_features_short.csv", index=False)


models = {
    "Naive Bayes": MultinomialNB(),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "Logistic Regression": LogisticRegression(max_iter=400, random_state=34),
    "Decission Tree": DecisionTreeClassifier(
        random_state=34,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=94,
        n_jobs=-1,
        random_state=34,
    ),
}


for model in models.values():
    model.fit(x_train, y_train)


# 5. Đánh giá các mô hình bằng ma trận nhầm lẫn, accuracy, precision, recall, và F1 score
# Tạo tập kiểm thử
testing_dataset_filepath = "../dataset/sqli.csv"
testing_dataset_features_list = extract_features_from_dataset(testing_dataset_filepath)
testing_df = pd.DataFrame(testing_dataset_features_list)
x_test = testing_df.drop("label", axis=1)
x_test = x_test[x_train.columns]
y_test = testing_df["label"]


# Hàm đánh giá 1 mô hình bằng ma trận
# nhầm lẫn, accuracy, precision, recall, và F1 score
def score_model(model):
    start_time = time.time()
    y_predict = model.predict(x_test)
    end_time = time.time()
    cm = confusion_matrix(y_test, y_predict)
    fn = cm[1][0]
    tp = cm[1][1]
    fp = cm[0][1]
    tn = cm[0][0]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    fnr = fn / (fn + tp)
    fpr = fp / (tn + fp)

    training_time = end_time - start_time
    return cm, accuracy, precision, recall, f1, training_time, fpr, fnr


def print_cm(cm):
    table_data = [
        ["", 0, 1],
        [0, cm[0][0], cm[0][1]],
        [1, cm[1][0], cm[1][1]],
    ]
    print(tabulate(table_data, tablefmt="fancy_grid"))


highest_f1 = 0
best_model = None
best_model_name = ""
for model_name, model in models.items():
    cm, accuracy, precision, recall, f1, training_time, fpr, fnr = score_model(model)
    print(f"{model_name}:")
    print_cm(cm)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"FPR: {fpr}")
    print(f"FNR: {fnr}")
    print(f"F1 score: {f1}")
    print(f"Time: {round(training_time, ndigits=6)}s")
    print("\n")

    if f1 > highest_f1:
        highest_f1 = f1
        best_model = model
        best_model_name = model_name

print(f"Thuật toán tốt nhất: {best_model_name}")
