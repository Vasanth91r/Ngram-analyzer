# Excel exporter placeholder
import pandas as pd
import os, tempfile

def export_to_excel(df):
    outputs = []
    for n in [1, 2, 3]:
        sub = df[df['n'] == n]
        path = os.path.join(tempfile.gettempdir(), f"ngram_{n}gram.xlsx")
        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            for ctx in ['Branded', 'Competitor', 'Generic']:
                sub_ctx = sub[sub['n-gram Context'] == ctx]
                sub_ctx.to_excel(writer, sheet_name=ctx, index=False)
        outputs.append(path)
    return outputs
