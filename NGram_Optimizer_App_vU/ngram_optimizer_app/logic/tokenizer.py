# Tokenizer logic placeholder
import pandas as pd

def generate_ngrams(text, n):
    tokens = text.lower().split()
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def tokenize_search_terms(df):
    records = []
    for _, row in df.iterrows():
        search_term = row['Customer Search Term']
        for n in [1, 2, 3]:
            ngrams = generate_ngrams(search_term, n)
            for gram in ngrams:
                record = row.to_dict()
                record['n'] = n
                record['ngram'] = gram
                records.append(record)
    return pd.DataFrame(records)
