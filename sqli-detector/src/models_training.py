import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from feature_selector import select_features


def join_all_except_last(arr):
    return [",".join(arr[:-1]), arr[-1]]


# 1. Đọc dataset
filepath = "../dataset/sqliv2.csv"
dataset = pd.read_csv(
    filepath,
    encoding="UTF-16",
    sep=",",
    engine="python",
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
df.to_csv("../dataset/selected_features.csv", index=False)

# 3. Chia dataset thành tập train và tập test
x_train, x_test, y_train, y_test = train_test_split(
    df.drop("label", axis=1), df["label"], test_size=0.2
)

# Tập hợp các mô hình
models = {
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "Logistic Regression": LogisticRegression(),
    "Decission Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=80),
}

# 4. Huấn luyện các mô hình
for model in models.values():
    model.fit(x_train, y_train)


# 5. Đánh giá các mô hình bằng ma trận nhầm lẫn, accuracy, precision, recall, và F1 score
def score_model(model):
    y_predict = model.predict(x_test)
    cm_df = pd.crosstab(y_test, y_predict, rownames=[""], colnames=[""])
    printable_cm = cm_df.to_string(index=True, header=True)
    cm = cm_df.to_numpy()
    tp = cm[0][0]
    fn = cm[0][1]
    fp = cm[1][0]
    tn = cm[1][1]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * precision * recall / (precision + recall)

    return printable_cm, accuracy, precision, recall, f1_score


highest_f1_score = 0
best_model = None
best_model_name = ""
for model_name, model in models.items():
    cm, accuracy, precision, recall, f1_score = score_model(model)
    print(f"{model_name}:")
    print(cm)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 score: {f1_score}")
    print("\n")

    if f1_score > highest_f1_score:
        highest_f1_score = f1_score
        best_model = model
        best_model_name = model_name

print(f"Thuật toán tốt nhất: {best_model_name}")
