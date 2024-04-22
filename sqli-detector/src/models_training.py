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
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


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

selected_features_indices = json.load(open("selected_features_index.json"))

# Lưu tập huấn luyện với những đặc trưng đã chọn vào file csv
x_train = x_train.iloc[:, selected_features_indices]
train_data = pd.concat([x_train, y_train], axis=1)
train_data.to_csv("../dataset/selected_features_short.csv", index=False)


models = {
    "Naive Bayes": MultinomialNB(),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "Logistic Regression": LogisticRegression(max_iter=400, random_state=42),
    "Decission Tree": DecisionTreeClassifier(
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=94,
        n_jobs=-1,
        random_state=42,
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
    cm_df = pd.crosstab(y_test, y_predict, rownames=[""], colnames=[""])
    printable_cm = cm_df.to_string()
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    f1 = f1_score(y_test, y_predict)
    training_time = end_time - start_time
    return printable_cm, accuracy, precision, recall, f1, training_time


highest_f1 = 0
best_model = None
best_model_name = ""
for model_name, model in models.items():
    cm, accuracy, precision, recall, f1, training_time = score_model(model)
    print(f"{model_name}:")
    print(cm)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 score: {f1}")
    print(f"Time: {round(training_time, ndigits=6)}s")
    print("\n")

    if f1 > highest_f1:
        highest_f1 = f1
        best_model = model
        best_model_name = model_name

print(f"Thuật toán tốt nhất: {best_model_name}")
