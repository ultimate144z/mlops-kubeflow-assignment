import pandas as pd

# Download the insurance dataset from a public URL (Kaggle or GitHub mirror)
url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
df = pd.read_csv(url)

df.to_csv("data/insurance.csv", index=False)
print("Insurance dataset saved to data/insurance.csv")