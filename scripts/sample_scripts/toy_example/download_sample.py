"""
download_sample.py:
- testing Hugging Face's 'datasets' by loading sample Common Pile filtered subset
- save as csv and jsonl
"""

from datasets import load_dataset
import pandas as pd
import os

# Set output directory
subset = "common-pile/arxiv_abstracts_filtered"
save_dir = "sample_outputs"
os.makedirs(save_dir, exist_ok=True)

# Load dataset (streaming=False to download) 
ds = load_dataset(subset, split="train")  # all subsets use split="train"

# Take 1K sample
sample = ds.shuffle(seed=42).select(range(1000))
df = pd.DataFrame(sample)

# Save as CSV or JSONL
csv_path = os.path.join(save_dir, "arxiv_abstracts_sample.csv")
jsonl_path = os.path.join(save_dir, "arxiv_abstracts_sample.jsonl")
df.to_csv(csv_path, index=False)
df.to_json(jsonl_path, orient="records", lines=True)