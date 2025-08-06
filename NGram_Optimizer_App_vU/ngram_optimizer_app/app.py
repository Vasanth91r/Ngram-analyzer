# Main Streamlit App Placeholder
import streamlit as st
import pandas as pd
import os
from io import StringIO
import tempfile

from logic.tokenizer import tokenize_search_terms
from logic.context_classifier import classify_context
from logic.metrics_calculator import compute_metrics
from logic.zone_classifier import assign_efficiency_zones
from outputs.excel_exporter import export_to_excel
from outputs.chart_generator import generate_charts
from outputs.ppt_generator import generate_ppt
from utils.file_manager import zip_outputs

st.set_page_config(page_title="Amazon SP N-Gram Optimizer", layout="wide")
st.title("📊 Amazon Sponsored Products N-Gram Analyzer")

with st.sidebar:
    st.header("Upload Files")
    csv_file = st.file_uploader("Amazon SP Impression Share Report (CSV)", type="csv")
    st.header("Context Keywords")
    brand_input = st.text_area("Brand Terms (one per line)")
    competitor_input = st.text_area("Competitor Terms (one per line)")
    generate_button = st.button("Generate Insights")

if generate_button and csv_file:
    with st.spinner("Processing data..."):
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip() #clean column headers
        brand_terms = [term.strip().lower() for term in brand_input.splitlines() if term.strip()]
        competitor_terms = [term.strip().lower() for term in competitor_input.splitlines() if term.strip()]

        token_df = tokenize_search_terms(df)
        context_df = classify_context(token_df, brand_terms, competitor_terms)
        metrics_df = compute_metrics(context_df)
        zoned_df, break_even = assign_efficiency_zones(metrics_df)

        excel_paths = export_to_excel(zoned_df)
        chart_paths = generate_charts(zoned_df, break_even)
        ppt_path = generate_ppt(zoned_df)
        zip_path = zip_outputs(excel_paths + chart_paths + [ppt_path])

        st.success("✅ All outputs generated!")
        with open(zip_path, "rb") as f:
            st.download_button("Download ZIP Bundle", f, file_name="ngram_outputs.zip")
