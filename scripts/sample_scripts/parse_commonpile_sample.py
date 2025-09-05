"""
parse_commonpile_sample.py
Sample unified pipeline for parsing Common Pile subsets into CoNLL-U format.
"""

import os
import gzip
import pickle
import argparse
import pandas as pd
from tqdm import tqdm
import stanza
from stanza.utils.conll import CoNLL
from datetime import datetime

# Default paths based on repo layout (see design doc)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "pile_tables")
CONLL_DIR = os.path.join(BASE_DIR, "conll")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure dirs exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONLL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Parse Common Pile samples to CoNLL-U format.")
    parser.add_argument(
        "--sample",
        type=str,
        required=True,
        help="Path to .pkl.gz sample (from load_commonpile.py).",
    )
    parser.add_argument(
        "--subset",
        type=str,
        default="arxiv",
        help="Subset name for output naming (ex. arxiv, github, pubmed).",
    )
    parser.add_argument(
        "--slice-size",
        type=int,
        default=9999,
        help="Rows per slice to process (default: 9999).",
    )
    parser.add_argument(
        "--use-gpu",
        action="store_true",
        help="Use GPU if available for Stanza.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Prepare output dirs
    subset_dir = os.path.join(CONLL_DIR, args.subset)
    os.makedirs(subset_dir, exist_ok=True)

    # Init stanza
    stanza.download("en")
    nlp = stanza.Pipeline("en", tokenize_no_ssplit=True, use_gpu=args.use_gpu)

    # Load sample
    print(f"[INFO] Loading sample from {args.sample}")
    with gzip.open(args.sample, "rb") as f:
        df = pickle.load(f)
    print(f"[INFO] Loaded {len(df)} rows.")

    # Slice processing
    total = len(df)
    slice_size = args.slice_size
    num_slices = (total + slice_size - 1) // slice_size
    print(f"[INFO] Processing {total} rows in {num_slices} slice(s).")

    meta_records = []

    for i in range(num_slices):
        start = i * slice_size
        end = min(start + slice_size, total)
        slice_df = df.iloc[start:end]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = os.path.join(subset_dir, f"{args.subset}_slice{i:04d}.conllu")

        print(f"[INFO] Processing slice {i+1}/{num_slices} → {out_file}")

        with open(out_file, "w", encoding="utf-8") as out_f:
            for _, row in tqdm(slice_df.iterrows(), total=len(slice_df)):
                text = row["text"]
                doc_id = row["id"]

                try:
                    doc = nlp(text)
                except Exception as e:
                    print(f"[WARN] Skipping doc {doc_id}: {e}")
                    continue

                # Convert stanza doc -> CoNLL
                conll = CoNLL.convert_dict(doc.to_dict())

                # Write header
                out_f.write(f"# newdoc id = {doc_id}\n")

                # Write each sentence in CoNLL-U format
                for sent in conll:
                    for idx, word in enumerate(sent, start=1):
                        out_f.write(
                            f"{idx}\t{word['text']}\t{word['lemma']}\t"
                            f"{word['upos']}\t{word['xpos']}\t{word['feats']}\t"
                            f"{word['head']}\t{word['deprel']}\t_\t"
                            f"start_char={word['misc'].get('start_char','_')}|end_char={word['misc'].get('end_char','_')}\n"
                        )
                    out_f.write("\n")

        # Add to metadata
        meta_records.append(
            {
                "subset": args.subset,
                "slice": i,
                "rows": len(slice_df),
                "output": out_file,
                "timestamp": timestamp,
            }
        )

    # Save meta index under info/
    info_dir = os.path.join(BASE_DIR, "info")
    os.makedirs(info_dir, exist_ok=True)
    meta_csv = os.path.join(info_dir, f"completed-{args.subset}_meta-index.csv")
    meta_df = pd.DataFrame(meta_records)
    meta_df.to_csv(meta_csv, index=False)

    print(f"[INFO] Completed parsing. Metadata saved to {meta_csv}")


if __name__ == "__main__":
    main()
