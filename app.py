import streamlit as st
from app_logic import process_files
import pandas as pd
import io

st.set_page_config(page_title="Card Reconciliation", layout="wide")
st.title("📊 Card Reconciliation App")

st.markdown("Upload your raw Excel files below (KCB, Equity, Aspire, Card Key).")

uploaded_files = st.file_uploader("Upload Files", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    file_dict = {f.name.split(".")[0].upper(): f for f in uploaded_files}
    try:
        report_df, output_excel = process_files(file_dict)
        st.success("✅ Reconciliation Report Generated")

        st.dataframe(report_df)

        st.download_button(
            label="📥 Download Reconciliation Report",
            data=output_excel,
            file_name="Reconciliation_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
