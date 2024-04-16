import sys
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier

sys.path.append("../")
from dataset_reader import read_datasets

x_train, y_train = read_datasets(["../../dataset/sqli.csv"])

best_i = best_f1 = 0
for i in range(1, 101):
    model = KNeighborsClassifier(n_neighbors=i, n_jobs=-1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_train)
    f1 = f1_score(y_train, y_pred)
    plt.scatter(i, f1, color="blue")

    if f1 > best_f1:
        best_i = i
        best_f1 = f1
    print(f"n_neighbors = {i}, F1 score = {f1}")

print(f"\nBest n_estimators = {best_i}, Best F1 score = {best_f1}")

plt.title("KNN")
plt.xlabel("n_estimators")
plt.ylabel("F1 score")
plt.grid(True)
plt.show()
