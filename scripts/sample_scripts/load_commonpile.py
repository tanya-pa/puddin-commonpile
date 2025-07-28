"""
load_commonpile.py:
- loads filtered Common Pile subset using Hugging Face's 'datasets'
- extracts a sample (ex. 1000 rows)
- convert it to a Pandas DataFrame
- save it to disk as .pkl.gz file (compatible with parse_pile.py)
"""

import argparse
import pandas as pd
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser(description="Load Common Pile subset and save as .pkl.gz")
    parser.add_argument('--subset', type=str, default='arxiv_abstracts_filtered',
                        help='Name of the Common Pile filtered subset (ex. arxiv_abstracts_filtered)')
    parser.add_argument('--sample_size', type=int, default=1000,
                        help='Number of rows to sample from the dataset')
    parser.add_argument('--output', type=str, default='sample_commonpile.pkl.gz',
                        help='Output file name (.pkl.gz)')
    args = parser.parse_args()

    print(f"Loading dataset: {args.subset}")
    dataset = load_dataset(f'common-pile/{args.subset}', split='train')

    print(f"Sampling {args.sample_size} rows...")
    df = dataset.shuffle(seed=42).select(range(min(args.sample_size, len(dataset)))).to_pandas()

    print(f"Saving to {args.output}")
    df.to_pickle(args.output, compression='gzip')

    print("Done.")

if __name__ == '__main__':
    main()


# sample loading command:
# python load_commonpile.py \
#   --subset arxiv_abstracts_filtered \
#   --sample_size 1000 \
#   --output ../samples/arxiv_sample.pkl.gz

