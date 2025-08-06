import zipfile
import os
import tempfile
import pandas as pd  # ✅ required for column_mapper

def zip_outputs(paths):
    zip_path = os.path.join(tempfile.gettempdir(), "ngram_outputs.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in paths:
            arcname = os.path.basename(path)
            zipf.write(path, arcname=arcname)
    return zip_path

# Column mapper function to input basis uploaded file with dropdowns to confirm user input
def column_mapper(df):
    reference = {
        'Impressions': ['impression'],
        'Clicks': ['click'],
        'Spend': ['spend', 'cost'],
        'Orders': ['order', 'unit'],
        'Sales': ['sales', 'revenue']
    }

    mapped = {}
    for key, keywords in reference.items():
        match = next(
            (col for col in df.columns if any(k in col.lower() for k in keywords)),
            None
        )
        if match:
            mapped[key] = match

    return mapped
