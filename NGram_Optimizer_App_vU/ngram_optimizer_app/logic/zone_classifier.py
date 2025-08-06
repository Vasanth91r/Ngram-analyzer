# Zone classifier placeholder
import pandas as pd

def assign_efficiency_zones(df):
    # Estimate AOV from data
    total_sales = df['Sales'].sum()
    total_orders = df['Orders'].sum()
    aov = total_sales / total_orders if total_orders else 1

    # Compute break-even CE
    df['BreakEven_CE'] = df['CPC'] / aov

    def get_zone(row):
        ce = row['CE']
        break_even = row['BreakEven_CE']
        if ce >= break_even * 1.10:
            return 'High-efficiency / Low-cost'
        elif ce <= break_even * 0.90:
            return 'Overpriced / Underperforming'
        elif abs(ce - break_even) / break_even <= 0.10:
            return 'Near Break-even'
        else:
            return 'Other'

    df['Efficiency Zone'] = df.apply(get_zone, axis=1)
    return df.drop(columns='BreakEven_CE'), round(df['BreakEven_CE'].mean(), 4)
