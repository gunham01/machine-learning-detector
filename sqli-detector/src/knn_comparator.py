import sys
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

sys.path.append("../")
from dataset_reader import (
    extract_features_from_dataset,
    split_features_to_data_and_label,
)

features = extract_features_from_dataset("../dataset/sqli.csv")
x_train, y_train = split_features_to_data_and_label(features)

best_i = best_f1 = 0
x = []
y = []
for i in range(1, 101):
    model = KNeighborsClassifier(n_neighbors=i, n_jobs=-1)
    results = cross_val_score(
        model,
        x_train,
        y_train,
        cv=KFold(n_splits=10, random_state=42, shuffle=True),
        scoring=make_scorer(f1_score),
        n_jobs=-1,
        verbose=3,
    )
    f1 = results.mean()
    x.append(i)
    y.append(f1)

    if f1 > best_f1 and i > 2:
        best_i = i
        best_f1 = f1
    print(f"n_neighbors = {i}, F1 score = {f1}")

print(f"\nBest n_neighbors = {best_i}, Best F1 score = {best_f1}")

plt.plot(x, y, "o-")
plt.scatter(i, f1, color="blue")
plt.scatter(i, f1, color="blue")
plt.title("KNN")
plt.xlabel(f"n_neighbors\n\nBest n_neighbors = {best_i}, Best F1 score = {best_f1}")
plt.ylabel("F1 score")
plt.grid(True)
plt.show()
