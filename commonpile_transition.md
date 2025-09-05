# Design Document: Transition to Common Pile for Puddin Pipeline

**Author**: Tanya Paul (tp389)
**Last updated**: 08/01/2025 
**Advisor**: Prof. Mats Rooth  

---

## Overview

This document outlines the design and implementation plan for transitioning the current [Puddin pipeline](https://github.com/AndreaTheLinguist/puddin) from The Pile to the Common Pile filtered subsets hosted on Hugging Face.

---

## Motivation

The Puddin pipeline has been used to preprocess and parse large-scale corpora from The Pile into [CoNLL-U Format](https://universaldependencies.org/format.html#conll-u-format). The Common Pile is a more curated and permissively licensed alternative. Migrating to Common Pile supports better data ethics, reproducibility, and continued research scalability.

---

## Goals

- Use **filtered Common Pile subsets** to supplement The Pile as the main source.
- Maintain compatibility with Andrea’s original directory structure and pipeline.
- Validate pipeline correctness with spot-checks and existing tools (`confirm_doc_ids.py`)
- Document progress and ensure reproducibility.

---

## Target Dataset

- **Source**: [Common Pile Filtered Data](https://huggingface.co/collections/common-pile/common-pile-v01-filtered-data-68300bb0a946d10dda697663)
- **Planned subsets to use**:

| Subset Name	                 | Rows                  |
|------------------------------|-----------------------|
| `arxiv_abstracts_filtered`	 | 2.5M                  |
| `pubmed_filtered`            | 4.77M                 |
| `stackexchange_filtered`     | 27.5M                 |
| `project_gutenberg_filtered	`| 57.1K (for debugging) |
Other considerations:          | `github_archive_filtered`, `wikimedia_filtered` or `wikiteam_filtered` |



---

## Proposed Directory Structure (Final)
Mirroring Andrea’s puddin layout, the new directory structure will be:  
```
commonpile/  
├── conll/                               # Store final parsed conllu outputs   
│  
├── data/                                # Main data directory (formerly pile_tables)
│   ├── pile_tables/  
│   │   ├── raw/  
│   │   ├── slices/  
│   │   └── tmp/  
│   └── pile_exclusions/  
│  
├── logs/                                # Slurm and validation logs  
│   ├── YYYY-MM-DD/                      # Keep dated folders for job runs  
│   └── validation_success/  
│       └── by_cpu/  
│
├── script/                              # Python scripts  
|   ├── sample_scripts/                  # Scripts for testing small-scale parsing & slicing
|       ├── load_commonpile.py           # Initial stage - Load common pile subset & save as .pkl.gz
|       ├── parse_to_json.py             # 1st third of original pipeline - raw -> parsed JSONL
│       ├── jsonl_to_conll.py            # 2nd third of original pipeline - parsed JSONL -> CoNLL-U   
│       ├── validate_conll.py/           # Last third of original pipeline - stats/val on .conll
|       └── parse_commonpile_sample.py/  # Combination of 
|   ├── sample_outputs/                  # Folder for sample_scripts outputs  
│   ├── confirm_doc_ids.py  
│   ├── parse_commonpile.py              # Final pipeline
│   └── ...  
│  
├── slurm/                               # TBA: All SLURM job scripts  
│   ├── public_slurm.sh  
│   └── ...  
│  
├── info/                                # TBA: Meta files  
│   ├── completed-puddin_meta-index.pkl  
│   └── completed-puddin_meta-index.csv  
│  
├── commonpile_env.yml                   # Conda environment file  
│  
├── requirements.txt                     # TBA: ython dependencies  
│  
├── commonpile_transition.md             # Design doc  
│  
└── README.md                            # Project structure and usage
```


---

## Pipeline Components

| Stage            | Description |
|------------------|-------------|
| Dataset Download | Load specific subset from Hugging Face |
| Filtering        | Pre-cleaning |
| Preprocessing    | Sentence splitting, cleaning |
| Slicing          | Divide into smaller chunks |
| Conllu Parsing   | Convert to `.conll` format |
| Metadata         | Add info for later lookup |
| Validation       | Ensure all slices accounted for |

---

## Validation Strategy

- **Spot-checking**: Inspect sample slices and conllu outputs manually.
- **Scripted validation**: Understand and (if needed) adapt `confirm_doc_ids.py` for Common Pile.
- **Metadata review**: Ensure entries are being written to `/info/completed-puddin_meta-index.pkl`.

---

## Timeline

| Week | Tasks |
|------|-------|
| Week 1 | Write design doc, set up Common Pile subset loading, draft directory structure |
| Week 2 | Prototype full pipeline with small subset and validate output |
| Week 3 | Scale up to another subset, finalize validation approach |
| Week 4+ | Full transition, metadata indexing, documentation |

---


## Resources

- Common Pile documentation: https://huggingface.co/common-pile
- Andrea's puddin repo: https://github.com/AndreaTheLinguist/puddin
- Tanya's modified puddin repo: https://github.com/tanya-pa/puddin
- Processed puddin data (internal): `/share/compling/data/puddin/`

---