
import os
import gzip
import json
import pickle
import stanza
import pandas as pd
from tqdm import tqdm

# Initialize Stanza pipeline (English)
stanza.download("en")
nlp = stanza.Pipeline("en", tokenize_no_ssplit=True, use_gpu=False)

# Load sample
sample_path = "../../samples/arxiv_sample.pkl.gz"
output_path = "../../parsed/arxiv_parsed.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

print(f"Loading sample from {sample_path}")
with gzip.open(sample_path, "rb") as f:
    df = pickle.load(f)

print(f"Sample loaded with {len(df)} entries.")
print(f"Parsing and saving output to {output_path}")

with open(output_path, "w", encoding="utf-8") as out_f:
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = row["text"]
        doc_id = row["id"]
        metadata = row.get("metadata", {})
        title = metadata.get("title", "")
        authors = metadata.get("authors", "")

        # Run Stanza on abstract text
        doc = nlp(text)

        parsed_sentences = []
        for sentence in doc.sentences:
            tokens = [word.text for word in sentence.words]
            parsed_sentences.append(tokens)

        # Write one JSON per entry
        parsed_entry = {
            "id": doc_id,
            "title": title,
            "authors": authors,
            "sentences": parsed_sentences
        }
        out_f.write(json.dumps(parsed_entry) + "\n")

print("Parsing complete.")
