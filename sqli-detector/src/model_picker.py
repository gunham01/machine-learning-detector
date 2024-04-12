import csv
import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import CategoricalNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from feature_selector import select_features


def extract_feature_from_csv_filepath(filepath):
    # Đọc dataset
    training_dataset = pd.read_csv(
        filepath,
        encoding="UTF-16",
        sep=",",
        engine="python",
        quoting=csv.QUOTE_NONE,
        na_filter=False,
        on_bad_lines=lambda arr: [",".join(arr[:-1]), arr[-1]],
    )
    # Trích xuất các đặc trưng
    extracted_features = []
    for _, row in training_dataset.iterrows():
        selected_features = select_features(row["Sentence"])
        selected_features["label"] = row["Label"]
        extracted_features.append(selected_features)

    return extracted_features


training_dataset_filepaths = [
    "../dataset/sqliv2.csv",
]
features_filepath = "../dataset/selected_features.csv"
features_list = []
for filepath in training_dataset_filepaths:
    extracted_features = extract_feature_from_csv_filepath(filepath)
    features_list.extend(extracted_features)

df = pd.DataFrame(features_list)
# df.to_csv(features_filepath, index=False)

x_train = df.drop("label", axis=1)
y_train = df["label"]

estimators = {
    # "Naive Bayes": {
    #     "model": MultinomialNB(),
    #     "params": {
    #         "alpha": [0.1] + list(x / 2 for x in range(1, 11)),
    #         "fit_prior": [True, False],
    #     },
    # },
    # "KNN": {
    #     "model": KNeighborsClassifier(),
    #     "params": {
    #         "n_neighbors": list(range(1, 51)),
    #         "weights": ["uniform", "distance"],
    #     },
    # },
    # "Logistic Regression": {
    #     "model": LogisticRegression(),
    #     "params": {
    #         "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    #         "penalty": ["l1", "l2", "elasticnet"],
    #         "max_iter": [1000],
    #     },
    # },
    # "Decision Tree": {
    #     "model": DecisionTreeClassifier(),
    #     "params": {
    #         "criterion": ["gini", "entropy"],
    #         "max_depth": np.arange(3, 15),
    #     },
    # },
    "Random Forest": {
        "model": RandomForestClassifier(),
        "params": {
            "n_estimators": list(x * 10 for x in range(1, 11)),
            "bootstrap": [True, False],
            "min_samples_leaf": list(x for x in range(1, 11)),
        },
    },
}

shuffle_split = ShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for estimatorName in estimators:
    estimator = estimators[estimatorName]
    grid_search = GridSearchCV(
        estimator=estimator["model"],
        param_grid=estimator["params"],
        scoring="f1",
        cv=shuffle_split,
        verbose=3,
        n_jobs=-1,
    )
    grid_search.fit(x_train, y_train)

    best_params = grid_search.best_params_
    print(f"{estimatorName}: {best_params}")
