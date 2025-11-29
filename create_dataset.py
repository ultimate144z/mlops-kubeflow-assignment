from sklearn.datasets import fetch_california_housing
import pandas as pd

# Load
data = fetch_california_housing(as_frame=True)
df = data.frame

df.to_csv("data/raw_data.csv", index=False)
print("Dataset saved to data/raw_data.csv")