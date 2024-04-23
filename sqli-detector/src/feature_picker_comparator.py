from tabnanny import verbose
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from dataset_reader import (
    extract_features_from_dataset,
    split_features_to_data_and_label,
)
from sklearn.feature_selection import (
    SequentialFeatureSelector,
)

features = extract_features_from_dataset("../dataset/sqli.csv")
x_train, y_train = split_features_to_data_and_label(features)

testing_dataset_filepath = "../dataset/sqli.csv"
testing_dataset_features_list = extract_features_from_dataset(testing_dataset_filepath)
testing_df = pd.DataFrame(testing_dataset_features_list)
x_test = testing_df.drop("label", axis=1)
y_test = testing_df["label"]

x_graph, y_graph = [], []
best_feature_count, best_f1 = 0, 0
for feature_count in range(2, 18):
    sfs = SequentialFeatureSelector(
        estimator=KNeighborsClassifier(n_neighbors=3, n_jobs=-1),
        n_features_to_select=feature_count,
        # direction="forward",
        direction="backward",
        scoring="f1",
        n_jobs=3,
        cv=10,
    )

    x_new = sfs.fit(x_train, y_train)
    selected_features_indices = sfs.get_support(indices=True)
    x_train_new = x_train.iloc[:, selected_features_indices]
    x_test_new = x_test[x_train_new.columns]
    model = RandomForestClassifier(
        n_estimators=94,
        n_jobs=-1,
        random_state=34,
    )

    model.fit(x_train_new, y_train)
    y_pred = model.predict(x_test_new)
    f1 = f1_score(y_train, y_pred)

    x_graph.append(feature_count)
    y_graph.append(f1)

    print(f"Số đặc trưng = {feature_count}, F1 score = {f1}")
    if f1 > best_f1:
        best_feature_count = feature_count
        best_f1 = f1

plt.plot(x_graph, y_graph, "o-")
plt.scatter(x_graph, y_graph, color="blue")
plt.title("SBS")
plt.xlabel(
    f"Số đặc trưng\n\nSố đặc trưng tốt nhất = {best_feature_count}, F1 score tốt nhất = {best_f1}"
)
plt.ylabel("F1 score")
plt.grid(True)
plt.show()
