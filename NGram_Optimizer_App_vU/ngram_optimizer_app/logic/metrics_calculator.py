# Metrics calculator with validation
import pandas as pd

def compute_metrics(df):
    # Standardized columns expected after renaming
    required_columns = ['Impressions', 'Clicks', 'Spend', 'Orders', 'Sales']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    # Clean and convert to numeric
    for col in required_columns:
        df[col] = (
            df[col].astype(str)
            .str.replace(',', '', regex=False)
            .str.replace('₹', '', regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Aggregate by n-gram info
    agg = df.groupby(['n', 'ngram', 'n-gram Context']).agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Spend': 'sum',
        'Orders': 'sum',
        'Sales': 'sum'
    }).reset_index()

    # Derived metrics with safe division
    agg['CTR'] = agg['Clicks'] / agg['Impressions'].replace(0, 1)
    agg['CPC'] = agg['Spend'] / agg['Clicks'].replace(0, 1)
    agg['Conversion Rate'] = agg['Orders'] / agg['Clicks'].replace(0, 1)
    agg['ROAS'] = agg['Sales'] / agg['Spend'].replace(0, 1)
    agg['RPI'] = agg['Sales'] / agg['Impressions'].replace(0, 1)
    agg['CE'] = agg['Orders'] / agg['Spend'].replace(0, 1)

    # Round metrics
    agg = agg.round({
        'CTR': 4,
        'CPC': 2,
        'Conversion Rate': 4,
        'ROAS': 2,
        'RPI': 4,
        'CE': 4
    })

    return agg
