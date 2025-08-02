import os
import json
import stanza

nlp = stanza.Pipeline("en", tokenize_no_ssplit=True, use_gpu=False)

parsed_path = "../../parsed/arxiv_parsed.jsonl"
conll_out_path = "../../conll/arxiv_parsed.conll"
os.makedirs(os.path.dirname(conll_out_path), exist_ok=True)

with open(parsed_path, "r", encoding="utf-8") as f_in, open(conll_out_path, "w", encoding="utf-8") as f_out:
    for line in f_in:
        entry = json.loads(line)
        doc_id = entry["id"]
        text = " ".join([" ".join(sent) for sent in entry["sentences"]])

        doc = nlp(text)

        for sentence in doc.sentences:
            for word in sentence.words:
                f_out.write(
                    f"{word.id}\t{word.text}\t{word.lemma}\t{word.upos}\t{word.xpos}"
                    f"\t{word.feats if word.feats else '_'}\t{word.head}\t{word.deprel}"
                    f"\t_\tstart_char={word.start_char}|end_char={word.end_char}\n"
                )
            f_out.write("\n")

print("CoNLL conversion complete.")