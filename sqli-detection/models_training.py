import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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

# 3. Chia dataset thành tập train và tập test
x_train, x_test, y_train, y_test = train_test_split(
    df.drop("label", axis=1), df["label"], test_size=0.2
)

# 4. Huấn luyện mô hình Random Forest
random_forest = RandomForestClassifier(n_estimators=80)
random_forest.fit(x_train, y_train)

# 4. Đánh giá mô hình bằng confusion matrix
y_predict = random_forest.predict(x_test)
cm_df = pd.crosstab(y_test, y_predict, rownames=[""], colnames=[""])
print(cm_df.to_string(index=True, header=True), "\n")
cm = cm_df.to_numpy()
tp = cm[0][0]
fn = cm[0][1]
fp = cm[1][0]
tn = cm[1][1]
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * precision * recall / (precision + recall)
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 score: {f1_score}")
