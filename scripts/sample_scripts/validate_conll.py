from collections import Counter

conll_path = "../../conll/arxiv_parsed.conll"

token_count = 0
sentence_count = 0
pos_counter = Counter()
dep_counter = Counter()

with open(conll_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            sentence_count += 1
            continue

        parts = line.split("\t")
        if len(parts) != 10:
            continue

        token_count += 1
        upos = parts[3]
        deprel = parts[7]

        pos_counter[upos] += 1
        dep_counter[deprel] += 1

print(f"Total tokens: {token_count}")
print(f"Total sentences: {sentence_count}")
print("\nTop POS tags:")
for tag, count in pos_counter.most_common(10):
    print(f"{tag}: {count}")

print("\nTop dependency relations:")
for dep, count in dep_counter.most_common(10):
    print(f"{dep}: {count}")
