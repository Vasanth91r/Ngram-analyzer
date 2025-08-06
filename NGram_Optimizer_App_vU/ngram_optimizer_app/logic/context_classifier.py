# Context classifier placeholder
import pandas as pd

def classify_context(df, brand_terms, competitor_terms):
    def get_context(term):
        t = term.lower()
        if any(b in t for b in brand_terms):
            return 'Branded'
        elif any(c in t for c in competitor_terms):
            return 'Competitor'
        else:
            return 'Generic'

    df['Context'] = df['Customer Search Term'].apply(get_context)
    df['n-gram Context'] = df['ngram'].apply(get_context)
    return df
