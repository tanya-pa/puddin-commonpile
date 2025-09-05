import gzip
import pickle

with gzip.open("../samples/arxiv_sample.pkl.gz", "rb") as f:
    df = pickle.load(f)

print(f"Sample size: {len(df)}")
print("Columns:", df.columns.tolist())
print("\nFirst row:\n", df.iloc[0])