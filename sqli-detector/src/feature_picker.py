import json
from sklearn.ensemble import RandomForestClassifier
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

# Lọc các đặc trưng ít quan trọng
sfs = SequentialFeatureSelector(
    estimator=RandomForestClassifier(n_estimators=94, n_jobs=-1, random_state=42),
    n_features_to_select=12,
    # direction="forward",
    direction="backward",
    scoring="f1",
    n_jobs=-1,
    cv=10,
)

x_new = sfs.fit(x_train, y_train)
selected_features_indices = sfs.get_support(indices=True)
selected_features_names = x_train.columns[selected_features_indices]
with open("selected_features_index.json", "w") as file:
    json.dump(selected_features_indices.tolist(), file)
with open("selected_features_name.json", "w") as file:
    json.dump(selected_features_names.tolist(), file)
