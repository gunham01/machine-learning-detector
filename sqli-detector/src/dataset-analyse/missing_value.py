import sys

sys.path.append("../")
from dataset_reader import read_dataset

# Fit DBSCAN to the data
data = read_dataset("../../dataset/sqliv2.csv")
data.info()
