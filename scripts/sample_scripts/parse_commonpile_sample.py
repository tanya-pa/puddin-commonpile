
import gzip
import pickle

# Load sample
with gzip.open("/share/compling/projects/tp389/commonpile/samples/arxiv_sample.pkl.gz", "rb") as f:
    df = pickle.load(f)

print(f"Loaded {len(df)} documents from Common Pile sample.\n")

# Inspect a few entries
for i, row in df.iterrows():
    doc_id = row["id"]
    text = row["text"]
    source = row["source"]
    metadata = row.get("metadata", {})

    print(f"Doc {i} — ID: {doc_id}, Source: {source}")
    print(f"Text (truncated): {text[:300]!r}")
    print("-" * 60)

    if i >= 4:
        break  # Only print first 5