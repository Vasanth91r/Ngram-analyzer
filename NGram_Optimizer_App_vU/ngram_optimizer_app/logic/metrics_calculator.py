# Metrics calculator placeholder
import pandas as pd

def compute_metrics(df):
    # Detect and convert numeric columns (handling ₹ symbols and commas)
    columns_to_convert = [
        'Impressions', 'Clicks', 'Spend',
        '14 Day Total Orders (#)', '14 Day Total Sales'
    ]

    for col in columns_to_convert:
        df[col] = (
            df[col].astype(str)
            .str.replace(',', '', regex=False)
            .str.replace('₹', '', regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    

# Force all numeric fields to numbers, double conversion?
    for col in ['Impressions', 'Clicks', 'Spend', '14 Day Total Orders (#)', '14 Day Total Sales']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    agg = df.groupby(['n', 'ngram', 'n-gram Context']).agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Spend': 'sum',
        '14 Day Total Orders (#)': 'sum',
        '14 Day Total Sales': 'sum'
    }).reset_index()

    agg = agg.rename(columns={
    '14 Day Total Orders (#)': 'Orders',
    '14 Day Total Sales': 'Sales'
    })

    agg['CTR'] = agg['Clicks'] / agg['Impressions'].replace(0, 1)
    agg['CPC'] = agg['Spend'] / agg['Clicks'].replace(0, 1)
    agg['Conversion Rate'] = agg['Orders'] / agg['Clicks'].replace(0, 1)
    agg['ROAS'] = agg['Sales'] / agg['Spend'].replace(0, 1)
    agg['RPI'] = agg['Sales'] / agg['Impressions'].replace(0, 1)
    agg['CE'] = agg['Orders'] / agg['Spend'].replace(0, 1)

    agg = agg.round({
        'CTR': 4, 'CPC': 2, 'Conversion Rate': 4,
        'ROAS': 2, 'RPI': 4, 'CE': 4
    })
    return agg
