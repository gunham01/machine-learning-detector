import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys

sys.path.append("../")
from dataset_reader import (
    extract_features_from_dataset,
    split_features_to_data_and_label,
)


def identify_outliers_iqr(data):
    outliers = np.zeros_like(data, dtype=bool)
    for col in range(data.shape[1]):
        col_data = data[:, col]
        Q1 = np.percentile(col_data, 25)
        Q3 = np.percentile(col_data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        col_outliers = (col_data < lower_bound) | (col_data > upper_bound)
        outliers[:, col] = col_outliers
    return outliers


def plot_outliers(data, outliers):
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(data)), data, color="blue", label="Data")
    plt.scatter(np.where(outliers)[0], data[outliers], color="red", label="Outliers")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Identified Outliers")
    plt.legend()
    plt.show()


# Example usage with pandas DataFrame
features = extract_features_from_dataset("../../dataset/sqli.csv")
x_train, y_train = split_features_to_data_and_label(features)
data = pd.concat([x_train, y_train], axis=1)

data_values = data.values
outliers = identify_outliers_iqr(data_values)
plot_outliers(data_values.flatten(), outliers.flatten())
